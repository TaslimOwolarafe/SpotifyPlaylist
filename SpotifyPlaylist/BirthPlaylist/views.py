from email import header
from glob import glob
from urllib import response
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse

from dotenv import load_dotenv
import os

load_dotenv()
import base64, requests
from urllib.parse import urlencode

import random
import string
# Create your views here.


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

code = ''
state = ''

client_id = os.getenv("client_id")
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv("redirect_uri")

auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

track_url = 'https://api.spotify.com/v1/tracks'
user_url = "https://api.spotify.com/v1/me/"
user_playlists_url = "https://api.spotify.com/v1/me/playlists"

base64_client_cred = ''

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
    # return render(request, 'BirthPlaylist/home.html', context={'code':code, 'state':state})
    # return HttpResponseRedirect(reverse("callback", args=[code, state]))
    return HttpResponseRedirect(reverse("callback", args=[state]))

access_token = ''
refresh_token = ''
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
    global access_token
    access_token = response['access_token']
    global refresh_token
    refresh_token = response['refresh_token']
    # token_type = response['token_type']
    # access_token = response['access_token']
    # expires_in = response['expires_in']
    # refresh_token = response['refresh_token']
    # scope = response['scope']

    # return JsonResponse({'access_token':access_token, 'token_type':token_type,
    # 'expires_in':expires_in, 'refresh_token':refresh_token, 'scope':scope})
    data = JsonResponse(response)
    return render(request, 'BirthPlaylist/callback.html')

# username = ''

# def me(request):
#     headers= {
#         'Authorization':f'Bearer {access_token}'
#     }
#     me_response = requests.get(user_url, headers=headers)
#     response = me_response.json()
#     print(response)
#     global username
#     username = response['display_name']
#     print(username)
#     return JsonResponse(response)

def me_playlist(request):
    headers = {
        'Authorization':f'Bearer {access_token}'
    }

    me_response = requests.get(user_url, headers=headers)
    response_me = me_response.json()
    print(response_me)
    print(me_response.status_code)
    if response_me.get('error') or me_response.status_code != 200:

        ## refresh token and redirect.. tell user token expired
        return JsonResponse(response_me)
    else:
        
        display_name = response_me['display_name']
        id = response_me['id']
        print(display_name, "\t", id)
        if len(response_me['images']) == 0:
            image_url = "{% static 'images/skateboard.jpg' %}"
        else:
            image_url = response_me['images'][0]['url']
        # print(response_me['images'][0]['url'])
        # print(len(response_me['images']))
        playlist_response = requests.get(user_playlists_url, headers=headers)
        response = playlist_response.json()
        # playlists = JsonResponse(response)
        playlists = response
        return render(request, "BirthPlaylist/playlists.html", context={'playlists':playlists, 'display_name':display_name, 'id':id,
            'image_url':image_url})

def refresh(request):
    refresh_headers = {
        'Authorization': f'Basic {base64_client_cred}',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    refresh_data = {
        'grant_type': 'refresh_token',
        'refresh_token': f'{refresh_token}'
    }

    token_request = requests.post(token_url, data=refresh_data, headers=refresh_headers)
    response = token_request.json()
    print(response)
    global access_token
    access_token = response['access_token']
    return HttpResponseRedirect(reverse(request.path, args=[state]))

def search(request):

    return
