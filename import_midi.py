import sys

if len(sys.argv) != 2:
    print("Usage is python import_midi.py <midi file>")
    sys.exit(0)

filename = sys.argv[1]

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
