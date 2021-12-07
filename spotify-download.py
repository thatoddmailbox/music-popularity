import json
import os

import spotipy

from parser import constants, dataset, song

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
													client_id=constants.SPOTIFY_CLIENT_ID,
													client_secret=constants.SPOTIFY_CLIENT_SECRET))

def get_data_for_song(s: song.Song):
	result = sp.search("track:\"" + s.title + "\" artist:\"" + s.artist + "\"", limit=1)
	items = result["tracks"]["items"]
	if len(items) == 0:
		return None
	item = items[0]
	return item

ds = dataset.Dataset()
song_count = len(ds.songs)
for i, s in enumerate(ds.songs):
	print("Processing song {} out of {}...".format(i + 1, song_count))

	spotify_data_file_path = os.path.join(s.data_dir(), "spotify.json")
	if os.path.exists(spotify_data_file_path):
		# already tried this
		continue

	spotify_data = get_data_for_song(s)

	# "but alex, you don't check if spotify_data is None!"
	# well, json.dump(None) returns "null", which, when loaded, will go back to None
	# and we *want* to save the fact that there's no data so that we don't try to fetch it again
	with open(spotify_data_file_path, "w+") as spotify_data_file:
		json.dump(spotify_data, spotify_data_file)