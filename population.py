import random
import math
import itertools
from chromosome import Chromosome

class Population:
    CROSSOVER_PROB = 0
    POPULATION_SIZE = 0
    NUMBER_OF_CHILDREN = 0
    ELITE_PERCENTAGE = 0
    INTERMEDIATE_POPULATION = POPULATION_SIZE + NUMBER_OF_CHILDREN

    def __init__(self, population=None):
        if population is not None:
            self.population = population
        else:
            self.population = self.generate_initial_population()
        self.fitness = self.get_population_fitness()

    def generate_initial_population(self):
        population = [Chromosome() for _ in range(0, self.POPULATION_SIZE)]
        return population

    def get_population_fitness(self):
        overall_fitness = 0
        for chromosome in self.population:
            overall_fitness += chromosome.fitness
        return overall_fitness / len(self.population)

    def choose_parents(self):
        parents = random.sample(self.population, 2)
        parent1, parent2 = parents[0], parents[1]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # ordered crossover
        if random.random() > self.CROSSOVER_PROB:
            return Chromosome(parent1), Chromosome(parent2)
        index_list = list(range(0, len(parent1)))
        start_index, stop_index = sorted(random.sample(index_list, 2))
        chunk1, chunk2 = parent1[start_index: stop_index + 1], parent2[start_index: stop_index + 1]
        offspring1 = [0] * start_index + chunk2 + [0] * (len(parent1) - stop_index - 1)
        offspring2 = [0] * start_index + chunk1 + [0] * (len(parent2) - stop_index - 1)
        missing_in_offspring1 = list(itertools.filterfalse(offspring1.__contains__, iter(parent1)))
        missing_in_offspring2 = list(itertools.filterfalse(offspring2.__contains__, iter(parent2)))
        missing_in_offspring1.reverse(), missing_in_offspring2.reverse()
        for i in range(0, len(parent1)):
            if offspring1[i] == 0:
                offspring1[i] = missing_in_offspring1.pop()
            if offspring2[i] == 0:
                offspring2[i] = missing_in_offspring2.pop()
        return Chromosome(offspring1), Chromosome(offspring2)

    def generate_children(self):
        while len(self.population) < self.INTERMEDIATE_POPULATION:
            parent1, parent2 = self.choose_parents()
            offspring1, offspring2 = self.crossover(parent1.solution, parent2.solution)
            offspring1.mutate()
            offspring2.mutate()
            self.population.extend([offspring1, offspring2])
        if len(self.population) > self.INTERMEDIATE_POPULATION:
            self.population.pop()

    def sort_by_fitness(self):
        return sorted(self.population, key=lambda chromosome: chromosome.fitness)

    def survivors_selection(self):
        sorted_population = self.sort_by_fitness()
        elite_chromosomes_number = math.ceil(self.ELITE_PERCENTAGE * len(self.population))
        new_population, tournament_participants = \
            sorted_population[0: elite_chromosomes_number], sorted_population[elite_chromosomes_number:]
        new_population.extend(self.tournament_winners(tournament_participants,
                                                      self.POPULATION_SIZE - len(new_population)))
        return new_population

    def tournament_winners(self, tournament_participants, expected_winners_number):
        winners = []
        while len(winners) < expected_winners_number:
            index_list = list(range(0, len(tournament_participants)))
            player1_index, player2_index = random.sample(index_list, 2)
            player1, player2 = tournament_participants[player1_index], tournament_participants[player2_index]
            if player1.fitness > player2.fitness:
                winners.append(player1)
                tournament_participants.pop(player1_index)
            else:
                winners.append(player2)
                tournament_participants.pop(player2_index)
        return winners

    def __str__(self):
        return f"Fitness - {self.fitness}. Individuals - {self.population}"