class status:
    def __init__(self):
        self.money = 200000 # текущие деньги
        self.debt = 300000 # текущий долг
        self.loyal = 4.0 # текущая лояльность
        self.users = 25000 # текущее кол-во пользователей
        self.number_sprint = 1 # номер спринта
        self.target = 1000000 # цель набрать миллион
        self.current_power = 0 # текущая трата энергии
        self.max_power = 20 # предел энергии
        self.count_blank_sprint = 0 # кол-во пустых спринтов подряд
        self.working_tasks = [] # эту штуку убрать!!!!!!!!
        self.available_tasks = [] # купленные истории
        self.selected_tasks = [] # истории которые уйдут на декомпозицию
        #self.available_subtasks = []
        #self.selected_subtasks = []
        #self.working_tasks = []
