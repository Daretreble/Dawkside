import pprint
# Define the musical modes as a list
MUSICAL_MODES = ['Major', [0, 2, 4, 5, 7, 9, 11], 'Minor', [0, 2, 3, 5, 7, 8, 10], 
                 'Dorian', [0, 2, 3, 5, 7, 9, 10], 'Mixolydian', [0, 2, 4, 5, 7, 9, 10], 
                 'Lydian', [0, 2, 4, 6, 7, 9, 11], 'Phrygian', [0, 1, 3, 5, 7, 8, 10], 
                 'Locrian', [0, 1, 3, 5, 6, 8, 10], 'Diminished', [0, 1, 3, 4, 6, 7, 9, 10], 
                 'Whole-half', [0, 2, 3, 5, 6, 8, 9, 11], 'Whole Tone', [0, 2, 4, 6, 8, 10], 
                 'Minor Blues', [0, 3, 5, 6, 7, 10], 'Minor Pentatonic', [0, 3, 5, 7, 10], 
                 'Major Pentatonic', [0, 2, 4, 7, 9], 'Harmonic Minor', [0, 2, 3, 5, 7, 8, 11], 
                 'Melodic Minor', [0, 2, 3, 5, 7, 9, 11], 'Super Locrian', [0, 1, 3, 4, 6, 8, 10], 
                 'Bhairav', [0, 1, 4, 5, 7, 8, 11], 'Hungarian Minor', [0, 2, 3, 6, 7, 8, 11], 
                 'Minor Gypsy', [0, 1, 4, 5, 7, 8, 10], 'Hirojoshi', [0, 2, 3, 7, 8], 
                 'In-Sen', [0, 1, 5, 7, 10], 'Iwato', [0, 1, 5, 6, 10], 
                 'Kumoi', [0, 2, 3, 7, 9], 'Pelog', [0, 1, 3, 4, 7, 8], 
                 'Spanish', [0, 1, 3, 4, 5, 6, 8, 10]]

# Create a new list for Modus objects
modus_list = []

# Iterate through the musical modes and create Modus objects
for i in range(0, len(MUSICAL_MODES), 2):
    mode_name = MUSICAL_MODES[i]
    mode_notes = MUSICAL_MODES[i + 1]
    modus_list.append({'name': mode_name, 'notes': mode_notes})

# Now, modus_list contains dictionaries with mode name and notes
# You can use modus_list as needed in your local scope
pprint.pprint(modus_list)