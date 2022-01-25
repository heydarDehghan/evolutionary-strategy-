from services import *
import random


class EA:
    zero_fitness_chromosome: Chromosome

    def __init__(self, numberPopulation=100, xover_type: XoverType = XoverType.LOCAL_INTERMEDIATE,
                 mutate_type: Mutate_Type = Mutate_Type.CASE_ONE, chromosome_len=2,
                 survivor_selection_type: SurvivorSelectionType = SurvivorSelectionType.ONLY_CHILD):
        self.numberPopulation = numberPopulation
        self.chromosome_len = chromosome_len
        self.mutate_type = mutate_type
        self.xover_type = xover_type
        self.survivor_selection_type = survivor_selection_type
        self.zero_fitness_chromosome = None
        self.population = []
        self.child_population = []
        self.generate_population()

    def update_fitness(self):
        for Crom in self.population:
            Crom.fitness_calculator()
            if -0.0009 < Crom.fitness < 0.0009:
                self.zero_fitness_chromosome = Crom
                break

    def update_sigma(self):
        for Crom in self.population:
            Crom.update_sigma()

    def generate_population(self):
        for x in range(self.numberPopulation):
            Crom = Chromosome(random.sample(range(-500, 500), self.chromosome_len), self.mutate_type)
            if Crom.fitness == 0:
                self.zero_fitness_chromosome = Crom
                break
            self.population.append(Crom)

    def local_intermediate(self):
        for x in range(self.numberPopulation * 7):
            parent_one, parent_two = random.sample(self.population, 2)
            child_body = [(x + y) / 2 for x, y in zip(parent_one.body, parent_two.body)]
            chromosome = Chromosome(child_body, self.mutate_type)

            if chromosome.fitness == 0:
                self.zero_fitness_chromosome = chromosome
                break

            self.child_population.append(chromosome)

    def global_intermediate(self):
        for counter in range(self.numberPopulation * 7):
            child_body = [None] * self.chromosome_len
            for i in range(self.chromosome_len):
                parent_one, parent_two = random.sample(self.population, 2)

                child_body[i] = (parent_one.body[i] + parent_two.body[i]) / 2

            chromosome = Chromosome(child_body, self.mutate_type)

            if chromosome.fitness == 0:
                self.zero_fitness_chromosome = chromosome
                break

            self.child_population.append(chromosome)

    def local_discrete(self):
        for x in range(self.numberPopulation * 7):
            parent_one, parent_two = random.sample(self.population, 2)
            child_body = [x if random.randint(0, 100) < 50 else y for x, y in zip(parent_one.body, parent_two.body)]
            chromosome = Chromosome(child_body, self.mutate_type)

            if chromosome.fitness == 0:
                self.zero_fitness_chromosome = chromosome
                break

            self.child_population.append(chromosome)

    def global_discrete(self):
        for counter in range(self.numberPopulation * 7):
            child_body = [None] * self.chromosome_len
            for i in range(self.chromosome_len):
                parent_one, parent_two = random.sample(self.population,2)
                child_body[i] = parent_one.body[i] if random.randint(0, 100) < 50 else parent_two.body[i]

            chromosome = Chromosome(child_body, self.mutate_type)

            if chromosome.fitness == 0:
                self.zero_fitness_chromosome = chromosome
                break

            self.child_population.append(chromosome)

    def survivor_selection_only_child(self):
        self.child_population.sort(key=lambda x: x.fitness)
        self.population = self.child_population[:self.numberPopulation]

    def survivor_selection_child_and_parent(self):
        self.child_population.extend(self.population)
        self.child_population.sort(key=lambda x: x.fitness)
        self.population = self.child_population[:self.numberPopulation]

    def xover(self):
        self.child_population = []
        if self.xover_type is XoverType.LOCAL_INTERMEDIATE:
            self.local_intermediate()
        elif self.xover_type is XoverType.GLOBAL_INTERMEDIATE:
            self.global_intermediate()
        elif self.xover_type is XoverType.LOCAL_DISCRETE:
            self.local_discrete()
        elif self.xover_type is XoverType.GLOBAL_DISCRETE:
            self.global_discrete()
        else:
            self.local_intermediate()

    def survivor_selection(self):
        if self.survivor_selection_type is SurvivorSelectionType.ONLY_CHILD:
            self.survivor_selection_only_child()
        elif self.survivor_selection_type is SurvivorSelectionType.CHILD_AND_PARENT:
            self.survivor_selection_child_and_parent()
        else:
            self.survivor_selection_only_child()

    def mutate(self):
        for Crom in self.population:
            Crom.mutation()
            if Crom.fitness == 0:
                self.zero_fitness_chromosome = Crom
                break
