# Imports 
import numpy as np
import matplotlib.pyplot as plt
# 1
# a)
# 1000 Werte
N = 5000
# create nromal distributed like  in the hint
x = np.random.rand(N)

bins = 20 
#estimate error with sqrt(N) normaliezed by Nb
hist, edges = np.histogram(x, bins=bins, range=(0,1))
b = edges[1]-edges[0]

#normalize probability density function
pdf = hist/(N*b)
#estimate error with sqrt(N) normaliezed by Nb
yerr = np.sqrt(hist)/(N*b)

centers = (edges[:-1]+edges[1:])/2

plt.bar(centers,pdf,width=b,yerr = yerr)
plt.xlabel("x")
plt.ylabel("pdf")
plt.show()

# for test proof if the integral is alway 1...
test = np.sum(pdf*b)
print(test)

# for proof, if arround 68% of values within
# one standard deviation from the mean
print()

