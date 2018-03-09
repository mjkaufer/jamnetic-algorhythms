from note_util import transpose, GANote

M6      = [0, 4, 7, 9]
m6      = [0, 3, 7, 9]
m7      = [0, 3, 7, 10]
d7      = [0, 4, 7, 10]
M7      = [0, 4, 7, 11]
d9      = d7 + [14]
d13     = d9 + [17, 21]
d7b9    = d7 + [13]
m7b9    = m7 + [13]

root_c = 72

Am7     = transpose(m7, root_c - 3)
Dm7     = transpose(m7, root_c + 2)
Bm7b9   = transpose(m7b9, root_c - 1)
E7b9    = transpose(d7b9, root_c + 4)
Cm7     = transpose(m7, root_c)
F7      = transpose(d7, root_c + 5)
Bbmaj7  = transpose(M7, root_c - 2)

chord_progression = [
    Am7, Am7, Dm7, Dm7,
    Bm7b9, E7b9, Am7, Am7,
    Cm7, F7, Bbmaj7, Bbmaj7,
    Bm7b9, E7b9, Am7, Am7
]

# variable shortcuts for ease of writing
N = GANote
w = 4
h = 2
q = 1.
e = 0.5
s = 0.25
t = 2/3.0
d = 1.5

piece = [
    # each line is a measure
    [N(root_c + 4, q * d), N(root_c + 2, e), N(root_c, e), N(root_c - 1, e), N(None, e), N(root_c - 3, e)],
    [N(root_c - 3, h), N(None, e), N(root_c - 5, q), N(root_c - 7, e)],
    [N(root_c - 7, h), N(None, e), N(root_c + 4, q), N(root_c + 2, e)],
    [N(root_c + 2, w)],

    [N(root_c + 2, q * d), N(root_c, e), N(root_c - 1, e), N(root_c - 3, e), N(None, e), N(root_c - 5, e)],
    [N(root_c - 5, h), N(None, e), N(root_c - 7, q), N(root_c - 8, e)],
    [N(root_c - 8, h), N(None, e), N(root_c + 2, q), N(root_c, e)],
    [N(root_c, w)],

    [N(root_c, q * d), N(root_c - 2, e), N(root_c - 3, e), N(root_c - 5, e), N(None, e), N(root_c - 7, e)],
    [N(root_c - 7, h), N(None, e), N(root_c - 10, q), N(root_c - 9, e)],
    [N(root_c - 9, q * d), N(root_c - 10, e), N(root_c - 5, q * d), N(root_c - 7, e)],
    [N(root_c - 7, w)],
    
    [N(root_c - 7, q), N(root_c - 8, e), N(root_c - 5, h), N(root_c - 7, e)],
    [N(root_c - 7, q), N(root_c - 8, e), N(root_c - 5, h), N(root_c - 7, e)],
    [N(root_c - 8, w)],
    [N(root_c - 8, h * d), N(root_c - 8, q)],
]

def getPiece():
    return (piece, chord_progression, 'Blue Bossa')