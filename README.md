A simple script to create Spotify PLaylists using spotipy

To make it work:

1) Go to https://developer.spotify.com/dashboard/applications
2) Create a new app to get your client ID and client secret
3) Create a .env file in the same directory as this script and add the following:

SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080

Sample usage
create_playlist(["The Warning", "Linkin Park"], "All Noise")
