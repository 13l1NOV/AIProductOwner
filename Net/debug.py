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
    backlog = model.status.backlog
    print("Status Story:")
    for story in backlog.arr:
        if story != None:
            print("status task - id {}, type {}, users {}, loyal {}".format(story.id_story, story.type_story,
                                                                            story.users, story.loyal))
    print()


def status_subtask(model):
    list_tasks = model.status.list_tasks
    print("Status Tasks:")
    for task in list_tasks.arr:
        if task is not None:
            print(
                "status task - id task {}, id task {}, weight {}".format(task.id, task.id_story,
                                                                         task.weight))

    print()


def status_office(model):
    print("Status Office: power = {} count room = {}".format(model.status.max_power, model.office.count_robot))
    print()
