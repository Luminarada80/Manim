from deap import tools, base, creator, algorithms
import numpy as np
import logging
import random
import boolean_rule_functions as brf

# 1 = AND relationship
# 0 = OR relationship

nodes = [1, 2, 3, 4]

dataset = [[0, 1, 1, 0, 1, 1],
           [1, 0, 0, 1, 1, 0],
           [0, 1, 1, 0, 0, 1],
           [1, 0, 0, 1, 1, 1]]

connections = [(1, 2), (2, 1), (1, 3), (3, 4), (3, 1), (4, 1), (1, 4), (3, 2)]

inversions = [0, 0, 0, 0]

incoming_nodes = {}
for (incoming, target) in connections:
    if not target in incoming_nodes:
        incoming_nodes[target] = []
    
    incoming_nodes[target].append(incoming)

print(incoming_nodes)


num_connections = {}  #keys = nodes, values = num of connections to that node
for i in connections:
    if not i[1] in num_connections.keys():
        num_connections[i[1]] = 0
    num_connections[i[1]] += 1

connections = []
for i in nodes:
    connections.append(num_connections[i])

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
two_node_rules = ["A_AND_B", "A_OR_B", "A", "B"]

one_node_rules = ["A", "B"]

rules_dict = {3: three_node_rules,
              2: two_node_rules,
              1: one_node_rules}

def create_one_hot(num_rules):
    rules = rules_dict[num_rules]

    bit_string = [0 for i, _ in enumerate(rules)]

    choice = random.randint(0, len(bit_string)-1)

    for i, _ in enumerate(bit_string):
        if i == choice:
            bit_string[i] = 1

    return bit_string

def find_node_start_end(individual):
    # Finds the start and stop of where each node's rule is in the individual
    node_indices = []
    node_start_end = []
    for i, node in enumerate(individual):
        # Find the length of the node
        node_length = len(node)

        # Get the start of the node as either 0 (start) or right after the previous node
        if len(node_indices) != 0:
            node_start = sum(node_indices)+1
        else:
            node_start = 1

        # Get the end of the node as the sum of the previous nodes plus the node length
        node_end = sum(node_indices) + node_length
        node_indices.append(node_length)
        node_start_end.append((node_start, node_end))

    return node_start_end

# Join all of the individual node rules into one individual for the genetic algorithm
def flatten_individual(individual):
    flattened_individual = [item for sublist in individual for item in sublist]
    return flattened_individual

# Reconstruct the individual
def reconstruct_individual(flattened_individual):
    reconstructed_individual = []
    for num, (start, end) in enumerate(node_start_end):
        node_list = [1 * flattened_individual[start-1+i] for i in range(end - start+1)]

        reconstructed_individual.append(node_list)

    return reconstructed_individual

def recover_rules(reconstructed_individual):
    rules = []
    for i, bit_string in enumerate(reconstructed_individual):
        # Find the index of '1' in the vector
        index = bit_string.index(1)

        # Retrieve the corresponding rule from the list
        if len(bit_string) == 12:
            rule = three_node_rules[index]
        elif len(bit_string) == 4:
            rule = two_node_rules[index]
        elif len(bit_string) == 2:
            rule = one_node_rules[index]
    
        # print(f'\tNode {i} = {rule}')
        rules.append(rule)
    return rules

def calculate_error(node, node_index, predicted_rule):
    node_evaluated = dataset[node_index]

def find_calculation_function(rule):
    # ----- Gate choice list/dictionary -----
    possible_rules = [
        brf.A_AND_B_AND_C,
        brf.A_AND_B_OR_C,
        brf.A_OR_B_AND_C,
        brf.A_OR_B_OR_C,
        brf.A_AND_B,
        brf.A_OR_C,
        brf.A_AND_C,
        brf.B_AND_C,
        brf.B_OR_C,
        brf.A_OR_B,
        brf.A,
        brf.B,
        brf.C
    ]

    # Find the function based on the name of the function
    rules = {func.__name__: func for func in possible_rules}

    # Find which rule function is in the best rule
    if rule in rules:
        calculation_function = rules[rule]

        return calculation_function

    else:
        msg = f'ERROR: rule "{rule}" is not in the list of possible rules'
        assert Exception(msg)

def create_individual():
    individual = []
    for node, connection in enumerate(num_connections):
        if connections[node] == 1:
            individual.append(create_one_hot(1))
        elif connections[node] == 2:
            individual.append(create_one_hot(2))
        elif connections[node] == 3:
            individual.append(create_one_hot(3))

    # Get the start and stop indices for each individual
    node_start_end = find_node_start_end(individual)
    # print(f'Node starts and ends = {node_start_end}')

    # Flatten the individuals
    flattened_individual = flatten_individual(individual)

    return individual

# Define the fitness criterion - minimize the error
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


population = []
print('Population')
for i in range(0, 100):
    # Create the individual
    individual = create_individual()
    # print(f'Individual = {individual}')
    
    # Get the start and stop indices for each individual
    node_start_end = find_node_start_end(individual)
    # print(f'Node starts and ends = {node_start_end}')

    # Flatten the individuals
    flattened_individual = flatten_individual(individual)
    # print(f'Flattened individual = {flattened_individual}')

    # Do Genetic Algorithm stuff here
    population.append(flattened_individual)

# for ind_num, ind in enumerate(population):
    # print(f"\tIndividual {ind_num}: {ind}")

# Reconstruct the rules
def evaluate_error(flattened_individual):
    reconstructed_individual = reconstruct_individual(flattened_individual)
    # print(f'Original individual = {individual}')
    # print(f'Reconstr individual = {reconstructed_individual}')

    rules = recover_rules(reconstructed_individual)
    ind_error = 0

    for node_index, node in enumerate(reconstructed_individual):
        # print(f'Index: {node_index}, Node: {nodes[node_index]} Prediction: {node}, connections: {incoming_nodes[node_index+1]}, rule: {rules[node_index]}')
        connections = incoming_nodes[node_index+1]
        # print(f'Rules[node_index]: {rules[node_index]}')
        calculation_function = find_calculation_function(rules[node_index])
        # print(f'Calculation function: {calculation_function}')
        # print(f'Rule: {rules[node_index]}')
        
        # Determine which connections and inversions to use
        filtered_connections = []
        required_nodes = rules[node_index].split('_')
        if "A" in required_nodes:
            # print(f'connections[0]: {connections[0]}')
            filtered_connections.append(connections[0])
        if "B" in required_nodes:
            if len(connections) == 1:
                filtered_connections.append(connections[0])
            else:
                # print(f'connections[1]: {connections[1]}')
                filtered_connections.append(connections[1])  # Adjust index as necessary
        if "C" in required_nodes:
            if len(connections) == 1:
                filtered_connections.append(connections[0])
            else:
                # print(f'connections[2]: {connections[2]}')
                filtered_connections.append(connections[2])  # Keep only A and B if C is not involved

        # print(f'Filtered connections: {filtered_connections}')

        for col_num in dataset[node_index]:
            node_data = dataset[node_index][col_num]
            incoming_node_indices = [dataset[inc_node-1][col_num] for inc_node in filtered_connections]
            incoming_node_data = [dataset[inc_node-1][col_num] for inc_node in filtered_connections]
            inversion_rules = [inversions[inc_node-1] for inc_node in filtered_connections]

            # print(f'Incoming node data" {incoming_node_data}')
            # print(f'Inversion rules: {inversion_rules}')


            predicted = calculation_function(incoming_node_data, inversion_rules)

            # print(f'predicted: {predicted}')
            # print(f'actual: {node_data}')
            error = np.abs(predicted - node_data)
            ind_error += error
    return ind_error

def evaluate(individual):
    error = evaluate_error(individual)
    return (error,)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)




            
