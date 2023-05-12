from Controllers.mainController import Controller
from Model.model import Model
from Model.Tasks.task import Task
from Model.Tasks.subtask import SubTask


class Actor:
    def __init__(self):
        self.is_win = False
        self.is_alive = True
        self.model = Model()
        self.Controller = Controller(self.model)
        self.countPref = 0
        self.actionPref = -1
        self.prefReward = 0
        self.prefReward = self.get_reward(0,0)

    def get_reward(self, action,done):

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
        Room = len(self.model.office.list_rooms) *  self.model.office.cost_room * 0.9
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

        #return action

        if action == 0 and done: # buy robot
            return 100
        if action == 1 and done: # buy room
            return 10
        if action == 2 and done: # buy easy task
            return 400
        if action == 3 and done: # buy hard task
            return 400
        if 4 <= action and action < 4 + cntTasks and done: # move task to selected
            return 200
        if 4 + cntTasks <= action and action < 4 + cntTasks + cntSubs and done: # move subtask to selected
            return 600
        if action == 4 + cntTasks + cntSubs and done: # decomposition
            return len(sel_task)*1000
        if action == 4 + cntTasks + cntSubs + 1 and done: # sprint
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
            if len(st.available_tasks) > i:
                res.append(st.available_tasks[i].get_target())
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
