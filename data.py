"""
Retrieves user data & artist data from the last.fm API.
"""

import json
import pip._vendor.requests as requests
from config import API_KEY, API_ENDPOINT

username = "henrytheswimmer"

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
        return [artist["name"] for artist in data["topartists"]["artist"]]
    else:
        return []
    
def get_artist_info(artist_name) -> dict:
    """
    Returns the artist genre.
    """

    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(API_ENDPOINT, params=params)
    data = json.loads(response.text)

    if "artist" in data:
        return data["artist"]
    else:
        return {}
    
def get_top_genres(username, limit=10) -> list:
    """
    Returns top 10 genres from a given last.fm account.
    """

    top_artists = get_top_artists(username, limit)

    if top_artists:
        genre_counts = {}
        for artist in top_artists:
            artist_info = get_artist_info(artist)
            if "tags" in artist_info and "tag" in artist_info["tags"]:
                artist_tags = artist_info["tags"]["tag"]
                for tag in artist_tags:
                    genre_name = tag["name"]
                    if genre_name in genre_counts:
                        genre_counts[genre_name] += 1
                    else:
                        genre_counts[genre_name] = 1

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        return [genre[0] for genre in sorted_genres[:limit]]
    else:
        return []
    
print(get_top_genres(username))
print(get_top_artists(username))
