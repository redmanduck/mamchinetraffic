Y = ["2016", "2017", "2018", "2019"]
L = None
for y in Y:
    f = open(y + "_1H.csv", "r")
    raw = f.readlines()
    lines = raw[1:]
    if L is None:
        L = [raw[0]]
    L = L + lines
    f.close()

print(len(L))
f = open("16171819_1H.csv", "w")
f.write("".join(L))
f.close()