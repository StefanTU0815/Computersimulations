# Imports 
import numpy as np
import matplotlib.pyplot as plt
# 1
# a)
# 1000 Werte
N = 10000
# create nromal distributed like  in the hint
x = np.random.rand(N)

bins = 50
#estimate error with sqrt(N) normaliezed by Nb
hist, edges = np.histogram(x, bins=bins, range=(0,1))
b = edges[1]-edges[0]

#normalize probability density function
pdf = hist/(N*b)
#estimate error with sqrt(N) normaliezed by Nb
yerr = np.sqrt(hist)/(N*b)

centers = (edges[:-1]+edges[1:])/2

# for test proof if the integral is alway 1...
test = np.sum(pdf*b)
print(test)

# for proof, if arround 68% of values within
# one standard deviation from the mean
sigma = np.std(hist)
mean = np.mean(hist)
print("Standarddeviation:" , sigma)
print("Samplemean: ", mean)

# wich bars are inside mean+-sima
inside = np.abs(hist - mean) < sigma
# marmation to bar-number
fraction = np.sum(inside) / len(hist)
print("Percentage within mean+-std: ",fraction*100,"%")

#Plot
plt.bar(centers,pdf,width=b,yerr = yerr)
plt.xlabel("x")
plt.ylabel("pdf")
plt.show()


