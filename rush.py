#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
import sys

file = open("inp3.txt", "r")

c=0;l=[]
for line in file:
    if(c==0):       # reading first line, value of n and limit
        n = int(line.strip().split(",")[0])
        limit = int(line.strip().split(",")[1])
    elif(c==1):     # reading second line, coordinate of red car
        Ri = int(line.strip().split(",")[0])
        Rj = int(line.strip().split(",")[1])
    else:           # reading 3rd onward lines, coordinates of horizontal, vertical car and mines
        l.append(line.strip().split(","))
    c=c+1


vs = [ [ [ [ Bool ("e_{}_{}_{}_{}".format(i,j,k,l)) for l in range(limit)] for k in range(4)] for j in range(n)] for i in range(n)]

#adding initial constraints i.e, filled position
F = []
F.append(vs[Ri] [Rj] [3][0]); F.append(vs[Ri][Rj+1][3][0])    #position of red car
#print(F)
for i in range(len(l)):
    F.append( vs[int(l[i][1])] [int(l[i][2])] [int(l[i][0])] [0] )  #initial position of cars and mines
    if(l[i][0]=='0'):
        F.append( vs[int(l[i][1])+1] [int(l[i][2])] [int(l[i][0])] [0])    #final position of vertical cars
    elif(l[i][0]=='1'):
        F.append( vs[int(l[i][1])] [int(l[i][2])+1] [int(l[i][0])] [0])    #final position of horizontal cars


#adding constraints of final position of red car
l=[]
for i in range(n):
    for j in range(limit):
        l.append((vs[i][n-1][3][j]))
F.append(Or(l))

#two cars can't on a same squares at same time
for l in range(limit):
    for i in range(n):
        for j in range(n):
            for k in range(4):
                for k1 in range(4):
                    if(k1!=k):
                        F.append(Or(Not(vs[i][j][k][l]), (Not(vs[i][j][k1][l]))))
                    elif (k==0 and j<n-3):
                        F.append(Not(And(vs[i][j][k][l],vs[i][j+1][k][l],vs[i][j+2][k][l],Not(vs[i][j+3][k][l]))))
                    elif (k==1 and i<n-3):
                        F.append(Not(And(vs[i][j][k][l],vs[i+1][j][k][l],vs[i+2][j][k][l],Not(vs[i+3][j][k][l]))))

shell=[] 
stone=[]
#Writing constraints foe shifts/moves:
for l in range(limit-1):
    shell=0
    for j in range(n):
        for k in range(4):
            for i in range(n):
                stone.append(And((k==2),(vs[i][j][k][l+1])=(vs[i][j][k][l]))

                shell.append(Implies((And((k==0),(i>0),(i<n-2),vs[i][j][k][l],vs[i+1][j][k][l])),(Or((And(vs[i][j][k][l],vs[i-1][j][k][l])),(And(vs[i+1][j][k][l],vs[i+2][j][k][l]))))))


'''                shell.append(Implies((And((k==0),(i>0),(i<n-2),(vs[i][j][k][l]),(vs[i+1][j][k][l]))),(Or(And((vs[i+1][j][k][l]),(vs[i+2][j][k][l])),(And((vs[i-1][j][k][l]),(vs[i][j][k][l])))))))
                shell.append(Implies((And((k==1),(vs[i][j][k][l]),(vs[i][j+1][k][l]))),(Or(And((vs[i][j+1][k][l]),(vs[i][j+2][k][l])),(And((vs[i][j-1][k][l]),(vs[i][j][k][l])))))))
                shell.append(Implies((And((k==3),(vs[i][j][k][l]),(vs[i][j+1][k][l]))),(Or(And((vs[i][j+1][k][l]),(vs[i][j+2][k][l])),(And((vs[i][j-1][k][l]),(vs[i][j][k][l])))))))
   '''             
#                shell.append(And(k==3),())
#                F.append()
#                if((vs[i][j][k][l+1])!=(vs[i][j][k][l])):
#                   shell=shell+1

#    F.append(shell==2)    
F.append(And(stone))
for member1 in shell :
    for member2 in shell :
        F.append(Or(shell))
        F.append(Or((Not(member1)),(Not(member2))))
                    

'''            for k in range(4):
               for k1 in range(4):
                    if (k!=k1): 
                        F.append(Or(Not(vs[i][j][k][l]), (Not(vs[i][j][k1][l])))) 
                
'''
#print(F)

s = Solver()
s.add( And( F ) )
if s.check() == sat:
    m = s.model()
    for l in range(limit):
        for i in range(n):
            for j in range(n):
                for k in range(4):
                    val = m[vs[i][j][k][l]]
                    if is_true( val ):
                        print("{},{}".format(i,j))
else:
    print("game is unsat")


file.close()
#print(file)
