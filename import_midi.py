import sys
import pretty_midi
import note_util

def exit(reason=None):
    if reason is not None:
        print(reason)
    print("Exiting")
    sys.exit(0)

if len(sys.argv) != 2:
    exit("Usage is python import_midi.py <midi file>")
    

filename = sys.argv[1]

bpm = None

with open(filename, 'rb') as f:
    byte = 'ignore'
    byte_list = []

    while byte != b'':
        byte = f.read(1)
        byte_list.append(byte.hex())
        # print(byte.hex())

        i = 4
        if len(byte_list) > i and byte_list[-i] == '00' and byte_list[-i+1] == 'ff' and byte_list[-i+2] == '51' and byte_list[-i+3] == '03':
            next_bytes = f.read(2).hex()
            
            bpm = round(234000 / int(next_bytes, 16))
            print("bpm is", bpm)

if bpm is None:
    exit("No BPM set in your midi - please add one")


midi_stream = pretty_midi.PrettyMIDI(filename)
notes = midi.instruments[0].notes

def updateNoteEndTime(pretty_midi_note):

    # slight underestimate, but better to be too short in measure than too long
    decay_constant = 1.05

    delta = pretty_midi_note.end - pretty_midi_note.start
    pretty_midi_note.end = delta * decay_constant + pretty_midi_note.start

