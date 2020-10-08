from datetime import datetime, time
import json
import csv
import reverse_geocoder as rg
i = 0

def isHoliday(dt):
    H = ["01-01-2018", 
        "02-01-2018", 
        "12-04-2018",
        "13-04-2018",
        "14-04-2018",
        "15-04-2018",
        "16-04-2018",
        "27-06-2018",
        "28-06-2018",
        "12-08-2018",
        "13-08-2018",
        "06-04-2019",
        "08-04-2019",
        "13-04-2019",
        "16-04-2019",
        "06-05-2019",
        "09-05-2019",
        "18-05-2019",
        "20-05-2019",
        "03-06-2019",
        "04-06-2019",
        "16-07-2019",
        "17-07-2019",
        "28-07-2019",
        "29-07-2019",
        "12-08-2019",
        "13-10-2019",
        "14-10-2019",
        "30-12-2019",
        "31-12-2019"]
    if(dt.strftime("%d-%m-%Y") in H):
        return True
    return False

PRECIPS = []
for pfile in ['precip2018', 'precip2019']:
    fprecip = open(pfile + ".json", "r")
    jx = json.loads("".join(fprecip.readlines()))
    for p in jx:
        PRECIP = p
        PRECIP['year'] = int(PRECIP['year'])
        PRECIP['mo'] = int(PRECIP['mo'])
        PRECIP['da'] = int(PRECIP['da'])
        PRECIPS.append(PRECIP)

    fprecip.close()

ACCI = {}
for pfile in ['acci2018', 'acci2019']:
    facci = open(pfile + ".csv", "r",encoding='utf-8')
    reader = csv.DictReader(facci, delimiter=',', quotechar='"')
    
    for line in reader:
        lat = line["latitude"]
        lng = line["longitude"]

        coordinates = (lat, lng)
        
        city = rg.search(coordinates,mode=1)
        if not city[0]['admin1'] == 'Bangkok':
            pass

        type = line["type"]
        begin = datetime.strptime(line["start"], "%Y-%m-%d %H:%M:%S")
        ends = datetime.strptime(line["stop"], "%Y-%m-%d %H:%M:%S")
        if type == "3":
            #print(type, begin, ends)
            if begin.strftime("%d-%m-%Y %H") not in ACCI:
                ACCI[begin.strftime("%d-%m-%Y %H")] = 0
            ACCI[begin.strftime("%d-%m-%Y %H")] += 1
            Hforward = int(begin.strftime("%H")) + 1
            if Hforward < int(ends.strftime("%H")):
                if ends.strftime("%d-%m-%Y %H") not in ACCI:
                    ACCI[ends.strftime("%d-%m-%Y %H")] = 0
                ACCI[ends.strftime("%d-%m-%Y %H")] += 1

def getNOAA(day,month,year):
    match = filter(lambda x: x['mo'] == int(month) and x['year'] == int(year) and x['da'] == int(day), PRECIPS)
    try:
        return list(match)[0]
    except IndexError:
        return  {
            "year": year,
            "mo": month,
            "da": day,
            "temp": 0,
            "min": "0",
            "max": "99.9",
            "prcp": "0.0",
            "stn": "484560",
            "name": "BANGKOK INTL"
        }

output = [
    ['traffic', "precip", "temp","first_week","last_wk", "acci", "public_hol", "rush_hr", "mon", "tue", "wed", "thu", "fri", "Sat", "sun", "jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sep", "oct","nov","dec"]
]

f = open("2018-19-1H.csv")
lines = f.readlines()
for line in lines:
    i += 1
    if i == 1:
        continue
    data = line.strip().split(',')
    timestamp = data[0]
    dt_object = datetime.fromtimestamp(int(timestamp))
    TRAF = float(data[2])
    MON = int(dt_object.weekday() == 0)
    TUES = int(dt_object.weekday() == 1)
    WED = int(dt_object.weekday() == 2)
    THU = int(dt_object.weekday() == 3)
    FRI = int(dt_object.weekday() == 4)
    SAT = int(dt_object.weekday() == 5)
    SUN = int(dt_object.weekday() == 6)
    JAN = int(dt_object.month == 1)
    FEB = int(dt_object.month == 2)
    MAR = int(dt_object.month == 3)
    APR = int(dt_object.month == 4)
    MAY = int(dt_object.month == 5)
    JUNE = int(dt_object.month == 6)
    JULY = int(dt_object.month == 7)
    AUG = int(dt_object.month == 8)
    SEP = int(dt_object.month == 9)
    OCT = int(dt_object.month == 10)
    NOV = int(dt_object.month == 11)
    DEC = int(dt_object.month == 12)
    RUSH = int((dt_object.hour > 7 and dt_object.hour < 10) or (dt_object.hour > 17 and dt_object.hour < 21))
    dateom = int(dt_object.strftime("%d"))
    FIRST_WEEK = int(dateom <= 7)
    LAST_WEEK = int(dateom >= 21)
    PUBLIC_HOL = int(isHoliday(dt_object))
    ACCI_CT = 0
    try:
        ACCI_CT  = int(ACCI[dt_object.strftime("%d-%m-%Y %H")])
    except Exception:
        pass
    
    noaa = getNOAA(dt_object.strftime("%d"), dt_object.strftime("%m"), dt_object.strftime("%Y"))
    output.append([TRAF, 
                    float(noaa['prcp'])*2.54, 
                    (float(noaa['temp']) - 32)*5/9, 
                    FIRST_WEEK,
                    LAST_WEEK, 
                    ACCI_CT,
                    PUBLIC_HOL,
                    RUSH,
                    MON,
                    TUES,
                    WED,
                    THU,
                    FRI,
                    SAT,
                    SUN,
                    JAN,
                    FEB,
                    MAR,
                    APR,
                    MAY,
                    JUNE,
                    JULY,
                    AUG,
                    SEP,
                    OCT,
                    NOV,
                    DEC,])

print(len(output))
fout = open("xfeatures_1h_1819_LATEST.csv", "w")
for oline in output:
    for o in range(len(oline)):
        oline[o] = str(oline[o])
        
    fout.write(",".join(oline) + "\n")
fout.close()
    