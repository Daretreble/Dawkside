from music21 import scale

def identify_key_and_scale(notes):
    if not notes:
        return "No notes provided"

    note_objects = [music21.note.Note(midi_to_note(note)) for note in notes]

    try:
        # Create a stream from the notes
        stream = music21.stream.Stream(note_objects)
        
        # Get the key and scale
        key = stream.analyze("key")
        scale_name = key.getScale().name
        
        return f"{key} {scale_name}"
    except:
        return "Unknown"

# Example usage:
midi_notes = [36, 38, 40]  # Example MIDI notes
result = identify_key_and_scale(midi_notes)
print(result)
