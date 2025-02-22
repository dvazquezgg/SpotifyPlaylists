import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
Go to https://developer.spotify.com/dashboard/applications and 
create a new app to get your client ID and client secret.
Create a .env file in the same directory as this script and add the following:
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080
"""
load_dotenv() # Load environment variables from .env file

# Authentication
# Spotify API Credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private"
))


def get_top_tracks(artist_name, country="US"):
    # Search for the artist
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)

    # Check if artist found
    if not results["artists"]["items"]:
        print(f"No artist found for {artist_name}")
        return []

    # Extract artist ID from search results
    artist_id = results["artists"]["items"][0]["id"]
    # Get top tracks for the artist in the given country (default: US)
    top_tracks = sp.artist_top_tracks(artist_id, country=country)  # Change country if needed

    # Print top tracks for the artist
    print(f"Top Tracks for {artist_name}:")
    for idx, track in enumerate(top_tracks["tracks"], start=1):
        print(f"{idx}. {track['name']} - Popularity: {track['popularity']}")

    # Return top 10 track URIs to add to the playlist
    return [track["uri"] for track in top_tracks["tracks"][:10]]  # Only top 10


def create_playlist(artists, playlist_name="My Playlist", country="US"):
    user_id = sp.me()["id"]  # Get user ID

    # Create Playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist["id"]

    # Collect top tracks for all artists
    track_uris = []
    for artist in artists:
        track_uris.extend(get_top_tracks(artist))

    # Add tracks to the playlist
    if track_uris:  # If tracks found
        sp.playlist_add_items(playlist_id, track_uris) # Add tracks to the playlist
        print(f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks!")
    else:
        print("No tracks found for the given artists.")

    return playlist_id

if __name__ == "__main__":
    # Example Usage
    # create_playlist(["Coldplay", "Imagine Dragons"], "Chill Vibes")
    create_playlist(["The Warning", "Linkin Park"], "All Noise")

