
# from array import array
import networkx as nx
import matplotlib.pyplot as plt

from sklearn.metrics.cluster import normalized_mutual_info_score
import pandas as pd
import numpy as np
import os


# -----------------------------Neighborsfinder----------------

def nodfinder(A, i, m,N):
    count = 0
    for act in range(N):
        if (A[i][act] == 1):
            if (count == m):
                s = act + 1
                return s
            count = count + 1

# -------------------------------------

def getData(a, b):
    data = pd.read_csv(a)
    result = pd.read_csv(b)
    result = result.values[:, 1]
    # result=pd.DataFrame(b)
    # print(data[_values])
    A = data.values.tolist()
    # result=result.values.tostring()
    # result = result.to_numpy()
    # result=result.get_values()
    # result = np.asarray(result)
    return A, result;

#----------------------------------------------------------Functions----------------------------------------

#return ACtion  for node i  according to p[i][ri]
def Action_selector(t,i,p,A):
    s=0
    a0 = 0
    rand = np.random.uniform(0, 1)
    for m in range(0,r[i]):
         if (a0<= rand < a0 + p[t][i][m]):
            break
         else:
             a0=a0+p[t][i][m]
             s=nodfinder(A,i,m,N)
    return s, m



def decoder(S, u, mVC, currentComponent):
    mVC[u] = currentComponent
    if mVC[ S[u] ] == 0:
        mVC[u] = decoder(S, S[u], mVC, currentComponent)
    else:
        mVC[u] = mVC[S[u]]
    return mVC[u]


def Q(mVC,A,edge,r,N):
    temp = 0
    for p in range(0,N):
        for q in range(0,N):
            if(mVC[p]==mVC[q]):
                temp= temp +( A[p][q] -( (r[p] * r[q]) / (2*edge)))

    Q=temp/(2*edge)
    return Q

def Eresponce(Q,Qbest,MVC,N,t,A,beta):
    for i in range(0,N):
        buf1 = MVC[t][i]
        c = 1            #raghavan
        cp = 0

        for k in range(N):
            if (A[i][k] == 1):
                buf2 = MVC[t][k]
                if (buf1 == buf2):
                    c = c + 1
                else:
                    cp = cp + 1

        if( (Q>= Qbest) & (cp <= c) ):
            beta[t][i]=0        #reward

        else:
            beta[t][i]=1        #penalty
    return beta[t]


def update_Qbest(Qbest,Qfinal,t):            # function for updating Q best according to env.response

    if(Qfinal[t]> Qbest):
       Qbest=Qfinal[t]
    return Qbest



def update_wzd(i,q,beta,w,z,t,D):                          #func of updating W and Z          #stiiiillll neeed work**************
    b=beta[t][i]
    rrr=r[i]
    for action in range(0,rrr):
        if ( q == action):
            w[i][q]=w[i][q]+(1-b)
            if(z[i][q]==0.05):
                z[i][q]=0
            z[i][q]=z[i][q]+1
            d[i][q] = w[i][q] / z[i][q]


    D[i]=d[i].index(max(d[i]))
    return w[i][q],z[i][q],D[i]; # q?action



def cprp_update(p,i,q,t,alpharate):
    rrr=r[i]
    for action in range(rrr):
        if ( q == action):
            p[t+1][i][q]=float(p[t][i][q]+alpharate*(1-p[t][i][q]))

        if ( q != action):
            p[t + 1][i][action] = float((1 - alpharate) * p[t][i][action])
    return p[t+1][i]


# def Lpr_updatep(p,i):   #workkkkkkkkkkkk on this
#     rrr=r[i]
#               #M=1 mm=9
#     for action in range(rrr):
#         if ( beta[t][i]==0 & M == action):
#             # print('1111 condision')
#             print("beta isss",beta[t][i])
#             print('p t i m',t,i,M,'is:',p[t][i][M])
#             p[t+1][i][M]=float(p[t][i][M]+alpharate*(1-p[t][i][M]))
#
#             # print('p[t+1][i][action]:', p[t + 1][i][action])
#
#         if( beta[t][i]==0 & M!=action):
#             # print('2222 condision')
#             p[t+1][i][action]=float((1-alpharate)*p[t][i][action])
#
#         #-----------------------------PENALTY UPDTE
#
#         if (beta[t][i]==1 & action== M):
#             # print('item',(1 - betarate) * p[t][i][M])
#             p[t + 1][i][M] = float((1 - betarate) * p[t][i][M])
#             # print('3333 condision')
#
#         if(beta[t][i]==1 & action!= M):
#             # print('444 condision')
#             # print('p[t][i][action]:',t,i,p[t][i][action])
#             # print('item',(betarate/(rrr-1))+(1-betarate)*(p[t][i][action]))
#             p[t+1][i][action]=float((betarate/(rrr-1))+(1-betarate)*(p[t][i][action]))
#             # print('p[t+1][i][action]:', p[t+1][i][action])
#
#     # print('p is:',t+1,'for node i',i ,p[t+1][i])
#     return p[t+1][i]

def edgeounter(r,N):          #find number of edges
    degree=0
    for i in range(N):
        degree=r[i]+degree
    return (degree/2)

def teminationcondition1(Qfinal,term1 ,t):
    if(abs(Qfinal[t] - Qfinal[t-1])!= 0):
        term1=0
        return 1, term1
    else:
        term1 =1+ term1
        if( term1 >= 2000 ):
            return 0,term1
        else:
            return 1,term1



def deltacounter(MVC,N,t):
    delta=0
    for i in range(N):
        # print('mvc t n',MVC[t])
        # print('mvc t-1 n', MVC[t-1])
        if(MVC[t][i]!=MVC[t-1][i]):
            # print('in loop',MVC[t][i],MVC[t-1][i])
            delta=delta+1
            # print('detaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa is',delta)
    return delta

def teminationcondition2(Delta,term2 ,t):

    if(Delta[t]!= 0):
        term2=0
        #print('delta is changing',Delta[t])           #uncomment later
        return 1, term2
    else:
        term2 =1+ term2
        if( term2 >= 2000 ):
            return 0,term2
        else:
            return 1,term2


path = 'size/'

files = []
filesNoAdd = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
            filesNoAdd.append(file)
# for f in files:
#     print(f)
path1 = 'siz-membership/'

files1 = []
filesNoAdd1 = []
# r=root, d=directories, f = files
for r1, d1, f1 in os.walk(path1):
    for file1 in f1:
        if '.csv' in file1:
            files1.append(os.path.join(r1, file1))
            filesNoAdd1.append(file1)
# for f1 in files1:
#     print(f1)




memShip = 0
for f in files:
    a=f
    b=files1[memShip]
    memShip += 1
    print(a,b)

    A,result=getData(a,b)

    print(A)

    #-------------------------------------------------------variables-----------------------------------------------------
    N=len(A)  #number of nodes
    alpharate=0.0003   #  0< alpha < 1
    # betarate=alpharate;
    T=150000
    Qfinal=[0]*T
    Delta=[0]*T
    Qbest= -10
    MVC=[0]*T
    beta=[[-1 for col in range(N)] for row in range(T)]

    #G = nx.from_numpy_matrix(np.array(A))
    #nx.draw(G)
    #plt.show()
    #Gf=G
    #-------------------------- Degree--------------

    r = np.zeros(N)
    r = [ int(x) for x in r ]     #convert all elements to int from float
    for row in range( N):
        for col in range(N):
            if(A[row][col]==1):
                r[row]=r[row]+1

    edge=edgeounter(r,N)
    #--------------------------------Action probablity-------

    p=[[0 for col in range(N)] for row in range(T)]

    for i in range(0,N):
        p[0][i]=[1/r[i]]*r[i]

    for o in range (1,T):
        for n in range(0,N):
            p[o][n]=[-1]*r[n]


    w=[0 for col in range(N)]
    for n in range(0,N):
        w[n]=[0]*r[n]

    z=[0 for col in range(N)]
    for n in range(0,N):
        z[n]=[0.05]*r[n]

    d=[0 for col in range(N)]
    for n in range(0,N):
        d[n]=[0]*r[n]


    D=[0]*N
    M=[[-1]*N for row in range(T)]

    term1 =0
    term2=0
    t=0
    flag=1

    while (flag and t<T):
        #print('counting iteration:',t)          #uncommetnt later
        S = [0] * N

        for i in range(N):
            S[i],m = Action_selector(t,i,p,A)
            M[t][i]=m

        S = [0] + list(S)  # to handle the 1-indexing of the content in S
        mVC = [0] * len(S)
        currentComponent = 1

        for i in range(1, len(S)):
            if mVC[i] == 0:
                componentAssigned = decoder(S, i, mVC, currentComponent)
                if componentAssigned == currentComponent:
                    currentComponent += 1
        mVC = mVC[1:]  # Gets rid of the dummy 0th element added above

        MVC[t]=mVC
        Qfinal[t]=Q(MVC[t], A,edge,r,N)
        beta[t]=Eresponce(Qfinal[t],Qbest,MVC, N, t, A, beta)
        Qbest= update_Qbest(Qbest,Qfinal,t)

        if(t==T-1):
             break
        else:
            for i in range (0,N):
                q=M[t][i]
                w[i][q], z[i][q],D[i] = update_wzd(i,q,beta,w,z, t , D)
                # p[t+1][i]=Lpr_updatep(p,i)
                p[t+1][i]=cprp_update(p,i,D[i], t, alpharate)

        if(t>3):
            Delta[t] =deltacounter(MVC, N , t)
            # print('dddddddddddddd',Delta)
            flag1,term1 = teminationcondition1(Qfinal,term1,t) #const Q
            flag2, term2 = teminationcondition2(Delta,term2,t )  # const Mvc

            if(flag1==0 or flag2==0):
                flag=0
            if(flag==0):
                break
        t+=1

    print('Number of nodes: ',N )
    print('Number of edges:',edge)
    print('Qfinal issssssssss:',Qfinal[t])
  #  print('final resultttttttttt:',MVC[t],)
    print('number of iteration:',t)
    print('NMI is: ',normalized_mutual_info_score(result,MVC[t]))
    print("-----------------------------------------------------------------")

    #print('labels',result)
    # for t in range (T):
    #     if(Qfinal[t] == Qbest):
    #         a=MVC[t]
    #         tbest=t
    #         print('final resultttttttttt:',a,)
    #         print('t best :',t)
    #         break


    #--------------------------------plot modularity---------------------------------------------------------------
    # plt.plot([0,1,2,...,T], Qfinal)

    # x_data = []*T

    y_data = Qfinal
    # y_data=[0]*t
    plt.subplot(2, 1, 1)
    plt.plot( Qbest, 'rx')
    plt.plot( y_data[0:t], 'b-')
    # plt.xlabel("Iteration")
    plt.ylabel("Modularity")

    plt.subplot(2, 1, 2)
    plt.plot( Delta[0:t], 'r-')
    plt.xlabel("Iteration")
    plt.ylabel("Delta")


    #print ('p size is:',np.size(p),'shape is:', np.shape(p))
    #plt.plot(p[1][1][:],'r-')

    plt.show()

