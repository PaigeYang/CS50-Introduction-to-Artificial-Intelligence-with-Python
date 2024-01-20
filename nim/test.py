class math():

    def __init__(self):
        self.m = []

    def __str__(self):

        return f"m = {self.m}"

    def add(self, x):
        self.m.append(x)

    def ad2(self, y):
        self.add(y*10)

    @classmethod
    def ad3(cls, z):
        return z*100



EX = math()

C = EX.ad2(1)

math().ad3(20)

print (NEW)
print (C)
print (EX)





