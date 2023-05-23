"""
Retrieves user data & artist data from the last.fm API.
"""

import json
from pip._vendor import requests
from config import API_KEY, API_ENDPOINT

class UserData:
    """
    Includes all the functions relating to retrieving user data & artist data from the last.fm API.
    """
    def __init__(self, username, limit=50) -> None:
        self.username = username
        self.limit = limit

    def get_artist_info(self, artist_name) -> dict:
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
        return {}

    def get_top_artists(self) -> list:
        """
        Returns top artists from a given last.fm account.
        """

        params = {
            "method": "user.gettopartists",
            "user": self.username,
            "limit": self.limit,
            "api_key": API_KEY,
            "format": "json",
        }

        response = requests.get(API_ENDPOINT, params=params)
        data = json.loads(response.text)

        if "topartists" in data and "artist" in data["topartists"]:
            return [artist["name"] for artist in data["topartists"]["artist"]]
        return []
        
    def get_top_genres(self) -> list:
        """
        Returns top genres from a given last.fm account.
        """

        top_artists = self.get_top_artists()
        genre_counts = {}
        for artist in top_artists:
            artist_info = self.get_artist_info(artist)
            if "tags" in artist_info and "tag" in artist_info["tags"]:
                artist_tags = artist_info["tags"]["tag"]
                for tag in artist_tags:
                    genre_name = tag["name"]
                    if genre_name in genre_counts:
                        genre_counts[genre_name] += 1
                    else:
                        genre_counts[genre_name] = 1

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        return [genre[0] for genre in sorted_genres[:self.limit]]
    
    def get_top_tags(self) -> list:
        """
        Returns top tags from a given last.fm account.
        """
        top_artists = self.get_top_artists()
        tag_counts = {}

        for artist in top_artists:
            artist_info = self.get_artist_info(artist)
            if "tags" in artist_info and "tag" in artist_info["tags"]:
                artist_tags = artist_info["tags"]["tag"]
                for tag in artist_tags:
                    tag_name = tag["name"]
                    if tag_name in tag_counts:
                        tag_counts[tag_name] += 1
                    else:
                        tag_counts[tag_name] = 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag[0] for tag in sorted_tags[:self.limit]]

    def user_preferences(self) -> dict:
        """
        Returns a dictionary of user preferences.
        """
        return {
            "top_artists": self.get_top_artists(),
            "top_genres": self.get_top_genres(),
            "top_tags": self.get_top_tags(),
        }

    def all_features(self) -> list:
        """
        Returns all the artist, genres, and tags in a user's last.fm account's history.
        """
        # need to implement pagination in the get_top_artists(), get_top_genres(), get_top_tags() before this function

    def user_feature_vector(self) -> list:
        """
        Returns the user feature vector.
        """
        user_feature_vector = []

        for feature in self.all_features():
            if feature in self.user_preferences()["top_artists"] \
            or feature in self.user_preferences()["top_genres"] \
            or feature in self.user_preferences()["top_tags"]:
                # Feature is present
                user_feature_vector.append(1)
            else:
                # Feature is absent
                user_feature_vector.append(0)

        return user_feature_vector
