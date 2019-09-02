"""

Home Work 1. Task 2.

"""

lat = input("Input latitude data, please: ")
lon = input("Input longitude data, please: ")

lat_num = [ float(i) for i in lat.split(sep=' ') ]
lon_num = [ float(i) for i in lon.split(sep=' ') ]

lat_center = sum(lat_num) / float(len(lat_num))
lon_center = sum(lon_num) / float(len(lon_num))

all_points = list(zip(lat_num, lon_num))

dist_to_center = []

for point in all_points:
    lat_point, lon_point = point
    dist = ((lat_point - lat_center) ** 2  + (lon_point - lon_center) **  2 ) ** (1/2)
    dist_to_center.append(dist)

# index 
index_with_min_dist = dist_to_center.index(min(dist_to_center))

# point
point_with_min_dist = all_points[index_with_min_dist]

print(point_with_min_dist)
