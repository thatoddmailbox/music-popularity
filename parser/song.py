class Song:
	def __init__(self, csv_row: "list[str]"):
		self.id = csv_row[0]
		self.id_pad = csv_row[0].zfill(4)
		self.chart_date = csv_row[1]
		self.target_rank = csv_row[2]
		self.actual_rank = csv_row[3]
		self.title = csv_row[4]
		self.artist = csv_row[5]
		self.peak_rank = csv_row[6]
		self.weeks_on_chart = csv_row[7]