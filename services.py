import numpy as np
import pandas as pd
from enum import Enum


class Mutate_Type(Enum):
    CASE_ONE = 1
    CASE_TWO = 2
    CASE_TREE = 3


class XoverType(Enum):
    LOCAL_INTERMEDIATE = 1
    GLOBAL_INTERMEDIATE = 2
    LOCAL_DISCRETE = 3
    GLOBAL_DISCRETE = 4


class SurvivorSelectionType(Enum):
    ONLY_CHILD = 1
    CHILD_AND_PARENT = 2


class Chromosome:

    def __init__(self, body, mutate_type=Mutate_Type.CASE_ONE):
        self.body: list = body
        self.mutate_type: Mutate_Type = mutate_type
        self.fitness = None
        self.sigma = 0.2
        self.sigma_list = [0.2] * len(self.body)
        self.alpha_list = []
        self.fitness_calculator()

    def mutate_case_one(self):
        tav = 1 / (len(self.body) ** 0.5)
        self.sigma = self.sigma * np.exp(tav * np.random.normal(0, 1))
        self.body = [x + (self.sigma * np.random.normal(0, 1)) for x in self.body]
        self.fitness_calculator()

    def mutate_case_two(self):
        tav = 1 / ((2 * len(self.body)) ** 0.5)
        tav_p = 1 / (((2 * len(self.body)) ** 0.5) ** 0.5)
        self.sigma_list = [sigma * np.exp(tav_p * np.random.normal(0, 1) + tav * np.random.normal(0, 1)) for sigma in
                           self.sigma_list]
        self.body = [x + (sigma * np.random.normal(0, 1)) for x, sigma in zip(self.body, self.sigma_list)]
        self.fitness_calculator()

    def fitness_calculator(self):
        n = len(self.body)
        body_list = [-1 * (xi * np.sin(np.sqrt(np.abs(xi)))) for xi in self.body]
        self.fitness = np.sum(body_list) + 418.9829 * n

    def mutation(self):
        if self.mutate_type is Mutate_Type.CASE_ONE:
            self.mutate_case_one()
        elif self.mutate_type is Mutate_Type.CASE_TWO:
            self.mutate_case_one()

    def update_sigma(self):
        self.sigma = self.sigma * 0.9
        self.sigma_list = [x * 0.9 for x in self.sigma_list]


def print_result(chromosome: Chromosome, populationNum, iteration_to_Answer):
    print('-------------------------')

    print('population number : ', populationNum)
    print('iteration number to get answer : ', iteration_to_Answer)
    print('answer_chromosome : ', chromosome.body)
    print('answer_fitness : ', chromosome.fitness)

    print('-------------------------')
