import copy
import random

import agym.param


class Individual:
    mut_count = 0

    def __init__(self):
        self.gen = [
            random.randint(-agym.param.max_gen_value, agym.param.max_gen_value)
            for i in range(agym.param.len_exp)
        ]
        self.calc_fitness()

    def calc_fitness(self):
        func = agym.param.init_f
        self.fitness = abs(
            sum([self.gen[i] * func[i] for i in range(agym.param.len_exp)])
            + func[-1]
        )

    def crossover(self, other):
        child = copy.copy(self)

        left, right = sorted(
            [random.randint(0, agym.param.len_exp - 1) for i in range(2)]
        )
        child.gen = self.gen[0:left] + self.gen[right:] + other.gen[left:right]
        for i in range(agym.param.len_exp):
            child.gen[i] = random.randint(*sorted([child.gen[i], self.gen[i]]))

        if random.random() < agym.param.mut_chance:
            child.mutation()

        child.calc_fitness()
        return child

    def mutation(self):
        Individual.mut_count += 1
        self.gen[random.randint(0, agym.param.len_exp - 1)] = random.randint(
            -agym.param.max_gen_value, agym.param.max_gen_value
        )

    def __str__(self):
        return str(self.fitness) + str(self.gen)
