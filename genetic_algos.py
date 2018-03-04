from random import random, choices
from copy import deepcopy

from mutators import pickRandomChordTone, copyNoteInMeasure, transposeWholeNote, becomeLeadingNote, subdivide, copyNoteFromSimilarChord, shiftNotes, shuffleNotes, dropNote, swapNotes
from note_util import isMeasureSilent, getNonRestNotes

measures_to_change_per_mutation = 4
max_attempts = 100

def mutatePiece(currentPiece, chordProgression, copy=True):

    if copy:
        currentPiece = deepcopy(currentPiece)

    # changes values within currentPiece
    measures_to_change = set()
    attempts = 0

    while len(measures_to_change) < measures_to_change_per_mutation:
        measure_index = int(random() * len(currentPiece))

        measure = currentPiece[measure_index]

        # if there are only rests in the measure...
        if isMeasureSilent(measure):
            # then we want to sample a new measure
            continue

        measures_to_change.add(measure_index)

        attempts += 1

        # a lazy quasi-probabalistic way to avoid stalling forever on a piece with all rests
        if attempts > max_attempts:
            break

    for measure_index in measures_to_change:
        # all measures in here are guaranteed to have at least one real note
        # TODO: I guess we should consider what if there's a measure with all rests – would we want a way to bring a new note into it?

        measure = currentPiece[measure_index]

        note_index = -1

        # make sure we're not applying our algo to a rest
        while note_index == -1:
            random_note_index = int(random() * len(measure))

            if not measure[random_note_index].is_rest():
                note_index = random_note_index

        mutation_result = mutateMeasure(currentPiece, chordProgression, measure_index, note_index)

        mutation_attempts = 0
        max_mutation_attempts = 4

        while mutation_result == False and mutation_attempts < max_attempts:
            mutation_result = mutateMeasure(currentPiece, chordProgression, measure_index, note_index)

            mutation_attempts += 1

        if mutation_result == False:
            continue

        # current_piece[measure_index] = measure[:note_index] + mutated_notes + measure[note_index+1:]

    return currentPiece

def mutateMeasure(currentPiece, chordProgression, measureIndex, noteIndex):
    p = random()

    quanta = currentPiece[measureIndex][noteIndex].duration / 4.0

    enable_become_leading = 0
    # issues with becoming leading note bc note being lead to often changes
    # maybe consider just leading into chord progression's root?

    mutators = [pickRandomChordTone, copyNoteInMeasure, transposeWholeNote, becomeLeadingNote, subdivide, copyNoteFromSimilarChord, shiftNotes, shuffleNotes, dropNote, swapNotes]
    probabilities = [0.25, 0.125, 0.125, 0.25 * (1 - quanta) * enable_become_leading, 0.25 * quanta, 0.05, 0.05, 0.05, 0.05, 0.05]

    mutator = choices(mutators, weights=probabilities)[0]

    return mutator(currentPiece, chordProgression, measureIndex, noteIndex)

def fitness(currentPiece, chordProgression, originalPiece):
    points = 0

    for measure_index in range(len(currentPiece)):

        measure = currentPiece[measure_index]
        chord = chordProgression[measure_index]

        distinct_notes = set()
        chord_tones = [chord_note % 12 for chord_note in chord]

        num_chord_tones = 0

        min_note = 256
        max_note = -1

        for note in measure:
            midi_note = note.midi_note

            if midi_note is not None:

                distinct_notes.add(midi_note)
                if midi_note % 12 in chord_tones:
                    num_chord_tones += 1

                min_note = min(min_note, midi_note)
                max_note = min(max_note, midi_note)

        # if just the same note is played
        if len(distinct_notes) <= 1:
            points -= 1

        # if there are literally notes from the chord
        if num_chord_tones == 0:
            points -= 1

        # if literally nothing has changed between mutated piece and original;
        # we can use equality here because GANote overrides default equality comparator
        if measure == originalPiece[measure_index]:
            points -= 1

        # make sure there was a note to be updated, and the measure wasn't just rests
        if min_note != 256:
            note_delta = abs(min_note - max_note)

            # if there's a jump over an octave
            if note_delta > 12:
                points -= 1

            # if there's a two octave jump, dock another point
            if note_delta > 24:
                points -= 1
        else:
            # this means that no real notes were logged at all, aka the measure was just silence
            points -= 2

    return points

def combinePieces(firstPiece, secondPiece):
    l = len(firstPiece) // 2
    return [
        firstPiece[:l] + secondPiece[l:],
        secondPiece[:l] + firstPiece[l:]
    ]

def generation(population, chordProgression, originalPiece, badPercentage=0.1):

    generation_size = len(population)

    mutated_pieces = [mutatePiece(current_piece, chordProgression) for current_piece in population]

    mutated_pieces.sort(key=lambda piece: -1 * fitness(piece, chordProgression, originalPiece))

    spliced_pieces = []

    # breed the best pieces with eachother
    for i in range(0, len(mutated_pieces), 2):
        spliced_pieces += combinePieces(mutated_pieces[i], mutated_pieces[i + 1])

    # breed best w/ worst, second best w/ second worst, etc
    for i in range(0, len(mutated_pieces) // 2):
        spliced_pieces += combinePieces(mutated_pieces[i], mutated_pieces[len(mutated_pieces) - 1 - i])

    spliced_pieces.sort(key=lambda piece: -1 * fitness(piece, chordProgression, originalPiece))


    num_bad = int(generation_size * badPercentage)
    num_good = generation_size - num_bad

    return spliced_pieces[:num_good] + spliced_pieces[(len(spliced_pieces) - num_bad):]