import csv
import os

from . import song

class Dataset:
	def __init__(self):
		self.index_file_path = os.path.join("data", "billboard-2.0-index.csv")
		self.data_path = os.path.join("data", "McGill-Billboard")

		self.songs_with_data = set(os.listdir(self.data_path))

		self.song_index = []
		self.songs_by_id_pad = {}
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
				self.song_index.append(s)
				self.songs_by_id_pad[s.id_pad] = s