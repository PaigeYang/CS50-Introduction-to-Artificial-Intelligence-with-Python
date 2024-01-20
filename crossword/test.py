import sys
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.age == other.age
    def __hash__(self):
        return hash((self.first_name))

    def add(self, x):
        self.age = self.age + x

    def mix(self, x):
        self.add(x)


def main():

    pep = Person("Paige", "Yang", 20)

    print(pep.first_name)

    # Save vocabulary list
    with open("data/words0.txt") as f:
        words = set(f.read().upper().splitlines())

    #print(words)

    dic = { var: {'FOUR', 'Five'} for var in range(3)}

    dic['4'] = {'FOUR', 'Six'}

    #students = [('john', 'A', 15, 10), ('jane', 'B', 12, 11), ('dave', 'B', 15, 12)]

    #print(sorted(students, key=lambda student : (student[2], student[3]), reverse=True))

    unassigned = [(("paige", 2, 3, 4), 5), (("Ken", 2, 3, 4), 8), (("Andy", 2, 3, 4), 6), (("CCy", 2, 3, 4), 9)]

    unassigned = sorted(unassigned, key=lambda value : value[1])

    print (unassigned)







if __name__=="__main__":
    main()