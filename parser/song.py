import csv
import json
import os

from typing import TYPE_CHECKING, Any, Union
if TYPE_CHECKING:
	from . import dataset
from . import salami

class Song:
	def __init__(self, ds: "dataset.Dataset", csv_row: "list[str]"):
		self.id = csv_row[0]
		self.id_pad = csv_row[0].zfill(4)
		self.chart_date = csv_row[1]
		self.target_rank = int(csv_row[2]) if csv_row[2] != "" else None
		self.actual_rank = int(csv_row[3]) if csv_row[3] != "" else None
		self.title = csv_row[4]
		self.artist = csv_row[5]
		self.peak_rank = int(csv_row[6]) if csv_row[6] != "" else None
		self.weeks_on_chart = int(csv_row[7]) if csv_row[7] != "" else None

		self._ds = ds
		self._tuning = None
		self._chords = None
		self._spotify = None

	def __str__(self) -> str:
		return "[{}] {} - {} ({} week{})".format(self.id_pad, self.title, self.artist, self.weeks_on_chart, "s" if self.weeks_on_chart != 1 else "")

	def __repr__(self) -> str:
		return "<Song {" + str(self) + "}>"

	def data_dir(self) -> str:
		return os.path.join(self._ds.data_path, self.id_pad)

	def chords(self) -> salami.Chords:
		if not self._chords:
			self._chords = salami.Chords(self)
		return self._chords

	def tuning(self) -> float:
		if self._tuning:
			return self._tuning

		tuning_file_path = os.path.join(self._ds.data_path, self.id_pad, "tuning.csv")
		with open(tuning_file_path) as tuning_file:
			data = csv.reader(tuning_file)
			row = next(data)
			freq = row[3]
			self._tuning = float(freq)
		return self._tuning

	def spotify_info(self) -> Union[Any, None]:
		spotify_file_path = os.path.join(self._ds.data_path, self.id_pad, "spotify.json")
		if not os.path.exists(spotify_file_path):
			raise RuntimeError("You must run the spotify-download.py script to fetch Spotify API data")

		with open(spotify_file_path) as spotify_file:
			self._spotify = json.load(spotify_file)

		return self._spotify