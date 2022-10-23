import math
import random
import time

from joblib import Parallel, delayed
from tqdm import tqdm

from constants import PARALLEL_SETTINGS, MAX_DIMENSION
from helpers.generate_helpers import check_if_same_solutions, generate_matrix_with_solution
from population import Population
from chromosome import Chromosome


# def migrate_best_to_the_next(from_population, to_population, percentage_to_migrate):
#     chromosomes_number_to_migrate = math.ceil(percentage_to_migrate * len(from_population.population))
#     print(from_population, "from pop")
#     chromosomes_to_migrate = from_population.sort_by_fitness()[0: chromosomes_number_to_migrate]
#     print(chromosomes_to_migrate, "chromosomes_to_migrate")
#     remained_number = len(to_population.population) - chromosomes_number_to_migrate
#     return Population(to_population.sort_by_fitness()[0:remained_number] + chromosomes_to_migrate)
#
#
# def circle_migration(populations, percentage_to_migrate):
#     for i in range(len(populations)):
#         if i != len(populations) - 1:
#             populations[i + 1] = migrate_best_to_the_next(populations[i], populations[i + 1], percentage_to_migrate)
#         else:
#             populations[i] = migrate_best_to_the_next(populations[i], populations[0], percentage_to_migrate)

def migration(populations):
    best_chromosomes = []
    number_to_migrate = math.ceil(len(populations[0].population) * PARALLEL_SETTINGS["CHROMOSOMES_PERCENTAGE_TO_MIGRATE"])
    for i in range(len(populations)):
        best_chromosomes += populations[i].sort_by_fitness()[0: number_to_migrate]
    random.shuffle(best_chromosomes)
    for i in range(len(populations)):
        sorted_array = populations[i].sort_by_fitness()
        sorted_array.reverse()
        populations[i] = Population(
            sorted_array[number_to_migrate:] + random.sample(best_chromosomes, number_to_migrate))
    return populations


# generate matrices and solutions (settings are taken from constants)
def run_generated_algorithms():
    for dimension in range(15, MAX_DIMENSION + 1):
        Chromosome.DISTANCE_MATRIX, expected_solution = generate_matrix_with_solution(dimension)
        Chromosome.CHROMOSOME_LENGTH = dimension
        Chromosome.MUTATION_PROB = PARALLEL_SETTINGS["MUTATION_PROB"]
        Population.POPULATION_SIZE = int(
            PARALLEL_SETTINGS["OVERALL_POPULATIONS_SIZE"] / PARALLEL_SETTINGS["POPULATIONS_NUMBER"])
        Population.ELITE_PERCENTAGE = PARALLEL_SETTINGS["ELITE_PERCENTAGE"]
        Population.CROSSOVER_PROB = PARALLEL_SETTINGS["CROSSOVER_PROB"]
        Population.NUMBER_OF_CHILDREN = PARALLEL_SETTINGS["NUMBER_OF_CHILDREN"]
        Population.INTERMEDIATE_POPULATION = PARALLEL_SETTINGS["NUMBER_OF_CHILDREN"] + Population.POPULATION_SIZE

        print("Solution for matrix of dimension ", dimension)

        populations = run_parallel_algorithm()
        best_chromosomes = []
        for i in range(len(populations)):
            best_chromosomes_in_population = populations[i].sort_by_fitness()[0]
            # print(f"Best chromosomes in {i + 1} population", best_chromosomes_in_population)
            best_chromosomes.append(best_chromosomes_in_population)

        best_chromosome = Population(best_chromosomes).sort_by_fitness()[0]
        print("Actual ", best_chromosome.solution)
        print("Expected ", expected_solution)

        if check_if_same_solutions(best_chromosome.solution, expected_solution):
            print("Yeeeeeeeah, we have found solution!")
        else:
            print("Unfortunately, we haven't found solution")
        print("=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)")


def run_parallel_algorithm():
    populations = [Population() for _ in range(PARALLEL_SETTINGS["POPULATIONS_NUMBER"])]
    result = []
    for _ in tqdm(range(int(PARALLEL_SETTINGS["MAX_POPULATIONS"] / PARALLEL_SETTINGS["ITER_NUMBER_BEFORE_MIGRATE"]))):
        result = Parallel(n_jobs=1)(
            delayed(run_one_algorithm)(populations[i]) for i in range(PARALLEL_SETTINGS["POPULATIONS_NUMBER"]))
        populations = migration(result)
    return result


def run_one_algorithm(population):
    counter = 0
    eps = math.inf
    while counter < PARALLEL_SETTINGS["ITER_NUMBER_BEFORE_MIGRATE"] and PARALLEL_SETTINGS["THRESHOLD_EPS"] < eps:
        prev_population_fitness = population.get_population_fitness()
        population.generate_children()
        new_population = population.survivors_selection()
        population = Population(new_population)
        eps = abs(population.get_population_fitness() - prev_population_fitness)
        counter += 1
    return population


if __name__ == "__main__":
    start_time = time.time()
    # run from constants settings + program generation of matrices and solutions (uncomment/comment line below)
    run_generated_algorithms()
    print("--- %s seconds ---" % (time.time() - start_time))
