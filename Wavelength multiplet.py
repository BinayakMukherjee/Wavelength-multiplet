import numpy
import matplotlib.pyplot as plt
import scipy.interpolate
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
        twoTheta.append(2*numpy.arcsin(lambdas[i]*((numpy.sqrt(numpy.asarray(h)**2 + numpy.asarray(k)**2 + numpy.asarray(l)**2))/(2*lattice_param))))
    #print(numpy.rad2deg(twoTheta))
    #value = (numpy.rad2deg(twoTheta))
    value = []
    for j in range(0,len(lambdas)):
        a = 2 * numpy.sin(twoTheta[j] / 2)
        #print(a)
        b = lambdas[j]
        #print(b)
        value.append(a/b)
    #print(value)
    return value

def plot(lambdas,x,h, k, l, lattice_param,peak_weight):
    for i in range(0, len(lambdas)):
        plt.plot(x, intensity(x, peak_posn_s(lambdas, h, k, l, lattice_param)[i], FWHM) * peak_weight[i])
    plt.plot(x, total_intensity(x, lambdas, h, k, l, lattice_param, peak_weight))

def XRD_dataset(lambdas,x,h, k, l, lattice_param,peak_weight):
    s = x
    I_s = total_intensity(x, lambdas, h, k, l, lattice_param, peak_weight)
    value  = []
    for i in range (0,len(x)):
        value.append([s[i],I_s[i]])
    return I_s

def s_to_2th(lambdas,x,h, k, l, lattice_param,peak_weight):
    twoTheta = []
    for i in range (0,len(lambdas)):
        twoTheta.append(numpy.rad2deg(2*numpy.arcsin((x*lambdas[i])/2)))
        #print(numpy.rad2deg(2*numpy.arcsin((x*lambdas[i])/2)))
    return (twoTheta)

def plot2(lambdas,x,h, k, l, lattice_param,peak_weight):
    var = 0
    for i in range(0, len(lambdas)):
        plt.plot(s_to_2th(lambdas, x, h, k, l, lattice_param,peak_weight)[i],XRD_dataset(lambdas,x,h, k, l,
                                                                            lattice_param,peak_weight) * peak_weight[i])

def interpolate(lambdas,h, k, l, lattice_param,peak_weight,x_val):
    value = 0
    for i in range (0,len(lambdas)):
        x_axis = s_to_2th(lambdas, x, h, k, l, lattice_param,peak_weight)[i]
        y_axis = XRD_dataset(lambdas, x, h, k, l,lattice_param,peak_weight) * peak_weight[i]
        y_interp = scipy.interpolate.interp1d(x_axis,y_axis)
        #print(x_val)
        value = value + y_interp(x_val)
    return value

def plot_tot(lambdas,h, k, l, lattice_param,peak_weight):
    x = numpy.arange(0,150,0.001)
    plt.plot(x,interpolate(lambdas,h, k, l, lattice_param,peak_weight,x))
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
FWHM = 0.001

wavelengths = open("wavelengths.txt").readlines()
lambdas = []
peak_weight = []
for i in range(0, len(wavelengths)):
    row = (wavelengths[i].split(" "))
    lambdas.append(float(row[0]))
    peak_weight.append(float(row[1]))
#print(lambdas)
x = numpy.arange(0,1.29,0.0001)

for i in range(0,len(h)):
    plot(lambdas,x,h[i],k[i],l[i],lattice_param,peak_weight)
plt.show()


for i in range(0,len(h)):
    plot2(lambdas,x,h[i],k[i],l[i],lattice_param,peak_weight)
    plot_tot(lambdas,h[i], k[i], l[i], lattice_param,peak_weight)
plt.show()
#print(XRD_dataset(lambdas,x,h, k, l, lattice_param,peak_weight))
#print(s_to_2th(lambdas,x,h, k, l, lattice_param,peak_weight))