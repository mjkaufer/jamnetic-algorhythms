from random import random, choices, sample
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

        for note_index in range(len(measure)):
            note = measure[note_index]
            midi_note = note.midi_note

            if midi_note is not None:

                distinct_notes.add(midi_note)
                if midi_note % 12 in chord_tones:
                    num_chord_tones += 1

                min_note = min(min_note, midi_note)
                max_note = min(max_note, midi_note)

                # if the note is the first note and it doesn't belong
                # make sure we're not unjustly penalizing a maj7 / m7b5
                if note_index == 0 and (midi_note % 12) not in chord_tones:
                    first_note_and_chord_root_delta = abs((midi_note % 12) - chord_tones[0])
                    points -= 0.5

                    # if the first note is an ugly interval from the chord's root
                    if first_note_and_chord_root_delta == 1 or first_note_and_chord_root_delta == 6:
                        points -= 1

                # if the last note doesn't have a value from the next chord in it
                if note_index == len(measure) - 1 and measure_index < len(currentPiece) - 1:
                    next_measure_chord_tones = [next_measure_chord_note % 12 for next_measure_chord_note in chordProgression[measure_index + 1]]

                    # last_note_and_next_chord_root_delta = abs((midi_note % 12) - next_measure_chord_tones[0])

                    # if the leading note to the next chord is the root note of the next chord, which usually sounds trash
                    if midi_note % 12 == next_measure_chord_tones[0]:
                        points -= 1.5
                    # if there's not a nice leading note to the next chord
                    # used to look at stuff like if it's a half step from the root chord tone, but that's redundant
                    # bc most jazz pieces have the 7th in them, so we might have a m7 note lead to a maj7 chord
                    elif not (midi_note % 12 in next_measure_chord_tones):
                        points -= 0.25

        # if just the same note is played
        if len(distinct_notes) <= 1:
            points -= 1

        # if the only note is a whole note, smh
        if measure[0].duration == 4:
            points -= 1.5

        # if there are literally no notes from the chord
        if num_chord_tones == 0:
            points -= (1 + len(getNonRestNotes(measure)))

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

            # if there's a two octave jump, dock another point and a half
            if note_delta > 24:
                points -= 1.5
        else:
            # this means that no real notes were logged at all, aka the measure was just silence
            points -= 2

        if measure_index > 0:
            prev_measure = currentPiece[measure_index - 1]

            # if there are really big jumps between measures
            if not isMeasureSilent(measure) and not isMeasureSilent(prev_measure) and max(abs(min(prev_measure).midi_note - max(measure).midi_note), abs(max(prev_measure).midi_note - min(measure).midi_note)) > 17:
                points -= 0.5

        if measure_index < len(currentPiece) - 1:
            next_measure = currentPiece[measure_index + 1]

            # if there are really big jumps between measures
            if not isMeasureSilent(measure) and not isMeasureSilent(next_measure) and max(abs(min(next_measure).midi_note - max(measure).midi_note), abs(max(next_measure).midi_note - min(measure).midi_note)) > 17:
                points -= 0.5



    return points

def combinePieces(firstPiece, secondPiece):
    split_indices = sample(range(len(firstPiece)), min(6, len(firstPiece) // 1.5))

    results = []

    for split_index in split_indices:
        results += [
            firstPiece[:split_index] + secondPiece[split_index:],
            secondPiece[:split_index] + firstPiece[split_index:]
        ]

    return results

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