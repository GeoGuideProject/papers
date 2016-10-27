import csv, math, mmap
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
        if((p1 < 40.495730) or (p1 > 40.915031) or (p3 < 40.495730) or (p3 > 40.915031)):
            return True
        elif((p2 < -74.255698) or (p2 > -73.700208) or (p4 < -74.255698) or (p4 > -73.700208)):
            return True
        else:
            return False
    except:
        return True


temp = csv.writer(open("dataanalysis/temp.csv", "wb"))
index = csv.writer(open("dataanalysis/index.csv", "wb"))
index.writerow(['p', 'latitude', 'longitude'])
print("Writing temp.csv with real distance and similarity values\n\nPoints ignored:")
with open('dataanalysis/arquivo.csv') as f1:
    for row in csv.reader(iter(f1.readline, '')):
        countlines += 1
        if(firstline == False): # Ignore header line
            loopfirstline = True
            loopcountlines = -1
            firstloop = True
            ignoreIndex = 0
            if(ignorePoint(float(row[latpick]), float(row[longpick]), float(row[latdrop]), float(row[longdrop]))):
                ignoreIndex += 2
                print(float(row[latpick]), float(row[longpick]), float(row[latdrop]), float(row[longdrop]))
            else:
                index.writerow([(countlines*2) - 1 - ignoreIndex, row[latpick], row[longpick]])
                index.writerow([(countlines*2) - ignoreIndex, row[latdrop], row[longdrop]])
                with open('dataanalysis/arquivo.csv') as f2:
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
                                    #print("Estou na linha: ", countlines, " do loop externo, e linha: ", loopcountlines, " do loop interno")
                        else:
                            loopfirstline = False

                loopfirstline = True
        else:
            firstline = False
print(biggerdistance, biggersimilarity)
print("Parsing distance and similarity from temp.csv to ds.csv")
f = open("dataanalysis/ds.csv", "wb")
dscsv = csv.writer(f)
with open('dataanalysis/temp.csv') as f3:
    for row in csv.reader(f3):
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
        if(camp1 == -1) or (camp2 == -1):
            None
        else:
            dscsv.writerow([row[0], row[1], camp1, camp2])
f.close()

similarity = [0,0,0,0,0,0,0,0,0,0]
distance = [0,0,0,0,0,0,0,0,0,0]
rowammount = 0
arquivos = []
from time import sleep
print("Sleeping to wait csv write,")
sleep(10) # sleep 4 seconds
print("Running experiments.")
for val in range(0, 10):
    strfile = 'dataanalysis/dspoints/' + str(val) + '_' + str(val+1) + '.csv'
    arquivos.append(csv.writer(open(strfile, 'wb')))
    arquivos[val].writerow(['p1', 'p2', 'distance', 'similarity'])

with open('dataanalysis/ds.csv') as f7:
    for row in csv.reader(f7):
        try:
            row2 = float(row[2])
            row3 = float(row[3])
        except:
            print(row)
        rowammount += 1
        if((row2 >= 0.0) and (row2 < 0.1)):
            distance[0] += 1
        elif((row2 >= 0.1) and (row2 < 0.2)):
            distance[1] += 1
        elif((row2 >= 0.2) and (row2 < 0.3)):
            distance[2] += 1
        elif((row2 >= 0.3) and (row2 < 0.4)):
            distance[3] += 1
        elif((row2 >= 0.4) and (row2 < 0.5)):
            distance[4] += 1
        elif((row2 >= 0.5) and (row2 < 0.6)):
            distance[5] += 1
        elif((row2 >= 0.6) and (row2 < 0.7)):
            distance[6] += 1
        elif((row2 >= 0.7) and (row2 < 0.8)):
            distance[7] += 1
        elif((row2 >= 0.8) and (row2 < 0.9)):
            distance[8] += 1
        elif((row2   >= 0.9) and (row2 <= 1)):
            distance[9] += 1
        if((row3 >= 0.0) and (row3 < 0.1)):
            similarity[0] += 1
            arquivos[0].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.1) and (row3 < 0.2)):
            similarity[1] += 1
            arquivos[1].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.2) and (row3 < 0.3)):
            similarity[2] += 1
            arquivos[2].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.3) and (row3 < 0.4)):
            similarity[3] += 1
            arquivos[3].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.4) and (row3 < 0.5)):
            similarity[4] += 1
            arquivos[4].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.5) and (row3 < 0.6)):
            similarity[5] += 1
            arquivos[5].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.6) and (row3 < 0.7)):
            similarity[6] += 1
            arquivos[6].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.7) and (row3 < 0.8)):
            similarity[7] += 1
            arquivos[7].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.8) and (row3 < 0.9)):
            similarity[8] += 1
            arquivos[8].writerow([row[0],row[1], row[2], row[3]])
        elif((row3 >= 0.9) and (row3 <= 1)):
            similarity[9] += 1
            arquivos[9].writerow([row[0],row[1], row[2], row[3]])
print("Distance: \n")
for indice, x in enumerate(distance):
    output = str(float(indice)/10) + " ~ " + str((float(indice)/10) + 0.1) + ": " + str(x)
    print(output)
print("\nSimilarity: \n")
for indice, x in enumerate(similarity):
    output = str(float(indice)/10) + " ~ " + str((float(indice)/10) + 0.1) + ": " + str(x)
    print(output)
    #Write the result in dscount.csv

dscount = csv.writer(open("dataanalysis/dscount.csv", "wb"))
dscount.writerow(['Value','All', '0.0 ~ 0.1','0.1 ~ 0.2','0.2 ~ 0.3', '0.3 ~ 0.4', '0.4 ~ 0.5', '0.5 ~ 0.6', '0.6 ~ 0.7','0.7 ~ 0.8','0.8 ~ 0.9','0.9 ~ 1.0'])
dscount.writerow(['Similarity',rowammount, similarity[0], similarity[1], similarity[2], similarity[3], similarity[4], similarity[5], similarity[6], similarity[7], similarity[8], similarity[9]])
dscount.writerow(['Distance',rowammount, distance[0], distance[1], distance[2], distance[3], distance[4], distance[5], distance[6], distance[7], distance[8], distance[9]])
print("Information about all point is locate in dscount.csv\n\nInside dspoints folder have 10 files, each to 0.1 range")
