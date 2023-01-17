###############################################################
# util.py
# Michael van Gompel - programmeer-project
#
# contains functions for extracting tracks of a user from the Last.fm API
# 
# data is shown in graphs, in a timeframe between 4 and all weeks of listening history
# 
#################################################################
from django.core.exceptions import ObjectDoesNotExist
import plotly
import plotly.graph_objects as go
import requests
import heapq
import json
import collections
import time
import csv
from .models import User, Song, GenreWeek, ArtistWeek, Artist, Genre

API_KEY = '36d684d9f9aebbae6061e37a0d8cf2f7'
API_ROOT = 'http://ws.audioscrobbler.com/2.0/'
USER_AGENT = 'streams_flow'
UNWANTED = ['image', 'streamable', 'url', '@attr', 'mbid']
charts = []

color_list = [ 'rgb(102,197,204)', 'rgb(246,207,113)','rgb(248,156,116)','rgb(220,176,242)','rgb(135,197,95)','rgb(158,185,243)','rgb(254,136,177)','rgb(201,219,116)','rgb(139,224,164)','rgb(180,151,231)' ]
color_list2 = ['rgb(133,92,117)', 'rgb(217,175,107)', 'rgb(175,100,88)', 'rgb(115,111,76)', 'rgb(82,106,131)','rgb(98,83,119)','rgb(104,133,92)','rgb(156,156,94)','rgb(150,97,119)','rgb(140,120,93)','rgb(124,124,124)']

def flatten_json(y):
    """
        Flatten function from https://stackoverflow.com/a/51379007
        combines dictionary keys to a single level dictionary
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    
    flatten(y)
    return out

def remove_unwanted(scrobble, unwanted):
    """ Trim the unwanted items of a json item """
    # iterate over copy because items will be deleted
    for item in scrobble.copy():
        # delete item if it is unwanted
        if item in unwanted:
            del(scrobble[item])
    return scrobble

def get_lastfm(payload, user):
    """ 
        Functions as a template for API calls to Last.fm
        the method has to be supplied in order for a successsful call
    """
    headers = {'user_agent': USER_AGENT}

    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['user'] = user

    # return the json response 
    response = requests.get(API_ROOT, headers=headers, params=payload)
    return response

def get_chart_list(user):
    """ Generate a list of weeks the user is active on Last.fm """
    payload = {'method': 'user.getWeeklyChartList'}
    chart_list = get_lastfm(payload, user)
    return chart_list


def get_weekly_artists(user):
    """get weekly top artists (for later use)"""
    payload = {'method': 'user.getWeeklyArtistChart'}
    weekly_top_ten = []
    total_weeks = len(charts)
    count = 1
    with open('data.txt', 'a') as outfile:
        for begin, end in charts:
            payload['from'] = begin
            payload['to'] = end
            response = get_lastfm(payload, user)
            if response.status_code != 200:
                print('something went wrong')
                return 0
            outfile.write(json.dumps(response.json()))
            outfile.write(",")
            weekly_top_ten.append(response.json())
            time.sleep(0.25)
            print(f'week {count} of {total_weeks}')
            count +=1
    return weekly_top_ten

def get_tracks(user, filename='default'):
    """ 
        Extracts all the the songs the user has listened 
        strips unwanted items from the results and modifies it suitable for creating graphs
        writes the results to a csv file
        only works for last.fm native songs, items imported to last.fm will generate an error
    """
    payload = {'method': 'user.getRecentTracks'}
    # set limit to the max amount of songs per page
    payload['limit'] = 200

    # check if the username exists 
    try:
        first_fetch = get_lastfm(payload, user)
    except KeyError:
        return None
    
    # calculate the total amount of pages
    total_pages = int(first_fetch.json()['recenttracks']['@attr']['totalPages'])

    scrobbles = []
    track_unwanted = ['image', 'streamable', 'url', '@attr', 'mbid']
    
    # iterate over the pages and extract all the tracks
    for page in range(1, total_pages):
        payload['page'] = page
        
        # raw json output
        tracks = get_lastfm(payload, user)    
        
        try: 
            # scrobbles with redundant information
            raw_scrobbles = tracks.json()['recenttracks']['track']
        except KeyError:
            print('grote keyfout')
            continue
        
        # iterate over the scrobbles of one page to trim the redundant information
        for scrobble in raw_scrobbles: 
            if not scrobble:
                continue
    
            scrobble = remove_unwanted(scrobble, track_unwanted)
            scrobble = flatten_json(scrobble)

            # remove id numbers because it is not often present
            del(scrobble['album_mbid'])
            del(scrobble['artist_mbid'])
            try:
                # change names of the flat json items
                scrobble['artist'] = scrobble.pop('artist_#text')
                scrobble['album'] = scrobble.pop('album_#text')
                scrobble['song'] = scrobble.pop('name')
                scrobble['week'] = round(int(scrobble['date_uts']) / float(604800))
            except KeyError:
                print(scrobble)
                print('keyfout')
                continue

            scrobbles.append(scrobble)
        print(f'page {page} of {total_pages}')
        # wait so the Last.fm server doesnt overflow
        time.sleep(0.25)

    filename = user + '.csv'
    # write the extracted songs to a csv file
    with open(filename, 'w', encoding='utf8', newline='') as outfile:
        fc = csv.DictWriter(outfile, 
            fieldnames=scrobbles[0].keys(),)
        fc.writeheader()
        fc.writerows(scrobbles)

    return scrobbles

def get_artist_info(artist, user):
    """ request artist information for generating lists of similar artists (for later use)"""
    payload = {'method': 'artist.getInfo'}
    payload['artist'] = artist

    # generate json response
    response = get_lastfm(payload, user)
    
    artist_info = response.json()['artist']
    artist_unwanted = ['ontour', 'image', 'streamable', 'url', 'bio', 'mbid']
    # remove onwanted items from the artist json object
    for item in artist_unwanted:
        if item in artist_info:
            del (artist_info[item])


    similar_artists = []
    # append similar artist to the artist object in a more suitable format
    for sim_artist in artist_info['similar']['artist']:
        similar_artists.append(sim_artist['name'])
    del(artist_info['similar'])
    artist_info[ 'similar'] = similar_artists

    new_tags = []
    # append the artist tags to the artist object in a more suitable format
    for tags in artist_info['tags']['tag']:
        new_tags.append(tags['name'])
    del(artist_info['tags'])
    artist_info['tags']= new_tags
    
    del (artist_info['stats'])

    try:
        # check for user playcount in this artist
        user_playcount = artist_info['stats']['userplaycount']
        artist_info['playcount'] = user_playcount
    except KeyError:
        pass
 
    return artist_info

def add_tag_to_artist(artist, tags):
    """ appendeds genres to new artist objecs """
    for tag in tags:
        new_genre = Genre.objects.get(genre_name=tag)
        artist.genre.add(new_genre)

def organize_weeks(song, user=''):
    """ """
    current_artist_week = ArtistWeek.objects.filter(week_number=song.week_number, artist=song.artist)
    
    if not current_artist_week.exists():
        new_week_object = ArtistWeek(user=user, week_number=song.week_number, artist=song.artist)
        new_week_object.save()
        genres = Genre.objects.filter(artist_in_genre=song.artist)
        for genre in genres:
            current_genre_week = GenreWeek.objects.filter(week_number=song.week_number, genre=genre)
            if not current_genre_week.exists():
                new_week_object = GenreWeek(user=user, week_number=song.week_number, genre=genre)
                new_week_object.save()
            else:
                current_genre_week = GenreWeek.objects.get(week_number=song.week_number, genre=genre)
                current_genre_week.genre_plays += 1
                current_genre_week.save()
    else:
        current_artist_week = ArtistWeek.objects.get(week_number=song.week_number, artist=song.artist)
        current_artist_week.artist_plays += 1
        current_artist_week.save()
        genres = Genre.objects.filter(artist_in_genre=song.artist)
        for genre in genres:
            
            current_genre_week = GenreWeek.objects.get(week_number=song.week_number, genre=genre)
            current_genre_week.genre_plays += 1
            current_genre_week.save()


def jconvert(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

def generate_top_ten_artist(begin_frame):
    artist_subset = ArtistWeek.objects.filter(week_number__gte=begin_frame)
    artist_count = {}

    for item in artist_subset:
        if item.artist in artist_count.keys():
            current_count = artist_count[item.artist]
            new_count = item.artist_plays
            artist_count[item.artist] = current_count + new_count
        else:
            artist_count[item.artist] = item.artist_plays 

    ten_artists = heapq.nlargest(10, artist_count, key=artist_count.get)
    return ten_artists

def generate_top_ten_genre(begin_frame):
    genre_subset = GenreWeek.objects.filter(week_number__gte=begin_frame)
    genre_count = {}
    for item in genre_subset:
        if item.genre in genre_count.keys():
            current_count = genre_count[item.genre]
            new_count = item.genre_plays
            genre_count[item.genre] = current_count + new_count
        else:
            genre_count[item.genre] = item.genre_plays

    ten_genres = heapq.nlargest(10, genre_count, key=genre_count.get)
    return ten_genres


def artists_for_graph(top_artists, start_frame, end_frame):
    names_artists = []
    list_artists = []
    for artist in top_artists:
        names_artists.append(artist.artist_name) 
        temp_list = []
        for week_number in range(start_frame, end_frame):
            try:
                this_week_plays = ArtistWeek.objects.get(week_number=week_number, artist=artist)
                temp_list.append(this_week_plays.artist_plays)
            except ObjectDoesNotExist:
                temp_list.append(int(0))
        list_artists.append(temp_list)
    result = [names_artists, list_artists]
    return result

def genres_for_graph(top_genres, start_frame, end_frame):
    names_genres = []
    list_genres = []
    for genre in top_genres:
        names_genres.append(genre.genre_name)
        temp_list = []
        for week_number in range(start_frame, end_frame):
            try:
                this_week_plays  = GenreWeek.objects.get(week_number=week_number, genre=genre)
                temp_list.append(this_week_plays.genre_plays)
            except ObjectDoesNotExist:
                temp_list.append(int(0))
        list_genres.append(temp_list)
    result=[names_genres, list_genres]
    return result

def create_graph(content_list, length_frame, names_list, color_list, type_graph):
    fig = go.Figure()
    if length_frame > 27:
        tick = 2
    else:
        tick = 1
    
    count = 0
    x = [week_number + 1 for week_number in (range(length_frame))]
    for artist in content_list:
        fig.add_trace(go.Scatter(
            x=x, y=content_list[count],
            name=names_list[count],
            hoverinfo= 'y',
            mode= 'lines',
            line=dict(width=0/5, color=color_list[count]),
            stackgroup='one',
        ))
        count += 1
 

    fig.update_layout(legend_title_text=type_graph,
        title=f'Top {type_graph}s of the Last {length_frame} Weeks', 
        width=1400,
        yaxis_range=(0,max(content_list)),
        xaxis_title="Week Number",
        yaxis_title="total plays",
        xaxis = dict(
            tickmode = 'linear',
            dtick = tick,
            tick0 = 1
            ),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="gray")
    )
    return plotly.offline.plot(fig, auto_open = False, output_type="div")

def artist_timeframe_plot(time_frame, latest_week_number):
    top_artists = generate_top_ten_artist(time_frame)

    artist_result = artists_for_graph(top_artists, time_frame, latest_week_number)
    names_artists = artist_result[0]
    list_artists = artist_result[1]

    length_frame = len(range(time_frame, latest_week_number))
    graph_div_artist = create_graph(list_artists, length_frame, names_artists, color_list, 'Artist')
    return graph_div_artist


def genre_timeframe_plot(time_frame, latest_week_number):
    top_genres = generate_top_ten_genre(time_frame)

    genre_result = genres_for_graph(top_genres, time_frame, latest_week_number) 
    names_genres = genre_result[0]
    list_genres = genre_result[1]

    length_frame = len(range(time_frame, latest_week_number))
    graph_div_genre = create_graph(list_genres, length_frame, names_genres, color_list2, 'Genre')
    return graph_div_genre
    
def count_stats(user):
    print(user)
    songs_number = Song.objects.filter(lastfm_account=user).count()
    print(songs_number)
    artist_number = Song.objects.filter(lastfm_account=user).values('artist').distinct().count()
    print(artist_number)
    genre_number = Song.objects.filter(lastfm_account=user).values('song_genre').distinct().count()
    return [songs_number, artist_number, genre_number]
