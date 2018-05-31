import numpy
import matplotlib.pyplot as plt
import scipy.stats
#======================================================================================================================#
def intensity(s,mean,FWHM):
    value = 0.5*FWHM/(numpy.pi*((s-mean)**2 + (0.5*FWHM)**2))
    return value

def total_intensity(x,lambdas,h,k,l,lattice_param,peak_weight):
    value = 0
    for i in range (0,len(lambdas)):
        value = value + intensity(x,peak_posn_s(lambdas,h,k,l,lattice_param)[i],FWHM)*peak_weight[i]
    return value

def peak_posn_s(lambdas,h,k,l,lattice_param):
    twoTheta = []
    for i in range(0, len(lambdas)):
        twoTheta.append(2*numpy.arcsin(lambdas[i]*((numpy.sqrt(h**2 + k**2 + l**2))/(2*lattice_param))))
    print(numpy.rad2deg(twoTheta))
    #value = (numpy.rad2deg(twoTheta))
    value = []
    for j in range(0,len(lambdas)):
        a = 2 * numpy.sin(twoTheta[j] / 2)
        #print(a)
        b = lambdas[j]
        #print(b)
        value.append(a/b)
    print(value)
    return value

def plot(lambdas,x,h, k, l, lattice_param,peak_weight):
    for i in range(0, len(lambdas)):
        plt.plot(x, intensity(x, peak_posn_s(lambdas, h, k, l, lattice_param)[i], FWHM) * peak_weight[i])
    plt.plot(x, total_intensity(x, lambdas, h, k, l, lattice_param, peak_weight))
#======================================================================================================================#
lattice_param = 3.571
hkl = open("hkl.txt").readlines()
h = []
k = []
l = []
for i in range(0, len(hkl)):
    row = (hkl[i].split(" "))
    h.append(int(row[0]))
    k.append(int(row[1]))
    l.append(int(row[2]))
FWHM = 0.0025

wavelengths = open("wavelengths.txt").readlines()
lambdas = []
peak_weight = []
for i in range(0, len(wavelengths)):
    row = (wavelengths[i].split(" "))
    lambdas.append(float(row[0]))
    peak_weight.append(float(row[1]))
print(lambdas)
x = numpy.arange(0,2,0.001)
for i in range(0,len(h)):
    plot(lambdas,x,h[i],k[i],l[i],lattice_param,peak_weight)

#plt.plot(x,intensity(x,5,2)*0.336)

plt.show()