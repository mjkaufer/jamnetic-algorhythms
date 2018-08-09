from note_util import transpose, GANote

M   = [0, 4, 7]

root_c = 72

C = transpose(M, root_c)
F = transpose(M, root_c + 5)

chord_progression = [
    F, F, C, F,
    F, F, C, F,

    F, F, C, F,
    F, F, C, F,
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
    [N(root_c + 9, q), N(root_c + 7, q), N(root_c + 5, q), N(root_c + 7, q)],
    [N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, h)],
    [N(root_c + 7, q), N(root_c + 7, q), N(root_c + 7, h)],
    [N(root_c + 9, q), N(root_c + 12, q), N(root_c + 12, h)],
    
    [N(root_c + 9, q), N(root_c + 7, q), N(root_c + 5, q), N(root_c + 7, q)],
    [N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, q)],
    [N(root_c + 7, q), N(root_c + 7, q), N(root_c + 9, q), N(root_c + 7, q)],
    [N(root_c + 5, w)],

    # repeat
    [N(root_c + 9, q), N(root_c + 7, q), N(root_c + 5, q), N(root_c + 7, q)],
    [N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, h)],
    [N(root_c + 7, q), N(root_c + 7, q), N(root_c + 7, h)],
    [N(root_c + 9, q), N(root_c + 12, q), N(root_c + 12, h)],
    
    [N(root_c + 9, q), N(root_c + 7, q), N(root_c + 5, q), N(root_c + 7, q)],
    [N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, q), N(root_c + 9, q)],
    [N(root_c + 7, q), N(root_c + 7, q), N(root_c + 9, q), N(root_c + 7, q)],
    [N(root_c + 5, w)],
       
]

def getPiece():
    return (piece, chord_progression, 'Mary Had A Little Lamb')