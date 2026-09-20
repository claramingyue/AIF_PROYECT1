import linecache 

thefilepath = 'exampleMap.txt' 
desired_line_number = 1
theline = linecache.getline(thefilepath, desired_line_number) 

size_x = int(theline[0])
size_y = theline[2]

test = size_x 
theline_start = linecache.getline(thefilepath, test) 

start_coo_x = theline_start[0]

print(start_coo_x)
