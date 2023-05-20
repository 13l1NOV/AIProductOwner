from Controllers.mainController import Controller
from Model.model import Model
from Model.Tasks.story import Story
from Model.Tasks.task import Task

import numpy as np
from numpy.random import randint
from random import random as rnd
from random import gauss, randrange


class Actor:
    def __init__(self):
        self.is_win = False
        self.is_alive = True
        self.model = Model()
        self.Controller = Controller(self.model)
        self.countPref = 0
        self.actionPref = -1
        self.prefReward = 0
        self.prefReward = self.get_reward(0, 0)

    def get_reward(self, action, done):

        if action == self.actionPref:
            self.countPref += 1
            if self.countPref >= 8:
                self.is_alive = False
        else:
            self.countPref = 0
            self.actionPref = action

        M = self.model.status.money
        L = self.model.status.loyal
        U = self.model.status.users

        Rbt = self.model.office.check_status_robot() * 50000 * 0.9
        Room = len(self.model.office.list_rooms) * self.model.office.cost_room * 0.9
        T = self.model.status.target

        simple = (Rbt + Room + M + L * U)
        tar = ((T - M) / T) if T > M else (M / T)
        pref = self.prefReward
        self.prefReward = simple * tar
        return self.prefReward - pref

        cntTasks = 6
        cntAvlTasks = 6
        cntSubs = 24
        cntAvlSubs = 24
        M = self.model.status.money
        L = self.model.status.loyal
        U = self.model.status.users
        s = self.model.status.number_sprint
        sel_task = self.model.status.selected_tasks
        T = self.model.status.target

        if action == self.actionPref:
            self.countPref += 1
            if self.countPref >= 8:
                self.is_alive = False
        else:
            self.countPref = 0
            self.actionPref = action

        if not done:
            return -1

        # return action

        if action == 0 and done:  # buy robot
            return 100
        if action == 1 and done:  # buy room
            return 10
        if action == 2 and done:  # buy easy task
            return 400
        if action == 3 and done:  # buy hard task
            return 400
        if 4 <= action and action < 4 + cntTasks and done:  # move task to selected
            return 200
        if 4 + cntTasks <= action and action < 4 + cntTasks + cntSubs and done:  # move subtask to selected
            return 600
        if action == 4 + cntTasks + cntSubs and done:  # decomposition
            return len(sel_task) * 1000
        if action == 4 + cntTasks + cntSubs + 1 and done:  # sprint
            return 120
        return 0

    def step(self):
        self.is_win = self.model.status.money > 10 ** 6
        self.is_alive = self.model.status.money > 0

    def get_data(self):
        res = []
        st = self.model.status
        res.append(st.money)
        res.append(st.loyal)
        res.append(st.users)
        res.append(st.number_sprint)
        res.append(st.target)
        res.append(st.current_power)
        res.append(st.max_power)
        res.append(st.count_room)
        res.append(st.count_blank_sprint)

        for i in range(6):
            if len(st.backlog) > i:
                res.append(st.backlog[i].get_target())
            else:
                res.append(Story(-1, 'S').get_target())
        for i in range(6):
            if len(st.selected_tasks) > i:
                res.append(st.selected_tasks[i].get_target())
            else:
                res.append(Story(-1, 'S').get_target())

        for i in range(24):
            if len(st.available_subtasks) > i:
                res.append(st.available_subtasks[i].get_target())
            else:
                res.append(Task(-1, -1, 20).get_target())

        for i in range(24):
            if len(st.selected_subtasks) > i:
                res.append(st.selected_subtasks[i].get_target())
            else:
                res.append(Task(-1, -1, 20).get_target())
        return res


def individual(number_of_genes, upper_limit, lower_limit):  # индивид
    individual = [round(rnd() * (upper_limit - lower_limit)
                        + lower_limit, 1) for x in range(number_of_genes)]
    return individual


def population(number_of_individuals,
               number_of_genes, upper_limit, lower_limit):  # группа индивидов
    return [individual(number_of_genes, upper_limit, lower_limit)
            for x in range(number_of_individuals)]


def fitness_calculation(individual):  # оценка пригодности
    fitness_value = sum(individual)
    return fitness_value


def selection(generation, method='Fittest Half'):  # выборка лучших 3 вар.
    generation['Normalized Fitness'] = \
        sorted([generation['Fitness'][x] / sum(generation['Fitness'])
                for x in range(len(generation['Fitness']))], reverse=True)
    generation['Cumulative Sum'] = np.array(
        generation['Normalized Fitness']).cumsum()
    if method == 'Roulette Wheel':
        selected = []
        for x in range(len(generation['Individuals']) // 2):
            selected.append(roulette(generation
                                     ['Cumulative Sum'], rnd()))
            while len(set(selected)) != len(selected):
                selected[x] = \
                    (roulette(generation['Cumulative Sum'], rnd()))
        selected = {'Individuals':
                        [generation['Individuals'][int(selected[x])]
                         for x in range(len(generation['Individuals']) // 2)]
            , 'Fitness': [generation['Fitness'][int(selected[x])]
                          for x in range(
                    len(generation['Individuals']) // 2)]}
    elif method == 'Fittest Half':
        selected_individuals = [generation['Individuals'][-x - 1]
                                for x in range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitnesses}
    elif method == 'Random':
        selected_individuals = \
            [generation['Individuals']
             [randint(1, len(generation['Fitness']))]
             for x in range(int(len(generation['Individuals']) // 2))]
        selected_fitnesses = [generation['Fitness'][-x - 1]
                              for x in range(int(len(generation['Individuals']) // 2))]
        selected = {'Individuals': selected_individuals,
                    'Fitness': selected_fitnesses}
    return selected


def pairing(elit, selected, method='Fittest'):  # спаривание двух индивидов 3 вар.
    individuals = [elit['Individuals']] + selected['Individuals']
    fitness = [elit['Fitness']] + selected['Fitness']
    if method == 'Fittest':
        parents = [[individuals[x], individuals[x + 1]]
                   for x in range(len(individuals) // 2)]
    if method == 'Random':
        parents = []
        for x in range(len(individuals) // 2):
            parents.append(
                [individuals[randint(0, (len(individuals) - 1))],
                 individuals[randint(0, (len(individuals) - 1))]])
            while parents[x][0] == parents[x][1]:
                parents[x][1] = individuals[
                    randint(0, (len(individuals) - 1))]
    if method == 'Weighted Random':
        normalized_fitness = sorted(
            [fitness[x] / sum(fitness)
             for x in range(len(individuals) // 2)], reverse=True)
        cummulitive_sum = np.array(normalized_fitness).cumsum()
        parents = []
        for x in range(len(individuals) // 2):
            parents.append(
                [individuals[roulette(cummulitive_sum, rnd())],
                 individuals[roulette(cummulitive_sum, rnd())]])
            while parents[x][0] == parents[x][1]:
                parents[x][1] = individuals[
                    roulette(cummulitive_sum, rnd())]
    return parents


def mating(parents, method='Single Point'):  # метод перемешивания генов родителей в потомке 2 вар.
    if method == 'Single Point':
        pivot_point = randint(1, len(parents[0]))
        offsprings = [parents[0] \
                          [0:pivot_point] + parents[1][pivot_point:], parents[1]
                      [0:pivot_point] + parents[0][pivot_point:]]
    if method == 'Two Pionts':
        pivot_point_1 = randint(1, len(parents[0] - 1))
        pivot_point_2 = randint(1, len(parents[0]))
        while pivot_point_2 < pivot_point_1:
            pivot_point_2 = randint(1, len(parents[0]))
        offsprings = [parents[0][0:pivot_point_1] +
                      parents[1][pivot_point_1:pivot_point_2] +
                      [parents[0][pivot_point_2:]], [parents[1][0:pivot_point_1] +
                                                     parents[0][pivot_point_1:pivot_point_2] +
                                                     [parents[1][pivot_point_2:]]]]
    return offsprings


def mutation(individual, upper_limit, lower_limit, muatation_rate=2,
             method='Reset', standard_deviation=0.001):  # мутация 2 вар.
    gene = [randint(0, 7)]
    for x in range(muatation_rate - 1):
        gene.append(randint(0, 7))
        while len(set(gene)) < len(gene):
            gene[x] = randint(0, 7)
    mutated_individual = individual.copy()
    if method == 'Gauss':
        for x in range(muatation_rate):
            mutated_individual[x] = \
                round(individual[x] + gauss(0, standard_deviation), 1)
    if method == 'Reset':
        for x in range(muatation_rate):
            mutated_individual[x] = round(rnd() * \
                                          (upper_limit - lower_limit) + lower_limit, 1)
    return mutated_individual


def next_generation(gen, upper_limit, lower_limit):  # создание нового поколения
    elit = {}
    next_gen = {}
    elit['Individuals'] = gen['Individuals'].pop(-1)
    elit['Fitness'] = gen['Fitness'].pop(-1)
    selected = selection(gen)
    parents = pairing(elit, selected)
    offsprings = [[[mating(parents[x])
                    for x in range(len(parents))]
                   [y][z] for z in range(2)]
                  for y in range(len(parents))]
    offsprings1 = [offsprings[x][0]
                   for x in range(len(parents))]
    offsprings2 = [offsprings[x][1]
                   for x in range(len(parents))]
    unmutated = selected['Individuals'] + offsprings1 + offsprings2
    mutated = [mutation(unmutated[x], upper_limit, lower_limit)
               for x in range(len(gen['Individuals']))]
    unsorted_individuals = mutated + [elit['Individuals']]
    unsorted_next_gen = \
        [fitness_calculation(mutated[x])
         for x in range(len(mutated))]
    unsorted_fitness = [unsorted_next_gen[x]
                        for x in range(len(gen['Fitness']))] + [elit['Fitness']]
    sorted_next_gen = \
        sorted([[unsorted_individuals[x], unsorted_fitness[x]]
                for x in range(len(unsorted_individuals))],
               key=lambda x: x[1])
    next_gen['Individuals'] = [sorted_next_gen[x][0]
                               for x in range(len(sorted_next_gen))]
    next_gen['Fitness'] = [sorted_next_gen[x][1]
                           for x in range(len(sorted_next_gen))]
    gen['Individuals'].append(elit['Individuals'])
    gen['Fitness'].append(elit['Fitness'])
    return next_gen


def fitness_similarity_check(max_fitness, number_of_similarity):  # критерий прекращения
    result = False
    similarity = 0
    for n in range(len(max_fitness) - 1):
        if max_fitness[n] == max_fitness[n + 1]:
            similarity += 1
        else:
            similarity = 0
    if similarity == number_of_similarity - 1:
        result = True
    return result
