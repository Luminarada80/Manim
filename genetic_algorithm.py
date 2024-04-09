import numpy as np
import random
import boolean_rule_functions as brf
import matplotlib.pyplot as plt
from manim import *

# 1 = AND relationship
# 0 = OR relationship

nodes = [1, 2, 3, 4]

dataset = [[0, 1, 1, 0, 1, 1],
           [1, 0, 0, 1, 1, 0],
           [0, 1, 1, 0, 0, 1],
           [1, 0, 0, 1, 1, 1]]

connections = [(1, 2), (2, 1), (1, 3), (3, 4), (3, 1), (4, 1), (1, 4), (3, 2)]

inversions = [0, 0, 0, 0]

# Create a dictionary of incoming nodes
incoming_nodes = {}
for (incoming, target) in connections:
    if not target in incoming_nodes:
        incoming_nodes[target] = []
    
    incoming_nodes[target].append(incoming)

# Create a dictionary of connections between nodes
num_connections = {}  #keys = nodes, values = num of connections to that node
for i in connections:
    if not i[1] in num_connections.keys():
        num_connections[i[1]] = 0
    num_connections[i[1]] += 1

connections = []
for i in nodes:
    connections.append(num_connections[i])

# Define the possible combinations of rules
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

# Create a string of 0's corresponding to each possible rule and set one of them to 1, indicating that rule is selected
def create_one_hot(num_rules):
    rules = rules_dict[num_rules]

    bit_string = [0 for i, _ in enumerate(rules)]

    choice = random.randint(0, len(bit_string)-1)

    for i, _ in enumerate(bit_string):
        if i == choice:
            bit_string[i] = 1

    return bit_string

# Creates an individual with each one-hot incoded list of genes
def create_individual():
    individual = []
    for node, connection in enumerate(num_connections):
        if connections[node] == 1:
            individual.append(create_one_hot(1))
        elif connections[node] == 2:
            individual.append(create_one_hot(2))
        elif connections[node] == 3:
            individual.append(create_one_hot(3))

    return individual

# Find the start and end indices for each rule, used to split up the individual back into the rules when needed
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

# Reconstruct the individual to have a list of lists, where each sublist is the one-hot encoded choice of rule
def reconstruct_individual(flattened_individual):
    reconstructed_individual = []
    # print(f'\nflattened individual: {flattened_individual}')
    for num, (start, end) in enumerate(node_start_end):
        node_list = [1 * flattened_individual[start-1+i] for i in range(end - start+1)]

        reconstructed_individual.append(node_list)
    # print(f'reconstructed individual: {reconstructed_individual}')

    return reconstructed_individual

# Rebuild the rules from the reconstructed individual based on which combination is chosen
def recover_rules(reconstructed_individual):
    rules = []

    for i, bit_string in enumerate(reconstructed_individual):
        # Find the index of '1' in the vector
        # print(bit_string)

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

# Returns the function that corresponds to the rule that was chosen
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

def mutation(offspring):
    reconstructed_individual = reconstruct_individual(offspring) 
    
    for gene in reconstructed_individual:
        # Mutation
        mutation_prob = 0.95
        mutation_roll = random.random()
        if mutation_roll > mutation_prob:
            # print(f"\t\tmutation_roll = {mutation_roll}, Mutate!")
            # print(f'\t\t\t{gene}')
            gene = [0 for _ in gene]

            # Generate a random index within the range of the list's indices
            random_index = random.randint(0, len(gene) - 1)

            # Set the value at the randomly chosen index to 1
            gene[random_index] = 1
            # print(f'\t\t\t{gene}')
        
def crossover(parent1, parent2):
    # Reconstruct the individuals in the population
    parent1 = reconstruct_individual(parent1)
    parent2 = reconstruct_individual(parent2)

    # Perform the crossover
    if random.random() <= 0.7:

        # Randomly select a gene (sublist) index for swapping, ensuring it's within the bounds of both individuals
        min_length = min(len(parent1), len(parent2))
        gene_index = random.randint(0, min_length - 1)
        
        # Swap the genes (sublists) at the chosen index
        parent1[gene_index], parent2[gene_index] = parent2[gene_index], parent1[gene_index]
        
        # # Log the operation (optional)
        # print(f"Crossover between individuals at gene index {gene_index}:")
        # print(f"  Individual 1: {parent1}")
        # print(f"  Individual 2: {parent2}")
    offspring1 = flatten_individual(parent1)
    offspring2 = flatten_individual(parent2)

    return offspring1, offspring2

def selection(population, N):
    # Pair each individual with its error
    indexed_errors = [(ind_num, evaluate_error(ind)) for ind_num, ind in enumerate(population)]
    
    # Sort by error
    sorted_by_error = sorted(indexed_errors, key=lambda x: x[1])
    
    # Select the top N individuals
    selected_indices = [x[0] for x in sorted_by_error[:N]]
    
    # Retrieve the individuals based on the selected indices
    selected_individuals = [population[i] for i in selected_indices]
    
    return selected_individuals

def graph_results(min_errors, max_errors, avg_errors):
    generations = range(number_of_generations)

    plt.figure(figsize=(10, 6))
    plt.plot(generations, min_errors, label='Minimum Error')
    plt.plot(generations, max_errors, label='Maximum Error')
    plt.plot(generations, avg_errors, label='Average Error')

    plt.title('GA Performance Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Error')
    plt.ylim(0, 25)
    plt.legend()
    plt.grid(True)
    plt.show()

min_errors = []
max_errors = []
avg_errors = []
number_of_generations = 100
number_of_individuals = 100
# for generation in range(number_of_generations):
#     print(f'Generation {generation}')
#     population = []
#     for i in range(number_of_individuals):
#         # Create the individual
#         individual = create_individual()
#         # print(f'Individual = {individual}')
        
#         # Get the start and stop indices for each individual
#         node_start_end = find_node_start_end(individual)
#         # print(f'Node starts and ends = {node_start_end}')

#         # Flatten the individuals
#         flattened_individual = flatten_individual(individual)
#         # print(f'Flattened individual = {flattened_individual}')

#         # Do Genetic Algorithm stuff here
#         population.append(flattened_individual)

#     selected_individuals = selection(population, 50)

#     next_generation = selected_individuals[:]

#     while len(next_generation) < len(population):
#         # Select parents for crossover
#         parent1, parent2 = random.sample(selected_individuals, 2)

#         # Crossover to produce offspring (you may need to implement or adjust your crossover function)
#         offspring1, offspring2 = crossover(parent1, parent2)

#         # Mutate the offspring (adjust your mutation function as needed)
#         mutation(offspring1)
#         mutation(offspring2)

#         # Add the offspring to the next generation, checking population size to avoid exceeding the limit
#         next_generation.append(offspring1)
#         if len(next_generation) < len(population):
#             next_generation.append(offspring2)
        
#     errors = []
#     for individual in next_generation:
#         individual_error = evaluate_error(individual)
#         errors.append(individual_error)

#     min_errors.append(min(errors))
#     max_errors.append(max(errors))
#     avg_errors.append(sum(errors) / len(errors))

# print(len(min_errors), len(max_errors), len(avg_errors))


class ErrorGraphScene(Scene):
    def construct(self):
        # Sample errors and generations data
        errors = [[0.1569298245614035, 0.17192982456140352, 0.19779816513761467, 0.20845454545454545, 0.214375, 0.19666666666666666, 0.16347457627118644, 0.19205128205128205, 0.22895652173913045, 0.19210526315789472, 0.17233333333333334, 0.19508474576271187, 0.1911304347826087, 0.1753448275862069, 0.20394736842105263, 0.20870689655172414, 0.16789473684210526, 0.20728813559322035, 0.21, 0.16157407407407406, 0.20448275862068965, 0.1939655172413793, 0.20339285714285715, 0.18967213114754097, 0.16424528301886793, 0.16572649572649573, 0.19425925925925927, 0.19936936936936936, 0.18827272727272729, 0.18900900900900902, 0.16741379310344828, 0.16855855855855856, 0.20758928571428573, 0.19423423423423422, 0.19882882882882882, 0.19162162162162164, 0.19288288288288288, 0.18575221238938053, 0.21150943396226415, 0.21717948717948718, 0.19470085470085471, 0.19369369369369369, 0.20710280373831777, 0.1906140350877193, 0.18649122807017543, 0.17147826086956522, 0.17293103448275862, 0.20401785714285714, 0.17266666666666666, 0.21116666666666667],[0.18827272727272729, 0.17293103448275862, 0.19423423423423422, 0.20710280373831777, 0.17054545454545456, 0.21, 0.17266666666666666, 0.18967213114754097, 0.16347457627118644, 0.19162162162162164, 0.19210526315789472, 0.18967213114754097, 0.19423423423423422, 0.19288288288288288, 0.16741379310344828, 0.18967213114754097, 0.19162162162162164, 0.19425925925925927, 0.20448275862068965, 0.16424528301886793, 0.17293103448275862, 0.214375, 0.1838679245283019, 0.20339285714285715, 0.2005982905982906],[0.19288288288288288, 0.18967213114754097, 0.20710280373831777, 0.18967213114754097, 0.21, 0.17512605042016807, 0.17293103448275862, 0.19425925925925927, 0.17266666666666666, 0.19162162162162164, 0.17266666666666666, 0.20710280373831777, 0.19423423423423422, 0.16741379310344828, 0.19162162162162164, 0.16741379310344828, 0.17266666666666666, 0.17293103448275862, 0.19920353982300884, 0.19423423423423422, 0.20339285714285715, 0.19162162162162164, 0.2005982905982906, 0.18228813559322035, 0.19162162162162164],[0.17266666666666666, 0.20339285714285715, 0.2097345132743363, 0.19162162162162164, 0.19288288288288288, 0.17512605042016807, 0.19162162162162164, 0.16741379310344828, 0.17266666666666666, 0.16741379310344828, 0.17293103448275862, 0.1847663551401869, 0.17266666666666666, 0.16741379310344828, 0.19288288288288288, 0.19162162162162164, 0.19425925925925927, 0.19, 0.19162162162162164, 0.19423423423423422, 0.18967213114754097, 0.19920353982300884, 0.18967213114754097, 0.19425925925925927, 0.17266666666666666],[0.16741379310344828, 0.19162162162162164, 0.2097345132743363, 0.18967213114754097, 0.17512605042016807, 0.16741379310344828, 0.17266666666666666, 0.19425925925925927, 0.1847663551401869, 0.17266666666666666, 0.19425925925925927, 0.19162162162162164, 0.20339285714285715, 0.19, 0.19162162162162164, 0.19288288288288288, 0.19162162162162164, 0.17293103448275862, 0.2097345132743363, 0.18035714285714285, 0.2097345132743363, 0.17293103448275862, 0.19920353982300884, 0.19162162162162164, 0.17293103448275862],[0.2097345132743363, 0.19162162162162164, 0.19425925925925927, 0.19162162162162164, 0.18967213114754097, 0.17512605042016807, 0.16741379310344828, 0.19, 0.19920353982300884, 0.17293103448275862, 0.17293103448275862, 0.19162162162162164, 0.2097345132743363, 0.17266666666666666, 0.18967213114754097, 0.19288288288288288, 0.2097345132743363, 0.17293103448275862, 0.19425925925925927, 0.17293103448275862, 0.19920353982300884, 0.19162162162162164, 0.20339285714285715, 0.17293103448275862, 0.2044642857142857],[0.19162162162162164, 0.2044642857142857, 0.19920353982300884, 0.17512605042016807, 0.1891304347826087, 0.17266666666666666, 0.17151785714285714, 0.19162162162162164, 0.17293103448275862, 0.19162162162162164, 0.18967213114754097, 0.2097345132743363, 0.17293103448275862, 0.16701612903225807, 0.18675, 0.18967213114754097, 0.19162162162162164, 0.17293103448275862, 0.17293103448275862, 0.18967213114754097, 0.1882300884955752, 0.17293103448275862, 0.18967213114754097, 0.17293103448275862, 0.1829059829059829],[0.18967213114754097, 0.18967213114754097, 0.17293103448275862, 0.19162162162162164, 0.1891304347826087, 0.17151785714285714, 0.18967213114754097, 0.18967213114754097, 0.19162162162162164, 0.17293103448275862, 0.1891304347826087, 0.18967213114754097, 0.20522522522522524, 0.18675, 0.19162162162162164, 0.17266666666666666, 0.1891304347826087, 0.19920353982300884, 0.17512605042016807, 0.17293103448275862, 0.2044642857142857, 0.1882300884955752, 0.18967213114754097, 0.1882300884955752, 0.17293103448275862],[0.18675, 0.1891304347826087, 0.17266666666666666, 0.17293103448275862, 0.17512605042016807, 0.19531531531531532, 0.17293103448275862, 0.19162162162162164, 0.18967213114754097, 0.18967213114754097, 0.1891304347826087, 0.18967213114754097, 0.18967213114754097, 0.17293103448275862, 0.18967213114754097, 0.19162162162162164, 0.17266666666666666, 0.17293103448275862, 0.17293103448275862, 0.20205357142857142, 0.18967213114754097, 0.17151785714285714, 0.17293103448275862, 0.1882300884955752, 0.1891304347826087],[0.1891304347826087, 0.17293103448275862, 0.19162162162162164, 0.18967213114754097, 0.17293103448275862, 0.19162162162162164, 0.18967213114754097, 0.1882300884955752, 0.17293103448275862, 0.18967213114754097, 0.17293103448275862, 0.18967213114754097, 0.18967213114754097, 0.18967213114754097, 0.17151785714285714, 0.1891304347826087, 0.19162162162162164, 0.17293103448275862, 0.17293103448275862, 0.19162162162162164, 0.19162162162162164, 0.17293103448275862, 0.17293103448275862, 0.18967213114754097, 0.18967213114754097],[0.17293103448275862, 0.18967213114754097, 0.1891304347826087, 0.18967213114754097, 0.18967213114754097, 0.18967213114754097, 0.17470588235294118, 0.17293103448275862, 0.17293103448275862, 0.19162162162162164, 0.17293103448275862, 0.17293103448275862, 0.17293103448275862, 0.17293103448275862, 0.18967213114754097, 0.19162162162162164, 0.19450450450450452, 0.18132743362831857, 0.1882300884955752, 0.1891304347826087, 0.18967213114754097, 0.19162162162162164, 0.1882300884955752, 0.18967213114754097, 0.17293103448275862],[0.1837391304347826, 0.18967213114754097, 0.1882300884955752, 0.18967213114754097, 0.17293103448275862, 0.17293103448275862, 0.19162162162162164, 0.18967213114754097, 0.18271186440677967, 0.17293103448275862, 0.17293103448275862, 0.17470588235294118, 0.17293103448275862, 0.17293103448275862, 0.18967213114754097, 0.18967213114754097, 0.18967213114754097, 0.17293103448275862, 0.19450450450450452, 0.1880909090909091, 0.17293103448275862, 0.18967213114754097, 0.17293103448275862, 0.17714285714285713, 0.19162162162162164],[0.17293103448275862, 0.19162162162162164, 0.17293103448275862, 0.19450450450450452, 0.17714285714285713, 0.17293103448275862, 0.18271186440677967, 0.18967213114754097, 0.17293103448275862, 0.18967213114754097, 0.17293103448275862, 0.1837391304347826, 0.18967213114754097, 0.17714285714285713, 0.18967213114754097, 0.17293103448275862, 0.1880909090909091, 0.17470588235294118, 0.18967213114754097, 0.1880909090909091, 0.17293103448275862, 0.17293103448275862, 0.1837391304347826, 0.18967213114754097, 0.17293103448275862],[0.18967213114754097, 0.1880909090909091, 0.18271186440677967, 0.1837391304347826, 0.18967213114754097, 0.17293103448275862, 0.17714285714285713, 0.17293103448275862, 0.17293103448275862, 0.18949579831932772, 0.18967213114754097, 0.19450450450450452, 0.18271186440677967, 0.19450450450450452, 0.17470588235294118, 0.17714285714285713, 0.18967213114754097, 0.1828099173553719, 0.18967213114754097, 0.1880909090909091, 0.18967213114754097, 0.17293103448275862, 0.1837391304347826, 0.17293103448275862, 0.17293103448275862],[0.18967213114754097, 0.18967213114754097, 0.17470588235294118, 0.18579831932773108, 0.1837391304347826, 0.1666086956521739, 0.17293103448275862, 0.18967213114754097, 0.1828099173553719, 0.17293103448275862, 0.19450450450450452, 0.1828099173553719, 0.18949579831932772, 0.17714285714285713, 0.16584745762711864, 0.1880909090909091, 0.1837391304347826, 0.17293103448275862, 0.17714285714285713, 0.17293103448275862, 0.1837391304347826, 0.18967213114754097, 0.17293103448275862, 0.17293103448275862, 0.18967213114754097],[0.18967213114754097, 0.1837391304347826, 0.16584745762711864, 0.1828099173553719, 0.17293103448275862, 0.1837391304347826, 0.18628318584070797, 0.16584745762711864, 0.17293103448275862, 0.18967213114754097, 0.1880909090909091, 0.18967213114754097, 0.1666086956521739, 0.17293103448275862, 0.17293103448275862, 0.17293103448275862, 0.17714285714285713, 0.18949579831932772, 0.17293103448275862, 0.17293103448275862, 0.18579831932773108, 0.18949579831932772, 0.18967213114754097, 0.17714285714285713, 0.18967213114754097]]
        generations = [1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

        # Determining the Y-axis range based on the maximum error value
        max_error_value = max([max(sublist) for sublist in errors])

        # Create Axes
        ax = Axes(
            x_range=[0, max(generations), 1],  # Adjusting X range according to generations
            y_range=[0, 0.5, 0.05],  # Adjusting Y range according to max error
            axis_config={"color": BLUE, "include_numbers": True},
            x_length=8,  # Width of the Axes
            y_length=4,   # Height of the Axes
            tips=False
        )

        # Add axis labels
        x_label = ax.get_x_axis_label("Generation")
        x_label.move_to(ax.x_axis).shift(DOWN * 1)

        y_label = ax.get_y_axis_label("Error", direction=UP)
        y_label.move_to(ax.y_axis).rotate(PI/2).shift(LEFT * 1)

        ax.move_to(LEFT*3)

        # Add axes and labels to the scene
        self.play(Create(ax), Write(x_label), Write(y_label))

        # Plotting the dots
        dots = []
        for gen, error_list in zip(generations, errors):
            for error in error_list:
                dot = Dot(ax.c2p(gen, error), color=BLUE)  # Place generation on x, error on y
                dots.append(dot)

        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=0.02))

        self.wait(2)










            
