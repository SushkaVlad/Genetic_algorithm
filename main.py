from settings import SETTINGS
from chromosome import Chromosome
from population import Population


def setup_static_variables():
    Chromosome.DISTANCE_MATRIX = SETTINGS["DISTANCE_MATRIX2"]
    Chromosome.CHROMOSOME_LENGTH = len(SETTINGS["DISTANCE_MATRIX2"])
    Chromosome.MUTATION_PROB = SETTINGS["MUTATION_PROB"]
    Population.POPULATION_SIZE = SETTINGS["POPULATION_SIZE"]
    Population.ELITE_PERCENTAGE = SETTINGS["ELITE_PERCENTAGE"]
    Population.CROSSOVER_PROB = SETTINGS["CROSSOVER_PROB"]
    Population.NUMBER_OF_CHILDREN = SETTINGS["NUMBER_OF_CHILDREN"]
    Population.INTERMEDIATE_POPULATION = SETTINGS["NUMBER_OF_CHILDREN"] + SETTINGS["POPULATION_SIZE"]


def run_genetic_algoritm():
    setup_static_variables()
    counter = 0
    eps = 1_000_000_000_000
    population = Population()
    while counter < SETTINGS["MAX_POPULATIONS"] and SETTINGS["THRESHOLD_EPS"] < eps:
    # while counter < SETTINGS["MAX_POPULATIONS"]:
        print(population.get_population_fitness())
        prev_population_fitness = population.get_population_fitness()
        population.generate_children()
        new_population = population.survivors_selection()
        population = Population(new_population)
        eps = abs(population.get_population_fitness() - prev_population_fitness)
        counter += 1
    print(population.sort_by_fitness())


if __name__ == "__main__":
    run_genetic_algoritm()

#todo eps