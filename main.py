from services import Mutate_Type, print_result, XoverType, SurvivorSelectionType
from EvolutionaryAlgorithm import EA

if __name__ == "__main__":
    populationNum = 200
    iteration = 100
    mutate_type = Mutate_Type.CASE_TWO
    xover_type = XoverType.LOCAL_INTERMEDIATE
    chromosome_len = 2
    survivor_selection_type = SurvivorSelectionType.ONLY_CHILD


    ea_model = EA(populationNum,
                  mutate_type=mutate_type,
                  xover_type=xover_type,
                  chromosome_len=chromosome_len,
                  survivor_selection_type =survivor_selection_type)
    for x in range(iteration):
        if ea_model.zero_fitness_chromosome is not None:
            print_result(ea_model.zero_fitness_chromosome, populationNum, x)
            break
        else:
            ea_model.update_fitness()

            ea_model.xover()
            ea_model.mutate()
            ea_model.survivor_selection()
            # ea_model.update_sigma()

        print(f'end of iteration {x}')
        ea_model.population.sort(key=lambda x: x.fitness)
        print(len(ea_model.population))
        print(f'best fitness in iteration {x} ===> {ea_model.population[0].fitness} ')
    # ea_model.update_fitness()
    ea_model.population.sort(key=lambda x: x.fitness)
    if ea_model.zero_fitness_chromosome is None:
        print_result(ea_model.population[0], populationNum, iteration)
