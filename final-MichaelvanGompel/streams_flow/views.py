###############################################################
# views.py
# Michael van Gompel - programmeer-project
#
# contains functions to render pages and handle a site to explore your last fm data
# data is shown in graphs, in a timeframe between 4 and all weeks of listening history
# 
#################################################################

from .models import User, Song, GenreWeek, ArtistWeek, Artist, Genre
from . import util
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Max, Min
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time

def index(request):
    """ render home page """
    if request.user.is_authenticated:
        user = request.user.lastfm_name
    else:
        user = None

    return render(request, "streams_flow/index.html",{
        "lastfmuser": user
    })

def login_view(request):
    """ generate a form in which users can log in """
    if request.method == "POST":

        # attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "streams_flow/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "streams_flow/login.html")

def logout_view(request):
    """ handles and redirects a logout request """
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    """generate and check a form for user registration """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "streams_flow/register.html", {
                "message": "Passwords must match."
            })

        # attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "streams_flow/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "streams_flow/register.html")

@login_required
def get_data(request):
    if request.method == 'POST':
        # extract username from form
        lastfm_username = request.POST.get('lastfm_user')

        # if user is authenticated append the last fm uername to the User profile 
        if request.user.is_authenticated:
            request.user.lastfm_username = lastfm_username
            request.user.save()
            print(request.user.lastfm_username)

        # get the tracks from the Lastfm API
        tracks = util.get_tracks(lastfm_username)

        if request.user.is_authenticated:
            fm_user = request.user
        else:
            fm_user = None
        
        # iterate over the tracks to check if artists and genres exist
        total_tracks = len(tracks)
        count_track = 1 
        for track in tracks:
            #print(f'track:{track["song"]} by {track["artist"]}')

            try:
                # try getting artist from data base
                current_artist = Artist.objects.get(artist_name=track['artist'])
                genres = Genre.objects.filter(artist_in_genre=current_artist)
                # increase the playcount of all the genres
                for genre in genres:
                    genre.playcount += 1
                    genre.save()
            
            # if artist does not exist create a new artist object
            except ObjectDoesNotExist:
                # get the artist info from the Lastfm API
                new_artist_info = util.get_artist_info(track['artist'], lastfm_username)
                time.sleep(0.25)

                tags_of_artist = new_artist_info['tags']

                # check for each of the tags if there is already a Genre object present
                for tag in tags_of_artist:
                    try:
                        # if genre exists increase the genre play by one
                        genre_play = Genre.objects.get(genre_name=tag)
                        genre_play.playcount = genre_play.playcount + 1
                        genre_play.save()
                    except ObjectDoesNotExist:
                        new_genre = Genre(genre_name=tag)
                        new_genre.save()

                # create a new artist object
                current_artist = Artist(artist_name=track['artist'])
                current_artist.save()

                # add genre tags to the new artist
                util.add_tag_to_artist(current_artist, tags_of_artist) 
                
            
            song = Song(fm_user=fm_user, lastfm_account=lastfm_username, song_name=track['song'], uts=track['date_uts'], artist=current_artist, week_number=track['week'])
            song.save()

            # fill in the week objects for genre and artist for later graph initialization
            util.organize_weeks(song, fm_user)

            print(f'track {count_track} of {total_tracks}')
            count_track += 1
    
        return HttpResponseRedirect(reverse("create_plot"))


# TODO LOGIN REQUIRED
def create_plot(request):
    if request.user.is_authenticated:
        lastfm_username = request.user.lastfm_name

    # get generic information about the user
    info = util.count_stats(lastfm_username)
    song_number = info[0]
    artist_number = info[1]
    genre_number = info[2]

    # generate the first and last week numbers for the timeframe
    latest_week = ArtistWeek.objects.aggregate(Max('week_number'))
    latest_week_number = int(latest_week['week_number__max'])
    first_week = ArtistWeek.objects.aggregate(Min('week_number'))
    first_week_number = int(first_week['week_number__min'])

    default_frame = latest_week_number - 4
    half_year_frame = latest_week_number - 26
    year_frame = latest_week_number - 52

    # graph names and time frames in lists for generating graphs in a loop
    time_frames = [default_frame, half_year_frame, year_frame, first_week_number]
    aritst_graph_names = [ 'graph_div_artist_default', 'graph_div_artist_half_year', 'graph_div_artist_year', 'graph_div_artist_all']
    genre_graph_names = ['graph_div_genre_default', 'graph_div_genre_half_year', 'graph_div_genre_year', 'graph_div_genre_all']

    graphs = {}
    # fill the dictionary with graphs of top artists and top genres 
    for count, item  in enumerate(time_frames):
        a_graph = aritst_graph_names[count]
        g_graph = genre_graph_names[count]
        graphs[a_graph] = util.artist_timeframe_plot(item, latest_week_number)
        graphs[g_graph] = util.genre_timeframe_plot(item, latest_week_number)

    return render(request, "streams_flow/graphs.html", {
        'graph_div_artist_default': graphs['graph_div_artist_default'],
        'graph_div_genre_default': graphs['graph_div_genre_default'],
        'graph_div_artist_half_year': graphs['graph_div_artist_half_year'],
        'graph_div_genre_half_year': graphs['graph_div_genre_half_year'],
        'graph_div_artist_year': graphs['graph_div_artist_year'],
        'graph_div_genre_year': graphs['graph_div_genre_year'],
        'graph_div_artist_all': graphs['graph_div_artist_all'],
        'graph_div_genre_all': graphs['graph_div_genre_all'],
        'lastfmuser': lastfm_username,
        'song_number':song_number,
        'artist_number':artist_number,
        'genre_number': genre_number
    })
    
@login_required
def send_file(request):
    if request.user.is_authenticated:
        lastfm_username = request.user.lastfm_name

    # find the users csv file
    filename= f"streams_flow/{lastfm_username}.csv" # Select your file here.
    
    # open the file and send it to the user as a response
    f = open(filename, 'r')
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={lastfm_username}.csv'
    return response