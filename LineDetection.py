# Line Detection Algorithm

def detectLines(path):
    data = open(path,"r").readlines()
    candidates = [i.split() for i in data]
    N = len(candidates)
    flags = N * [0]

    rangeMax = 20
    baseMin = 2
    areaMax = 1
    heightMax = 1

    def frame(i):
        return candidates[i][0]

    def x(i):
        return float(candidates[i][1])

    def y(i):
        return float(candidates[i][2])

    def isBadPair(i,j):
        return frame(i) == frame(j) or \
               abs(x(i)-x(j)) >= rangeMax or \
               abs(y(i)-y(j)) >= rangeMax

    def distance(i,j):
        return ((x(i)-x(j))**2 + (y(i)-y(j))**2)**0.5

    for i in range(N-2):
        for j in range(i+1,N-1):
            if isBadPair(i,j):
                continue
            for k in range(j+1,N):
                if isBadPair(i,k) or isBadPair(j,k):
                    continue
                base = max(distance(i,j),distance(j,k),distance(k,i))
                area = abs((x(j)-x(i))*(y(k)-y(i)) - (x(k)-x(i))*(y(j)-y(i))) / 2
                height = 2*area/base
                if base > baseMin and area < areaMax and height < heightMax:
                    for index in [i,j,k]:
                        flags[index] += 1
    
    return [data[i] for i in range(N) if flags[i]>10]

