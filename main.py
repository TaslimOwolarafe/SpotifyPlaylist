from secrets import client_id, state, client_creds
import requests, base64
from urllib.parse import urlencode

import random
import string

auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

auth_data = {
    'response_type': 'code',
    'client_id': f'{client_id}',
    'scope':'playlist-modify-public playlist-modify-private',
    'redirect_uri':'https://TaslimOwolarafe.github.io/',
    "state": state
}



# print(f"{auth_url}?{urlencode(auth_data)}")
auth_response = requests.get(f"{auth_url}?{urlencode(auth_data)}")
# # response = requests.post(auth_url, urlencode(auth_data))
print(auth_response)
# .callback.code, response.json().callback.state

base64_client_cred = base64.b64encode(client_creds.encode()).decode()
# print(base64_client_cred)
auth_code = "AQBnyA5clqUpGoWWvAJ_2UFZzhemywCQjirSV4inBpJsY-Gmc6MI3oqlLLWYMbZGKHaQPGDGoV472qnzFDPER6I5gjTPEcWY3uQEwE5feMVWDut7FHqr2xfgGtc_EbYteVnqaUl2rwV-vXj2vOskqsLJZoSroc7fUFsbSubWcug8pKANfENWRLtKFHaiCHpx_EmDWv8KkgPLeBkzx_-0a9UKwamOq7FAnZ4iTli1Qe9GMbhhrhva"

token_data = {
    "code": auth_code,
    'redirect_uri':'https://TaslimOwolarafe.github.io/',
    "grant_type": 'authorization_code'
}


token_headers = {
    'Authorization': f'Basic {base64_client_cred}',
    'Content-Type':'application/x-www-form-urlencoded'
}

# token_response = requests.post(token_url, data=token_data, headers=token_headers)
# print(token_response.json())