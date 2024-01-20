import random
import pandas as pd

dic = {"page1":0.01,
       "page2":1,
       "page3":0.01}


keys = list(dic)
values = list(dic.values())


page1 = 0
page2 = 0
page3 = 0


for i in range(1000):
    x = random.choices(keys, values)

    if x[0] == "page1":
        page1 += 1

    elif x[0] == "page2":
        page2 += 1

    elif x[0] == "page3":
        page3 += 1


#print (f"page1 = {page1}, page2 = {page2}, page3 = {page3}")

x = {"html1": [], "html2": [3, 4], "html3": [5, 6], "html4": [7, 8]}

x["html1"].append(5)
x["html1"].append(6)
x["html1"].append(7)

x["html1"] = x["html1"][-1]

new = pd.DataFrame(dict())

new = new._append({
    "html1": 12,
    "html2": 13,
    "html3": 14,},
    ignore_index=True
)

new = new._append({
    "html1": 111},
    ignore_index=True
)

new = new._append({
    "html2": 1333},
    ignore_index=True
)

new = new._append({
    "html3": 1433},
    ignore_index=True
)


list = [1, 5, 9]

for i in list:
    print(i)








