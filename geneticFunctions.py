import random
import imageio
import numpy
from PIL import Image

inputPath = "test.png"
outputPath = "output.png"
length = 64
size = 64*64
populationSize = 5000
Generations = 50

def weightedChoice(items):
  weight_total = sum((item[1] for item in items))
  n = random.uniform(0, weight_total)
  for item, weight in items:
    if n < weight:
      return item
    n = n - weight
  return item

def imageToMatrix(path):
    return imageio.imread(path)

def cutIntoSingleDimension(imageMatrix):
    return imageMatrix.ravel().tolist()

def rollBackIntoImage(values):
    image =[[0]*length]*length
    matrixCount = 0
    for i in range(size):
        image[matrixCount][size%length] = values
        if size%length == length -1:
            matrixCount+=1
    return image


def randomInteger():
    return int(random.randrange(0,255,1))

def randomPopulation():
    pop = []
    for i in range(populationSize):
        chromosome = [0]*size
        for c in range(0,size):
            chromosome[c] = randomInteger()
        pop.append(chromosome)
    return pop

def fitness(chromosome):
    fitness = 0
    imageToDraw = cutIntoSingleDimension(imageToMatrix(inputPath))
    for i in range(size):
        fitness += abs(chromosome[i]-imageToDraw[i])
    return fitness

def mutate(chromosome):
    chromosomeOutput = [0]*size
    mutationChance = 100
    for i in range(size):
        if int(random.random()*mutationChance) == 1:
            chromosomeOutput[i] = randomInteger()
        else:
            chromosomeOutput[i] = chromosome[i]
    return chromosomeOutput

def crossover(chromosomeA,chromosomeB):
    position = int(random.random()*size)
    return chromosomeA[:position]+chromosomeB[position:],chromosomeB[:position]+chromosomeA[position:]


if __name__ == "__main__":

    population = randomPopulation()
    for generation in range(Generations):
        print("Generation" + str(generation))
        weightedPopulation=[]

        for induvidual in population:
            fitnessValue = fitness(induvidual)

            if fitnessValue == 0:
                pair = induvidual,1.0
            else:
                pair = induvidual,1.0/fitnessValue
        weightedPopulation.append(pair)

        population = []

        for a in range(int(populationSize/2)):
            induvidualA = weightedChoice(weightedPopulation)
            induvidualB = weightedChoice(weightedPopulation)

            induvidualA,induvidualB = crossover(induvidualA,induvidualB)
            population.append(mutate(induvidualA))
            population.append(mutate(induvidualB))

    fittestImage = population[0]
    minimumFitness = fitness(population[0])

    for induvidual in population:
        induvidualFitness = fitness(induvidual)
        if induvidualFitness <= minimumFitness:
            fittestImage = induvidual
            minimumFitness = induvidualFitness

        
    outputImage = numpy.array(rollBackIntoImage(fittestImage))
    outputImage = Image.fromarray(outputImage,"I")
    outputImage.save(outputPath)
    
        



    