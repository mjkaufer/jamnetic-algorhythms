from note_util import transpose, GANote
from convert import convert


m   = [0, 3, 7]
M   = [0, 4, 7]
d7  = [0, 4, 7, 10]
dim = [0, 3, 6]
in1 = [-5, 0, 4]

root_c = 72

Dm   = transpose(m, root_c + 2)
C7   = transpose(d7, root_c)
D7   = transpose(d7, root_c + 2)
F    = transpose(M, root_c + 5)
G7   = transpose(d7, root_c - 5)
Bb   = transpose(M, root_c - 2)
Bdim = transpose(dim, root_c - 1)
F1   = transpose(in1, root_c + 5)



chord_progression = [
    Dm, Dm, C7, F,
    Dm, Dm, G7, C7,
    Dm, Dm, C7, F,
    list(set(Bb + Bdim)), list(set(F1 + D7)), list(set(G7 + C7)), F
]

piece = convert('cantina.xml')

def getPiece():
    return (piece, chord_progression, 'Cantina Band')