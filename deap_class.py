class CustomDeap:
    def __init__(self,network,network_name,dataset_name,binMat,nodeList,nodes,individual_length,nodeDict,successorNums):
        # Pass in the node objects
        self.nodes = nodes

        # Genetic algorithm parameters
        self.mutate_percent_pop = 0.25
        self.generations = 10
        self.starting_population_size = 25
        self.parent_population_size = 5
        self.child_population_size = 20
        self.crossover_probability = 0.1
        self.mutation_probability = 0.9
        self.bitFlipProb = 0.5
        self.nodeDict = nodeDict
        self.successorNums = successorNums

        # General parameters
        self.network = network
        self.network_name = network_name
        self.dataset_name = dataset_name
        self.binMat = binMat
        self.nodeList = nodeList
        self.stats = tools.Statistics(key=self.get_fitness_values)
        self.individual_length = individual_length
        self.individualParse = [0] + [node.rule_end_index if node.rule_end_index else nodes[i-1].rule_end_index for i, node in enumerate(nodes)]
        self.size = len(self.individualParse)
        self.node_combination_length = [node.total_combo_length for node in nodes]
        self.total_combinations = [node.total_combos for node in nodes]
        self.total_inversions = [node.inversions for node in nodes]
        self.make_toolbox()

        logging.basicConfig(format='%(message)s', level=logging.INFO)

        _, num_columns = np.shape(self.binMat)

        # Chunk the data matrix to reduce noise and put into numpy array to speed up processing
        self.num_chunks = 100

        # Chunk if there are more cells than columns, otherwise just use the columns
        if num_columns > self.num_chunks:
            self.chunked_data_numpy = np.array(self.chunk_data(num_chunks=self.num_chunks))
            self.coarse_chunked_dataset = np.array(self.chunk_data(num_chunks=round(self.num_chunks / 2, 1)))
        else:
            self.num_chunks = num_columns
            self.chunked_data_numpy = np.array(self.chunk_data(num_chunks=num_columns))
            self.coarse_chunked_dataset = np.array(self.chunk_data(num_chunks=num_columns))

        logging.debug(f'self.chunked_data_numpy: {self.chunked_data_numpy}')

    # 1. Main Genetic Algorithm Function
    def genetic_algorithm(self):
        logbook = tools.Logbook()

        logging.info(f'\n-----CHUNKING DATASET-----')
        num_rows, num_columns = np.shape(self.binMat)
        logging.info(f"\tOriginal Data Shape: {num_rows} rows, {num_columns} columns")

        chunked_rows, chunked_columns = np.shape(self.chunked_data_numpy)
        logging.info(f"\tChunked Data Shape: {chunked_rows} rows, {chunked_columns} columns")

        coarse_chunked_rows, coarse_chunked_columns = np.shape(self.coarse_chunked_dataset)
        logging.info(f"\tCoarse Chunked Data Shape: {coarse_chunked_rows} rows, {coarse_chunked_columns} columns")

        logging.info(f'\n-----GENETIC ALGORITHM-----')
        population = self.toolbox.population(n=self.starting_population_size)

        total_fitnesses = []

        logbook.header = ["gen", "nevals"] + (self.stats.fields if self.stats else [])
        lastcheck = []
        modellist = []
        fitnesslist = []
        popList = []

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]

        raw_fitnesses, fitnesses = self.fitness_calculation(invalid_ind, self.chunked_data_numpy, current_gen=0, max_gen=self.generations)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Append the fitnesses for graphing
        total_fitnesses.append(raw_fitnesses)

        fitnesslist.append([list(ind.fitness.values) for ind in population])
        popList.append([list(inder[1]) for inder in population])
        modellist.append(
            [
                [
                    (modeler[0].size),
                    list(modeler[0].nodeList),
                    list(modeler[0].individualParse),
                    list(modeler[0].total_combinations),
                    list(modeler[0].total_inversions),
                    list(modeler[0].node_combination_length),
                    list(modeler[0].nodeList),
                    dict(modeler[0].nodeDict),
                ]
                for modeler in population
            ]
        )

        # Calculate values to display to the terminal for the initial generation
        average_fitness = round(sum(raw_fitnesses) / len(raw_fitnesses), 3)
        min_fitness = round(min(raw_fitnesses), 3)
        max_fitness = round(max(raw_fitnesses), 3)
        stdev_fitness = round(stdev(raw_fitnesses), 3)

        logging.info(f'ngen\tnevals\tavg\tstd\tmin\tmax')
        logging.info(f'{0}\t{len(raw_fitnesses)}\t{average_fitness}\t{stdev_fitness}\t{min_fitness}\t{max_fitness}')

        # Begin the generational process
        for gen in range(1, self.generations + 1):

            # Perform mutation and crossover
            offspring = self.__varOrAdaptive(
                population,
                self.toolbox,
                (1.0 * gen / self.generations),
                self.mutate_percent_pop
            )

            invalid_offspring = [ind for ind in offspring if not ind.fitness.valid]

            # Calculate the fitness for each individual
            raw_fitnesses, fitnesses = self.fitness_calculation(invalid_offspring, self.chunked_data_numpy, gen, self.generations+1)

            for ind, fit in zip(invalid_offspring, fitnesses):
                ind.fitness.values = fit

            # Append the fitnesses for graphing
            total_fitnesses.append(raw_fitnesses)

            if gen == self.generations:
                # self.graph_results(total_fitnesses)
                return raw_fitnesses, invalid_offspring, logbook
            else:

                # Select the next generation population
                population[:] = self.toolbox.select(offspring, self.parent_population_size)

                # Get the fitness
                fitnesslist.append([list(ind.fitness.values) for ind in population])
                popList.append([list(inder[1]) for inder in population])
                modellist.append(
                    [
                        [
                            (modeler[0].size),
                            list(modeler[0].nodeList),
                            list(modeler[0].individualParse),
                            list(modeler[0].total_combinations),
                            list(modeler[0].total_inversions),
                            list(modeler[0].node_combination_length),
                            list(modeler[0].nodeList),
                            dict(modeler[0].nodeDict),
                        ]
                        for modeler in population
                    ]
                )

                # Calculate values to display to the terminal for the initial generation
                average_fitness = round(sum(raw_fitnesses) / len(raw_fitnesses), 3)
                min_fitness = round(min(raw_fitnesses), 3)
                max_fitness = round(max(raw_fitnesses), 3)
                stdev_fitness = round(stdev(raw_fitnesses), 3)

                logging.info(f'{gen}\t{len(population)+len(raw_fitnesses)}\t{average_fitness}\t{stdev_fitness}\t{min_fitness}\t{max_fitness}')
