import random

from helpers.generate_helpers import generate_matrix_with_solution


class Chromosome:
    MUTATION_PROB = 0
    DISTANCE_MATRIX = []
    CHROMOSOME_LENGTH = 0

    def __init__(self, solution=None):
        if solution is not None:
            self.solution = solution[:]
        else:
            self.solution = self.generate_chromosome()
        self.fitness = self.get_chromosome_fitness()

    def generate_chromosome(self):
        chromosome = list(range(1, self.CHROMOSOME_LENGTH + 1))
        random.shuffle(chromosome)
        return chromosome

    def get_chromosome_fitness(self):
        fitness = 0
        for i in range(0, len(self.solution)):
            if i != len(self.solution) - 1:
                fitness += self.DISTANCE_MATRIX[self.solution[i] - 1][self.solution[i + 1] - 1]
            else:
                fitness += self.DISTANCE_MATRIX[self.solution[i] - 1][self.solution[0] - 1]
        return fitness

    def mutate(self):
        if random.random() < self.MUTATION_PROB:
            index_list = list(range(0, len(self.solution)))
            first_gene_index, second_gene_index = random.sample(index_list, 2)
            self.solution[first_gene_index], self.solution[second_gene_index] = \
                self.solution[second_gene_index], self.solution[first_gene_index]
            self.fitness = self.get_chromosome_fitness()

    def __repr__(self):
        return f"\nFitness - {self.fitness}. Route - {self.solution}."


if __name__ == "__main__":
    print("Playground with Chromosome class")

