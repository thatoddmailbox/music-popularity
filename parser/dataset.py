import csv
import os

from . import song

class Dataset:
	def __init__(self):
		self.index_file_path = os.path.join("data", "billboard-2.0-index.csv")
		self.data_path = os.path.join("data", "McGill-Billboard")

		self.songs_with_data = set(os.listdir(self.data_path))

		self.songs: "list[song.Song]" = []
		self.songs_by_id_pad = {}
		self.existing = set()
		with open(self.index_file_path, newline="") as index_file:
			index_raw_data = csv.reader(index_file)
			first = True
			for row in index_raw_data:
				if first:
					# skip first line (header)
					first = False
					continue

				s = song.Song(self, row)
				if s.id_pad not in self.songs_with_data:
					continue
				if (s.title, s.artist) in self.existing:
					# remove duplicates
					# (this happens when a song is on multiple charts)
					# (we only care about the peak and the weeks, so OK to throw awat)
					continue

				self.songs.append(s)
				self.songs_by_id_pad[s.id_pad] = s
				self.existing.add((s.title, s.artist))

	def songs_with_spotify(self):
		for s in self.songs:
			if s.spotify_info() is not None:
				yield s