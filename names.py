names = set()

with open("names2.txt", mode="r") as f:
    for name in f.readlines():
        names.add(name.split('\n')[0])
