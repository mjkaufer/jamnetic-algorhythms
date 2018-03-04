from random import seed
from copy import deepcopy

from all_of_me import piece, chord_progression
from genetic_algos import generation
from note_util import writePiece

# currently just mutating, no fitness

seed_num = 18
iter_count = 400

seed(seed_num)

population_size = 20
original_piece = deepcopy(piece)

population = [deepcopy(piece) for i in range(population_size)]


for gen_num in range(iter_count):

    population = generation(population, chord_progression, piece)
    title = 'All of Me ft. Genetic Algos, Gen {}'.format(gen_num)

    for index in [0, len(population) - 1]:
        fname = './pieces/Gen{}-Rank-{}-Seed{}.mid'.format(gen_num, index, seed_num)
        
        writePiece(population[index], title, fname)

    