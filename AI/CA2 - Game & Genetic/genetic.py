import random, time

#TODO assign numbers to variables below
crossoverProbability = 0.90
carryPercentage = 0.10
populationSize = 100

class EquationBuilder:
    
    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber
        # Create the earliest population at the begining
        self.population = self.makeFirstPopulation()
        
    def makeFirstPopulation(self):
        #TODO create random chromosomes to build the early population, and return it
        operandsCount = (self.equationLength + 1) // 2
        operatorsCount = (self.equationLength - 1) // 2
        operatorsLen = len(self.operators)
        operandsLen = len(self.operands)
        q1 = operandsCount // operandsLen
        q2 = operatorsCount // operatorsLen
        
        #extend the operands if its len is less than opernadsCount
        if operandsCount > operandsLen :
            for i in range(q1) :
                tmpOperands = self.operands.copy()
                self.operands = self.operands + tmpOperands

        #extend the operators if its len is less than operatorsCount
        if operatorsCount > operatorsLen :
            for i in range(q2) :
                tmpOperators = self.operators.copy()
                self.operators = self.operators + tmpOperators

        population = []

        for i in range(populationSize) :
            operands = random.sample(self.operands, operandsCount)
            operators = random.sample(self.operators, operatorsCount)
            chromosome = [None for i in range(self.equationLength)]
            for i in range(operandsCount) :
                chromosome[2 * i] = str(operands[i])
                if i < operandsCount - 1 :
                    chromosome[2 * i + 1] = operators[i]
            population.append(chromosome)
        
        return population

    def mutate(self, chromosome):
        #TODO mutate the input chromosome
        a, b = random.randrange(0, self.equationLength, 2), random.randrange(0, self.equationLength, 2)
        c, d = random.randrange(1, self.equationLength - 1, 2), random.randrange(1, self.equationLength - 1, 2)
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]
        chromosome[c], chromosome[d] = chromosome[d], chromosome[c]
        return chromosome

    def calcFitness(self, chromosome):
        #TODO define the fitness measure here
        try :
            return abs(self.goalNumber - eval(chromosome))
        except SyntaxError :
            return 10 ** 12


    def findEquation(self):
        # Create a new generation of chromosomes, and make it better in every iteration
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            for i in range(populationSize):
                #TODO calculate the fitness of each chromosome
                #TODO return chromosome if a solution is found, else save the fitness in an array
                chromosome = self.population[i]
                fitness = self.calcFitness("".join(chromosome))
                if fitness == 0 :
                    return chromosome
                else :
                    fitnesses.append((fitness, chromosome))

            #TODO find the best chromosomes based on their fitnesses, and carry them directly to the next generation (optional)
            fitnesses.sort(key = lambda fitness : fitness[0])
            carriedChromosomes = []
            for i in range(0, int(populationSize*carryPercentage)):
                carriedChromosomes.append(fitnesses[i][1]) 

            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(self.population[int(populationSize * carryPercentage):])

            # Delete the previous population
            self.population.clear()

            # Create the portion of population that is undergone crossover and mutation
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))
                
            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)
        
    def createCrossoverPool(self, matingPool):
        crossoverPool = []
        for i in range(0, len(matingPool), 2):
            if i == len(matingPool) - 1 :
                crossoverPool.append(matingPool[i])
                break
            if random.random() > crossoverProbability:
                #TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
                crossoverPool.append(matingPool[i])
                crossoverPool.append(matingPool[i + 1])
            else:
                #TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
                tmp_rand = random.randint(0, self.equationLength - 1)
                crossoverPool.append(matingPool[i][:tmp_rand] + matingPool[i + 1][tmp_rand:])
                crossoverPool.append(matingPool[i + 1][:tmp_rand] + matingPool[i][tmp_rand:])
        return crossoverPool

operands = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
operators = ['+', '-', '*']
equationLength = 15
goalNumber = 1234

equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
s_time = time.time()
equation = equationBuilder.findEquation()
e_time = time.time()
print(equation)
print(f'executation time = {e_time - s_time}')