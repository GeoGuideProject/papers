import csv
def rangeAmmount(filename):
    similarity = [0,0,0,0,0,0,0,0,0,0]
    distance = [0,0,0,0,0,0,0,0,0,0]
    with open(filename) as f1:
        for row in csv.reader(iter(f1.readline, '')):
            row[2] = float(row[2])
            row[3] = float(row[3])

            if((row[2] >= 0.0) and (row[2] < 0.1)):
                distance[0] += 1
            elif((row[2] >= 0.1) and (row[2] < 0.2)):
                distance[1] += 1
            elif((row[2] >= 0.2) and (row[2] < 0.3)):
                distance[2] += 1
            elif((row[2] >= 0.3) and (row[2] < 0.4)):
                distance[3] += 1
            elif((row[2] >= 0.4) and (row[2] < 0.5)):
                distance[4] += 1
            elif((row[2] >= 0.5) and (row[2] < 0.6)):
                distance[5] += 1
            elif((row[2] >= 0.6) and (row[2] < 0.7)):
                distance[6] += 1
            elif((row[2] >= 0.7) and (row[2] < 0.8)):
                distance[7] += 1
            elif((row[2] >= 0.8) and (row[2] < 0.9)):
                distance[8] += 1
            elif((row[2] >= 0.9) and (row[2] <= 1)):
                distance[9] += 1


            if((row[3] >= 0.0) and (row[3] < 0.1)):
                similarity[0] += 1
            elif((row[3] >= 0.1) and (row[3] < 0.2)):
                similarity[1] += 1
            elif((row[3] >= 0.2) and (row[3] < 0.3)):
                similarity[2] += 1
            elif((row[3] >= 0.3) and (row[3] < 0.4)):
                similarity[3] += 1
            elif((row[3] >= 0.4) and (row[3] < 0.5)):
                similarity[4] += 1
            elif((row[3] >= 0.5) and (row[3] < 0.6)):
                similarity[5] += 1
            elif((row[3] >= 0.6) and (row[3] < 0.7)):
                similarity[6] += 1
            elif((row[3] >= 0.7) and (row[3] < 0.8)):
                similarity[7] += 1
            elif((row[3] >= 0.8) and (row[3] < 0.9)):
                similarity[8] += 1
            elif((row[3] >= 0.9) and (row[3] <= 1)):
                similarity[9] += 1
    print("Distance: \n")
    for indice, x in enumerate(distance):
        output = str(float(indice)/10) + " ~ " + str((float(indice)/10) + 0.1) + ": " + str(x)
        print(output)

    print("\nSimilarity: \n")
    for indice, x in enumerate(similarity):
        output = str(float(indice)/10) + " ~ " + str((float(indice)/10) + 0.1) + ": " + str(x)
        print(output)

rangeAmmount('ds.csv')
