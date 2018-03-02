from midiutil.MidiFile import MIDIFile
from random import seed

from all_of_me import piece, chord_progression
from genetic_algos import mutatePiece

# currently just mutating, no fitness

seed_num = 100
iter_count = 100

seed(seed_num)


for i in range(iter_count):

    mf = MIDIFile(1)
    track = 0
    time = 0
    bpm = 120

    mf.addTrackName(track, time, "Genetic Algos")
    mf.addTempo(track, time, bpm)

    # add some notes
    channel = 0
    volume = 100

    for measure in piece:
        for note in measure:
            if note.midi_note is not None:
                mf.addNote(track, channel, note.midi_note, time, note.duration, volume)        

            time += note.duration

    fname = "./pieces/{}-{}.mid".format(seed_num, i)

    with open(fname, 'wb') as outf:
        mf.writeFile(outf)
        print("Writing to", fname)

    mutatePiece(piece, chord_progression)