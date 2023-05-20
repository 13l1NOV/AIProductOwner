
class Game:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        pass

    def execute(self, do, index):
        if do == GameDoing.RELEASE:
            self.controller # ДОБАВИТЬ
        elif do == GameDoing.SPRINT:
            self.controller.start_sprint()
        elif do == GameDoing.DO_RESEARCH:
            self.controller.create_two_easy_task()
        elif do == GameDoing.DO_SURVEY:
            self.controller.create_one_hard_task()
        elif do == GameDoing.DECOMPOSE:
            self.controller.decomposition_tasks(index) # ДОБАВИТЬ В КОНТРОЛЛЕР ВЫПОЛНЕНИЕ ТОЛЬКО ОДНОЙ ЗАДАЧИ НА ДЕКОМПОЗЩИЦИЮ
        elif do == GameDoing.SELECT_TASK:
            self.controller.move_subtask_to_selected_list(index) # ПЕРЕДЕЛАИТЬ НАЗВАНИЕ В КОНТРОЛЛЕРЕ
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
        res.append(st.count_room)
        res.append(st.count_blank_sprint)

        for i in range(6):
            if len(st.backlog) > i:
                res.append(st.backlog[i].get_target())
            else:
                res.append(Task(-1, 'S').get_target())
        for i in range(6):
            if len(st.selected_tasks) > i:
                res.append(st.selected_tasks[i].get_target())
            else:
                res.append(Task(-1, 'S').get_target())

        for i in range(24):
            if len(st.available_subtasks) > i:
                res.append(st.available_subtasks[i].get_target())
            else:
                res.append(SubTask(-1, -1, 20).get_target())

        for i in range(24):
            if len(st.selected_subtasks) > i:
                res.append(st.selected_subtasks[i].get_target())
            else:
                res.append(SubTask(-1, -1, 20).get_target())
        return res
