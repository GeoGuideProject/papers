#!/usr/bin/env python

import operator
import datetime
import diversity, sys
from random import randint
from sys import argv

p_arg, k_arg, lowest_acceptable_similarity_arg = argv

# parameters
input_g = 968
time_limit = 200 				# in miliseconds
#k = 5
k = int(k_arg)						# number of returned records
input_file = "dataanalysis/nyctaxi10000/ds.csv"			# indexing file
#lowest_acceptable_similarity = 0.2
lowest_acceptable_similarity = float(lowest_acceptable_similarity_arg)
stop_visiting_once = False		# should the algorithm stop if it reaches the end of the index (i.e., scanning all records once)

# Note that in case of user group analysis, each group is a record. In case of spatiotemporal data, each geo point is a record.

# variables
current_records = {}		# the ID of current k records will be recorded in this object.
new_records = {}			# ths ID of next potential k records will be recorded in this object.
total_time = 0.0			# total execution time

# dimensions
similarities = {}
distances = {}

# read input file
f = open(input_file)
for line in f:
	line = line.strip()
	parts = line.split(",")
	from_id = int(parts[0])
	if from_id > input_g:
		break
	to_id = int(parts[1])
	similarity = float(parts[2])
	distance = float(parts[3])
	similarities[to_id] = similarity
	distances[to_id] = distance

# sorting similarities and distances in descending order
similarities_sorted = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
distances_sorted = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)

# begin - prepare lists for easy retrieval
records = {}
similarity_by_id = {}
distance_by_id = {}

cnt = 0
for value in similarities_sorted:
	records[cnt] = value[0]
	similarity_by_id[value[0]] = value[1]
	cnt += 1

for value in distances_sorted:
	distance_by_id[value[0]]=value[1]
# begin - prepare lists for easy retrieval

#print str(len(records))+" records retrieved and indexed."

# begin - retrieval functions
def get_distances_of(elements):
	my_distances = []
	for i in range(0,k):
		my_distances.append(distance_by_id[elements[i]])
	return my_distances

def make_new_records(elements,new_element):
	output= {}
	for i in range(0,k):
		output[i] = elements[i]
	replacement = randint(0,k-1)
	output[replacement] = records[new_element]
	return output

def show(elements):
	min_similarity = 1
	out = "[ "
	for i in range(0,k):
		out += str(elements[i])+" "
		if similarity_by_id[elements[i]] < min_similarity:
			min_similarity = similarity_by_id[elements[i]]
	out += "]"
	out += ", " + str() + str(min_similarity)
	my_distances = get_distances_of(elements)
	my_diversity = diversity.diversity(my_distances)
	out += "," + str(round(my_diversity,2))
	return out

# end - retrieval functions

# initialization by k most similar records
for i in range(0,k):
	current_records[i]=records[i]

#print "begin: ",show(current_records)

# greedy algorithm
pointer = k-1
nb_iterations = 0
while total_time < time_limit and pointer < len(records):
	nb_iterations += 1
	pointer += 1
	redundancy_flag = False
	for i in range(0,k):
		if current_records[i] == records[pointer]:
			redundancy_flag = True
			break
	if redundancy_flag == True:
		continue
	begin_time = datetime.datetime.now()
	current_distances = get_distances_of(current_records)
	current_diversity = diversity.diversity(current_distances)
	new_records = make_new_records(current_records, pointer)
	new_distances = get_distances_of(new_records)
	new_diversity = diversity.diversity(new_distances)
	if new_diversity > current_diversity:
		current_records = new_records
	end_time = datetime.datetime.now()
	duration = (end_time - begin_time).microseconds / 1000.0
	total_time += duration
	if similarity_by_id[records[pointer]] < lowest_acceptable_similarity:
		if stop_visiting_once == False:
			pointer = k
		else:
			break
print str(k) + "," + str(lowest_acceptable_similarity) + "," + str(show(current_records)) + "," + str( nb_iterations) + "," + str(total_time)
#print "end: ", show(current_records)
#print "execution time (ms)", total_time
#print "# iterations", nb_iterations
