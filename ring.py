# Ring list

class Ring():
    def __init__(self,lst):
        self.loc = 0
        self.lst = lst
    def now(self):
        return self.lst[self.loc]

    def next(self):
        n = self.loc + 1 if self.loc < len(self.lst) else 0
        return self.lst[n]
    def goNext(self):
        self.loc = self.loc + 1 if self.loc < len(self.lst) else 0

    def pre(self):
        n = self.loc - 1 if self.loc > 0 else len(self.lst)-1
        return self.lst[n]
    def goBack(self):
        self.loc = self.loc - 1 if self.loc > 0 else len(self.lst)-1

    def getNowId(self):
        return self.loc

    def getPreId(self):
        return len(self.lst)-1 if self.loc == 0 else self.loc - 1

    def getNextId(self):
        return self.loc + 1 if self.loc < len(self.lst) else 0

if __name__ == '__main__':
    r = Ring([1,2,3])
    for i in range(10):
        print(r.getNowId(), r.now())
        r.goNext()
        