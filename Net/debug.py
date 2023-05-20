def status_bar(model):
    money = model.status.money
    debt = model.status.debt
    loyal = model.status.loyal
    users = model.status.users
    print("number sprint: {}".format(model.status.number_sprint))
    print("status_bar:")
    print("money {} and debt {}".format(money, debt))
    print("users {} and loyal {}".format(users, loyal))
    print()


def status_task(model):
    available_tasks = model.status.backlog
    selected_tasks = model.status.selected_tasks
    print("Status Tasks: count available tasks = {}".format(len(model.status.backlog)))
    for task in available_tasks:
        print("status task - id {}, type {}, users {}, loyal {}".format(task.id_story, task.type_story,
                                                                        task.users, task.loyal))

    print("Status Tasks: count selected tasks = {}".format(len(model.status.selected_tasks)))
    for task in selected_tasks:
        print("status task - id {}, type {}, users {}, loyal {}".format(task.id_story, task.type_story,
                                                                        task.users, task.loyal))

    print()


def status_subtask(model):
    available_subtasks = model.status.available_subtasks
    selected_subtasks = model.status.selected_subtasks
    print("Status Tasks: count available subtasks = {}".format(len(model.status.available_subtasks)))
    for subtask in available_subtasks:
        print(
            "status subtask - id subtask {}, id task {}, weight {}".format(subtask.id, subtask.id_story,
                                                                           subtask.weight))

    print("Status Tasks: count selected subtasks = {}".format(len(model.status.selected_subtasks)))
    for subtask in selected_subtasks:
        print(
            "status subtask - id subtask {}, id task {}, weight {}".format(subtask.id, subtask.id_story,
                                                                           subtask.weight))

    print()


def status_office(model):
    cost_room = model.office.cost_room
    count_rooms = len(model.office.list_rooms)
    print("Status Office: power = {} count room = {}".format(model.status.max_power, len(model.office.list_rooms)))
    for room in model.office.list_rooms:
        print("status room №{} count robots {} - full? {}".format(room.id, room.count_robots, room.status_full))
    print()


