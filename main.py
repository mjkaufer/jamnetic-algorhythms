import sys
from random import seed
from copy import deepcopy

from all_of_me import piece, chord_progression
from genetic_algos import generation
from note_util import writePiece

seed_num = 42
iter_count = 100


if len(sys.argv) == 0:
    print("FYI, usage is python main.py <seed number> <number of generations>")
    print("Don't worry, we'll use the default values for you")

if len(sys.argv) >= 1:
    try:
        seed_num = int(sys.argv[1])
    except ValueError:
        print("Invalid seed param; using {} instead".format(seed_num))

if len(sys.argv) >= 2:
    try:
        iter_count = int(sys.argv[2])
    except ValueError:
        print("Invalid generation number; using {} instead".format(iter_count))

print("Running with seed of {} and generation number of {}".format(seed_num, iter_count))

seed(seed_num)

population_size = 20
original_piece = deepcopy(piece)

population = [deepcopy(piece) for i in range(population_size)]
# print([sum(measure) for measure in original_piece])

for gen_num in range(iter_count):

    population = generation(population, chord_progression, piece)
    title = 'All of Me ft. Genetic Algos, Gen {}'.format(gen_num)

    for index in [0, len(population) - 1]:
        fname = './pieces/Seed{}-Gen{}-Rank{}.mid'.format(seed_num, gen_num, index)
        
        writePiece(population[index], title, fname)

    