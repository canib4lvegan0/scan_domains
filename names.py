import os

names = set()

with open("names.txt", mode="r") as f:
    readded = f.readlines()
    for name in readded:
        names.add(name.split('\n')[0])
    print("There are {} names into file".format(len(names)))

def clean_names(new, old):
    global names
    added = old.difference(new)
    names = added
    added = '\n'.join(added)

    with open("names_new.txt", mode="w+") as file:
        file.writelines(added)

    print("There are {} names into new file".format(len(names)))
    os.remove("names.txt")
    os.rename("names_new.txt", "names.txt")


