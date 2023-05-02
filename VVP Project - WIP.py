import numpy as np
import time

def nactiBludiste(path):
    soubor = open(path, encoding='utf-8')
    obsah = soubor.read()
    split = obsah.split()
    n=len(split)
    m=(len(split[0])+1)//2
    maze = np.zeros((n,m))
    i=0
    for line in split:
        split2 = line.split(",")
        j=0
        for point in split2:
            if(point=='1'):
                maze[i,j] = 1
            #maze[i,j]= ord(point)-ord('0')
            j+=1
        i+=1
    return maze

path = "testing1.csv"
maze = nactiBludiste(path)
#print(maze)

def printMaze(maze):
    n=len(maze)
    borderline = "--"
    for i in range(n):
        borderline = borderline +"--"
    print(borderline)
    for i in maze:
        line = "|"
        for j in i:
            if j==0:
                line = line + "  "
            else:
                line = line + "■ "
        line = line + "|"
        print(line)
    print(borderline)

printMaze(maze)

def makeIncidencniMatice(maze):
    n= len(maze)*len(maze[0])
    m= n*2-len(maze)-len(maze[0])
    inmat = np.zeros((n,m))

    n=len(maze)
    m=len(maze[0])
    for i in range(n):
        for j in range(m):
            if(maze[i][j]!=1):
                #up
                if((i!=0) and maze[i-1][j]==0):
                    inmat[i * m + j , i * (m - 1) + (i - 1) * m + j]=1
                #down
                if((i!=n-1) and maze[i+1][j]==0):
                    inmat[i * m + j , (i + 1) * (m - 1) + i * m + j]=1
                #left
                if((j!=0) and maze[i][j-1]==0):
                    inmat[i * m + j , i * (m - 1) + i * m + j-1]=1
                #right
                if((j!=m-1) and maze[i][j+1]==0):
                    inmat[i * m + j , i * (m - 1) + i * m + j]=1
            print(i,j)
    print(inmat)

def makeIncidencniMatice1(maze):
    

    n=len(maze)
    m=len(maze[0])
    n_nodes=0
    n_edges=0
    for i in range(n):
        for j in range(m):
            if(maze[i][j]!=1):
                #down
                if((i!=n-1) and maze[i+1][j]==0):
                    n_edges+=1
                #right
                if((j!=m-1) and maze[i][j+1]==0):
                    n_edges+=1
                n_nodes+=1
    edges = np.zeros((n_edges,2))
    nodes = np.zeros(1)
    p=0
    for i in range(n):
        for j in range(m):
            if(maze[i][j]!=1):
                #right
                if((j!=m-1) and maze[i][j+1]==0):
                    edges[p,0]=i * m + j
                    edges[p,1]=i * m + j+1
                    p+=1

                    is_in_array = False
                    for k in nodes:
                        if (k == i * m + j):
                            is_in_array = True
                    if is_in_array==False:
                        nodes = np.append(nodes,i * m + j)

                    is_in_array = False
                    for k in nodes:
                        if (k == i * m + j+1):
                            is_in_array = True
                    if is_in_array==False:
                        nodes = np.append(nodes,i * m + j+1)
                #down
                if((i!=n-1) and maze[i+1][j]==0):
                    edges[p,0]=i * m + j
                    edges[p,1]=(i+1) * m + j
                    p+=1
                    
                    is_in_array = False
                    for k in nodes:
                        if (k == i * m + j):
                            is_in_array = True
                    if is_in_array==False:
                        nodes = np.append(nodes,i * m + j)

                    is_in_array = False
                    for k in nodes:
                        if (k == (i+1) * m + j):
                            is_in_array = True
                    if is_in_array==False:
                        nodes = np.append(nodes,(i+1) * m + j)
    #print(edges)
    nodes =np.sort(nodes)
    #print(nodes)
    low_edges = np.copy(edges)
    for i in range(len(low_edges)):
        for j in range(2):
            for k in range(len(nodes)):
                if (low_edges[i,j] == nodes[k]):
                    low_edges[i,j] = k
    """max = 0
    for i in low_edges:
        if i[0]>max:
            max = i[0]
        if i[1]>max:
            max = i[1]
    imin = -1
    while(imin< max):
        for i in low_edges:
            if i[0]==imin+1:
                imin+=1
            elif i[0]>imin:
                i[0]-=1

            if i[1]==imin+1:
                imin+=1
            elif i[1]>imin:
                i[1]-=1
        max-=1"""
    
    #print(low_edges)
    #print("-------------")
    inmat = np.zeros((n_nodes,n_edges))
    for i in range(n_nodes):
        for j in range(n_edges):
            if(low_edges[j,0]==i):
                inmat[i,j]=1
            if(low_edges[j,1]==i):
                inmat[i,j]=1
    return inmat, nodes


inmat, nodes = makeIncidencniMatice1(maze)
#print(inmat,"\n", edges)

def DijkstraFindPath(inmat):
    notvisited = np.arange(len(inmat))
    visited = np.zeros(1,dtype=int)
    for i in notvisited:
        isempty=True
        for j in inmat[-i-1]:
            if j == 1:
                isempty = False
        if isempty:
            visited=np.append(visited,notvisited[-1])
            notvisited = notvisited[:-1]
    notvisited = notvisited[1:]
    distance = np.ones(len(notvisited)+1)*-1
    distance[0] = 0
    end = notvisited[-1]
    while distance[end]==-1:
        if len(visited)>1:
            for v in visited:
                i=0
                for n in notvisited:
                    for col in inmat.T:
                        if(col[v]==1 and col[n]==1):
                            #print("----------------")
                            #print(v,n,visited,notvisited,i)
                            visited = np.append(visited,n)
                            notvisited = np.append(notvisited[:i],notvisited[i+1:])
                            i-=1
                            if ((distance[n]) < (distance[v]+1)):
                                distance[n]=distance[v]+1
                                #print(distance[n])
                            #print("----------------")
                    i+=1
        else:
            i=0
            for n in notvisited:
                for col in inmat.T:
                    if(col[0]==1 and col[n]==1):
                        #print("----------------")
                        #print(0,n,visited,notvisited,i)
                        visited = np.append(visited,n)
                        notvisited = np.append(notvisited[:i],notvisited[i+1:])
                        i-=1
                        distance[n]=1
                        #print(distance[n])
                        #print("----------------")
                i+=1
    #print(distance)
    path = np.ones(1,dtype=int)*end
    while path[0]!=0:
        for i in range(len(inmat[0])):
            if inmat[path[0],i]==1:
                for j in range(len(inmat)):
                    if inmat[j,i]==1 and distance[j]==distance[path[0]]-1:
                        path = np.append(j,path)
    return path

path = DijkstraFindPath(inmat)
print(path,"\n",nodes)
for i in range(len(path)):
    for j in range(len(nodes)):
        if path[i]==j:
            path[i]=nodes[j]
            break
print(path)
def printMazePath(maze,path):
    n=len(maze)
    for i in path:
        maze[i//n,i-(i//n)*n]=2
    borderline = "--"
    for i in range(n):
        borderline = borderline +"--"
    print(borderline)
    for i in maze:
        line = "|"
        for j in i:
            if j==0:
                line = line + "  "
            elif j==2:
                line = line + "▪ "
            else:
                line = line + "■ "
        line = line + "|"
        print(line)
    print(borderline)
printMazePath(maze,path)