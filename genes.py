import random
import decimal

#This program executes a genetic algorithm by creating a population of
#genomes made up of 1's and 0's of a given size and crossing and mutating
#them until an optimal genome of all 1's is found. Data is reported into a file

# creates string of 0s and 1s which represents a genome
def randomGenome(length):
    gene_string = ''
    i = 0
    #loop in order to create genome with requested length
    while i < length:
        #add random 0 or 1 to end of string
        gene_string = gene_string + str(random.randint(0, 1))
        i+=1
    
    return gene_string
    
def makePopulation(size, length):
    #list to strore the genomes
    pop = []
    i = 0
    #iterate through requested number of genomes
    while i < size:
        #call reandomGenome func 
        currentGenome = randomGenome(length)
        #add genome to list
        pop.append(currentGenome)
        i+=1
        
    return pop

def fitness(gene_string):
    fit = 0
    #iterate through genome as a string
    for i in str(gene_string):
        #convert to int then add to fitness sum
        num = int(i)
        fit += num
        
    return fit

def evaluateFitness(population):
    #values for most fit and total fitness(used for avg)
    high = 0
    total = 0
    
    #iterate through entire population
    for i in population:
        current = fitness(i)
        #sum up total 1's
        total += current
        #if current genome is most fit then update
        if current > high:
            high = current
           
    #calculate average as a decimal
    avg = decimal.Decimal(total)/decimal.Decimal(len(population))

    return high, avg

def crossover(genome1, genome2):
    #randomly generate cut point within genome length
    cut = random.randint(1, len(genome1))
    
    #creates two new genome strings
    #mut1 starts with genome 1 then switches to genome 2 at a random cut
    mut1 = genome1[0:cut] + genome2[cut:len(genome1)]
    #mut2 starts with genome 2 then switches to genome 1 at the same random cut
    mut2 = genome2[0:cut] + genome1[cut:len(genome1)]
    
    return mut1, mut2
        
    
def mutate(genome, mutationRate): 
    #generate random decimal and check if its below the provided mutationRate
    if (decimal.Decimal(random.randrange(0, 999))/1000 < mutationRate):
        #randomly select a bit from the genome to alter
        flipBit = random.randint(0, len(genome)-1)
        #check the selected bit and flip
        if (genome[flipBit] == '0'):
            genome = genome[0:flipBit] + '1' + genome[flipBit + 1:len(genome)]
        else:
            genome = genome[0:flipBit] + '0' + genome[flipBit + 1:len(genome)]
            
    return genome
        
        
#impliments roulette wheel selection by choosing a random genome 
#with probability proportional to each  fitness 
def select(population):
    total = 0
    #sum up total fitness sum of population
    for i in population:
        total += fitness(i)
        
    #generate random number from 0-total fitness sum in population
    ranNum = random.randint(0, total-1)
           
    sumFit = 0
    #iterate through entire population
    
    count = 0
    for i in population:
        sumFit += fitness(i)
        
        #check if total 1's is above
        #if so then we select that genome 
        if ranNum < sumFit:
            return i, count
        
        count+=1
        
    
def runGA(populationSize, crossoverRate, mutationRate, logFile=""):
    genomeLength = 10
    currentAvg = 0
    
    generationCount = 1
    
    print("Population size: " + str(populationSize))
    print("Genome Length: " + str(genomeLength))
    
    #create population
    pop = makePopulation(populationSize, genomeLength)
    
    #boolean to check if the optimum genome has been found
    found = -1
    
    #loop until there is a genome with all 1's
    while True:
    
        #loop to prevent incest - make sure the same genome is not crossed
        while True:  
            #select two geneomes(fitness proportionate) and store position so 
            #the parent can be removed and replaced by offspring
            gen1, position1 = select(pop)
            gen2, position2 = select(pop)
            if(gen1 != gen2):  
                break
                
        #remove parents to make room for children
        del(pop[position1])
        if position1 < position2:
            position2 -=1
        del(pop[position2])

        #create new offspring
        offspring1 = gen1
        offspring2 = gen2

        #using crossover rate, decide whether to cross the pairs 
        if (decimal.Decimal(random.randrange(0, 999))/1000 < crossoverRate):
            offspring1, offspring2 = crossover(gen1, gen2)

        #add new offspring to population
        pop.append(offspring1)
        pop.append(offspring2)

        #iterate through population and mutate based on rate
        cnt = 0
        for i in pop:
            pop[cnt] = mutate(i, mutationRate)
            cnt+=1

        #book keep avg and best
        high, avg = evaluateFitness(pop)

        #create new txt file(a for append) and write gen stats to the file
        f = open(logFile, "a")
        info = "Generation " + str(generationCount) + '\n' + "Average: " + str(avg) + "  High: " + str(high) + '\n'
         
        infoFile = str(generationCount) + "    Average: " + str(avg) + "  High: " + str(high) + '\n'
        
        #only bookkeep if the avg increases
        if avg > currentAvg:
            currentAvg = avg
            f.write(infoFile)
            print(info)
            generationCount+=1
        
        #iterate through population and check if there exists 
        #a genome with all 1's
        for i in pop:
            if fitness(i) == genomeLength:
                print(info)
                f.write(infoFile)
                found = 1
                break
            
        #if genome found then break from main loop
        if found == 1:
            f.close()
            break
    
    
runGA(100, .7, .001,  "generations.txt")



