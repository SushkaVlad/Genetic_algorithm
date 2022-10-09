import math
import time
from constants import SETTINGS, MAX_DIMENSION
from helpers.generate_helpers import check_if_same_solutions
from helpers.configurations import read_excel_configurations, initialize_classes_excel, \
    initialize_classes_from_constants
from population import Population


# use configurations from excel
def run_excel_algorithms(excel_settings):
    for settings in excel_settings:
        initialize_classes_excel(settings)
        print(f"Solution for matrix of dimension ", len(settings["DISTANCE_MATRIX"]))
        solutions = run_genetic_algorithm(settings["MAX_POPULATIONS"], settings["THRESHOLD_EPS"])
        print(solutions[0:5])
        print("=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)")


# generate matrices and solutions (settings are taken from constants)
def run_generated_algorithms():
    for dimension in range(5, MAX_DIMENSION + 1):
        expected_solution = initialize_classes_from_constants(SETTINGS, dimension)
        print(f"Solution for matrix of dimension ", dimension)
        solutions = run_genetic_algorithm(SETTINGS["MAX_POPULATIONS"], SETTINGS["THRESHOLD_EPS"])
        print(solutions[0:5])
        print(expected_solution)
        if check_if_same_solutions(solutions[0].solution, expected_solution):
            print("Yeeeeeeeah, we have found solution!")
        else:
            print("Unfortunately, we haven't found solution")
        print("=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)=)")


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
    return population.sort_by_fitness()


if __name__ == "__main__":
    start_time = time.time()
    excel_settings = read_excel_configurations()
    # run_excel_algorithms(excel_settings)  # run from excel
    run_generated_algorithms()  # run from constants settings + program generation of matrices and solutions
    print("--- %s seconds ---" % (time.time() - start_time))
