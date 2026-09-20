import linecache 

thefilepath = 'exampleMap.txt' 
desired_line_number = 1
theline = linecache.getline(thefilepath, desired_line_number) 

size_x = int(theline[0])
size_y = theline[2]

start_line = size_x + 2 
theline_start = linecache.getline(thefilepath, start_line) 

start_coo_x = theline_start[0]
start_coo_y = theline_start[2]
start_coo_rot = theline_start[4]

start_coo = {
    "x": start_coo_x,
    "y": start_coo_y,
    "rotation": start_coo_rot
}

goal_line = size_x + 3
theline_goal = linecache.getline(thefilepath, goal_line)

goal_coo_x = theline_goal[0]
goal_coo_y = theline_goal[2]
goal_coo_rot = theline_goal[4]

goal_coo = {
    "x": goal_coo_x,
    "y": goal_coo_y,
    "rotation": goal_coo_rot
}

print("Which algorithm would you like to use? (1) Depth-First (2) Breadth-First (3) A* :")

choice = input()

if choice == "1":
    print("You chose Depth-First Search and will now be performed")
    

elif choice == "2":
    print("You chose Breadth-First Search and will now be performed")

elif choice == "3":
    print("You chose A* Search and will now be performed")

else:
    print("Invalid choice. Please select 1, 2, or 3.")
