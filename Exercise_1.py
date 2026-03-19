# Imports 
import numpy as np
import matplotlib.pyplot as plt
one_a = False
one_b = False
one_c = False
one_d = False
two = False
three_b = False
three_c = False
four_a = True

# Define a Function to creat a Histogramm with estimatet errorbars
def create_histogram (N, N_bins,seed):
    # create nromal distributed like  in the hint
    # if a seed is given -> use it 
    if seed is not None:
        np.random.seed(seed)

    x = np.random.rand(N)

    #estimate error with sqrt(N) normaliezed by Nb
    hist, edges = np.histogram(x, bins=N_bins, range=(0,1))
    b = edges[1]-edges[0]

    #normalize probability density function
    pdf = hist/(N*b)
    #estimate error with sqrt(N) normaliezed by Nb
    yerr = np.sqrt(hist)/(N*b)

    centers = (edges[:-1]+edges[1:])/2
    # retrun of crated histogram
    return hist, edges, yerr, centers, pdf, b

# Define a function for sampling a exponential function
def sample_exponential(N, seed=None):
    if seed is not None:
        np.random.seed(seed)

    u = np.random.rand(N)
    x = -np.log(u)

    return x

#functiondefinietion fo ra half guassian
def rejection_half_gaussian(N, seed=None):
    if seed is not None:
        np.random.seed(seed)

    accepted = []
    n_trials = 0

    while len(accepted) < N:
        # Vorschlag aus g(x)=exp(-x)
        x = -np.log(np.random.rand())
        u = np.random.rand()

        # Akzeptanzwahrscheinlichkeit
        accept_prob = np.exp(-0.5 * (x - 1)**2)

        if u <= accept_prob:
            accepted.append(x)

        n_trials += 1

    accepted = np.array(accepted)
    acceptance_rate = N / n_trials
    return accepted, acceptance_rate

#sample half gaussian with modified function...
def rejection_half_gaussian_lambda(N, lam=1.0, seed=None):
    if seed is not None:
        np.random.seed(seed)

    c = np.sqrt(2/np.pi) / lam * np.exp(lam**2 / 2)

    accepted = []
    n_trials = 0

    while len(accepted) < N:
        # x ~ g_lambda(x) = lam * exp(-lam x)
        x = -np.log(np.random.rand()) / lam
        u = np.random.rand()

        f = np.sqrt(2/np.pi) * np.exp(-x**2 / 2)
        g = lam * np.exp(-lam * x)

        if u <= f / (c * g):
            accepted.append(x)

        n_trials += 1

    accepted = np.array(accepted)
    acceptance_rate = N / n_trials
    return accepted, acceptance_rate, c

#a -----------------------------------------------------------------
# for test proof if the integral is alway 1 (CDF)
if one_a:
    hist, edges, yerr, centers, pdf, b = create_histogram (N = 1000, N_bins=50, seed = 5)


    cdf = np.sum(pdf*b)
    print("-----------------------------------------------------")
    print("results for a")
    print("the Integal over PDF = ", cdf)


    plt.bar(centers,pdf,width=b,yerr = yerr)
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.show()

# b ---------------------------------------------------------------
# for proof, if arround 68% of values within
# one standard deviation from the mean
# to this for 2 different N
if one_b:
    N = [100,1000]
    print("-----------------------------------------------------")
    print("results for b")
    for i in range(2):
        hist, edges, yerr, centers, pdf, b = create_histogram (N = N[i], N_bins=50, seed = 5)
        print("Für N = ",N[i],":")
        sigma = np.std(hist)
        mean = np.mean(hist)
        print("Standarddeviation:" , sigma)
        print("Samplemean: ", mean)

        # wich bars are inside mean+-sima
        inside = np.abs(hist - mean) < sigma
        # marmation to bar-number
        fraction = np.sum(inside) / len(hist)
        print("Percentage within mean+-std: ",fraction*100,"%")

        plt.bar(centers,pdf,width=b,yerr = yerr)
        plt.xlabel("x")
        plt.ylabel("pdf")
        plt.show(block=False)
        plt.title(f"N = {N[i]} | within 1σ: {fraction*100:.2f}%")
        plt.grid()
        plt.show()

#c ------------------------------------------------------------------
#create M histogramms, check the 6. bin of 10
if one_c or one_d:
    M = 10000
    N_bins = 10
    N = 10000
    samples = np.empty(M)
    for i in range(M):
        hist,_,_,_,_,_ = create_histogram (N = N, N_bins=N_bins, seed = None)
        samples[i] = hist[5]
    print("samples",samples)
    #now build a histogramm the bins of hist_M
    hist, edges = np.histogram(samples, bins=20, range=(np.min(samples),np.max(samples)))
    b = edges[1]-edges[0]
    centers = (edges[:-1]+edges[1:])/2
    #print the length of the hist to check
    print(len(hist))
    print("hist:", hist)
    #normalize probability density function
    pdf = hist/(M*b)
    #estimate error with sqrt(N) normaliezed by Nb
    yerr = np.sqrt(hist)/(M*b)
    centers = (edges[:-1]+edges[1:])/2
    #plot this distribution
    plt.bar(centers,pdf,width=b,yerr = yerr)
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.show(block=False)
    plt.title("M = 1000")
    plt.grid()
    plt.show()

#d--------------------------------------------------------------------
#consider N_i particles in the colume V_i corresponding to bar i in 
#the histogram, calc the isothermal comprssibilit in units k_B T 
#it needs one_c, so this is also activatied with one_d
if one_d:
    #take samples from 1c as Ni
    Ni_mean = np.mean(samples)
    var_Ni = np.mean(samples**2)-np.mean(samples)**2
    #use with of bins from c 
    vi = 1.0 / N_bins
    # V must be one, calculation just for checking
    V = sum(pdf)*b
    print("Volumelemts: ", vi)
    print("Whole volume V:", V)
    kt = vi*(var_Ni/(Ni_mean**2))
    print(kt)
    print(1.0/N)
# results are very similar :)


#2---------------------------------------------------------------------
#Inverse transformation sampling
if two:
    N = 10000
    samples = sample_exponential(N, seed=42)

    # Histogramm
    plt.hist(samples, bins=50, density=True, alpha=0.6, label="Samples")

    # echte PDF
    x = np.linspace(0, 5, 100)
    pdf = np.exp(-x)

    plt.plot(x, pdf, 'r-', label="exp(-x)")
    plt.legend()
    plt.title("Exponential distribution via inverse transform")
    plt.show()

#3-----------------------------------------------------------------------
#b Rejection sampling
if three_b:
    N = 10000
    samples, acc_rate = rejection_half_gaussian(N, seed=42)

    print("Acceptance rate:", acc_rate)

    # Histogramm
    x_plot = np.linspace(0, 4, 400)
    f_plot = np.sqrt(2/np.pi) * np.exp(-x_plot**2 / 2)

    plt.hist(samples, bins=50, density=True, alpha=0.6, label="accepted samples")
    plt.plot(x_plot, f_plot, label="target pdf f(x)")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.title(f"Half Gaussian via rejection sampling\nacceptance rate = {acc_rate:.3f}")
    plt.grid()
    plt.legend()
    plt.show()

#c--------------------------------------------------------------------------
if three_c:
    N = 10000
    samples1, rate1, c1 = rejection_half_gaussian_lambda(N, lam=1.0, seed=42)
    samples2, rate2, c2 = rejection_half_gaussian_lambda(N, lam=0.5, seed=42)

    print(f"lambda = 1.0: c = {c1:.3f}, acceptance rate = {rate1:.3f}")
    print(f"lambda = 0.5: c = {c2:.3f}, acceptance rate = {rate2:.3f}")

    x_plot = np.linspace(0, 4, 400)
    f_plot = np.sqrt(2/np.pi) * np.exp(-x_plot**2 / 2)

    plt.hist(samples1, bins=50, density=True, alpha=0.5, label=f"lambda=1.0, rate={rate1:.3f}")
    plt.hist(samples2, bins=50, density=True, alpha=0.5, label=f"lambda=0.5, rate={rate2:.3f}")
    plt.plot(x_plot, f_plot, 'k-', label="target f(x)")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.title("Comparison of rejection sampling envelopes")
    plt.grid()
    plt.legend()
    plt.show()


if four_a:
    