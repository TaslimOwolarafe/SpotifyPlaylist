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

track_url = 'https://api.spotify.com/v1/tracks'
user_url = "https://api.spotify.com/v1/me/"
user_playlists_url = "https://api.spotify.com/v1/me/playlists"
account_playlists_url = "https://api.spotify.com/v1/users/{}/playlists"
search_url = "https://api.spotify.com/v1/search"
personal_url = "https://api.spotify.com/v1/me/top/{}"
# spotify_account_id = 'https://open.spotify.com/user/spotify?si=c9a85eeb1011418c'

base64_client_cred = ''

def get_resource_headers(request):
    access_token = request.COOKIES.get('access_token')
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    return headers


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
        return JsonResponse(response_me)
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

def search(request):
    headers = get_resource_headers(request)
    params = {'q':'6', 'type':'playlist,artist'}
    # params = {'q':' ', 'type':'track'}
    search_response = requests.get(search_url, headers=headers, params=params)
    if search_response.json().get('error') or search_response.status_code != 200:
        return HttpResponseRedirect(reverse("refresh"))
    all_playlists = search_response.json()['playlists']
    all_artists = search_response.json()['artists']
    return render(request, "BirthPlaylist/search.html", context={'all_playlists':all_playlists, 'all_artists':all_artists})

def personalization(request):
    headers = get_resource_headers(request)
    # print(personal_url.format("artists")) 
    person_response = requests.get(personal_url.format("track"), headers=headers)
    print(person_response)
    return HttpResponse(person_response.text)

def tracks(request):
    access_token = request.COOKIES.get('access_token')
    headers = {
        'Authorization':f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type':'application/json'
    }

    track_response = requests.get(track_url, headers=headers)
    # if response.get('error')
    return JsonResponse(track_response.json())
