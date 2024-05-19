# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 12:05:20 2020

@author: yingl
"""

import numpy as np

T=np.zeros((5,5,2),dtype=float) # |S|x|S|x|A| # T(s,s',a) # T(s,a,s')

R=np.zeros((5,5,2),dtype=float) # |S|x|S|x|A| # R(s, s',a) # R(s,a,s')

# s1,s2,s3,s4,s5

                               
# action 1                         
T[:,:,0]=[[0,0.5,0.5,0,0],             
          [0,0,0,0.5,0.5],        
          [0,0,0,0.9,0.1],
          [0,0,0,1,0],
          [0,0,0,0,1]]             

                               
                               
R[:,:,0]=[[0,1,0,0,1],             
          [0,1,0,0,1],             
          [0,1,0,0,1],
          [0,1,0,0,1],
          [0,1,0,0,1]]             

                               
# action 2                      
T[:,:,1]=[[0,0.9,0.1,0,0],         
          [0,0,0,0.9,0.1],             
          [0,0,0,0.5,0.5],
          [0,0,0,0,1],
          [0,0,0,0,1]]             


R[:,:,1]=[[0,1,0,0,1],             
          [0,1,0,0,1],           
          [0,1,0,0,1],
          [0,1,0,0,1],
          [0,1,0,0,1]]             

max_iteration= 2000 
V=np.zeros((5,max_iteration+1),dtype=float) # V: 5 x (max_iteration+1)
#gamma = 0.9
gamma = 0.9
epsilon = 1e-4
threshold = epsilon*(1-gamma)/gamma

for k in range(max_iteration):  
    # V[s,k+1] = max_a { sum_s' T[s,s',a]*( R[s,s',a]+gamma*V[s',k] ) }
    # [current, next, action]
    # s1:
    # action1:
    tmp11 = T[0,1,0]*(R[0,1,0]+gamma*V[1,k]) + T[0,2,0]*(R[0,2,0]+gamma*V[2,k]) # R[s]
    # action2:
    tmp12 = T[0,1,1]*(R[0,1,1]+gamma*V[1,k]) + T[0,2,1]*(R[0,2,1]+gamma*V[2,k])
    V[0,k+1]=np.max([tmp11,tmp12])
    
    # s2:
    # action1:
    tmp21 = T[1,3,0]*(R[1,3,0]+gamma*V[3,k]) + T[1,4,0]*(R[1,4,0]+gamma*V[4,k]) 
    # action2:
    tmp22 = T[1,3,1]*(R[1,3,1]+gamma*V[3,k]) + T[1,3,1]*(R[1,3,1]+gamma*V[4,k]) # s'=2 (overheated)
    V[1,k+1]=np.max([tmp21,tmp22])
    
    # s3
    # action1:
    tmp31 = T[2,3,0]*(R[2,3,0]+gamma*V[3,k]) + T[2,4,0]*(R[2,4,0]+gamma*V[4,k]) 
    # action2:
    tmp32 = T[2,3,1]*(R[2,3,1]+gamma*V[3,k]) + T[2,4,1]*(R[2,4,1]+gamma*V[4,k]) 
    V[2,k+1]= np.max([tmp31,tmp32])
  

    # s4
    # action1:
    tmp41 = T[3,3,0]*(R[3,3,0]+gamma*V[3,k]) 
    # action2:
    tmp42 = T[3,3,1]*(R[3,3,1]+gamma*V[3,k])
    V[3,k+1]= np.max([tmp41,tmp42])

    # s5
    # action1:
    tmp51 = T[4,4,0]*(R[4,4,0]+gamma*V[4,k]) 
    # action2:
    tmp52 = T[4,4,1]*(R[4,4,1]+gamma*V[4,k])
    V[4,k+1]= np.max([tmp51,tmp52])

    # check stopping criterion
    #COMMENT OUT THESE TWO LINES IF YOU WANT TO FIND CONV. VALUES
    if np.max(np.abs(V[:,k+1]-V[:,k])) <= threshold: # V: 5 x (max_iteration+1)
        break

print(V)

