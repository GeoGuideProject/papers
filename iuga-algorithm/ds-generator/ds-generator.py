import csv, math
latpick, longpick           = [6, 5]
latdrop, longdrop           = [10, 9]
Distance, Hour, Passenger   = [4, 1, 3]
biggerdistance, biggersimilarity, firstline, countlines =   [0, 0, True, 0]
def getHour(strdate):
    try:
        strdate = strdate.split()
        return int(strdate[1].split(':')[0])
    except(IndexError):
        return 0

def harvestine_distance(lat1, lng1, lat2, lng2):
    try:
    	dept_lat_rad = math.radians(lat1)
    	dept_lng_rad = math.radians(lng1)
    	arr_lat_rad = math.radians(lat2)
    	arr_lng_rad = math.radians(lng2)
    	earth_radius = 3963.1
    	d = math.acos(math.cos(dept_lat_rad)*math.cos(dept_lng_rad)*math.cos(arr_lat_rad)*math.cos(arr_lng_rad) + math.cos(dept_lat_rad)*math.sin(dept_lng_rad)*math.cos(arr_lat_rad)*math.sin(arr_lng_rad) + math.sin(dept_lat_rad)*math.sin(arr_lat_rad)) * earth_radius
    	return round(d,2)
    except:
        return 0
def setBiggerValue(disval, simval):
    global biggerdistance
    global biggersimilarity
    if(biggerdistance < disval):
        biggerdistance = disval
    if(biggersimilarity < simval):
        biggersimilarity = simval
countlines = -1
#North Limit: 40.915031, -73.910336
#East Limit: 40.739040, -73.700208
#South Limit:  40.495730, -74.248575
#West Limit: 40.508258, -74.255698
def ignorePoint(p1,p2,p3,p4):
    try:
        if((p1 > -73.699) and (p1 < 40.494)) or ((p2 > -73.699) and (p2 < 40.494)) or ((p3 > -73.699) and (p3 < 40.494)) or ((p4 > -73.699) and (p4 < 40.494)):
            return True
        else:
            return False
    except:
        return True


temp = csv.writer(open("temp.csv", "wb"))
index = csv.writer(open("index.csv", "wb"))
print("Writing temp.csv with real distance and similarity values\n\nPoints ignored:")
with open('arquivo.csv') as f1:
    for row in csv.reader(iter(f1.readline, '')):
        countlines += 1
        if(firstline == False): # Ignore header line
            index.writerow([(countlines*2) - 1, row[latpick], row[longpick]])
            index.writerow([(countlines*2), row[latdrop], row[longdrop]])
            loopfirstline = True
            loopcountlines = -1
            firstloop = True
            ignoreIndex = 0
            if(ignorePoint(float(row[latpick]), float(row[longpick]), float(row[latdrop]), float(row[longdrop]))):
                ignoreIndex += 2
                print(float(row[latpick]), float(row[longpick]), float(row[latdrop]), float(row[longdrop]))
            else:
                with open('arquivo.csv') as f2:
                    for looprow in csv.reader(iter(f2.readline, '')):
                        loopcountlines += 1
                        ignoreIndexloop = 0
                        if(loopfirstline == False):
                            if(countlines < loopcountlines):
                                if(ignorePoint(float(looprow[latpick]), float(looprow[longpick]), float(looprow[latdrop]), float(looprow[longdrop]))):
                                    ignoreIndexloop += 2
                                else:
                                    columnsid = [(countlines*2) - 1 - ignoreIndex, (countlines*2)  - ignoreIndex, (loopcountlines*2) - 1 - ignoreIndexloop, (loopcountlines*2) - ignoreIndexloop]
                                    # Column 1 actual X Column 2 actual
                                    # partsimilarity to iguals rows
                                    if(firstloop == True):
                                        partsimilarity =  (   (int(row[Passenger]) * 2) + 1  )
                                        distance = harvestine_distance(float(row[latpick]), float(row[longpick]), float(row[latdrop]), float(row[longdrop]))
                                        similarity = distance * partsimilarity
                                        temp.writerow([columnsid[0], columnsid[1], distance, similarity])
                                        setBiggerValue(distance, similarity)
                                        # partsimilarity to diferent rows
                                        firstloop = False
                                    try:
                                        partsimilarity =  (  (int(row[Passenger]) + int(looprow[Passenger])) + (getHour(row[Hour]) / getHour(looprow[Hour]))  )
                                    except:
                                        partsimilarity =  (  (int(row[Passenger]) + int(looprow[Passenger]))  )
                                    # Column 1 actual X Column 2 below
                                    distance = harvestine_distance(float(row[latpick]), float(row[longpick]), float(looprow[latdrop]), float(looprow[longdrop]))
                                    similarity = distance * partsimilarity
                                    temp.writerow([columnsid[0], columnsid[3], distance, similarity])
                                    setBiggerValue(distance, similarity)
                                    # Column 1 actual X Column 1 below
                                    distance = harvestine_distance(float(row[latpick]), float(row[longpick]), float(looprow[latpick]), float(looprow[longpick]))
                                    similarity = distance * partsimilarity
                                    temp.writerow([columnsid[0], columnsid[2], distance, similarity])
                                    setBiggerValue(distance, similarity)
                                    # Column 2 actual X Column 2 below
                                    distance = harvestine_distance(float(row[latdrop]), float(row[longdrop]), float(looprow[latpick]), float(looprow[longpick]))
                                    similarity = distance * partsimilarity
                                    temp.writerow([columnsid[1], columnsid[3], distance, similarity])
                                    setBiggerValue(distance, similarity)
                                    # Column 2 actual X Column 1 below
                                    distance = harvestine_distance(float(row[latdrop]), float(row[longdrop]), float(looprow[latdrop]), float(looprow[longdrop]))
                                    similarity = distance * partsimilarity
                                    temp.writerow([columnsid[1], columnsid[2], distance, similarity])
                                    setBiggerValue(distance, similarity)
                        else:
                            loopfirstline = False

                loopfirstline = True
                f2.close()
        else:
            firstline = False
f1.close()
print(biggerdistance, biggersimilarity)
print("Parsing distance and similarity from temp.csv to ds.csv")
dscsv = csv.writer(open("ds.csv", "wb"))
with open('temp.csv') as f1:
    for row in csv.reader(iter(f1.readline, '')):
        try:
            camp1 = float(row[2]) / biggerdistance
            camp1 = "%.10f" % camp1
        except:
            camp1 = -1

        try:
            camp2 = float(row[3]) / biggersimilarity
            camp2 = "%.10f" % camp2
        except:
            camp2 = -1

        dscsv.writerow([row[0], row[1], camp1, camp2])
f1.close()
