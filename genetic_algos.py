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

    quanta = (currentPiece[measureIndex][noteIndex].duration / 4.0) ** 1.5

    enable_become_leading = 0
    # issues with becoming leading note bc note being lead to often changes
    # maybe consider just leading into chord progression's root?

    mutators = [pickRandomChordTone, copyNoteInMeasure, transposeWholeNote, becomeLeadingNote, subdivide, copyNoteFromSimilarChord, shiftNotes, shuffleNotes, dropNote, swapNotes]
    probabilities = [0.25, 0.125, 0.125, 0.25 * (1 - quanta) * enable_become_leading, 0.25 * quanta, 0.05, 0.05, 0.05, 0.05, 0.05]

    mutator = choices(mutators, weights=probabilities)[0]

    return mutator(currentPiece, chordProgression, measureIndex, noteIndex)

def generateMeasureContour(measure, last_midi=None):
    # [[normalized same, normalized (half/whole)steps up, normalized (half/whole)steps down, normalized leaps up, normalized leaps down], ...]
    current_measure_contour = [0, 0, 0, 0, 0]

    for note in measure:
        if last_midi is not None and note.midi_note is not None:
            d = note.midi_note - last_midi

            index = 0

            if 0 < abs(d) <= 2:
                if d > 0:
                    index = 1
                else:
                    index = 2
            elif abs(d) > 2:
                if d > 0:
                    index = 3
                else:
                    index = 4

            current_measure_contour[index] += 1

        last_midi = note.midi_note

    return last_midi, normalize(current_measure_contour)


def distSquared(a, b, backwards=False):
    d = 0

    for i in range(len(a)):
        opposite_index = i

        # 1 -> 2, 2 -> 1, 3 -> 4, 4 -> 3, etc
        if backwards and i != 0:
            opposite_index = i + 1
            if opposite_index % 2 == 1:
                opposite_index -= 2

        d += (a[i] - b[opposite_index]) ** 2

    return d

def normalize(a):
    d = distSquared(a, [0] * len(a)) ** 0.5

    if d == 0:
        return a

    return [i / d for i in a]

# if backwards, something with strictly leap increasing is equivalent to something with strictly leap decreasing
def contourDistanceSquared(countour_a, countour_b, backwards=False):
    distance_squared = 0

    for i in range(len(countour_a)):
        a = countour_a[i]
        b = countour_b[i]

        distance_squared += distSquared(a, b)

    if backwards:
        backwards_distance_squared = 0

        for i in range(len(countour_a)):
            a = countour_a[i]
            b = countour_b[i]

            backwards_distance_squared += distSquared(a, b, backwards=True)

        distance_squared = min(backwards_distance_squared, distance_squared)

    return distance_squared

def generatePieceContour(piece):

    last_midi = None

    contour = []

    for measure in piece:
        last_midi, current_measure_contour = generateMeasureContour(measure, last_midi)
        contour.append(current_measure_contour)

    return contour

def fitness(currentPiece, chordProgression, originalPiece, originalContour=None):
    points = 0

    if originalContour is None:
        originalContour = generatePieceContour(originalPiece)

    new_contour = generatePieceContour(currentPiece)

    points -= contourDistanceSquared(originalContour, new_contour, True) / len(originalContour) * 0.5

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
                    points -= 1

                    # if the first note is an ugly interval from the chord's root
                    if first_note_and_chord_root_delta == 1 or first_note_and_chord_root_delta == 6:
                        points -= 1.5

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

                    # # temporarily comment this out
                    # elif not (midi_note % 12 in next_measure_chord_tones):
                    #     points -= 0.25

        # if just the same note is played
        if len(distinct_notes) <= 1:
            points -= 0.5

        # if the only note is a whole note, smh
        if measure[0].duration == 4:
            points -= 1.5

        if measure[0].duration < 1 / 8.0:
            # no 32nd notes pls
            points -= 2.0

        # if there are literally no notes from the chord
        if num_chord_tones == 0:
            points -= (1 + len(getNonRestNotes(measure)) * 1.5)

        # if literally nothing has changed between mutated piece and original;
        # we can use equality here because GANote overrides default equality comparator
        if measure == originalPiece[measure_index]:
            points -= 2

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
    split_indices = sample(range(len(firstPiece)), min(6, len(firstPiece) * 3 // 2))

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

    contour = generatePieceContour(originalPiece)

    mutated_pieces.sort(key=lambda piece: -1 * fitness(piece, chordProgression, originalPiece, contour))

    spliced_pieces = []

    # breed the best pieces with eachother
    for i in range(0, len(mutated_pieces), 2):
        spliced_pieces += combinePieces(mutated_pieces[i], mutated_pieces[i + 1])

    # breed best w/ worst, second best w/ second worst, etc
    for i in range(0, len(mutated_pieces) // 2):
        spliced_pieces += combinePieces(mutated_pieces[i], mutated_pieces[len(mutated_pieces) - 1 - i])

    spliced_pieces.sort(key=lambda piece: -1 * fitness(piece, chordProgression, originalPiece, contour))


    num_bad = int(generation_size * badPercentage)
    num_good = generation_size - num_bad

    return spliced_pieces[:num_good] + spliced_pieces[(len(spliced_pieces) - num_bad):]