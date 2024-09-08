# Thomas Nelson - 2023
# Code to demonstrate how an evolutionary algorithm can
# do complex optimization through genetic processes

# Import packages needed
import random
from numpy.random import rand
from Levenshtein import distance
from Bio import Align

# Define the fitness function that will be minimized
# Returns the Levenstein distance between 2 DNA sequences
# There are probably better fitness functions to use
def fitness_function(solution):
    return distance(solution, target_sequence)

# Generate a random DNA sequence
def random_sequence(length):
    return ''.join(random.choice('GATC') for _ in range(length))

# Create an initial population of candidate solutions
def initialize_population(population_size, chromosome_length):
    return [list(random_sequence(chromosome_length)) for _ in range(population_size)]

# Select parents for reproduction using tournament selection
def select_parents(population, num_parents):
    parents = []
    for _ in range(num_parents):
        tournament = random.sample(population, k=int(population_size*0.2))
        parents.append(min(tournament, key=fitness_function))
    return parents

# Perform crossover to create offspring
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Perform mutation on an individual
# Mutations, deletions and insertions
def mutate(sequence):
    for i in range(len(sequence)):
		   # check for a mutation
        if rand() < mutation_rate:
			     # mutate the sequence
            sequence[i] = random.choice('GATC')
        if rand() < deletion_rate:
            # random deletion
            sequence.pop(random.randrange(len(sequence)))
            sequence.append(random.choice('GATC'))
        if rand() < insertion_rate:
            # random deletion
            sequence.insert(random.randrange(len(sequence)), random.choice('GATC'))
            sequence.pop()
    return sequence

# Evolutionary algorithm
def evolutionary_algorithm(population_size, num_generations, chromosome_length):
    population = initialize_population(population_size, chromosome_length)
    
    for generation in range(num_generations):
        parents = select_parents(population, 2)
        
        offspring = []
        for i in range(0, population_size, 2):
            child1, child2 = crossover(parents[0], parents[1])
            child1 = mutate(child1)
            child2 = mutate(child2)
            offspring.extend([child1, child2])
        
        population = offspring
        
        # print progress
        if generation % 100 == 0:
            print(f'Generation: {generation}')
            
    # Find the best individual in the final population
    best_individual = min(population, key=fitness_function)
    best_fitness = fitness_function(best_individual)
    print(f"Best Solution: {''.join(best_individual)}")
    print(f"Best Fitness: {best_fitness}")
    
    return best_individual, best_fitness

# Set parameters
target_sequence = 'ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTA'
chromosome_length = len(target_sequence)
population_size = 100
num_generations = 2000
mutation_rate = (1.0 / chromosome_length)
insertion_rate = (1.0 / chromosome_length) / 8
deletion_rate = (1.0 / chromosome_length) / 8

# Run algorithm
best_individual, best_fitness = evolutionary_algorithm(population_size, num_generations, chromosome_length)
solution = ''.join(best_individual)


# Illustrate the alignment between the best solution and the target
aligner = Align.PairwiseAligner()
alignments = aligner.align(target_sequence, solution)
print(alignments[0])

'''
counter = 0
for i in range(4):
    print(target_sequence[counter:counter+50])
    print(solution[counter:counter+50] + '\n')
    counter = counter + 50

counter = 0
for i in range(4):
    aligner = Align.PairwiseAligner()
    alignments = aligner.align(target_sequence[counter:counter+50], solution[counter:counter+50])
    print(alignments[0])
    counter = counter + 50
''' 