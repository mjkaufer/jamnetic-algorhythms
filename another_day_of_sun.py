from note_util import transpose, GANote
from convert import convert

M6  = [0, 4, 7, 9]
m6  = [0, 3, 7, 9]
m7  = [0, 3, 7, 10]
d7  = [0, 4, 7, 10]
M7  = [0, 4, 7, 11]
d9  = [0, 4, 7, 10, 14]
d13 = [0, 4, 7, 10, 14, 17, 21]

root_c = 72


Fm7  = transpose(m7, root_c + 5)
Bb7  = transpose(d7, root_c - 2)
EbM7 = transpose(M7, root_c + 3)
C7   = transpose(d7, root_c)
Cm7  = transpose(m7, root_c)



chord_progression = [
    Fm7, Bb7, EbM7, C7,
    Fm7, Bb7, EbM7, Cm7,
    Fm7, Bb7, EbM7, C7,
    Fm7, Bb7, EbM7, Cm7,
]

piece = convert('another_day_of_sun_short.mxl')

def getPiece():
    return (piece, chord_progression, 'Another Day Of Sun')