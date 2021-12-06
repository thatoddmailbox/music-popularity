import csv
import os

from . import salami, song

index_file_path = os.path.join("data", "billboard-2.0-index.csv")
data_path = os.path.join("data", "McGill-Billboard")

songs_with_data = set(os.listdir(data_path))

song_index = []
with open(index_file_path, newline="") as index_file:
	index_raw_data = csv.reader(index_file)
	first = True
	for row in index_raw_data:
		if first:
			# skip first line (header)
			first = False
			continue

		s = song.Song(row)
		if s.id_pad not in songs_with_data:
			continue
		song_index.append(s)