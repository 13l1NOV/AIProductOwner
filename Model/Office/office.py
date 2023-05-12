from Model.Rooms.rooms import Room


class Office:
    def __init__(self):
        self.limit_rooms = 8
        self.list_rooms = [Room(0)]
        self.list_rooms[0].add_robot()
        self.status_full = False
        self.cost_room = 200000

    def add_room(self):
        if not self.status_full:
            self.list_rooms.append(Room(len(self.list_rooms)))
            self.cost_room *= 1.5
            self.cost_room = int(self.cost_room)
            if len(self.list_rooms) >= self.limit_rooms:
                self.status_full = True

    def check_status_robot(self):
        result = 0
        for room in self.list_rooms:
            result += room.count_robots
        return result
