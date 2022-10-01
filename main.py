import math
import pandas as pd
from chromosome import Chromosome
from population import Population


def read_all_configurations(doc_name="examples.xlsx", list_of_sheets=("5x5", "6x6", "7x7", "8x8", "9x9", "10x10")):
    list_of_settings = []
    for sheet in list_of_sheets:
        configuration = pd.read_excel(doc_name, sheet_name=sheet, nrows=8, usecols="A:B")
        settings = {"POPULATION_SIZE": int(configuration.iloc[0][1]),
                    "NUMBER_OF_CHILDREN": int(configuration.iloc[1][1]),
                    "CROSSOVER_PROB": configuration.iloc[2][1],
                    "MUTATION_PROB": configuration.iloc[3][1],
                    "ELITE_PERCENTAGE": configuration.iloc[4][1],
                    "MAX_POPULATIONS": int(configuration.iloc[5][1]),
                    "THRESHOLD_EPS": configuration.iloc[6][1],
                    "MATRIX_DIMENSION": int(configuration.iloc[7][1])}
        settings["DISTANCE_MATRIX"] = pd.read_excel(doc_name,
                                                    sheet_name=sheet,
                                                    usecols=list(range(4, settings["MATRIX_DIMENSION"] + 4)),
                                                    nrows=settings["MATRIX_DIMENSION"]).values
        list_of_settings.append(settings)
    return list_of_settings


def run_all_algorithms(all_settings):
    for settings in all_settings:
        Chromosome.DISTANCE_MATRIX = settings["DISTANCE_MATRIX"]
        Chromosome.CHROMOSOME_LENGTH = len(settings["DISTANCE_MATRIX"])
        Chromosome.MUTATION_PROB = settings["MUTATION_PROB"]
        Population.POPULATION_SIZE = settings["POPULATION_SIZE"]
        Population.ELITE_PERCENTAGE = settings["ELITE_PERCENTAGE"]
        Population.CROSSOVER_PROB = settings["CROSSOVER_PROB"]
        Population.NUMBER_OF_CHILDREN = settings["NUMBER_OF_CHILDREN"]
        Population.INTERMEDIATE_POPULATION = settings["NUMBER_OF_CHILDREN"] + settings["POPULATION_SIZE"]
        print(f"Solution for matrix of dimension ", len(settings["DISTANCE_MATRIX"]))
        run_genetic_algorithm(settings["MAX_POPULATIONS"], settings["THRESHOLD_EPS"])


def run_genetic_algorithm(max_populations, threshold_eps):
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
    print("==============================================================================================")


if __name__ == "__main__":
    all_settings = read_all_configurations()
    run_all_algorithms(all_settings)
