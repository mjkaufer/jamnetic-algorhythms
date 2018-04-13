import sys
from random import seed
from copy import deepcopy

# from all_of_me import piece, chord_progression as all_of_me_piece, all_of_me_chords
# from blue_bossa import piece, chord_progression as blue_bossa_piece, blue_bossa_chords
# from all_of_me import getPiece as allOfMe
# from blue_bossa import getPiece as blueBossa
import all_of_me, blue_bossa, another_day_of_sun, minor_swing, fly_me_to_the_moon

from genetic_algos import generation
from note_util import writePiece

seed_num = 42
iter_count = 100

pieces = [
    all_of_me.getPiece(),
    blue_bossa.getPiece(),
    another_day_of_sun.getPiece(),
    minor_swing.getPiece(),
    fly_me_to_the_moon.getPiece()
    # (all_of_me.piece, all_of_me.chord_progression, "All of Me"),
    # (blue_bossa.piece, blue_bossa.chord_progression, "Blue Bossa")
]

piece_num = 2

# piece_indices_to_double = [2]
piece_indices_to_double = []

piece, chord_progression, piece_title = pieces[piece_num]

if piece_num in piece_indices_to_double:
    piece = deepcopy(piece * 2)
    chord_progression = deepcopy(chord_progression * 2)

print(piece_title)

if len(sys.argv) == 0:
    print("FYI, usage is python main.py <seed number> <number of generations>")
    print("Don't worry, we'll use the default values for you")

if len(sys.argv) > 1:
    try:
        seed_num = int(sys.argv[1])
    except ValueError:
        print("Invalid seed param; using {} instead".format(seed_num))

if len(sys.argv) > 2:
    try:
        iter_count = int(sys.argv[2])
    except ValueError:
        print("Invalid generation number; using {} instead".format(iter_count))

print("Running on {} with seed of {} and generation number of {}".format(piece_title, seed_num, iter_count))

seed(seed_num)

population_size = 20
original_piece = deepcopy(piece)

population = [deepcopy(piece) for i in range(population_size)]

writePiece(piece, chord_progression, 'init', 'init.mid')

for gen_num in range(iter_count):

    population = generation(population, chord_progression, piece)
    title = '{} ft. Genetic Algos, Gen {}'.format(piece_title, gen_num)

    for index in [0, len(population) - 1]:
        fname = './pieces/Seed{}-Gen{}-Rank{}.mid'.format(seed_num, gen_num, index)
        
        writePiece(population[index], chord_progression, title, fname)

    