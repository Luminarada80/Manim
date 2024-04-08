from deap import tools, base, creator
import numpy as np
import logging
import random


# 1 = AND relationship
# 0 = OR relationship
combinations = [[1, 1], # A AND B AND C
                [1, 0], # A AND B OR C
                [0, 1], # A OR B AND C
                [0, 0], # A OR B OR C
                [1], # A AND B
                [0], # A OR B
                ["A"],
                ["B"]
                ]



nodes = [1, 2, 3, 4]
connections = [(1, 2), (2, 1), (1, 3), (3, 4), (3, 1), (4, 1), (1, 4), (3, 2)]

num_connections = {}  #keys = nodes, values = num of connections to that node
for i in connections:
    if not i[1] in num_connections.keys():
        num_connections[i[1]] = 0
    num_connections[i[1]] += 1

print(num_connections)
connections = []
for i in nodes:
    connections.append(num_connections[i])

individual = []

for node, connection in enumerate(num_connections):
    three_node = random.choice([i for i, _ in enumerate(combinations)])
    two_node = random.choice([i for i , _ in enumerate(combinations[4:])])
    one_node = random.choice([i for i , _ in enumerate(combinations[6:])])  

    print(f"Node {node} has {connections[node]} connections")
    if connections[node] == 1:
        individual.append(6 + one_node)
    elif connections[node] == 2:
        individual.append(4 + two_node)
    elif connections[node] == 3:
        individual.append(three_node)

print(individual)

one_hot = []
for i, choice in enumerate(individual):
    one_hot_rule = [0 for i, _ in enumerate(combinations)]
    one_hot_rule[choice] = 1
    one_hot.append(one_hot_rule)

three_node_rules = ["A_AND_B_AND_C",
          "A_AND_B_OR_C",
          "A_OR_B_AND_C", 
          "A_AND_B", 
          "A_OR_B", 
          "A_AND_C", 
          "A_OR_C", 
          "B_AND_C", 
          "B_OR_C", 
          "A", 
          "B", 
          "C"]
two_node_rules = ["A_AND_B"]

print(one_hot)
individual = [1, 0, 0, 1]