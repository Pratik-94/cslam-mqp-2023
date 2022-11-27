import random, numpy, math, time
import params

def isTravelable(path):
  nodes_visit = []
  nodes_reachable = []
  for i in range(nodes):
        if (math.floor(path[1] / ( 2**i )) % 2 == 1):
          nodes_visit.append(i)
  if nodes_visit[0] != 0:
      return False
  else:
    nodes_reachable.append(nodes_visit[0])
  for curr_node in nodes_reachable:
    for test_node in nodes_visit:
      if adj_grid[curr_node][test_node] == 1 and test_node not in nodes_reachable:
        nodes_reachable.append(test_node)
  if len(nodes_reachable) == len(nodes_visit):
    return True
  return False

#settings params from params.py
nodes = params.nodes
robot_memory = params.memory
robots = params.robots
random.seed(params.seed)
for i in range(0,1):
  adj_grid = numpy.eye(nodes)
  node_memory = numpy.empty(nodes)
  nodes_mapped = numpy.empty(nodes)
  prob_connection = 0.5
  for i in range(0,nodes): #assumes the starting node is only connected to the first node add the ability for other nodes to be reached from the start
    rfloat = random.random()
    node_memory[i] = (robot_memory/1.5)*rfloat
    for j in range(i,nodes):
      if(i == j or random.random() < prob_connection):
        adj_grid[i][j] = 1
        adj_grid[j][i] = 1
  # print(adj_grid)
  # print(node_memory)

  # greedy algorithm
  # adds the highest possible cost to explore the longest as possible

  # mapping the path
  # make that the next node
  
  nodes_mapped[0] = 1
  # while not at the end or no more possible options
  start = time.monotonic_ns()
  def isDone():
    for i in nodes_mapped:
        if(i != 1):
            return True
    return False
  
  robot = 0
  while(isDone()):
    at_end = False
    expand = False
    highest_cost = 0
    memory_left = robot_memory
    next_node = 0
    nodes_visited = []
    possible_next_nodes = []
    nodes_visited.append(next_node)
    while (not at_end):
        # can only consider a node if there's an edge and hasn't been visited yet and has a smaller memory cost
        possible_next_nodes = []
        # can only consider a node if there's an edge and hasn't been visited yet and has a smaller memory cost
        for j in nodes_visited:
            for i in range(0,nodes):
                if((adj_grid[j][i] == 1) and (i not in nodes_visited) and (j != i) and node_memory[i] <= memory_left):
                    # add number to array
                    possible_next_nodes.append(i)
        
        # if robot has enough memory to go to the selected node and robot has not visited it already
        if (len(possible_next_nodes) > 0):
          for i in possible_next_nodes:
              if(highest_cost < node_memory[i] and nodes_mapped[i] != 1):
                  highest_cost = node_memory[i]
                  next_node = i
          nodes_visited.append(next_node)
          nodes_mapped[next_node] = 1
          memory_left -= node_memory[next_node]
          highest_cost = 0
        elif(not expand):
            expand = True
            for i in range(1, len(nodes_mapped)):
                if (i not in nodes_visited and nodes_mapped[i] == 1):
                    nodes_visited.append(i)
        else:
            at_end = True
            print("robot-" + str(robot)+ " " + str(robot_memory - memory_left)+ " " + str((time.monotonic_ns()-start)/1000000))
            print(nodes_mapped)
            robot += 1
            # print("Not enough memory left, done with path at node " + str(current_node))
            # print("Available memory left: " + str(memory_left))
            # print(adj_grid[current_node])
            print("Path: " + str(nodes_visited))
            input()