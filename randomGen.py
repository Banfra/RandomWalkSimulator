#Bastien Anfray 8INF802 – Simulation de systèmes
#Partie 1 - Création d'un générateur

from random import random, seed, randrange
from datetime import datetime

def generateSequence(min, max, sequence_size):
    #declaration
    x = []
    y = []
    u = []

    #generate a seed with the current os time
    seed(a=None)

    #This generator is based on linear recurrence with two terms
    #We generate 6 numbers x0,x1,x2,y0,y1,y2
    for i in range(0,3):
        x.append(randrange(4294967086))
        y.append(randrange(4294944442))

    if((x[0] == 0 and x[1] == 0 and x[2] == 0) or (y[0] == 0 and y[1] == 0 and y[2] == 0)):
        generateSequence()

    #We calculate a sequence of numbers based on the 6 pseudo-random ones
    #Then we calculate a number sequence with the two numbers calculated each time
    for i in range(3,sequence_size + 3):
        x.append((1403580 * x[i-2] - 810728 * x[i-3])%4294967087)
        y.append((527612 * y[i-2] - 1370589 * y[i-3])%4294944443)
        u.append(((x[i] - y[i])%(max-min+1) + min))
    return u

