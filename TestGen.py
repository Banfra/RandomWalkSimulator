#Bastien Anfray 8INF802 – Simulation de systèmes
#Partie 2 - Test du générateur

import randomGen
import numpy as np
from scipy.stats import chisquare, chi2_contingency

#initialisation
results = []
categories = []
probs = []

#we launch 2 dices 1000 times and calculate the sum of the two values
for i in range(0,1000):
    dices = randomGen.generateSequence(1,6,2)
    results.append(dices[0] + dices[1])

#We regroup the number of times we have each value and calculate their probability
i = 2
while(i != 13):
    #We regroup 2 and 3 together and 11 and 12 together because of the normal distribution
    if i == 2 or i == 11:
        count = results.count(i) + results.count(i+1)
        categories.append(count)
        probs.append(count/1000)
        #print(i, i+1, categories[len(categories)-1])
        i = i+1
        
    else:
        count = results.count(i)
        categories.append(count)
        probs.append(count/1000)
        #print(i, categories[len(categories)-1])

    i = i+1

print(categories)

#We use the chisquare test to compare the probabilities observed with the probabilities expected
print(chisquare(probs, f_exp=[1/12,1/12,1/9,5/36,1/6,5/36,1/9,1/12,1/12], ddof= 6)) #1/36 + 1/18 = 1/12
#Here we have a p value near 1, it means that the values are almost the same everytime

#I also tested with chi2_contingency
c, p, dof, expected = chi2_contingency(categories)
print(c, p, dof, expected)
#Result : 0.0 1.0 0 [0.079 0.084 0.113 0.145 0.166 0.138 0.113 0.094 0.068]