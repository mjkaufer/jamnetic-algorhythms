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

def evaluatePieceFitness(originalPiece, currentPiece, chordProgression):
    pass

def mutatePiece(currentPiece, chordProgression):
    pass

def combinePieces(firstPiece, secondPiece):
    pass