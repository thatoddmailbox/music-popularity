import os

from . import dataset, salami

class Song:
	def __init__(self, ds: dataset.Dataset, csv_row: "list[str]"):
		self.id = csv_row[0]
		self.id_pad = csv_row[0].zfill(4)
		self.chart_date = csv_row[1]
		self.target_rank = csv_row[2]
		self.actual_rank = csv_row[3]
		self.title = csv_row[4]
		self.artist = csv_row[5]
		self.peak_rank = csv_row[6]
		self.weeks_on_chart = csv_row[7]

		self._ds = ds

	def __str__(self) -> str:
		return "{} - {}".format(self.title, self.artist)

	def data_dir(self) -> str:
		return os.path.join(self._ds.data_path, self.id_pad)

	def chords(self) -> salami.Chords:
		return salami.Chords(self)