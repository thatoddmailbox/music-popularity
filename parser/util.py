import re

import chordparser

from music21 import chord, note

_m21_accidental_symbols = {
	-2: "--",
	-1: "-",
	0: "",
	1: "#",
	2: "##"
}

def convert_note(cp_note: chordparser.Note) -> note.Note:
	# octave = "4" if cp_note.letter not in {"A", "B"} else "5"
	m21_note = note.Note(cp_note.letter + _m21_accidental_symbols[cp_note.symbol_value()])
	return m21_note

def parse_chord_string(chord_string: str) -> chord.Chord:
	parser = chordparser.Parser()

	# conversion
	chord_string = re.sub("\(.*?\)", "", chord_string)
	chord_string = re.sub(":1([^\d]|$)", r'\1', chord_string)
	chord_string = chord_string.replace(":", "")
	if "hdim" in chord_string:
		chord_string = chord_string.replace("hdim", "")
		chord_string += "b5"
	chord_string = chord_string.strip()

	chordparser_chord = parser.create_chord(chord_string)
	m21_notes = list(map(convert_note, chordparser_chord.notes))
	return chord.Chord(m21_notes)
