from email import header
from wsgiref import headers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse

from dotenv import load_dotenv
import os

load_dotenv()
import base64, requests
from urllib.parse import urlencode

import random, json
import string
import datetime as dt
# Create your views here.


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# code = ''
# state = ''

client_id = os.getenv("client_id")
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv("redirect_uri")

auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

tracks_url = 'https://api.spotify.com/v1/tracks'
user_url = "https://api.spotify.com/v1/me/"
user_playlists_url = "https://api.spotify.com/v1/me/playlists"
account_playlists_url = "https://api.spotify.com/v1/users/{}/playlists"
search_url = "https://api.spotify.com/v1/search"
personal_url = "https://api.spotify.com/v1/me/top/{}"

playlist_tracks_url = "https://api.spotify.com/v1/playlists/{}/tracks"
create_playlist_url = "https://api.spotify.com/v1/users/{}/playlists"
add_to_playlist_url = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}"
# spotify_account_id = 'https://open.spotify.com/user/spotify?si=c9a85eeb1011418c'

base64_client_cred = ''

def get_resource_headers(request):
    access_token = request.COOKIES.get('access_token')
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    return headers

def get_resource(request, _id, resource_type='albums'):
    endpoint = f"https://api.spotify.com/v1/{resource_type}/{_id}"
    headers = get_resource_headers(request)
    response = requests.get(endpoint, headers=headers)
    return response

def perform_search(request, query=None, type='artist'):
    headers = get_resource_headers(request)
    params = {'q':query, 'type':type}
    response = requests.get(search_url, headers=headers, params=params)
    return response



sample_track = {'album': {'album_type': 'single', 
'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6k8odn7NzzTT4K3NBNtsfV'}, 
'href': 'https://api.spotify.com/v1/artists/6k8odn7NzzTT4K3NBNtsfV', 
'id': '6k8odn7NzzTT4K3NBNtsfV', 
'name': 'Felo Le Tee', 
'type': 'artist', 
'uri': 'spotify:artist:6k8odn7NzzTT4K3NBNtsfV'}, 
{'external_urls': {'spotify': 'https://open.spotify.com/artist/6egY1uh8HjHy6TrD0qmQNN'}, 
'href': 'https://api.spotify.com/v1/artists/6egY1uh8HjHy6TrD0qmQNN', 
'id': '6egY1uh8HjHy6TrD0qmQNN', 
'name': 'Myztro', 
'type': 'artist', 
'uri': 'spotify:artist:6egY1uh8HjHy6TrD0qmQNN'}, 
{'external_urls': {'spotify': 'https://open.spotify.com/artist/0oW137oXCLwA5b4uYRxvIn'}, 
'href': 'https://api.spotify.com/v1/artists/0oW137oXCLwA5b4uYRxvIn', 
'id': '0oW137oXCLwA5b4uYRxvIn', 
'name': 'Daliwonga', 
'type': 'artist', 
'uri': 'spotify:artist:0oW137oXCLwA5b4uYRxvIn'}], 
'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 
'AO', 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 
'BF', 'BG', 'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 
'BT', 'BW', 'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 
'CL', 'CM', 'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 
'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 
'FI', 'FJ', 'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH', 
'GM', 'GN', 'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 
'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 
'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 
'KN', 'KR', 'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 
'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 
'ME', 'MG', 'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 
'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 
'NI', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 
'PG', 'PH', 'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 
'RO', 'RS', 'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 
'SK', 'SL', 'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 
'TG', 'TH', 'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 
'TW', 'TZ', 'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 
'VN', 'VU', 'WS', 'XK', 'ZA', 'ZM', 'ZW'], 
'external_urls': {'spotify': 'https://open.spotify.com/album/7u3mrMGgYgQkpIO5ntmezv'}, 
'href': 'https://api.spotify.com/v1/albums/7u3mrMGgYgQkpIO5ntmezv', 
'id': '7u3mrMGgYgQkpIO5ntmezv', 
'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b2737a37f1f12f09f6a0d4033980', 'width': 640}, 
{'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e027a37f1f12f09f6a0d4033980', 'width': 300}, 
{'height': 64, 'url': 'https://i.scdn.co/image/ab67616d000048517a37f1f12f09f6a0d4033980', 'width': 64}], 
'name': 'Dipatje Tsa Felo (feat. Daliwonga)', 
'release_date': '2021-12-17',
'release_date_precision': 'day', 
'total_tracks': 1, 'type': 'album', 
'uri': 'spotify:album:7u3mrMGgYgQkpIO5ntmezv'},

'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6k8odn7NzzTT4K3NBNtsfV'}, 
'href': 'https://api.spotify.com/v1/artists/6k8odn7NzzTT4K3NBNtsfV', 'id': '6k8odn7NzzTT4K3NBNtsfV', 
'name': 'Felo Le Tee', 
'type': 'artist', 
'uri': 'spotify:artist:6k8odn7NzzTT4K3NBNtsfV'}, 
{'external_urls': {'spotify': 'https://open.spotify.com/artist/6egY1uh8HjHy6TrD0qmQNN'}, 
'href': 'https://api.spotify.com/v1/artists/6egY1uh8HjHy6TrD0qmQNN', 
'id': '6egY1uh8HjHy6TrD0qmQNN', 
'name': 'Myztro', 
'type': 'artist', 'uri': 
'spotify:artist:6egY1uh8HjHy6TrD0qmQNN'}, 
{'external_urls': {'spotify': 'https://open.spotify.com/artist/0oW137oXCLwA5b4uYRxvIn'}, 
'href': 'https://api.spotify.com/v1/artists/0oW137oXCLwA5b4uYRxvIn', 
'id': '0oW137oXCLwA5b4uYRxvIn', 
'name': 'Daliwonga', 
'type': 'artist', 
'uri': 'spotify:artist:0oW137oXCLwA5b4uYRxvIn'}],

'available_markets': ['AD', 'AE', 'AG', 'AL', 'AM', 'AO',
 'AR', 'AT', 'AU', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG',
  'BH', 'BI', 'BJ', 'BN', 'BO', 'BR', 'BS', 'BT', 'BW',
   'BY', 'BZ', 'CA', 'CD', 'CG', 'CH', 'CI', 'CL', 'CM', 
   'CO', 'CR', 'CV', 'CW', 'CY', 'CZ', 'DE', 'DJ', 'DK', 
   'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FJ', 
   'FM', 'FR', 'GA', 'GB', 'GD', 'GE', 'GH', 'GM', 'GN', 
   'GQ', 'GR', 'GT', 'GW', 'GY', 'HK', 'HN', 'HR', 'HT', 
   'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IS', 'IT', 'JM', 
   'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KR', 
   'KW', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 
   'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MG', 
   'MH', 'MK', 'ML', 'MN', 'MO', 'MR', 'MT', 'MU', 'MV', 
   'MW', 'MX', 'MY', 'MZ', 'NA', 'NE', 'NG', 'NI', 'NL', 
   'NO', 'NP', 'NR', 'NZ', 'OM', 'PA', 'PE', 'PG', 'PH', 
   'PK', 'PL', 'PS', 'PT', 'PW', 'PY', 'QA', 'RO', 'RS', 
   'RW', 'SA', 'SB', 'SC', 'SE', 'SG', 'SI', 'SK', 'SL', 
   'SM', 'SN', 'SR', 'ST', 'SV', 'SZ', 'TD', 'TG', 'TH', 
   'TJ', 'TL', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 
   'UA', 'UG', 'US', 'UY', 'UZ', 'VC', 'VE', 'VN', 'VU', 
   'WS', 'XK', 'ZA', 'ZM', 'ZW'],

   'disc_number': 1, 'duration_ms': 379285, 
   'episode': False, 'explicit': False, 
   'external_ids': {'isrc': 'ZB1OS2100044'}, 
   'external_urls': {'spotify': 'https://open.spotify.com/track/3rDd1X68wGTaKYRATrcARb'}, 
   'href': 'https://api.spotify.com/v1/tracks/3rDd1X68wGTaKYRATrcARb', 
   'id': '3rDd1X68wGTaKYRATrcARb', 'is_local': False, 
   'name': 'Dipatje Tsa Felo (feat. Daliwonga)', 
   'popularity': 53, 'preview_url': 'https://p.scdn.co/mp3-preview/99b2344252c1cd33a68483025deb4fbac206e397?cid=07cfd7114c6b41fc8a90aa54f8c9bd95', 
   'track': True, 'track_number': 1, 'type': 'track', 'uri': 'spotify:track:3rDd1X68wGTaKYRATrcARb'}

def index(request):
    return render(request, 'BirthPlaylist/index.html')

def auth(request):
    state = get_random_string(16)

    auth_data = {
        'response_type': 'code',
        'client_id': client_id,
        'scope':'playlist-modify-public playlist-modify-private',
        'redirect_uri': redirect_uri,
        "state": state
    }

    auth_location = f'{auth_url}?{urlencode(auth_data)}'
    print(auth_location)
    return HttpResponseRedirect(f'{auth_url}?{urlencode(auth_data)}')

def home(request):
    global code
    code = request.GET.get('code', '')
    global state
    state = request.GET.get('state', '')
    # print(request.COOKIES.get('id'))
    # return render(request, 'BirthPlaylist/home.html', context={'code':code, 'state':state})
    # return HttpResponseRedirect(reverse("callback", args=[code, state]))
    home_response = HttpResponseRedirect(reverse("callback", args=[state]))
    home_response.set_cookie('code', code)
    home_response.set_cookie('state', state)
    return home_response

# access_token = ''
# refresh_token = ''
# def callback(request, code, state):
def callback(request, state):
    client_creds = f'{client_id}:{client_secret}'
    global base64_client_cred
    base64_client_cred = base64.b64encode(client_creds.encode()).decode()
    print(code, "\n")
    print(state, "\n")
    token_data = {
        "code": code,
        'redirect_uri':'http://127.0.0.1:8000/home',
        "grant_type": 'authorization_code'
    }


    token_headers = {
        'Authorization': f'Basic {base64_client_cred}',
        'Content-Type':'application/x-www-form-urlencoded'
    }

    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    response = token_response.json()
    # print(response, "\n")
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    data = JsonResponse(response)
    print(request.COOKIES.get('id'))
    # return render(request, 'BirthPlaylist/callback.html')
    callback_response = HttpResponseRedirect(reverse("me_playlist"))
    callback_response.set_cookie('access_token', access_token)
    callback_response.set_cookie('refresh_token', refresh_token)
    return callback_response


def me_playlist(request):
    access_token = request.COOKIES.get('access_token')
    headers = {
        'Authorization':f'Bearer {access_token}'
    }

    me_response = requests.get(user_url, headers=headers)
    response_me = me_response.json()
    # print(response_me)
    # print(me_response.status_code)
    if response_me.get('error') or me_response.status_code != 200:

        ## refresh token and redirect.. tell user token expired
        return HttpResponseRedirect(reverse("index"))
    else:
        
        display_name = response_me['display_name']
        id = response_me['id']
        if len(response_me['images']) == 0:
            image_url = "{% static 'images/skateboard.jpg' %}"
        else:
            image_url = response_me['images'][0]['url']
        playlist_response = requests.get(user_playlists_url, headers=headers)
        response = playlist_response.json()
        playlists = response
        Playlists = render(request, "BirthPlaylist/playlists.html", context={'playlists':playlists, 'display_name':display_name, 'id':id,
            'image_url':image_url})
        Playlists.set_cookie('id', id)
        return Playlists

def refresh(request):
    refresh_headers = {
        'Authorization': f'Basic {base64_client_cred}',
        'Content-Type': "application/x-www-form-urlencoded"
    }

    refresh_token = request.COOKIES.get('refresh_token')
    refresh_data = {
        'grant_type': 'refresh_token',
        'refresh_token': f'{refresh_token}'
    }

    token_request = requests.post(token_url, data=refresh_data, headers=refresh_headers)
    response = token_request.json()
    print(response)
    if response.get('error') == 'invalid_client':
        return HttpResponseRedirect(reverse("index"))
    access_token = response['access_token']
    print(request.path_info)
    print(request.META['HTTP_REFERER'])
    # refresh_response = HttpResponseRedirect(reverse("me_playlist"))
    refresh_response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    refresh_response.set_cookie('access_token', access_token)
    return refresh_response

uris = ""
def search(request):
    playlist_id = "4V7FeV9kyMsTKabfG6Ph0M"
    # query will be done dynamiclly later
    # search_response = perform_search(request, query={'month':'12','day':'17'},type='playlist,artist,album')
    headers = get_resource_headers(request)
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    alphanum_list = list(string.ascii_lowercase + string.digits)

    required_data= []
       

    for letter in alphanum_list:
        search_response = perform_search(request, query={letter},type='track,album,playlist,artist')
    # print(search_response.json())
        if search_response.json().get('error') or search_response.status_code != 200:
            print(search_response.json().get('error'))
            return HttpResponseRedirect(reverse("refresh"))
        if search_response.json().get('error') or search_response.status_code != 200:
            break
        if len(required_data) > 50:
            break

        playlists = search_response.json()['playlists']
        # playlist_url = 
        artists = search_response.json()['artists']
        albums = search_response.json()['albums']
        tracks = search_response.json()['tracks']

        for track in tracks['items']:
            if track not in required_data:
                release_date = track['album']['release_date']
                if len(release_date) > 4:
                # print(release_date)
                    d = dt.datetime.strptime(release_date, "%Y-%m-%d")
                    # print(d.month)
                    if d.month == 12 and d.day == 17:
                        required_data.append(track)
            else:
                continue

        for playlist in playlists['items']:
            print(playlist['href']+'/tracks')
            playlist_req = requests.get(playlist['href']+'/tracks', headers=headers)
            if playlist_req.json().get('error') or playlist_req.status_code > 299:
                print("error while getting playlist tracks",playlist_req.json().get('error'))
                return HttpResponseRedirect(reverse("refresh"))
            # print(playlist_req.json())
            if len(required_data) > 50:
                break
            playlist_data = playlist_req.json()['items']
            for track_data in playlist_data:
                # if track_data['track']['album']['release_date']
                if track_data['track'] not in required_data:
                    try:
                        release_date = track_data['track']['album']['release_date']
                        if len(release_date) > 4:
                        # print(release_date)
                            d = dt.datetime.strptime(release_date, "%Y-%m-%d")
                            # print(d.month)
                            if d.month == 12 and d.day == 17:
                                required_data.append(track_data['track'])
                    except:
                        print(track_data)
                else:
                    continue


    print(len(required_data))
    global uris
    uris = ""
    for track in required_data:
        uris += (track['uri'] + ",")
    uris = uris[:-1]
    print(uris)

    response = render(request, "BirthPlaylist/search.html", context={'albums':albums, 'tracks':tracks, 'playlists':playlists, 'artists':artists, 'required_data':required_data})
    # response.set_cookie("uris", uris)
    return response

def playlist_tracks(request, _id):
    playlist_response = requests.get(playlist_tracks_url.format(_id), headers=get_resource_headers(request))
    if playlist_response.json().get('error') or playlist_response.status_code != 200:
        return HttpResponseRedirect(reverse("refresh"))
    tracks = playlist_response.json()
    # return JsonResponse(playlist_response.json())
    return render(request, "BirthPlaylist/playlist_tracks.html", context={'tracks':tracks})

def create_playlist(request):
    # uris = request.COOKIES.get("uris")

    body = json.dumps({
        "name":"DEC 17",
        "description":"created from PlaylistsByTas",
        "public":True
    })
    user_id = request.COOKIES.get('id')
    playlist = requests.post(create_playlist_url.format(user_id), data=body, headers=get_resource_headers(request))
    playlist_id = playlist.json()["id"]
    print(playlist_id)
    
    # if request.COOKIES.get('playlist_id') == None:
    print(uris)
    request_body = json.dumps({
          'uris' : uris
        })

    
    access_token = request.COOKIES.get('access_token')
    headers = {
        "Content-Type": "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    add_tracks_to_playlist = requests.post(add_to_playlist_url.format(playlist_id, uris), headers=headers)
    print(add_tracks_to_playlist.json())

    return HttpResponseRedirect(reverse("me_playlist"))

def personalization(request):
    headers = get_resource_headers(request)
    # print(personal_url.format("artists")) 
    person_response = requests.get(personal_url.format("track"), headers=headers)
    print(person_response)
    return HttpResponse(person_response.text)

def tracks(request):
    headers = get_resource_headers(request)
    track_response = requests.get(tracks_url, headers=headers)
    if track_response.json().get('error') or track_response.status_code != 200:
        return HttpResponseRedirect(reverse("refresh"))
    # if response.get('error')
    return JsonResponse(track_response.json())
