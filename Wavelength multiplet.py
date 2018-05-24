import numpy
import scipy.stats
import matplotlib.pyplot as plt
#=====================================================================================================================#
def intensity(s,mu,sigma):
    value = scipy.stats.norm.pdf(s,mu,sigma)
    return value

def d_hkl(h,k,l,lattice_param):
    d = []
    for i in range(0,len(h)):
        d.append(lattice_param/numpy.sqrt(h[i]**2 + k[i]**2 + l[i]**2))
    return d

def peak_posn_s(lambdas,h,k,l,lattice_param):
    th_lambda = []
    for j in range(0,len(lambdas)):
        th_d = []
        for i in range(0,len(d_hkl(h,k,l,lattice_param))):
            th_d.append(2*numpy.arcsin(lambdas[j]/(2*(d_hkl(h,k,l,lattice_param)[i]))))
            #print(th_d)
        th_lambda.append(th_d)
        #print(th_lambda)
    twoTheta = numpy.deg2rad(numpy.asarray(th_lambda))
    value = []
    for i in range (0,len(lambdas)):
        value.append(2*numpy.sin(twoTheta[i]/2)/lambdas[i])
    return numpy.asarray(value)

def addition(lambdas,sigmas,peak_weight,h,k,l,lattice_param,x):
    value = []
    for j in range (0,len(h)):
        sum = 0
        for i in range(0,len(lambdas)):
            sum = sum + intensity(x,peak_posn_s(lambdas,h,k,l,lattice_param)[i][j],sigmas[i])[i]*peak_weight[i]
        value.append(sum)
    return numpy.asarray(value)

#=====================================================================================================================#

def main():
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
    #print(peak_posn_s(lambdas,h,k,l,lattice_param))
    x = numpy.arange(0,2/lambdas[0],0.001)
    for j in range(0,len(h)):
        for i in range(0, len(lambdas)):
            plt.plot(x, intensity(x, peak_posn_s(lambdas,h,k,l,lattice_param)[i][j], sigmas[i]))
    print(len(x))
    print(len(addition(lambdas, sigmas, peak_weight, h, k, l, lattice_param, x)))
    #plt.plot(x, addition(lambdas, sigmas, peak_weight, h, k, l, lattice_param, x))
    plt.show()
    return

main()