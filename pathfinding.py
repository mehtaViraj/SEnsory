import math

# so we have three variables: the length, the width, and the range of the camera

# def num_nodes():
# always start on the top-left
# example array :  [(10,1),(5,1),(5,2)]
# direction 1-front 2-right 3-left


def calc_cam(radius, theta):
    cam_range = radius*math.cos(theta/2)
    # this only accounts for half the width
    cam_width = radius*math.sin(theta/2)


def pathfinder(length, width, cam_range, cam_width):
    number_nodes_l = length//cam_range
    number_nodes_w = width//cam_range
    path = []  # empty list that stores the path
    count_nodes = 0

    for i in range(1, number_nodes_w+1):
        distance_travelled_l = 0
        while(distance_travelled_l < length):
            if i != 1 and distance_travelled_l == 0:
                direction = 2
            else:
                direction = 1
            node_dist = cam_range
            path.append((node_dist, direction))
            distance_travelled_l += cam_range
            count_nodes += 1

        else:
            node_dist = cam_range
            direction = 2
            path.append((node_dist, direction))
            count_nodes += 1
    if number_nodes_w % 2 != 0:
        path.append((width, 2))  # this is to go back to the initial position
    else:
        path.append((width, 3))
        path.append((length, 3))
