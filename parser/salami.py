import os

from collections import Counter
from typing import TYPE_CHECKING, Dict, Generator

from music21 import key, roman

if TYPE_CHECKING:
	from . import song
from . import util

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

			# ok, then we're looking at an actual bar
			bar = []
			bar_chords = stripped_part.split(" ")
			for chord in bar_chords:
				if chord[0] == "(" and chord[-1] == ")":
					# this is a time signature indicator
					# ignore it
					continue

				if chord == "*":
					# "For passages that were too musically elaborate to merit beat-level chord
					#  annotations, annotators sometimes filled the bar with an asterisk"
					continue

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

	def linear(self) -> Generator[str, None, None]:
		last_chord = None
		for t, block in self.blocks:
			for bar in block.bars:
				for chord in bar:
					if chord != last_chord and chord != "N" and chord != "&pause":
						yield chord
						last_chord = chord

	def linear_roman(self) -> Generator[roman.RomanNumeral, None, None]:
		if self.tonic is None:
			raise ValueError("song does not have a tonic")

		k = key.Key(self.tonic)
		for chord_str in self.linear():
			m21_chord = util.parse_chord_string(chord_str)
			yield roman.romanNumeralFromChord(m21_chord, k)

	def transition_counts(self, roman=False) -> Dict[str, Dict[str, int]]:
		result = {}
		last_chord = None
		stream = self.linear_roman() if roman else self.linear()
		for chord in stream:
			if roman:
				chord = chord.romanNumeral
			if last_chord is not None:
				if last_chord not in result:
					result[last_chord] = {}
				if chord not in result[last_chord]:
					result[last_chord][chord] = 0
				result[last_chord][chord] += 1
			last_chord = chord
		return result

	def transition_probabilities(self, roman=False) -> Dict[str, Dict[str, float]]:
		result = self.transition_counts(roman=roman)
		for from_chord in result:
			total_count = 0
			for to_chord in result[from_chord]:
				total_count += result[from_chord][to_chord]
			for to_chord in result[from_chord]:
				result[from_chord][to_chord] /= float(total_count)
		return result