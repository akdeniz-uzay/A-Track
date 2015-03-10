# Hough Transform Algorithm

import math
import numpy as np
import matplotlib.pyplot as plt

def houghTransform(path, Tres = 1, Rres = 1):
    
    data = open(path,"r").readlines()
    candidates = [i.split() for i in data]
    N = len(candidates)
    Rmax = 2048 * 2 ** 0.5

    T = np.linspace(-90.0, 90.0, 2*np.ceil(90.0/Tres) + 1)
    numT = len(T)
    q = np.ceil(Rmax/Rres)
    numR = 2*q + 1
    R = np.linspace(-q*Rres, q*Rres, numR)
    H = np.zeros((numR,numT))

    def x(i):
        return float(candidates[i][1])

    def y(i):
        return float(candidates[i][2])

    X = np.zeros(N)
    Y = np.zeros(N)
    
    for i in range(N):
        X[i] = x(i)
        Y[i] = y(i)
        Rval = np.floor(x(i)*np.cos(T*np.pi/180) + y(i)*np.sin(T*np.pi/180))
        for j in range(numT):
            H[Rval[j],j] += 1
    
    return X,Y,R,T,H
        

X,Y,R,T,H = houghTransform("aday_noktalar.txt",2,2)

print(H[H>4])

intersections = np.where(H>4)
print(intersections)
indices = list(zip(intersections[0],intersections[1]))
print(indices)
RT = [(R[i],T[j]) for (i,j) in indices]
print(RT)

def MC(RT):
    M = -math.cos(RT[1]*math.pi/180)/math.sin(RT[1]*math.pi/180)
    C = RT[0]/math.sin(RT[1]*math.pi/180)
    return M,C


plt.plot(X,Y,"o")

Xaxis = np.array([0,2000])
for i in RT:
    try:
        M,C = MC(i)
        plt.plot(Xaxis,M*Xaxis+C,"-")
    except ZeroDivisionError:
        continue
plt.ylim((0,2000))
plt.xlim((0,2000))
plt.figure()
plt.imshow(H, aspect="auto")
plt.show()


