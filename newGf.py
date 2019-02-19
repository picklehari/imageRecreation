import random
import numpy
from PIL import Image

inputPath="test.png"
outputPath="output.png"
length=256
size=length**2
populationSize=5
generations=5

def imageToMatrix(path):
    return numpy.array(Image.open(path),dtype='uint8')


def randomPopulation():
    population=[]
    citizen = [[[0]*4]*length]*length
    for i in range(0,populationSize):
        for c in range(0,length):
            for d in range(0,length):
                citizen[c][d] = [int(random.uniform(0,1)*255) for e in range(4)]
        population.append(citizen)
    return population

def mate(chromsomeA,chromsomeB,position):
    for i in range(position):
        chromsomeA[len-i]=chromsomeB[len-i]    
        chromsomeB[len-i]=chromsomeA[len-i]
    return chromsomeA,chromsomeB