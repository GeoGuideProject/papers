import math

def harvestine_distance(lat1, lng1, lat2, lng2):
	dept_lat_rad = math.radians(lat1)
	dept_lng_rad = math.radians(lng1)
	arr_lat_rad = math.radians(lat2)
	arr_lng_rad = math.radians(lng2)
	earth_radius = 3963.1
	d = math.acos(math.cos(dept_lat_rad)*math.cos(dept_lng_rad)*math.cos(arr_lat_rad)*math.cos(arr_lng_rad) + math.cos(dept_lat_rad)*math.sin(dept_lng_rad)*math.cos(arr_lat_rad)*math.sin(arr_lng_rad) + math.sin(dept_lat_rad)*math.sin(arr_lat_rad)) * earth_radius
	return round(d,2)