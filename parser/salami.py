import os

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from . import song

class ChordBlock:
	def __init__(self, parts: "list[str]"):
		# https://ismir2011.ismir.net/papers/PS4-14.pdf
		# see salami paper, section 3.2, figure 1

		self.block = None
		self.function = None
		self.instrument = None

		bars = []
		for i, part in enumerate(parts):
			stripped_part = part.strip()
			if len(stripped_part) == 0:
				continue

			if i == 0:
				# similarity info
				info = stripped_part.split(",")
				if len(info) == 3:
					self.block = info[0].strip()
					self.function = info[1].strip()
				elif (len(info) == 2 or len(info) == 1) and len(info[0]) > 0:
					self.function = info[0].strip()
				continue

			if i == len(parts) - 1:
				# last part, will have instrument info
				self.instrument = part
				continue

			# ok, then we're looking at an actual vvar
			bar = []
			bar_chords = stripped_part.split(" ")
			for chord in bar_chords:
				if chord == ".":
					# it's repeated
					bar.append(bar[-1])
					continue
				bar.append(chord)

			bars.append(tuple(bar))

		self.bars: "tuple[tuple[str]]" = tuple(bars)

	def __str__(self) -> str:
		metadata = []
		if self.block:
			metadata.append(self.block)
		if self.function:
			metadata.append(self.function)

		result = ", ".join(metadata)
		if len(self.bars) > 0:
			if len(result) > 0:
				result += " "
			result += str(self.bars)
		return result

	def __repr__(self) -> str:
		return "<ChordBlock " + str(self) + ">"

class Chords:
	def __init__(self, s: "song.Song"):
		self.chord_file_path = os.path.join(s.data_dir(), "salami_chords.txt")

		self.meter = ""
		self.tonic = ""
		self.progression = []
		self.blocks: list[tuple[float, ChordBlock]] = []

		with open(self.chord_file_path) as chord_file:
			for line in chord_file.readlines():
				if line[0] == "#":
					# it's a comment
					parts = line.split(":")
					key = parts[0].strip()
					value = parts[1].strip()
					if key == "# metre":
						self.meter = value
					elif key == "# tonic":
						self.tonic = value

					continue

				stripped_line = line.strip()
				if stripped_line == "":
					# blank line
					continue

				parts = stripped_line.split("\t")

				time = float(parts[0])
				chord_block = ChordBlock(parts[1].split("|"))

				self.blocks.append((time, chord_block))

		# print(self.meter, self.tonic)
		# print(self.progression)
		# print(self.blocks)

	def chord_occurrences(self) -> Counter:
		result = Counter()
		for t, block in self.blocks:
			for bar in block.bars:
				for chord in bar:
					result[chord] += 1
		return result