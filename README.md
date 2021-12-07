# music-popularity
Final project for 21M.383. Conducted analysis of [McGill Billboard dataset](https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/), along with Spotify data.

Requires music21 and chordparser.

## Setup
* Download [McGill data](https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/), extract it all into a folder called `data/`, next to the ipynb file in this directory.
* Register for [Spotify API Key](https://developer.spotify.com/dashboard/), follow "Spotify instructions" below
* Open the ipynb file in jupyter, or start importing stuff from the `parser` folder.

### Spotify instructions
Sign up on the [Spotify dashboard](https://developer.spotify.com/dashboard/) for a Web API application. Give it any name and description you want.

Then, create the file `parser/constants.py`, with the following contents:
```py
SPOTIFY_CLIENT_ID = "(fill in client ID from Spotify dashboard)"
SPOTIFY_CLIENT_SECRET = "(fill in client secret from Spotify dashboard)"
```

## Usage
```python
from parser import dataset
ds = dataset.Dataset()
print(ds.songs) # => [<Song {[0003] I Don't Mind - James Brown (8 weeks)}>, <Song {[0004] You've Got A Friend - Roberta Flack,Donny Hathaway (12 weeks)}>, <Song {[0006] The Rose - Bette Midler (25 weeks)}>, .... etc ....]

s = ds.songs[0]
print(s) # => [0003] I Don't Mind - James Brown (8 weeks)

c = s.chords()
print(c.blocks) # => [(0.0, <ChordBlock silence>), (0.073469387, <ChordBlock A, intro (('A:min',), ('A:min',), ('C:maj',), ('C:maj',))>), (8.714013605, <ChordBlock (('A:min',), ('A:min',), ('C:maj',), ('C:maj',))>), (15.611995464, <ChordBlock (('A:min',), ('A:min',), ('C:maj',), ('C:maj',))>), .... etc ....]

list(c.linear()) # => ['A:min', 'C:maj', 'A:min', 'C:maj', 'A:min', 'C:maj', 'A:min', 'C:maj', 'A:min', 'C:maj', 'F:maj', 'D:maj', .... etc ....]

list(c.linear_roman()) # => [<music21.roman.RomanNumeral vi6 in C major>, <music21.roman.RomanNumeral I in C major>, <music21.roman.RomanNumeral vi6 in C major>, <music21.roman.RomanNumeral I in C major>, <music21.roman.RomanNumeral vi6 in C major>, <music21.roman.RomanNumeral I in C major>, .... etc ....]

c.transition_probabilities()
'''
{
	'A:min': {'C:maj': 1.0},
	'C:maj': {
		'A:min': 0.5294117647058824,
		'F:maj': 0.23529411764705882,
		'A:maj': 0.23529411764705882
	},
	'F:maj': {'D:maj': 1.0},
	'D:maj': {'G:maj': 1.0},
	'G:maj': {'C:maj': 1.0},
	'A:maj': {'C:maj': 1.0}
}
'''
```