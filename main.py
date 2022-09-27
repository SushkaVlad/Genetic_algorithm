import math
import pandas as pd
from chromosome import Chromosome
from population import Population


def initialize_algorithm(doc_name="examples.xlsx", config_sheet="config", main_list="test"):
    configuration = pd.read_excel(doc_name, sheet_name=config_sheet, nrows=8, usecols="A:B")
    settings = {"POPULATION_SIZE": int(configuration.iloc[0][1]),
                "NUMBER_OF_CHILDREN": int(configuration.iloc[1][1]),
                "CROSSOVER_PROB": configuration.iloc[2][1],
                "MUTATION_PROB": configuration.iloc[3][1],
                "ELITE_PERCENTAGE": configuration.iloc[4][1],
                "MAX_POPULATIONS": int(configuration.iloc[5][1]),
                "THRESHOLD_EPS": configuration.iloc[6][1],
                "MATRIX_DIMENSION": int(configuration.iloc[7][1])}
    settings["DISTANCE_MATRIX"] = pd.read_excel(doc_name,
                                                sheet_name=main_list,
                                                usecols=list(range(1, settings["MATRIX_DIMENSION"] + 1)),
                                                nrows=settings["MATRIX_DIMENSION"]).values
    Chromosome.DISTANCE_MATRIX = settings["DISTANCE_MATRIX"]
    Chromosome.CHROMOSOME_LENGTH = len(settings["DISTANCE_MATRIX"])
    Chromosome.MUTATION_PROB = settings["MUTATION_PROB"]
    Population.POPULATION_SIZE = settings["POPULATION_SIZE"]
    Population.ELITE_PERCENTAGE = settings["ELITE_PERCENTAGE"]
    Population.CROSSOVER_PROB = settings["CROSSOVER_PROB"]
    Population.NUMBER_OF_CHILDREN = settings["NUMBER_OF_CHILDREN"]
    Population.INTERMEDIATE_POPULATION = settings["NUMBER_OF_CHILDREN"] + settings["POPULATION_SIZE"]
    return settings["MAX_POPULATIONS"], settings["THRESHOLD_EPS"]


def run_genetic_algorithm():
    max_populations, threshold_eps = initialize_algorithm()
    counter = 0
    eps = math.inf
    population = Population()
    while counter < max_populations and threshold_eps < eps:
        prev_population_fitness = population.get_population_fitness()
        population.generate_children()
        new_population = population.survivors_selection()
        population = Population(new_population)
        eps = abs(population.get_population_fitness() - prev_population_fitness)
        counter += 1
    print(population.sort_by_fitness())


if __name__ == "__main__":
    initialize_algorithm()
    run_genetic_algorithm()
