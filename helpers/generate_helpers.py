import random

import numpy as np


# generate random solution (the same way as in the class Chromosome)
def generate_random_solution(dimension):
    solution = list(range(1, dimension + 1))
    random.shuffle(solution)
    return solution


# generate random solution and corresponding matrix
def generate_matrix_with_solution(dimension, low_cost=2):
    expected_solution = generate_random_solution(dimension)
    distance_matrix = np.random.randint(low=100, high=200, size=(dimension, dimension))
    for i in range(0, len(expected_solution)):
        distance_matrix[i][i] = 0
        if i != len(expected_solution) - 1:
            distance_matrix[expected_solution[i] - 1][expected_solution[i + 1] - 1] = low_cost
        else:
            distance_matrix[expected_solution[i] - 1][expected_solution[0] - 1] = low_cost
    return distance_matrix, expected_solution


# check if two arrays are the same solution (for example, [1,2,3] and [2,3,1] - answer True)
def check_if_same_solutions(for_check_solution, real_solution):
    first_gene = real_solution[0]
    first_gene_index = for_check_solution.index(first_gene)
    reformatted_check_solution = for_check_solution[first_gene_index:] + for_check_solution[:first_gene_index]
    for i in range(0, len(real_solution)):
        if real_solution[i] != reformatted_check_solution[i]:
            return False
    return True


if __name__ == "__main__":
    print("Playground with generate helpers")
