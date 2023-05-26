from Model.model import Model
from Controllers.mainController import Controller
from Net.GameDoing import GameDoing

class Game:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        self.isWin = False
        self.isAlive = True
        self.prefState = self.get_hash_state()

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
            self.controller.decomposition_tasks(index)
        elif do == GameDoing.SELECT_TASK:
            self.controller.select_task(index) # ПЕРЕДЕЛАИТЬ НАЗВАНИЕ В КОНТРОЛЛЕРЕ
        elif do == GameDoing.BUY_ROBOT:
            self.controller.buy_robot()
        elif do == GameDoing.DIE:
            self.model.status.money = -1
        else:
            raise NameError("bad state")
        self.prefState = self.get_hash_state()

    def get_reward2(self):
        M = self.model.status.money
        L = self.model.status.loyal
        U = self.model.status.users
        S = self.model.status.number_sprint

        if self.model.status.money > 10**6:
            self.isWin = True
            return
        if M <= 0 or L <= 0 or U <= 0:
            self.isAlive = False
        Rbt = self.model.office.count_robot * 50000 * 0.8

        T = self.model.status.target
        simple = (Rbt + M + L * U)
        tar = ((T - M) / T) if T > M else (M / T)
        #pref = self.prefReward
        #self.prefReward = simple * tar
        #return self.prefReward - pref

    def state_changed(self):
        return self.get_hash_state() != self.prefState

    def get_reward(self):
        M = self.model.status.money
        L = self.model.status.loyal
        U = self.model.status.users
        CB = self.model.office.count_robot
        S = self.model.status.number_sprint

        if self.model.status.money > 10**6:
            self.isWin = True
            return (M + U*L)/S

        if M <= 0 or L <= 0 or U <= 0:
            self.isAlive = False

        if not self.isAlive:
            return S

        return (M + U*L)/S

    def get_state(self): # НАСТРОИТЬ ВХОДНЫЕ
        res = []
        st = self.model.status
        res.append(st.money / 1000000)
        res.append(st.loyal / 5)
        res.append(st.users / 100000)
        res.append(st.number_sprint / 150)
        res.append(st.target / 1000000)
        res.append(st.current_power / 160)
        res.append(st.max_power / 160)
        res.append(st.count_blank_sprint / 3)
        # добавить стоимость покупки робота

        tasks = self.model.status.list_tasks
        working_story = self.model.status.working_story
        backlog = self.model.status.backlog

        for i in range(backlog.get_len()):
            story = backlog.get(i)
            if story is not None:
                res.append(story.loyal / 0.4)
                res.append(story.users / 4000)
                res.append(story.weight / 152)
            else:
                self.add_in_arr(0, 3, res)

        for i in range(working_story.get_len()):
            story = working_story.get(i)
            if story is not None:
                res.append(story.loyal / 0.4)
                res.append(story.users / 4000)
                res.append(story.weight_complete / 152)
            else:
                self.add_in_arr(0, 3, res)

        for i in range(tasks.get_len()):
            task = tasks.get(i)
            if task is not None:
                res.append(task.weight / 20)
                res.append(working_story.get_index(task.id_story) / 6)
                res.append(task.isWorking)
            else:
                self.add_in_arr(0, 3, res)
        return res


    def add_in_arr(self, value, count, arr):
        for i in range(count):
            arr.append(value)

    def get_hash_state(self):
        s = self.model.status
        b = s.backlog.get_len()
        w = s.working_story.get_len()
        l = s.list_tasks.get_len()
        return hash((s.money, s.loyal, s.users, b, w, l, s.current_power, s.number_sprint))