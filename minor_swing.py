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


Am6  = transpose(m6, root_c - 3)
Dm6  = transpose(m6, root_c + 2)
E7  = transpose(d7, root_c + 4)
Bb7  = transpose(d7, root_c - 2)



chord_progression = [
    # intro first round
    Am6, Dm6, Am6, Dm6, 
    Am6, Dm6, E7, Bb7,

    # intro second round
    Am6, Dm6, Am6, Dm6, 
    Am6, Dm6, E7, Bb7,


    Am6, Am6, Dm6, Dm6,
    E7, E7, Am6, Am6,
    Dm6, Dm6, Am6, Am6,
    Bb7, E7, Am6, E7
]

piece = convert('minor_swing.mxl')

def getPiece():
    return (piece, chord_progression, 'Minor Swing')