import os
import time

def read_from_file(filename):
    inpFile=open(filename,"r")
    lines=inpFile.readlines()
    words=[]
    for line in lines:
        words.extend(line.split(" "))

    final_words=[]
    for word in words:
        if len(word)>0 :
            final_words.append(word.rstrip())

    print(final_words)
    l=len(final_words)
    i=0

    while final_words[i]!="DIMENSION":
        i+=1
    i+=2
    n=int(final_words[i])
    i+=1

    while final_words[i]!="EDGE_WEIGHT_TYPE":
        i+=1
    i+=2
    EDGE_WEIGHT_TYPE=str(final_words[i])
    i+=1

    while final_words[i]!="CAPACITY":
        i+=1
    i+=2
    capacity=int(final_words[i])
    i+=1

    if EDGE_WEIGHT_TYPE == "EUC_2D":
        while final_words[i]!="NODE_COORD_SECTION":
            i+=1
        i+=1
        coordinates=[]
        for j in range(0,n):
            coordinates.append([int(final_words[i+3*j+1]),int(final_words[i+3*j+2])])
        i+=n*3
    else:
        while final_words[i]!="EDGE_WEIGHT_SECTION":
            i+=1
        i+=1
        edges=[]
        for j in range(0,int(n*(n-1)/2)):
            edges.append(int(final_words[i+j]))
        i+=int(n*(n-1)/2)

    while final_words[i]!="DEMAND_SECTION":
        i+=1
    i+=1

    demand=[]
    for j in range(0,n):
        demand.append(int(final_words[i+j*2+1]))

    if EDGE_WEIGHT_TYPE == "EUC_2D":
        print(n)
        print(coordinates)
        print(demand)
        print(capacity)
    else:
        print(n)
        print(edges)
        print(demand)
        print(capacity)





location=os.path.join("..","Data","eil22.vrp")
read_from_file(location)
