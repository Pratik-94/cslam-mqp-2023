import random, numpy, math, time
import params

def calculateNodeWeight(node_weights, index):
  total = 0
  for node_weight in node_weights:
    total += node_weight
  return node_weights[index]/total

#settings params from params.py
nodes = params.nodes
robot_memory = params.memory
robots = params.robots
random.seed(params.seed)
for i in range(0,20): # the number of times we're running the experiment
  adj_grid = numpy.eye(nodes, nodes, 0, int)
  node_memory = numpy.empty(nodes)
  prob_connection = 0.5
  for i in range(0,nodes): #assumes the starting node is only connected to the first node add the ability for other nodes to be reached from the start
    rfloat = random.random()
    node_memory[i] = (robot_memory/1.5)*rfloat
    for j in range(i,nodes):
      if(i == j or random.random() < prob_connection):
        adj_grid[i][j] = 1
        adj_grid[j][i] = 1
  # print(adj_grid)
  #print(node_memory)

  # perform bfs to check whether the graph is connected
  current_node_index = 0
  nodes_checked = []
  nodes_checked.append(current_node_index)
  queue = []
  queue.append(current_node_index)
  while queue:
    current_node_index = queue.pop(0)
    # print(current_node_index)
    for i in adj_grid[current_node_index]:
      if i not in nodes_checked and adj_grid[current_node_index][i] == 1:
        nodes_checked.append(i)
        queue.append(i)
  
  # now we check which nodes were not covered by bfs
  for j in range(nodes):
    if j not in nodes_checked:
      # connect the node to a random node in the main part of the graph
      connection_index = math.floor(random.random() * len(nodes_checked))
      adj_grid[connection_index][j] = 1
      adj_grid[j][connection_index] = 1
      # print("connected " + str(j) + " to " + str(connection_index))


  # weighted probabilistic algorithm
  # gives each adj node an equal chance and picks one

  # mapping the path
  at_end = False
  memory_left = robot_memory
  nodes_visited = [0]
  # while not at the end or no more possible options
  start = time.monotonic_ns()
  while (not at_end):
    possible_next_nodes = []
    # can only consider a node if there's an edge and hasn't been visited yet and has a smaller memory cost
    for j in nodes_visited:
      for i in range(0,nodes):
        if((adj_grid[j][i] == 1) and (i not in nodes_visited) and (j != i) and node_memory[i] <= memory_left):
          # add number to array
          possible_next_nodes.append(i)
    

    
    # if robot has enough memory to go to the selected node and robot has not visited it already
    if (len(possible_next_nodes) > 0):
      # pick next node
      choice = random.random() - calculateNodeWeight(node_memory, possible_next_nodes[0])
      next_node_index = 0
      while choice >= 0 and next_node_index < len(possible_next_nodes)-1:
        next_node_index = 1 + next_node_index
        choice -= calculateNodeWeight(node_memory, possible_next_nodes[next_node_index])
      nodes_visited.append(possible_next_nodes[next_node_index])
      memory_left -= node_memory[possible_next_nodes[next_node_index]]
      #print("Next node: " + str(possible_next_nodes[next_node_index]) + ", has cost of " + str(node_memory[possible_next_nodes[next_node_index]]))
      #print("Available memory left: " + str(memory_left))
    else:
      at_end = True
      #print("Path: " + str(nodes_visited))
      print(str(robot_memory - memory_left)+ " " + str((time.monotonic_ns()-start)/1000000))