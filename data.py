"""
Retrieves user data & artist data from the last.fm API.
"""

import json
import pip._vendor.requests as requests
from config import API_KEY, API_ENDPOINT

def get_top_artists(username, limit=10) -> list:
    """
    Returns top 10 artists from a given last.fm account.
    """

    params = {
        "method": "user.gettopartists",
        "user": username,
        "limit": limit,
        "api_key": API_KEY,
        "format": "json",
    }

    response = requests.get(API_ENDPOINT, params=params)
    data = json.loads(response.text)

    if "topartists" in data and "artist" in data["topartists"]:
        return data["topartists"]["artist"]
    else:
        return []

top_artists = get_top_artists("henrytheswimmer")

if top_artists:
    for artist in top_artists:
        print(artist["name"])
else:
    print("User has no top artists.")
