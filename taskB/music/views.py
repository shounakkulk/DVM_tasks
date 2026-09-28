import os
import requests

from django.shortcuts import render


def home(request):
    country = request.GET.get("country")
    artist_search = request.GET.get("artist_search")
    album_search = request.GET.get("album_search")
    track_search = request.GET.get("track_search")
    username = request.GET.get("username")
    period = request.GET.get("period")
    
    
    top_artists = []
    artists = []
    tracks = [] 
    artist_results = []
    album_results=[]
    track_results=[]
    error_message = None

    if country:
        api_key = os.environ.get("LASTFM_API_KEY")

        url = "https://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "geo.gettopartists",
            "country": country,
            "api_key": api_key,
            "format": "json",
            "limit": 10,
        }

        response = requests.get(url, params=params)

        data = response.json()

        if "error" in data:
            artists = []
            error_message = data["message"]
        else:
            artists = data["topartists"]["artist"]



        params = {
            "method": "geo.gettoptracks",
            "country": country,
            "api_key": api_key,
            "format": "json",
            "limit": 10,
        }

        response = requests.get(url, params=params)

        data = response.json()

        if "error" in data:
            tracks = []
            error_message = data["message"]
        else:
            tracks = data["tracks"]["track"]

    if artist_search:
        api_key = os.environ.get("LASTFM_API_KEY")

        url = "https://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "artist.search",
            "artist": artist_search,
            "api_key": api_key,
            "format": "json",
            "limit": 10,
        }

        response = requests.get(url, params=params)

        data = response.json()

        if "error" in data:
            error_message = data["message"]
        else:
            artist_results = data["results"]["artistmatches"]["artist"]

    if album_search:
        api_key = os.environ.get("LASTFM_API_KEY")

        url = "https://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "album.search",
            "album": album_search,
            "api_key": api_key,
            "format": "json",
            "limit": 10,
        }

        response = requests.get(url, params=params)

        data = response.json()

        if "error" in data:
            error_message = data["message"]
        else:
            album_results = data["results"]["albummatches"]["album"]    

    if track_search:
            api_key = os.environ.get("LASTFM_API_KEY")
    
            url = "https://ws.audioscrobbler.com/2.0/"
    
            params = {
                "method": "track.search",
                "track": track_search,
                "api_key": api_key,
                "format": "json",
                "limit": 10,
            }
    
            response = requests.get(url, params=params)
    
            data = response.json()
    
            if "error" in data:
                error_message = data["message"]
            else:
                track_results = data["results"]["trackmatches"]["track"]   
    if username and period:
        api_key = os.environ.get("LASTFM_API_KEY")
        url = "https://ws.audioscrobbler.com/2.0/"

        params = {
            "method": "user.gettopartists",
            "user": username,
            "api_key": api_key,
            "format": "json",
            "period": period,
            "limit": 10,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            error_message = data["message"]
        else:
            top_artists = data["topartists"]["artist"]    
    return render(
        request,
        "music/home.html",
        {
            "artists": artists,
            "tracks": tracks,
            "country": country,
            "artist_results": artist_results,
            "artist_search": artist_search,
            "album_results": album_results,
            "track_search": track_search,
            "track_results": track_results,
            "album_search": album_search, 
            "error_message":error_message,
            "username": username,
            "period": period,
            "top_artists": top_artists,
        },
    )

