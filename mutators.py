from note_util import isMeasureSilent, GANote, getNonRestNotes
from random import random, choice, shuffle, sample

# all functions here have same args, and will return an array of notes, without editing anything
# return false if operation fails for some reason

def pickRandomChordTone(currentPiece, chordProgression, measureIndex, noteIndex):
    original_midi_note = currentPiece[measureIndex][noteIndex].midi_note
    octave = original_midi_note // 12
    new_midi_note = choice(chordProgression[measureIndex]) + 12 * octave
    if random() < 0.25 and new_midi_note > 12:
        new_midi_note -= 12

    currentPiece[measureIndex][noteIndex].midi_note = new_midi_note
    return True

def copyNoteInMeasure(currentPiece, chordProgression, measureIndex, noteIndex):

    currentPiece[measureIndex][noteIndex].midi_note = choice(currentPiece[measureIndex]).midi_note
    return True

def transposeWholeNote(currentPiece, chordProgression, measureIndex, noteIndex):
    note = currentPiece[measureIndex][noteIndex]

    transpose = 2
    if random() > 0.5:
        transpose *= -1

    currentPiece[measureIndex][noteIndex].midi_note = note.midi_note
    return True

def becomeLeadingNote(currentPiece, chordProgression, measureIndex, noteIndex):
    measure = currentPiece[measureIndex]
    is_last_note = (noteIndex == len(measure) - 1)

    # if it's literally the last note
    if (measureIndex == len(currentPiece) - 1 and is_last_note) or (not is_last_note and measure[noteIndex + 1].midi_note is None) or (currentPiece[measureIndex + 1][0].midi_note is None):
        return False

    next_note = None

    if is_last_note:
        next_note = currentPiece[measureIndex + 1][0].midi_note
    else:
        next_note = measure[noteIndex + 1].midi_note

    delta = 1
    if random() < 0.5:
        delta = -1

    currentPiece[measureIndex][noteIndex].midi_note = (next_note + delta)
    return True


def subdivide(currentPiece, chordProgression, measureIndex, noteIndex):
    p = random()

    note = currentPiece[measureIndex][noteIndex]

    note_array = []

    if p < 0.5:
        # even subdivision
        note_array = [note.clone(note.duration / 2.0), note.clone(note.duration / 2.0)]
    elif p < 0.75:
        # triplet
        note_array = [note.clone(note.duration / 3.0), note.clone(note.duration / 3.0), note.clone(note.duration / 3.0)]
    else:
        # dotted
        long_note = note.clone(note.duration * 0.75)
        short_note = note.clone(note.duration * 0.25)

        if random() < 0.5:
            note_array = [long_note, short_note]
        else:
            note_array = [short_note, long_note]


    measure = currentPiece[measureIndex]

    currentPiece[measureIndex] = measure[:noteIndex] + note_array + measure[noteIndex+1:]

    return True

def copyNoteFromSimilarChord(currentPiece, chordProgression, measureIndex, noteIndex):
    target_chord = chordProgression[measureIndex]

    measure_indices_with_same_chord = []

    for i in range(len(chordProgression)):
        if i == measureIndex:
            continue

        chord = chordProgression[i]
        if chord == target_chord:
            measure = currentPiece[measureIndex]

            if not isMeasureSilent(measure):
                measure_indices_with_same_chord.append(i)

    if len(measure_indices_with_same_chord) == 0:
        return False

    similar_index = choice(measure_indices_with_same_chord)
    note_possibilities = getNonRestNotes(currentPiece[similar_index])

    currentPiece[measureIndex][noteIndex].midi_note = currentPiece[similar_index][choice(note_possibilities)].midi_note
    return True

def shiftNotes(currentPiece, chordProgression, measureIndex, noteIndex):
    measure = currentPiece[measureIndex]

    notes = [note.midi_note for note in measure]

    # TODO, consider deltas > 1
    delta = 1
    if random() < 0.5:
        delta = -1

    for i in range(len(notes)):
        shifted_index = (i + delta + len(notes)) % len(notes)
        currentPiece[measureIndex][i].midi_note = notes[shifted_index]

    return True

def shuffleNotes(currentPiece, chordProgression, measureIndex, noteIndex):
    shuffle(currentPiece[measureIndex])
    return True

def dropNote(currentPiece, chordProgression, measureIndex, noteIndex):
    measure = currentPiece[measureIndex]

    random_index = int(random() * len(measure))

    currentPiece[measureIndex][random_index].midi_note = None

    return True

def swapNotes(currentPiece, chordProgression, measureIndex, noteIndex):
    measure = currentPiece[measureIndex]

    # not enough notes to swap
    if len(measure) <= 1:
        return False

    a, b = sample(range(0, len(measure)), 2)

    temp = measure[a]
    measure[a] = measure[b]
    measure[b] = temp

    currentPiece[measureIndex] = measure

    return True
