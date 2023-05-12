from Model.status import status
from Model.Office.office import Office


class Model:

    def __init__(self):
        self.status = status()
        self.office = Office()

