import requests
import json
import collections
import time
import requests_cache
requests_cache.install_cache()

API_KEY = '36d684d9f9aebbae6061e37a0d8cf2f7'
API_ROOT = 'http://ws.audioscrobbler.com/2.0/'
USER_AGENT = 'streams_flow'
USER = 'MacaroniMan'
UNWANTED = ['image', 'streamable', 'url', '@attr', 'mbid']
charts = []


# flatten function from https://stackoverflow.com/a/51379007
def flatten_json(y):
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

def remove_unwanted(scrobble):
    for item in scrobble.copy():
        if item in UNWANTED:
            del(scrobble[item])
    return scrobble

def get_lastfm(payload, user):
    
    headers = {'user_agent': USER_AGENT}

    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['user'] = user
    response = requests.get(API_ROOT, headers=headers, params=payload)
    return response

def get_chart_list(user):
    payload = {'method': 'user.getWeeklyChartList'}
    chart_list = get_lastfm(payload, user)
    return chart_list


def get_weekly_artists(user):
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

def get_tracks(user):

    payload = {'method': 'user.getRecentTracks'}
    payload['limit'] = 200
    first_fetch = get_lastfm(payload, user)
    # TODO if invalid username key error so add try/except
    total_pages = int(first_fetch.json()['recenttracks']['@attr']['totalPages'])
    print(total_pages)

    #temp limit
    payload['limit'] = 10
    
    tracks = get_lastfm(payload, user)
    
    raw_scrobbles = tracks.json()['recenttracks']['track']
    scrobbles = []
    artists = ()
    for scrobble in raw_scrobbles:

        scrobble = remove_unwanted(scrobble)
        scrobble = flatten_json(scrobble)

        del(scrobble['album_mbid'])

        scrobble['artist'] = scrobble.pop('artist_#text')
        scrobble['album'] = scrobble.pop('album_#text')
        scrobble['song'] = scrobble.pop('name')
        scrobble['week'] = round(int(scrobble['date_uts']) / float(604800))
        print(f'scrobble = {scrobble}')
        scrobbles.append(scrobble)


    
    

    return(scrobbles)


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)





# response = chart_list(USER)
# print(response.status_code)
# if not getattr(response.json(), 'from_cache', False):
#     print('no')
# else:
#     print('yes')

# json_response = response.json()

# for value in json_response['weeklychartlist']['chart']:
#     week = (value['from'], value['to'])
#     charts.append(week)

#all_weekly_artists = get_weekly_artists(USER)


tracks = get_tracks(USER)
#print(tracks)




#jprint(json_response)