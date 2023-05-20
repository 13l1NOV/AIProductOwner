from Controllers.SmartArray import SmartArray
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
        self.backlog = SmartArray(6) # купленные истории
        self.working_story = SmartArray(6) # истории которые уйдут на декомпозицию
        self.list_tasks = SmartArray(32) # список задач
        self.cost_work_robots = self.max_power * 1000 # стоимость работы за всех роботов

