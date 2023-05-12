from Net.actor import Actor
# from Net.debug import Debug
from Net.debug import status_bar, status_office, status_task, status_subtask
import neat

generation = 0

def format(a):
   return [print(str(i) if len(str(i))>1 else "0"+str(i), end=' ') for i in a]
def debug(actors, genomes, history):
    best = 0
    bestActor = actors[0]
    id_actor = 0
    for i, actor in enumerate(actors):
        if genomes[i][1].fitness > best:
            best = genomes[i][1].fitness
            bestActor = actor
    for i in history:
        format(i)
        print()

    print("==========================================================")
    print(best)

    print("==========================================================")
    status_bar(bestActor.model)
    status_office(bestActor.model)
    status_task(bestActor.model)
    status_subtask(bestActor.model)


cntTasks = 6
cntAvlTasks = 6
cntSubs = 24
cntAvlSubs = 24


def selectDo(actors, nets):
    global cntTasks
    global cntAvlTasks
    global cntSubs
    global cntAvlSubs

    deb = []
    for i, actor in enumerate(actors):
        output = nets[i].activate(actor.get_data())
        i = output.index(max(output)) # никогда нет 0 поэтому сделали костыль
        done = False
        if i == 0:
            done = actor.Controller.buy_robot()
        elif i == 1:
            done = actor.Controller.buy_room()
        elif i == 2:
            done = actor.Controller.create_two_easy_task()
        elif i == 3:
            done = actor.Controller.create_one_hard_task()
        elif 4 <= i and i < 4 + cntTasks:
            done = actor.Controller.move_task_to_selected_list(i - 4)
        #elif 4 + cntTasks <= i and i < 4 + cntTasks + cntAvlTasks:
        #    done = actor.Controller.move_task_to_available_list(i - 4 - cntTasks)
        elif 4 + cntTasks <= i and i < 4 + cntTasks + cntSubs:
            done = actor.Controller.move_subtask_to_selected_list(i - 4 - cntTasks - cntAvlTasks)
        #elif 4 + cntTasks + cntAvlTasks + cntSubs <= i and i < 4 + cntTasks + cntAvlTasks + cntSubs + cntAvlSubs:
        #    done = actor.Controller.move_subtask_to_available_list(i - 4 - cntTasks - cntAvlTasks - cntSubs)
        elif i == 4 + cntTasks + cntSubs:
            done = actor.Controller.decomposition_tasks()
        elif i == 4 + cntTasks + cntSubs + 1:
            done = actor.Controller.start_sprint()

        deb.append(i if actor.is_alive else -1)
    return deb, i, done


def run_generation(genomes, config):
    nets = []
    actors = []
    global generation
    generation += 1

    # init genomes
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0  # every genome is not successful at the start

        # init actor
        actors.append(Actor())

    for i, actor in enumerate(actors):
        genomes[i][1].fitness = 200

    iteration = 0
    history = []
    print("generation " + str(generation))
    countIteration = 5 + generation
    brk = False
    while iteration <= countIteration and not brk:
        iteration += 1
        # clock = pygame.time.Clock()
        h, action, done = selectDo(actors, nets)
        history.append(h)

        #for i, actor in enumerate(actors):
        #    actor.step()

        actors_left = 0
        for i, actor in enumerate(actors):
            actor.step()
            if actor.is_win:
                print("win actor!!!!")
                break

            if actor.is_alive:
                # print(actor.model.status.money)
                actors_left += 1
                genomes[i][1].fitness += actor.get_reward(action, done)
            else:
                genomes[i][1].fitness = 0
        if not actors_left:
            brk = True
        if iteration % countIteration == 0:
            print(actors_left)
            debug(actors,genomes, history)
            print(generation)
            if generation % 200 == 0:
                input()
            history = []