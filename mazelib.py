import numpy as np
import random
from PIL import Image

def nactiBludiste(mazefile):
    soubor = open(mazefile, encoding='utf-8')
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

def IsMaze(maze):
    visited = np.zeros(1,dtype=int)
    wasAdded = True
    n,m = np.shape(maze)
    while(wasAdded==True and visited[-1]!=m*n-1):
        wasAdded = False
        for vis in visited:
            #up
            if vis>m and visited[-1]!=m*n-1:
                neighbour=vis-m
                if(maze[neighbour//m,neighbour-(neighbour//m)*m] == 0):
                    repeat = False
                    for vis2 in visited:
                        if vis2 == neighbour:
                            repeat = True
                    if repeat == False:
                        wasAdded = True
                        visited = np.append(visited,neighbour)
            
            #down
            if vis<(n*m-m) and visited[-1]!=m*n-1:
                neighbour=vis+m
                if(maze[neighbour//m,neighbour-(neighbour//m)*m] == 0):
                    repeat = False
                    for vis2 in visited:
                        if vis2 == neighbour:
                            repeat = True
                    if repeat == False:
                        wasAdded = True
                        visited = np.append(visited,neighbour)
            
            #left
            if vis%m!=0 and visited[-1]!=m*n-1:
                neighbour=vis-1
                if(maze[neighbour//m,neighbour-(neighbour//m)*m] == 0):
                    repeat = False
                    for vis2 in visited:
                        if vis2 == neighbour:
                            repeat = True
                    if repeat == False:
                        wasAdded = True
                        visited = np.append(visited,neighbour)
            
            #right
            if vis%m!=m-1 and visited[-1]!=m*n-1:
                neighbour=vis+1
                if(maze[neighbour//m,neighbour-(neighbour//m)*m] == 0):
                    repeat = False
                    for vis2 in visited:
                        if vis2 == neighbour:
                            repeat = True
                    if repeat == False:
                        wasAdded = True
                        visited = np.append(visited,neighbour)
    
    if visited[-1]==m*n-1:
        return True
    else:
        return False
  
def printMaze(maze):
    n=len(maze[0])
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

def makeIncidencniMatice(maze):
    
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

def DijkstraFindPath(inmat,nodes):
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
        
    #print(distance)
    path = np.ones(1,dtype=int)*end
    while path[0]!=0:
        for i in range(len(inmat[0])):
            if inmat[path[0],i]==1:
                for j in range(len(inmat)):
                    if inmat[j,i]==1 and distance[j]==distance[path[0]]-1:
                        path = np.append(j,path)
    for i in range(len(path)):
        for j in range(len(nodes)):
            if path[i]==j:
                path[i]=nodes[j]
                break
    return path

def printMazePath(maze,path):
    n=len(maze[0])
    pathmaze = np.copy(maze)
    for i in path:
        pathmaze[i//n,i-(i//n)*n]=2
    borderline = "--"
    for i in range(n):
        borderline = borderline +"--"
    print(borderline)
    for i in pathmaze:
        line = "|"
        for j in i:
            if j==0:
                line = line + "  "
            elif j==2:
                line = line + ". "
            else:
                line = line + "■ "
        line = line + "|"
        print(line)
    print(borderline)

def generateMaze(n,m,choice = "random"):
    maze = np.ones((n,m))
    maze[0,0]=0
    maze[n-1,m-1]=0
    
    if (choice == "random"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if i<len(walls):
                    if walls[i] == x:
                        tempwalls = np.append(walls[:i],walls[i+1:])
                        break
            walls=tempwalls

    elif(choice =="grid"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        
        for i in range(n-1,0,-1):
            for j in range(m-1,0,-1):
                if(i%2==1 and j%2==1):
                    walls = np.append(walls[:i*m+j-1],walls[i*m+j:])
        for i in range(n-1,-1,-1):
            for j in range(m-1,-1,-1):
                if(i%2==0 and j%2==0):
                    walls = np.append(walls[:i*m+j-1],walls[i*m+j:])
                    maze[i,j]=0
        #printMaze(maze)
        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if walls[i] == x:
                    tempwalls = np.append(walls[:i],walls[i+1:])
            walls=tempwalls

    elif(choice =="clean"):
        maze = np.zeros((n,m))

    elif(choice =="zigzag1"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        for i in range(m-1,1,-1):
            row=(n//3)*2*m
            walls = np.append(walls[:row+i-1],walls[row+i:])
        
        for i in range(m-3,-1,-1):
            row=(n//3)*m
            walls = np.append(walls[:row+i-1],walls[row+i:])

        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if walls[i] == x:
                    tempwalls = np.append(walls[:i],walls[i+1:])
            walls=tempwalls

    elif(choice =="zigzag2"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        
        for i in range(m-3,-1,-1):
            row=(n//3)*2*m
            walls = np.append(walls[:row+i-1],walls[row+i:])

        for i in range(m-1,1,-1):
            row=(n//3)*m
            walls = np.append(walls[:row+i-1],walls[row+i:])
        

        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if walls[i] == x:
                    tempwalls = np.append(walls[:i],walls[i+1:])
            walls=tempwalls

    elif(choice =="zigzag3"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        
        for i in range(n*m-(m//3),m*2,-m):
            walls = np.append(walls[:i-1],walls[i:])

        j=3
        for i in range(n*m-(m//3)*2-2*m,-1-n-2,-m):
            walls = np.append(walls[:i-1+j],walls[i+j:])
            if(i>2*m):
                j+=1

        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if walls[i] == x:
                    tempwalls = np.append(walls[:i],walls[i+1:])
            walls=tempwalls
            
    elif(choice =="zigzag4"):
        walls = np.linspace(1,n*m-1,n*m-1,dtype=int)
        
        for i in range(n*m-(m//3)-2*m,-1,-m):
            walls = np.append(walls[:i-1],walls[i:])
        j=0
        for i in range(n*m-(m//3)*2+1,1+n-2,-m):
            walls = np.append(walls[:i-1+j],walls[i+j:])
            if(i<m*n-2*m):
                j+=1

        while(IsMaze(maze)==False):
            x = random.choice(walls)
            maze[x//m,x-(x//m)*m]=0
            for i in range(len(walls)):
                if walls[i] == x:
                    tempwalls = np.append(walls[:i],walls[i+1:])
            walls=tempwalls
        
    elif(choice =="zigzagRandom"):
        x = random.randint(1,4)
        print("zigzag"+str(x))
        maze = generateMaze(n,m,"zigzag"+str(x))
    
    elif(choice =="snake"):
        i=0
        j=1
        while (j!=m-1 or i!=n-1):
            while(j<m-1):
                maze[i,j]=0
                j+=1
            if(n-i==4):
                maze[i,j]=0
                i+=1
                maze[i,j]=0
                i+=1
                maze[i,j]=0
                i+=1
            elif(n-i==2):
                maze[i,j]=0
                i+=1
                continue
            elif(n-i==1):
                continue
            else:
                maze[i,j]=0
                i+=1
                maze[i,j]=0
                i+=1
            while(j>0):
                maze[i,j]=0
                j-=1
            if(i!=n-1):
                maze[i,j]=0
                i+=1
                maze[i,j]=0
                i+=1
        
    return maze

def mazePathToImg(maze,path,name):
    n,m=np.shape(maze)
    pathmaze = np.ones((n, m, 3), dtype=np.uint8)
    for i in range(n):
        for j in range(m):
            if maze[i,j]==0:
                pathmaze[i,j]=[255,255,255]
            else:
                pathmaze[i,j]=[0,0,0]
    for i in path:
        pathmaze[i//m,i-(i//m)*m]=[255, 0, 0]
    img = Image.fromarray(pathmaze, 'RGB')

    img.save(name + ".png")



