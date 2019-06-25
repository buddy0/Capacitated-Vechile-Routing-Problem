import operator
import os
import time
import sys

def edgelength(fr,to,edges,n):
    if fr==0:
        fr=n-1
    elif fr==n-1:
        fr=0

    if to==0:
        to=n-1
    elif to==n-1:
        to=0

    if fr<to :
        temp=fr
        fr=to
        to=temp
    elif int(fr)==int(to):
        return 0

    return edges[int(((fr-1)*fr)/2+to)]


def combine_subtours_usingGreedy(n,anslstdb,DPAdb):
    n-=1
    ival=0
    flst=[]
    vertexOrder=[]
    total_cost=0
    anslstdb.sort(key = operator.itemgetter(1))
    for anslst in anslstdb:
        i=anslst[0]
        print(i)
        if ival+i == ival^i :
            flst.append(i)
            presentOrder=getOrder(anslst[2],anslst[0],n+1,DPAdb)
            vertexOrder.append(presentOrder)
            ival=ival+i
            total_cost+=anslst[3]
            if ival == (2**n -1):
                break
    return (vertexOrder,total_cost)

def combine_subtours(n,DPBdb,DPAdb):
    n-=1
    for i in range(1,2**n):
        print(i)
        for j in range(1,i) :
            if i+j == i^j and DPBdb[i][0]!=None and DPBdb[j][0]!=None:
                combineDistance=DPBdb[i][0]+DPBdb[j][0]

                if DPBdb[i+j][0]==None or DPBdb[i+j][0]>combineDistance:

                    DPBdb[i+j][0]=combineDistance
                    DPBdb[i+j][1]=i
                    DPBdb[i+j][2]=j

    return (getOrderwithDPB(2**n-1,DPBdb,n+1,DPAdb),DPBdb[2**n-1][0])

def getOrderwithDPB(i,DPBdb,n,DPAdb):
    if DPBdb[i][2]==None:
        return [getOrder(DPBdb[i][1],i,n,DPAdb)]
    else :
        a=getOrderwithDPB(DPBdb[i][2],DPBdb,n,DPAdb)
        b=getOrderwithDPB(DPBdb[i][1],DPBdb,n,DPAdb)
        a.extend(b)
        return a


def getOrder(vertexno,groupno,n,DPAdb):
    n-=1 #removing one deport
    ans=[vertexno]
    nextverno=DPAdb[(groupno,vertexno)][1]
    while nextverno != n:
        ans.append(nextverno)
        groupno=groupno & ~(1 << vertexno)
        vertexno=nextverno
        nextverno=DPAdb[(groupno,vertexno)][1]
    return ans


def CVRP_sol_by_DP(n,edges,demand,capacity,greedy=False):
    #-----------------INPUT FORMAT-----------------------------
    #n=number of customers + 1  ,as there is one deport
    #edges= an array which represents the lower triangular distance matrix column wise(excluding the digonal)t
    #demands= an array which represents the demands of the customers.
    ######index starts from 0 to n-1.
    ######(0)th vertex is the deport , So demand[0]=0
    ######1 to n-1 represents n-1 customers
    #capacity=The maximum capacity of the vechicle

    #------------------OUTPUT FORMAT----------------------------
    # a list L, where L[0]=number of subtours
    # l[1]=total distance that needs to be covered
    # L[2]= a list of subtours indexed according to computation format.

    #----------------Compution Format-----------------------------
    # vetrex 0 and n-1 are interchanged for ease of computation

    demand[0]=demand[n-1]
    demand[n-1]=0

    bigIntVal=999999999999999
    maxmusk= 2 ** (n-1)
    grpwt= [None] * maxmusk #It stores the total wt of the group
    grpwt[0]= 0

    DPAdb={}
    DPBdb=[]
    anslstdb=[]

    for i in range(maxmusk):
        '''f3=open("Status.txt","w")
        f3.write(str(i))
        f3.close'''
        print(i)
        #check if the groups total weight is a valid one.

        if grpwt[i]==None or grpwt[i]>capacity:
            DPBdb.append([None,None,None])
            continue

        #Find the distance that needs to be travelled for visiting this group as a subtour.
        mincostsub=bigIntVal
        nextvertexno=-1
        cnt=0
        for y in range(n):
            if i&(1<<y) > 0:
                cnt+=1
                cost=edgelength(n-1,y,edges,n) + DPAdb[(i,y)][0]
                if cost < mincostsub :
                    mincostsub=cost
                    nextvertexno=y

        if greedy==True:
            if mincostsub!=bigIntVal:
                anslstdb.append((i,mincostsub/cnt,nextvertexno,mincostsub))
        else:
            if mincostsub!=bigIntVal:
                DPBdb.append([mincostsub,nextvertexno,None])
            else :
                DPBdb.append([None,None,None])

        #trying to enlarge the group by placing 1's in place of 0's.
        for j in range(0,n-1):
            if i&(1<<j) == 0:
                newgrp=i|(1<<j)
                newgrpwt=(grpwt[i]+demand[j]) if (grpwt[newgrp]==None) else (grpwt[newgrp])
                grpwt[newgrp]=newgrpwt
                if newgrpwt > capacity:
                    continue
                #here newgroup is newgrp starting with j,having min ditance starting with j covering all vertices and returning
                #back to n-1(deport).
                mincost=bigIntVal
                nextvno=-1
                for k in range(n):
                    if i&(1<<k) > 0:
                        cost=edgelength(j,k,edges,n) + DPAdb[(i,k)][0]
                        if cost < mincost :
                            mincost=cost
                            nextvno=k
                if mincost == bigIntVal:
                    mincost=edgelength(j,n-1,edges,n)
                    nextvno=n-1
                DPAdb[(newgrp,j)]=[mincost,nextvno]

    if greedy == True:
        (subtours,total_distance)=combine_subtours_usingGreedy(n,anslstdb,DPAdb)
    else :

        (subtours,total_distance)=combine_subtours(n,DPBdb,DPAdb)

    L=[]
    L.append(len(subtours))
    L.append(total_distance)
    L.append(subtours)
    return L

def CVRP_sol_coordinate_wrap(n,coordinates,demand,capacity,greedy=False):
    #-----------------INPUT FORMAT-----------------------------
    #n=number of customers + 1  as there is one deport
    #coordinates= an array which represents the coordinates of the customers and the deport at begining.
    #demands= an array which represents the demands of the customers.
    #index starts from 0 to n-1.
    #(n-1)th vertex is the deport , So demand[n-1]=0
    #capacity=The maximum capacity of the vechicle

    #------------------OUTPUT FORMAT----------------------------
    # a list L, where L[0]=number of subtours
    # l[1]=total distance that needs to be covered
    # L[2]= a list of subtours , where each subtour starts with n-1, followed by vertex indexes in order, ending with n-1.
    edges=[]
    for i in range(1,n):
        for j in range(i):

            edges.append(((coordinates[i][0]-coordinates[j][0])**2 + (coordinates[i][1]-coordinates[j][1])**2)** 0.5)

    if greedy == False:
        return CVRP_sol_by_DP(n,edges,demand,capacity)
    else:
        return CVRP_sol_by_DP(n,edges,demand,capacity,True)




def read_from_file(filename,outputname,greedy=False):
    inpFile=open(filename,"r")
    lines=inpFile.readlines()
    words=[]
    for line in lines:
        words.extend(line.split(" "))

    final_words=[]
    for word in words:
        if len(word)>0 and len(word.rstrip())>0:
            final_words.append(word.rstrip())

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
    #print(final_words)

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

    if greedy==False:
        if EDGE_WEIGHT_TYPE == "EUC_2D":
            #print(n)
            #print(coordinates)
            #print(demand)
            #print(capacity)
            start_time=time.time()
            LAns=CVRP_sol_coordinate_wrap(n,coordinates,demand,capacity)
            end_time=time.time()
            time_taken=end_time-start_time
            LAns.append(time_taken)
            print(str(LAns))
        else:
            #print(n)
            #print(edges)
            #print(demand)
            #print(capacity)
            start_time=time.time()
            LAns=CVRP_sol_by_DP(n,edges,demand,capacity)
            end_time=time.time()
            time_taken=end_time-start_time
            LAns.append(time_taken)
            print(str(LAns))
    else:
        if EDGE_WEIGHT_TYPE == "EUC_2D":
            #print(n)
            #print(coordinates)
            #print(demand)
            #print(capacity)
            start_time=time.time()
            LAns=CVRP_sol_coordinate_wrap(n,coordinates,demand,capacity,True)
            end_time=time.time()
            time_taken=end_time-start_time
            LAns.append(time_taken)
            print(str(LAns))
        else:
            #print(n)
            #print(edges)
            #print(demand)
            #print(capacity)
            start_time=time.time()
            LAns=CVRP_sol_by_DP(n,edges,demand,capacity,True)
            end_time=time.time()
            time_taken=end_time-start_time
            LAns.append(time_taken)
            print(str(LAns))

    f2=open(outputname,"w")
    for items in LAns:
        f2.write(str(items))
        f2.write("\n")
    f2.close()




greedy=str(sys.argv[2])
name=sys.argv[1]
location=os.path.join("..","Data",name+".vrp")
if greedy=="True":
    outputname=str(name)+"output_greedy.txt"
    read_from_file(location,outputname,True)
else :
    outputname=str(name)+"output.txt"
    read_from_file(location,outputname,False)


'''
n=7
coordinates=[[0,0],[5,1],[6,2],[7,1],[-5,-1],[-6,-2],[-7,-1]]
demand=[0,20,20,20,20,20,20]
capacity=60
L=CVRP_sol_coordinate_wrap(n,coordinates,demand,capacity)
print(L[0])
print(L[1])
print(L[2])

L=CVRP_sol_coordinate_wrap(n,coordinates,demand,capacity,True)
print(L[0])
print(L[1])
print(L[2])
'''
