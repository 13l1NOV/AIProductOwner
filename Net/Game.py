from Model.model import Model
from Controllers.mainController import Controller

class Game:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        pass

    def execute(self, do, index):
        if do == GameDoing.RELEASE:
            self.controller.start_release()
        elif do == GameDoing.SPRINT:
            self.controller.start_sprint()
        elif do == GameDoing.DO_RESEARCH:
            self.controller.create_two_easy_task()
        elif do == GameDoing.DO_SURVEY:
            self.controller.create_one_hard_task()
        elif do == GameDoing.DECOMPOSE:
            self.controller.decomposition_tasks(index) # ДОБАВИТЬ В КОНТРОЛЛЕР ВЫПОЛНЕНИЕ ТОЛЬКО ОДНОЙ ЗАДАЧИ НА ДЕКОМПОЗЩИЦИЮ
        elif do == GameDoing.SELECT_TASK:
            self.controller.select_task(index) # ПЕРЕДЕЛАИТЬ НАЗВАНИЕ В КОНТРОЛЛЕРЕ
        elif do == GameDoing.BUY_ROBOT:
            self.controller.buy_robot()
        else:
            raise NameError("bad state")



    def get_state(self): # НАСТРОИТЬ ВХОДНЫЕ
        res = []
        st = self.model.status
        res.append(st.money)
        res.append(st.loyal)
        res.append(st.users)
        res.append(st.number_sprint)
        res.append(st.target)
        res.append(st.current_power)
        res.append(st.max_power)
        #res.append(st.count_room)
        res.append(st.count_blank_sprint)

        tasks = self.model.status.list_tasks
        working_story = self.model.status.working_story
        backlog = self.model.status.backlog

        for i in range(backlog.get_len()):
            story = backlog.get(i)
            if story is not None:
                res.append(story.loyal)
                res.append(story.users)
                res.append(story.weight)
            else:
                self.add_in_arr(0, 3, res)

        for i in range(working_story.get_len()):
            story = working_story.get(i)
            if story is not None:
                res.append(story.loyal)
                res.append(story.users)
                res.append(story.weight_complete)
            else:
                self.add_in_arr(0, 3, res)

        for i in range(tasks.get_len()):
            task = tasks.get(i)
            if task is not None:
                res.append(task.weight)
                res.append(working_story.get_index(task.id_story))
                res.append(task.isWorking)
            else:
                self.add_in_arr(0, 3, res)
        return res


    def add_in_arr(self, value, count, arr):
        for i in range(count):
            arr.append(value)
