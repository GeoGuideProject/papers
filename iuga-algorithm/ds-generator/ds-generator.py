import csv, math
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
latpick, longpick           = [6, 5]
latdrop, longdrop           = [10, 9]
Distance, Hour, Passenger   = [4, 1, 3]
biggerdistance, biggersimilarity, firstline, countlines =   [0, 0, True, 0]
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
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
        #       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
        #       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
        #       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
        #       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
countlines = -1
dscsv = csv.writer(open("ds.csv", "wb"))
index = csv.writer(open("index.csv", "wb"))
with open('arquivo.csv') as f1:
    for row in csv.reader(iter(f1.readline, '')):
        countlines += 1
        if(firstline == False): # Ignore header line
            index.writerow([(countlines*2) - 1, row[latpick], row[longpick]])
            index.writerow([(countlines*2), row[latdrop], row[longdrop]])
            loopfirstline = True
            loopcountlines = -1
            with open('arquivo.csv') as f2:
                for looprow in csv.reader(iter(f2.readline, '')):
                    loopcountlines += 1
                    if(loopfirstline == False):
                        if(countlines < loopcountlines):
                            try:
                                partsimilarity =  (  (int(row[Passenger]) + int(looprow[Passenger])) + (getHour(row[Hour]) / getHour(looprow[Hour]))  )
                            except:
                                partsimilarity =  (  (int(row[Passenger]) + int(looprow[Passenger]))  )
                            columnsid = [(countlines*2) - 1, (countlines*2) , (loopcountlines*2) - 1, (loopcountlines*2)]
                            # Column 1 actual X Column 2 below
                            distance = harvestine_distance(float(row[latpick]), float(row[longpick]), float(looprow[latdrop]), float(looprow[longdrop]))
                            similarity = distance * partsimilarity
                            dscsv.writerow([columnsid[0], columnsid[3], distance, similarity])
                            # Column 1 actual X Column 1 below
                            distance = harvestine_distance(float(row[latpick]), float(row[longpick]), float(looprow[latpick]), float(looprow[longpick]))
                            similarity = distance * partsimilarity
                            dscsv.writerow([columnsid[0], columnsid[2], distance, similarity])
                            # Column 2 actual X Column 2 below
                            distance = harvestine_distance(float(row[latdrop]), float(row[longdrop]), float(looprow[latpick]), float(looprow[longpick]))
                            similarity = distance * partsimilarity
                            dscsv.writerow([columnsid[1], columnsid[3], distance, similarity])
                            # Column 2 actual X Column 1 below
                            distance = harvestine_distance(float(row[latdrop]), float(row[longdrop]), float(looprow[latdrop]), float(looprow[longdrop]))
                            similarity = distance * partsimilarity
                            dscsv.writerow([columnsid[1], columnsid[2], distance, similarity])
                    else:
                        loopfirstline = False

            loopfirstline = True
            f2.close()
        else:
            firstline = False
f1.close()

#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!#       NOT FINISHED!
