import music21
import sys
from note_util import GANote

# Will create melody
# You still need to write underlying chord progression manually

def convert(filename):
    score = music21.converter.parse(filename, format='musicxml')

    notes = [n for n in score.recurse().notesAndRests]

    formatted_piece = []

    current_measure_length = 0
    max_measure_length = 4
    current_measure = []

    for note in notes:
        duration = note.quarterLength

        # don't bother with v small things
        if duration < 1e-10:
            continue

        if duration >= max_measure_length * 2:
            print("Please don't use long notes; keep it to a whole note at the largest, and avoid slurs as we'll break those")
            print("Cancelling")
            sys.exit(0)

        pitch = None

        if hasattr(note, 'pitch'):
            pitch = note.pitch.midi

        if current_measure_length + duration > max_measure_length:
            first_half = GANote(pitch, max_measure_length - current_measure_length)
            second_half = GANote(pitch, duration - (max_measure_length - current_measure_length))

            if first_half.duration > 1e-10:
                current_measure.append(first_half)

            formatted_piece.append(current_measure)

            current_measure = [second_half]

            current_measure_length = second_half.duration

        else:
            current_measure.append(GANote(pitch, duration))
            current_measure_length += duration

    if len(current_measure) != 0:
        formatted_piece.append(current_measure)

    return formatted_piece