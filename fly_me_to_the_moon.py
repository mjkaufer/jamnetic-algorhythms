from note_util import transpose, GANote
from convert import convert

M6  =  [0, 4, 7, 9]
m6  =  [0, 3, 7, 9]
m7  =  [0, 3, 7, 10]
d7  =  [0, 4, 7, 10]
M7  =  [0, 4, 7, 11]
d9  =  [0, 4, 7, 10, 14]
d13 =  [0, 4, 7, 10, 14, 17, 21]
m7b5 = [0, 3, 6, 10]

root_c = 72


C6      = transpose(M6, root_c)
CM7     = transpose(M7, root_c)
Dm7     = transpose(m7, root_c + 2)
Am7     = transpose(m7, root_c - 3)
G7      = transpose(d7, root_c - 5)
A7      = transpose(d7, root_c - 3)
FM7     = transpose(M7, root_c + 5)
Bm7b5   = transpose(m7b5, root_c - 1)
E7      = transpose(d7, root_c + 4)
Em7     = transpose(m7, root_c + 4)



chord_progression = [
    # A section
    Am7, Dm7, G7, CM7,
    FM7, Bm7b5, E7, Am7,
    Dm7, G7, CM7, Em7,
    Dm7, G7, CM7, Bm7b5,

    # B section
    Am7, Dm7, G7, CM7,
    FM7, Bm7b5, E7, Am7,
    Dm7, G7, Em7, A7,
    Dm7, G7, CM7, Bm7b5,
]

piece = convert('fly_me_to_the_moon.mxl')

def getPiece():
    return (piece, chord_progression, 'All of Me')