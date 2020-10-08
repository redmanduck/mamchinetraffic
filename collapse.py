from datetime import datetime, time

f = open("2016.csv", "r")
i = 0
tmp = []
output = []
for line in f.readlines():
    i += 1
    if i == 1:
        continue
    L = line.strip().split(",")
    timestamp = L[0]
    dt_object = datetime.fromtimestamp(int(timestamp))
    tmp.append(float(L[2]))
    if i % 12 == 0:
        output.append("%s,%s,%s" % (int(dt_object.timestamp()),  dt_object.isoformat(), sum(tmp)/len(tmp)))
        tmp = []


txtout = "timestamp,datetime,index\n" + "\n".join(output)
f.close()
f = open("2016_1H.csv", "w")
f.write(txtout)
f.close()