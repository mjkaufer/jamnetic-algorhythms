def transpose(chord, root_note_midi):
    new_chord = []
    for note in chord:
        new_chord.append(note + root_note_midi)

    return new_chord

class GANote:
    # pass in 'None' for the midi_note if it's a rest
    # duration is a fraction, where a quarter note = 1
    # issues with this paradigm is you can't really do ties that well, but that's ok
    def __init__(self, midi_note, duration):
        self.midi_note = midi_note
        self.duration = duration

    # TODO, fill in mutation function
    def mutate(self):
        pass

    def is_rest(self):
        return self.midi_note is None

    def clone(self, new_midi_note=-1, new_duration=-1):
        if new_midi_note == -1:
            new_midi_note = self.midi_note

        if new_duration == -1:
            new_duration = self.duration

        return GANote(new_midi_note, new_duration)

    def __repr__(self):
        return str(self.midi_note) + ':' + str(self.duration)

def evaluatePieceFitness(originalPiece, currentPiece, chordProgression):
    pass

def getNonRestNotes(measure):
    return [i for i in range(len(measure)) if not measure[i].is_rest()]

def isMeasureSilent(measure):
    return len(getNonRestNotes(measure)) == 0