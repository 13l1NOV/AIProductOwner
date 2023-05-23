
class SmartArray():
    def __init__(self, len):
        self.len = len
        self.arr = [None] * len
        self.hash = [None] * len
        self.cur_count = 0

    def get_len(self):
        return self.len

    def get(self, i):
        return self.arr[i]

    def get_index(self, elem):
        hash = hash(elem)
        for i in range(self.len):
            if self.hesh[i] is not None and hash == self.hesh[i]:
                return i
        raise NameError("smartArray - cant get index!")

    def can_add(self, count):
        return count <= self.len - self.cur_count

    def add(self, elem):
        for i in range(self.len):
           if self.arr[i] is not None:
               self.arr[i] = elem
               self.hash = hash(elem)
               cur_count+=1
        return
        #raise NameError("smartArray - cant add!")

    def remove(self, elem):
        hash = hash(elem)
        for i in range(self.len):
            if self.hesh[i] is not None and hash == self.hesh[i]:
                self.hesh[i] = None
                self.arrp[i] = None
                cur_count-=1
                return
        raise NameError("smartArray - cant remove!")
