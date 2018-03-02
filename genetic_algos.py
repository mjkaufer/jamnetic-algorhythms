from random import random, choices

from mutators import pickRandomChordTone, copyNoteInMeasure, transposeWholeNote, becomeLeadingNote, subdivide, copyNoteFromSimilarChord, shiftNotes, shuffleNotes, dropNote, swapNotes
from note_util import isMeasureSilent, getNonRestNotes

measures_to_change_per_mutation = 4
max_attempts = 100

def mutatePiece(currentPiece, chordProgression):
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

    mutators = [pickRandomChordTone, copyNoteInMeasure, transposeWholeNote, becomeLeadingNote, subdivide, copyNoteFromSimilarChord, shiftNotes, shuffleNotes, dropNote, swapNotes]
    probabilities = [0.25, 0.125, 0.125, 0.25 * (1 - quanta), 0.25 * quanta, 0.05, 0.05, 0.05, 0.05, 0.05]

    mutator = choices(mutators, weights=probabilities)[0]

    return mutator(currentPiece, chordProgression, measureIndex, noteIndex)

def combinePieces(firstPiece, secondPiece):
    pass