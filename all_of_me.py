from note_util import transpose, GANote

M6  = [0, 4, 7, 9]
m6  = [0, 3, 7, 9]
m7  = [0, 3, 7, 10]
d7  = [0, 4, 7, 10]
M7  = [0, 4, 7, 11]
d9  = [0, 4, 7, 10, 14]
d13 = [0, 4, 7, 10, 14, 17, 21]

root_c = 72


C6  = transpose(M6, root_c)
E7  = transpose(d7, root_c + 4)
A7  = transpose(d7, root_c - 3)
Dm7 = transpose(m7, root_c + 2)
Am7 = transpose(m7, root_c - 3)
D13 = transpose(d13, root_c + 2)
G7  = transpose(d7, root_c - 5)
F6  = transpose(M6, root_c + 5)
Fm6 = transpose(m6, root_c + 5)
Em7 = transpose(m7, root_c + 4)
A9  = transpose(d9, root_c - 3)
G13 = transpose(d13, root_c - 5)


chord_progression = [
    # A section
    C6, C6, E7, E7,
    A7, A7, Dm7, Dm7,
    E7, E7, Am7, Am7,
    D13, D13, Dm7, G7,

    # B section
    C6, C6, E7, E7,
    A7, A7, Dm7, Dm7,
    F6, Fm6, Em7, A9,
    Dm7, G13, C6, (Dm7 + G7)
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
    # A section
    [N(root_c, q * d), N(root_c - 5, e), N(root_c - 8, h)],
    [N(root_c - 8, h), N(root_c, t), N(root_c + 2, t), N(root_c, t)],
    [N(root_c - 1, q * d), N(root_c - 4, e), N(root_c - 8, h)],
    [N(root_c - 8, w)],

    [N(root_c - 3, q * d), N(root_c - 5, e), N(root_c - 8, h)],
    [N(root_c - 8, q), N(root_c - 9, q), N(root_c - 8, t), N(root_c - 2, t), N(root_c - 3, t)],
    [N(root_c - 5, h), N(root_c - 7, h)],
    [N(root_c - 7, w)],

    [N(root_c - 8, q * e), N(root_c - 9, e), N(root_c - 10, h)],
    [N(root_c - 10, h), N(root_c - 8, t), N(root_c - 4, t), N(root_c - 1, t)],
    [N(root_c + 2, h), N(root_c, h)],
    [N(root_c, w)],

    [N(root_c - 1, q * d), N(root_c - 2, e), N(root_c - 3, h)],
    [N(root_c - 3, h), N(root_c - 3, t), N(root_c + 2, t), N(root_c - 1, t)],
    [N(root_c - 3, w)],
    [N(root_c - 1, w)],

    # B section
    [N(root_c, q * d), N(root_c - 5, e), N(root_c - 8, h)],
    [N(root_c - 8, h), N(root_c, t), N(root_c + 2, t), N(root_c, t)],
    [N(root_c - 1, q * d), N(root_c - 4, e), N(root_c - 8, h)],
    [N(root_c - 8, w)],

    [N(root_c - 3, q * d), N(root_c - 5, e), N(root_c - 8, h)],
    [N(root_c - 8, q), N(root_c - 9, q), N(root_c - 8, t), N(root_c - 2, t), N(root_c - 3, t)],
    [N(root_c - 5, h), N(root_c - 7, h)],
    [N(root_c - 7, w)],

    [N(root_c + 2, h), N(root_c, q), N(root_c - 1, q)],
    [N(root_c + 2, h * d), N(root_c, q)],
    [N(root_c - 1, h), N(root_c - 8, q), N(root_c - 5, q)],
    [N(root_c - 1, h * d), N(root_c - 3, q)],

    [N(root_c, h), N(root_c - 3, q), N(root_c, q)],
    [N(root_c + 4, h), N(root_c + 4, h)],
    [N(root_c, h), N(root_c + 3, h)],
    [N(root_c + 2, h * d), N(root_c - 3, e), N(root_c - 5, h)]
       
]