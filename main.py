import GAsignal

def main():
    FIND_STRING = list("Somethig new to get in this")
    # FIND_STRING = list("test")
    CHILDREN_IN_FAMILY = 60
    FAMILIES_IN_GENERATION    = 4
    MUTATION_RATE      = 0.05
    GA_test = GAsignal.GAsignal(FIND_STRING, CHILDREN_IN_FAMILY, FAMILIES_IN_GENERATION, MUTATION_RATE)
    while not GA_test.updateGeneration():
        pass
    print("\n---- END ----")
if __name__ == '__main__':
    main()
