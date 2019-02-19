import random
import imageio
import numpy
from PIL import Image

inputPath = "test.png"
outputPath = "output.png"
length = 256
size = 256*256
numberOfAttributes = 3
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
    return numpy.array(Image.open(path),dtype='uint8')


def randomPopulation():
    population=[]
    citizen = [[[0]*numberOfAttributes]*length]*length
    for i in range(0,populationSize):
        for c in range(0,length):
            for d in range(0,length):
                citizen[c][d] = [int(random.uniform(0,1)*255) for e in range(numberOfAttributes)]
        population.append(numpy.array(citizen,dtype='uint8'))
    return population

def fitness(chromosome):
    fitness = 0
    imageToDraw = imageToMatrix(inputPath)
    for i in range(0,length):
        for j in range(length):
            for k in range(numberOfAttributes):
                fitness += abs(int(chromosome[i][j][k])-int(imageToDraw[i][j][k]))
    return fitness

def mutate(chromosome):
    mutationChance = 100
    for i in range(length):
        for j in range(length):
            for k in range(numberOfAttributes):
                if int(random.random()*mutationChance) == 1:
                    chromosome[i][j][k] = random.randrange(0,255)
    return chromosome


def crossover(chromosomeA,chromosomeB):
    position = int(random.random()*length)
    return mate(chromosomeA,chromosomeB,position)

def mate(chromsomeA,chromsomeB,position):
    for i in range(position):
        chromsomeA[(length-1)-i] = chromsomeB[(length-1)-i]    
        chromsomeB[(length-1)-i] = chromsomeA[(length-1)-i]
    return chromsomeA,chromsomeB

def generateImage():
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
            induvidualA = mutate(induvidualA)
            induvidualB = mutate(induvidualB)
            population.append(induvidualA)
            population.append(induvidualB)

    fittestImage = population[0]
    minimumFitness = fitness(population[0])

    for induvidual in population:
        induvidualFitness = fitness(induvidual)
        if induvidualFitness <= minimumFitness:
            fittestImage = induvidual
            minimumFitness = induvidualFitness

        
    outputImage = numpy.array(fittestImage,dtype='uint8')
    outputImage = Image.fromarray(outputImage)
    outputImage.save('output.png')
    return outputImage
        
generateImage()


    
