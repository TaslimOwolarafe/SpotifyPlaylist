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
# def callback(request, code, state):
def callback(request, state):
    client_creds = f'{client_id}:{client_secret}'
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
    # token_type = response['token_type']
    # access_token = response['access_token']
    # expires_in = response['expires_in']
    # refresh_token = response['refresh_token']
    # scope = response['scope']

    # return JsonResponse({'access_token':access_token, 'token_type':token_type,
    # 'expires_in':expires_in, 'refresh_token':refresh_token, 'scope':scope})
    data = JsonResponse(response)
    return render(request, 'BirthPlaylist/callback.html')



def me(request):
    headers= {
        'Authorization':f'Bearer {access_token}'
    }
    me_response = requests.get(user_url, headers=headers)
    response = me_response.json()
    print(response)
    # username = response['display_name']
    # print(username)
    return JsonResponse(response)

def me_playlist(request):
    headers = {
        'Authorization':f'Bearer {access_token}'
    }
    playlist_response = requests.get(user_playlists_url, headers=headers)
    response = playlist_response.json()
    return JsonResponse(response)
