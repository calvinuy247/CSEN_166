# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 12:05:20 2020

@author: yingl
"""

import numpy as np

T=np.zeros((3,3,2),dtype=float) # |S|x|S|x|A| # T(s,s',a) # T(s,a,s')

R=np.zeros((3,3,2),dtype=float) # |S|x|S|x|A| # R(s, s',a) # R(s,a,s')

# high = 0, medium = 1, low = 2
# spin = 0, no spin = 1
                               
# action spin                        
T[:,:,0]=[[1,1,1],           
          [1,1,1],        
          [1,1,1],]             

                               
                               
R[:,:,0]=[[2,0,0],             
          [2,0,0],             
          [0,-1,0,]]             

                               
# action no spin                     
T[:,:,1]=[[1,1,1],           
          [1,1,1],        
          [1,1,1],]            


R[:,:,1]=[[0,3,0],             
          [0,0,0],             
          [0,0,0,]]              

max_iteration= 2000 
V=np.zeros((3,max_iteration+1),dtype=float) # V: 3 x (max_iteration+1)
#gamma = .8
gamma = 0.8
epsilon = 1e-4
threshold = epsilon*(1-gamma)/gamma

for k in range(max_iteration):  
    # V[s,k+1] = max_a { sum_s' T[s,s',a]*( R[s,s',a]+gamma*V[s',k] ) }
    # [current, next, action]
    # high:
    # spin:
    high_spin = T[0,0,0]*(R[0,0,0]+gamma*V[0,k])
    # no spin:
    high_nospin = T[0,1,1]*(R[0,1,1]+gamma*V[1,k])
    V[0,k+1]=np.max([high_spin,high_nospin])
    
    # medium:
    # spin:
    medium_spin = T[1,0,0]*(R[1,0,0]+gamma*V[0,k])
    # no spin:
    medium_nospin = T[1,2,1]*(R[1,2,1]+gamma*V[2,k])
    V[1,k+1]=np.max([medium_spin,medium_nospin])
    
    # low
    # spin:
    low_spin = T[2,1,0]*(R[2,1,0]+gamma*V[1,k])
    # no spin:
    low_nospin = T[2,2,1]*(R[2,2,1]+gamma*V[2,k])
    V[2,k+1]= np.max([low_spin,low_nospin])

    # check stopping criterion
    #COMMENT OUT THESE TWO LINES IF YOU WANT TO FIND CONV. VALUES

    if np.max(np.abs(V[:,k+1]-V[:,k])) <= threshold: # V: 3 x (max_iteration+1)
        break

print(V)

