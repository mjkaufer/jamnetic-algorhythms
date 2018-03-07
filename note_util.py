from midiutil.MidiFile import MIDIFile

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

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            # do an absolute value comparison for floating point error
            return self.midi_note == other.midi_note and abs(self.duration - other.duration) <= 1e-7

        return False

    def __radd__(self, other):
        # so we can call sum(measure) and get a value which represents the measure duration
        # this should always be around 4

        if isinstance(other, int) or isinstance(other, float):
            return self.duration + other
        else:
            return self.duration + other.duration

    def __lt__(self, other):
        if self is None or self.midi_note is None:
            return False
        if other is None or other.midi_note is None:
            return True

        return self.midi_note < other.midi_note

    def __le__(self, other):
        if self is None or self.midi_note is None:
            return False
        if other is None or other.midi_note is None:
            return True

        return self.midi_note <= other.midi_note

    def __gt__(self, other):
        if self is None or self.midi_note is None:
            return False
        if other is None or other.midi_note is None:
            return True

        return self.midi_note > other.midi_note

    def __ge__(self, other):
        if self is None or self.midi_note is None:
            return False
        if other is None or other.midi_note is None:
            return True

        return self.midi_note >= other.midi_note

    def __ne__(self, other):
        return not self.__eq__(other)

def evaluatePieceFitness(originalPiece, currentPiece, chordProgression):
    pass

def getNonRestNotes(measure):
    return [i for i in range(len(measure)) if not measure[i].is_rest()]

def isMeasureSilent(measure):
    return len(getNonRestNotes(measure)) == 0

def writePiece(piece, title='Genetic Algos', filename='./pieces/untitled.mid', bpm=120, debug=False):
    mf = MIDIFile(1)
    track = 0
    time = 0

    mf.addTrackName(track, time, title)
    mf.addTempo(track, time, bpm)

    # add some notes
    channel = 0
    volume = 100

    for measure in piece:
        for note in measure:
            if note.midi_note is not None:
                mf.addNote(track, channel, note.midi_note, time, note.duration, volume)        

            time += note.duration

    with open(filename, 'wb') as outf:
        mf.writeFile(outf)
        if debug:
            print("Writing to", fname)