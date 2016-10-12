import csv
#   Configuration
#
#       First Point:
#           latpick = Latitude Point
#           longpick = Longitude Point
#       Seccond Point:
#           latdrop = Latitude Point
#           longdrop = Longitude Point
#       Others columns:
#           Distance            4
#           Hours pickup        1
#           Passengers          3
    
latpick, longpick           = [6, 5]
latdrop, longdrop           = [10, 9]
Distance, Hour, Passenger   = [4, 1, 3]

# if csv have headers line 'firstline = True' else 'firstline = False'
biggerdistance, biggersimilarity, firstline =   [0, 0, True]

#   Basic function
#   Read date format and extract the hour

# Placido considerei remover as linhas com informacoes erradas... fiz o try para corrigir algumas linhas vazias, porem nao acredito que seja o caminho correto.
def getHour(strdate):  
    try:
        strdate = strdate.split()
        return int(strdate[1].split(':')[0])
    except(IndexError):
        return 0

print("\n\nLoading CSV...")

with open('arquivo.csv') as f1:
    print("\n\nReading CSV to find reference values...\n\n")
    for row in csv.reader(iter(f1.readline, '')):
#   searching bigger similarity value and bigger distance
        if(firstline == False): # Ignore header line
            row[Distance] = float(row[Distance])
            if(biggerdistance < row[Distance]):
                biggerdistance = row[Distance]
#   Similarity is the result of:
#       hour + (distance * passengers)
            similarity = getHour(row[Hour]) + (row[Distance] * int(row[Passenger]))
            if(biggersimilarity < similarity):
                biggersimilarity = similarity
        else:
            firstline = False    
#   Writing ds.csv
print("Bigger distance: ", biggerdistance, "Bigger similarity: ", biggersimilarity)

print("\n\nWriting ds.csv")
 # If True not read headers line
firstline = True   

w = csv.writer(open("ds.csv", "wb"))
with open('arquivo.csv') as f1:
    for row in csv.reader(iter(f1.readline, '')):
        if(firstline == False): # Ignore header line
            similarity = getHour(row[Hour]) + (float(row[Distance]) * int(row[Passenger]))
            #    Plus 180 to remove negative numbers, and concatene with '_' to facility split after
            #    I not found other way to convert latitude and longitude to unique number
            pickuppoint = str(float(row[latpick]) + 180) + "_" + str(float(row[longpick])+180)
            dropoffpoint = str(float(row[latdrop]) + 180) + "_" + str(float(row[longdrop])+180)   

            w.writerow([pickuppoint, dropoffpoint, float(row[Distance])/biggerdistance, similarity/biggersimilarity])
        else:
            firstline = False  
print("\n\nFinished!")



