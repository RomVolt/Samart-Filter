import string
import random
import multiprocessing



class GAsignal(object):
    """docstring for GAtext."""
    current_generation = []
    def __init__(self, str_toFind, children_in_family, families_in_population, mutarion_rate):
        self.CLEAR_SPACE = "          "
        self.TARGET             = str_toFind
        self.PERSON_SIZE        = len(str_toFind)
        self.GENOM_CHOISE_SIZE  = len(string.printable)
        self.CHILDREN_IN_FAMILY = children_in_family
        self.FAMILIES_IN_GENERATION = families_in_population
        self.POPULATION_SIZE    = children_in_family * families_in_population
        self.MUTATION_RATE      = mutarion_rate
        self.createNewPopulation()
        self.generation_num     = 0


    """
    @name   - createNewPopulation
    @desc   - Initiate new population
    @Input  - population size
    @Output - new population
    """
    def createNewPopulation(self):
        more_then_2 = False
        while not more_then_2:
            self.current_generation = [random.choices(string.printable, k = self.PERSON_SIZE) for i in range(self.POPULATION_SIZE)]
            how_Match   = self.calcMatchCurrentGenration()
            more_then_2 = self.isMoreThenTwo(how_Match)
        self.generation_strength = how_Match


    """
    @name   - calcMatch
    @desc   - evaluating given population with goal
    @Input  - goal to reach, current population for evaluation
    @Output - population evaluation vector
    """

    def calcMatch(self, current_Persson):
        return sum([1 for a,b in zip(self.TARGET, current_Persson) if a==b])

    def calcMatchCurrentGenration(self):
        return list([sum([1 for a,b in zip(self.TARGET, cp) if a==b]) for cp in self.current_generation])

    def isMoreThenTwo(self, evaluation_vec):
        return sum([1 for x in evaluation_vec if x > 0.0]) >= 2
    """
    @name   - createNewGeneration
    @desc   - generate new generation based on current population and its strength
    @Input  - current_population:    vector of people
            - generation_strength: vector avaluatig how much each person close to ideal goal
    @Output - new_generation:        vector with new children for new generation
    """
    def createNewChild(self, children_num, new_parents, q_new_generation):
        # for family in range(self.FAMILIES_IN_GENERATION):
            # for child in range(self.CHILDREN_IN_FAMILY):
        for child in children_num:
            p_mutation = random.random()
            if p_mutation >= 0.5:
                new_child = self.current_generation[new_parents[0]][0:round(self.PERSON_SIZE/2)] +\
                            self.current_generation[new_parents[1]][round(self.PERSON_SIZE/2):]
            else:
                new_child = self.current_generation[new_parents[1]][0:round(self.PERSON_SIZE/2)] +\
                            self.current_generation[new_parents[0]][round(self.PERSON_SIZE/2):]
            if p_mutation <= self.MUTATION_RATE:
                genom = random.choice(string.printable)
                mutaion_index = random.randint(0, self.PERSON_SIZE-1)
                new_child_M = self.insertMutation(new_child, genom, mutaion_index)
                child_strength = self.calcMatch(new_child_M)
                q_new_generation.put([new_child_M, child_strength])
            else:
                child_strength = self.calcMatch(new_child)
                q_new_generation.put([new_child, child_strength])

    def createNewGeneration(self):
        #change evaluation vector to probability value
        eval_sum = sum(self.generation_strength)
        if eval_sum == 0.0 or not self.isMoreThenTwo(self.generation_strength):
            print("\n Restart evaluation ------ \n")
            self.createNewPopulation()
            eval_sum = sum(self.generation_strength)
        prob_parent = [pop_val/eval_sum for pop_val in self.generation_strength]

        previous_value = 0.0
        for i in range(self.POPULATION_SIZE):
            if not prob_parent[i] == 0.0:
                prob_parent[i] += previous_value
                previous_value  = prob_parent[i]

        q_new_generation = multiprocessing.Queue()
        process_list = []
        for family in range(self.FAMILIES_IN_GENERATION):
            new_parents = self.get2parents(prob_parent)
            p = multiprocessing.Process(target=GAsignal.createNewChild, args=(self,range(self.CHILDREN_IN_FAMILY),new_parents,q_new_generation,))
            p.start()
            process_list.append(p)

        for i in range(self.FAMILIES_IN_GENERATION):
            process_list[i].join()

        new_generation = []
        new_generation_strength = []
        while not q_new_generation.empty():
            Person = q_new_generation.get()
            new_generation.append(Person[0])
            new_generation_strength.append(Person[1])
        return new_generation , new_generation_strength


    """
    @name   - get2parents
    @desc   - find new parents using their Strength
    @Input  - current population
              Probability parent vector - vector must be sum of probabilities from current parent to all previous
                                          when cells with the same probability mean the parent has 0 chance to be chosen
                                          vector end alway with p=1
    @Output - unique parents indexes
    """

    def get2parents(self, prob_parent):
        new_parents = []
        max_parents = 2
        previous_value = -1
        i = 0
        while i < max_parents:
            p_parent = random.random()
            for index_parent in range(self.POPULATION_SIZE):
                if (prob_parent[index_parent] >= p_parent):
                    if index_parent == previous_value: break
                    new_parents.append(index_parent)
                    i += 1
                    break
            previous_value = index_parent
        return new_parents


    """
    @name   - insertMutation
    @desc   - inserts mutated genom into child
    @Input  - child
              Mutation vector - genom mutation vector
              mutation_index  - index into which the mutation be inserted
    @Output - new_child
    """
    def insertMutation(self, child, mutation_vec, mutation_index):
        mutation_vec_size = len(mutation_vec)
        # for string just insert random character
        end_index = mutation_index + mutation_vec_size
        if end_index >= self.PERSON_SIZE:
            mutation_index = self.PERSON_SIZE - mutation_vec_size
            new_child = child[:mutation_index] + list(mutation_vec)
        else:
            new_child = child[:mutation_index] + list(mutation_vec) + child[end_index:]
        return new_child

    def updateGeneration(self):
        if self.PERSON_SIZE in self.generation_strength:
            self.dispCurrentPopulation(self.generation_num)
            return True
        new_generation , new_population_evaluation = self.createNewGeneration()
        self.generation_num += 1
        if max(new_population_evaluation) >= max(self.generation_strength):
            self.current_generation  = new_generation
            self.generation_strength = new_population_evaluation
            self.dispCurrentPopulation(self.generation_num)
        return False

    """
    @name   - dispPopulation
    @desc   - displays given pupulatin
    @Input  - current_population
              current_generation_strength
              generation_num - number to display for analisis
    @Output -
    """

    def dispCurrentPopulation(self, generation_num):
        max_strength = max(self.generation_strength)
        index_person = self.generation_strength.index(max_strength)
        print("{0} ---\tGeneration {1}{2}\r".format(repr(self.current_generation[index_person]), generation_num, self.CLEAR_SPACE),end="")
