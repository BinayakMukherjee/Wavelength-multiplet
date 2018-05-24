import numpy
import matplotlib.pyplot as plt
import scipy.stats

def intensity(s,mu,sigma):
    value = scipy.stats.norm.pdf(s,mu,sigma)
    return value
def total_intensity(x,lambdas,h,k,l,lattice_param,peak_weight):
    value = 0
    for i in range (0,len(lambdas)):
        value = value + intensity(x,peak_posn_s(lambdas,h,k,l,lattice_param)[i],sigmas[i])*peak_weight[i]
    return value

def peak_posn_s(lambdas,h,k,l,lattice_param):
    d_hkl = (lattice_param/numpy.sqrt(h**2 + k**2 + l**2))
    twoTheta = []
    for i in range(0, len(lambdas)):
        twoTheta.append(2*numpy.arcsin(lambdas[i]/(2*(d_hkl))))
    value = (numpy.rad2deg(twoTheta))
    print(value)
    #twoTheta_rad = numpy.deg2rad(numpy.asarray(twoTheta))
    return value

def plot(lambdas,x,h, k, l, lattice_param,peak_weight):
    for i in range(0, len(lambdas)):
        plt.plot(x, intensity(x, peak_posn_s(lambdas, h, k, l, lattice_param)[i], sigmas[i]) * peak_weight[i])
    plt.plot(x, total_intensity(x, lambdas, h, k, l, lattice_param, peak_weight))
#=====================================================================================================================#
lattice_param = 3.62
hkl = open("hkl.txt").readlines()
h = []
k = []
l = []
for i in range(0, len(hkl)):
    row = (hkl[i].split(" "))
    h.append(int(row[0]))
    k.append(int(row[1]))
    l.append(int(row[2]))

wavelengths = open("wavelengths.txt").readlines()
lambdas = []
peak_weight = []
sigmas = []
for i in range(0, len(wavelengths)):
    row = (wavelengths[i].split(" "))
    lambdas.append(float(row[0]))
    peak_weight.append(float(row[1]))
    sigmas.append(float(row[2]))

x = numpy.arange(0,180,0.001) #2/lambdas[0]
for i in range(0,len(h)):
    plot(lambdas,x,h[i],k[i],l[i],lattice_param,peak_weight)

#plt.plot(x,intensity(x,5,2)*0.336)

plt.show()