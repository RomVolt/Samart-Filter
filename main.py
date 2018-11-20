import GAsignal

def main():
    FIND_STRING = list("Somethig new to get in this")
    # FIND_STRING = list("test")
    CHILDREN_IN_FAMILY = 4
    FAMILIES_IN_GENERATION    = 150
    MUTATION_RATE      = 0.05
    GA_test = GAsignal.GAsignal(FIND_STRING, CHILDREN_IN_FAMILY, FAMILIES_IN_GENERATION, MUTATION_RATE)
    # current_generation    = GA_test.current_generation
    # population_evaluation = GA_test.generation_strength
    #
    # generation_num = 0
    # current_max_value = max(population_evaluation)
    # while not (GA_test.PERSON_SIZE in population_evaluation):
    #     new_generation , new_population_evaluation = GA_test.createNewGeneration(current_generation)
    #     new_max_value = max(new_population_evaluation)
    #     generation_num += 1
    #     if new_max_value >= current_max_value:
    #         current_generation    = new_generation
    #         population_evaluation = new_population_evaluation
    #         current_max_value     = new_max_value
    #         # GA_test.dispPopulation(current_generation, population_evaluation, generation_num)
    #         GA_test.dispCurrentPopulation(generation_num)
    while not GA_test.updateGeneration():
        pass
    print("\n---- END ----")
    # GA_test.dispPopulation(new_generation, howMatch, generation_num)

if __name__ == '__main__':
    main()
