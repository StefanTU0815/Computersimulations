# Imports 
import numpy as np
import matplotlib.pyplot as plt
# Activate parts of the excersice
one_a   =   False
one_b   =   False
one_c   =   False
one_d   =   False
two     =   False
three_b =   False
three_c =   False
four_a  =   False
four_b  =   True
four_c  =   True

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

#sample half gaussian with modified function...
def rejection_half_gaussian(N, seed=None):
    #seed if defined
    if seed is not None:
        np.random.seed(seed)

    # lambdas function for easyer code
    f = lambda x: np.sqrt(2/np.pi)*np.exp(-x**2/2)
    g = lambda x: np.exp(-x)

    # cread samples like in 2
    x = sample_exponential(N=N)

    #calc c from a
    c = np.sqrt(2/np.pi)*np.exp(0.5)

    # use a list for all accepted values
    accepted = []

    #itterate through N random numbers
    i=0
    cnt_not_acc = 0
    for i in range(N):
        u = np.random.rand()
        # if criteria fullfillt accept number
        if u <= f(x[i]) / (c * g(x[i])):
            accepted.append(x[i])
        else:
            cnt_not_acc +=1
    
    accrate = len(accepted)/ N
    samples = accepted

    return samples, accrate

# same as above but with other samplingfunction g
def rejection_half_gaussian_2(N, seed=None):
    if seed is not None:
        np.random.seed(seed)

    f = lambda x: np.sqrt(2/np.pi) * np.exp(-x**2 / 2)
    g = lambda x: 1 / (1 + x)**2

    # cread samples like in 2
    u = np.random.rand(N)
    x = u / (1 - u)

    #calc c from a
    c = 4 * np.sqrt(2/np.pi) * np.exp(-0.5)

    # use a list for all accepted values
    accepted = []

    #itterate through N random numbers
    i=0
    cnt_not_acc = 0
    for i in range(N):
        u = np.random.rand()
        # if criteria fullfillt accept number
        if u <= f(x[i]) / (c * g(x[i])):
            accepted.append(x[i])
        else:
            cnt_not_acc +=1
    
    accrate = len(accepted)/ N
    samples = accepted

    return samples, accrate

#1_a -----------------------------------------------------------------
# for test proof if the integral is alway 1 (CDF)
if one_a:
    hist, edges, yerr, centers, pdf, b = create_histogram (N = 1000, N_bins=50, seed = 5)

    # for test proof if the integral is alway 1 (CDF)
    cdf = np.sum(pdf*b)
    print("-----------------------------------------------------")
    print("results for a")
    print("the Integal over PDF = ", cdf)


    plt.bar(centers,pdf,width=b)
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
        print("mean: ", mean)

        # wich bars are inside mean+-sima
        inside = np.abs(hist - mean) < sigma
        # marmation to bar-number
        fraction = np.sum(inside) / len(hist)
        print("Percentage within mean+-std: ",fraction*100,"%")

        plt.figure()
        plt.bar(centers,pdf,width=b,yerr = yerr)
        plt.xlabel("x")
        plt.ylabel("pdf")
        plt.show(block=False)
        plt.title(f"N = {N[i]} | within 1sigam: {fraction*100:.2f}%")
        plt.grid()
        plt.show(block=False)
    plt.show()
#c ------------------------------------------------------------------
#create M histogramms, check the 6. bin of 10
if one_c or one_d:
    M = 10000
    N_bins = 10
    N = 1000
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
    print("determined value", kt)
    print("comparevalue", 1.0/N)
# results are very similar :)


#2---------------------------------------------------------------------
#Inverse transformation sampling
if two:
    N = 10000
    #use function of part two
    samples = sample_exponential(N, seed=42)

    # Histogramm
    plt.hist(samples, bins=50, density=True, alpha=0.6, label="Samples")

    # echte PDF
    x = np.linspace(0, 5, 100)
    pdf = np.exp(-x)

    plt.plot(x, pdf, 'r-', label="exp(-x)")
    plt.legend()
    plt.title("Exponential distribution via inverse transform")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.show()

#3-----------------------------------------------------------------------
#b Rejection sampling
if three_b:
    N = 10000
    N_bins = 100
    samples, acc_rate = rejection_half_gaussian(N, seed=42)

    print("Acceptance rate:", acc_rate)

    #Normalization for the histogramm 
    hist, edges = np.histogram(samples, bins=N_bins)
    b = edges[1]-edges[0]
    pdf = hist/(len(samples)*b)
    centers = (edges[:-1]+edges[1:])/2
    print(np.sum(pdf *b))

    # For Plot of the funktion to campare
    x_plot = np.linspace(0, 4, 400)
    f_plot = np.sqrt(2/np.pi) * np.exp(-x_plot**2 / 2)

    plt.bar(centers,pdf,width=b)
    plt.plot(x_plot, f_plot,'r-', label="target pdf f(x)")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.title(f"acceptance rate = {acc_rate:.3f}")
    plt.grid()
    plt.legend()
    plt.show()

#c--------------------------------------------------------------------------
if three_c:
    N = 10000
    samples1, rate1 = rejection_half_gaussian(N, seed=42)
    samples2, rate2 = rejection_half_gaussian_2(N, seed=42)

    print(f" acceptance rate = {rate1:.3f}")
    print(f" acceptance rate = {rate2:.3f}")

    x_plot = np.linspace(0, 4, 400)
    f_plot = np.sqrt(2/np.pi) * np.exp(-x_plot**2 / 2)
    plt.hist(samples1, bins=50, density=True, alpha=0.5, label="g(x) = exp(-x)")
    plt.hist(samples2, bins=50, density=True, alpha=0.5, label="g(x) = (1/(1+x)^2)")
    plt.plot(x_plot, f_plot, 'r-', label="target f(x)")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.title("Comparison of rejection sampling")
    plt.grid()
    plt.legend()
    plt.show()

#4-----------------------------------------------------------------------
#a Velocity distribution
if four_a:
    N = 100000
    N_bins = 50

    # use half guassian function from 3b
    sx, rate_x = rejection_half_gaussian(N, seed=1)
    sy, rate_y = rejection_half_gaussian(N, seed=2)
    sz, rate_z = rejection_half_gaussian(N, seed=3)

    # convert the lists of the function to arry
    # for easier handling
    sx = np.array(sx)
    sy = np.array(sy)
    sz = np.array(sz)
    # because of the halfside gaussian add a random sign
    vx = sx * np.random.choice([-1, 1], size=len(sx))
    vy = sy * np.random.choice([-1, 1], size=len(sy))
    vz = sz * np.random.choice([-1, 1], size=len(sz))

    # all v-array have to be equal long
    N_acc = min(len(vx), len(vy), len(vz))
    vx = vx[:N_acc]
    vy = vy[:N_acc]
    vz = vz[:N_acc]
    print("number of accseptet calues: ",len(vz))

    # calc betrag of v
    v = np.sqrt(vx**2 + vy**2 + vz**2)

    # criate a histogram for c
    hist, edges = np.histogram(v, bins=N_bins, range=(0, np.max(v)))
    b = edges[1] - edges[0]
    pdf = hist / (len(v) * b)
    centers = (edges[:-1] + edges[1:]) / 2

    # calc maxwell bolzmann for comparence
    v_plot = np.linspace(0, np.max(v), 400)
    p_function = np.sqrt(2/np.pi) * v_plot**2 * np.exp(-v_plot**2 / 2)

    plt.bar(centers, pdf, width=b, alpha=0.6, label="sampled pdf")
    plt.plot(v_plot, p_function, 'r-', label="calculated pdf")
    plt.xlabel("v")
    plt.ylabel("pdf")
    plt.title("Velocity distribution")
    plt.grid()
    plt.legend()
    plt.show()

if four_b:
    N = 100000
    N_bins = 40

    generators = [
        ("Generator 1 (exp)", rejection_half_gaussian),
        ("Generator 2 (1/(1+x)^2)", rejection_half_gaussian_2)
    ]

    for name, generator in generators:

        # --- generate 3 velocity components ---
        sx, _ = generator(N, seed=42)
        sy, _ = generator(N)
        sz, _ = generator(N)

        sx = np.array(sx)
        sy = np.array(sy)
        sz = np.array(sz)

        # random signs → full Gaussian
        vx = sx * np.random.choice([-1, 1], size=len(sx))
        vy = sy * np.random.choice([-1, 1], size=len(sy))
        vz = sz * np.random.choice([-1, 1], size=len(sz))

        # equal length
        N_acc = min(len(vx), len(vy), len(vz))
        vx = vx[:N_acc]
        vy = vy[:N_acc]
        vz = vz[:N_acc]

        # speed
        v = np.sqrt(vx**2 + vy**2 + vz**2)

        # histogram
        hist, edges = np.histogram(v, bins=N_bins, range=(0, np.max(v)))
        b = edges[1] - edges[0]
        centers = (edges[:-1] + edges[1:]) / 2

        pdf = hist / (len(v) * b)
        yerr = np.sqrt(hist) / (len(v) * b)   # frequentist error

        # theory
        v_plot = np.linspace(0, np.max(v), 400)
        p_function = np.sqrt(2/np.pi) * v_plot**2 * np.exp(-v_plot**2 / 2)

        # plot
        plt.figure()
        plt.bar(centers, pdf, width=b, yerr=yerr, alpha=0.6, capsize=3, label=name)
        plt.plot(v_plot, p_function, 'r-', label="Maxwell-Boltzmann")
        plt.xlabel("v")
        plt.ylabel("pdf")
        plt.title(name)
        plt.grid()
        plt.legend()
        plt.show(block = False)
    plt.show()

if four_c:
    N = 100000
    N_bins = 40

    # --- generate 3 velocity components ---
    sx, _ = rejection_half_gaussian(N, seed=42)
    sy, _ = rejection_half_gaussian(N)
    sz, _ = rejection_half_gaussian(N)
    sx = np.array(sx)
    sy = np.array(sy)
    sz = np.array(sz)
    # random signs → full Gaussian
    vx = sx * np.random.choice([-1, 1], size=len(sx))
    vy = sy * np.random.choice([-1, 1], size=len(sy))
    vz = sz * np.random.choice([-1, 1], size=len(sz))
    # equal length
    N_acc = min(len(vx), len(vy), len(vz))
    vx = vx[:N_acc]
    vy = vy[:N_acc]
    vz = vz[:N_acc]
    # speed
    v = np.sqrt(vx**2 + vy**2 + vz**2)
    # histogram
    hist, edges = np.histogram(v, bins=N_bins, range=(0, np.max(v)))
    b = edges[1] - edges[0]
    centers = (edges[:-1] + edges[1:]) / 2

    pdf = hist / (len(v) * b)
    #yerr = np.sqrt(hist) / (len(v) * b) 
    # Bayesian estimate
    p_mean = (hist + 1) / (len(v) + N_bins)

    # variance
    p_var = p_mean * (1 - p_mean) / (len(v) + N_bins + 2)

    pdf = p_mean / b
    yerr = np.sqrt(p_var) / b

    # theory
    v_plot = np.linspace(0, np.max(v), 400)
    p_function = np.sqrt(2/np.pi) * v_plot**2 * np.exp(-v_plot**2 / 2)

    # plot
    plt.figure()
    plt.bar(centers, pdf, width=b, yerr=yerr, alpha=0.6, capsize=3, label="Generator 1 (exp)")
    plt.plot(v_plot, p_function, 'r-', label="Maxwell-Boltzmann")
    plt.xlabel("v")
    plt.ylabel("pdf")
    plt.title('Errors by Baysian analysis')
    plt.grid()
    plt.legend()
    plt.show(block = False)
    plt.show()
    