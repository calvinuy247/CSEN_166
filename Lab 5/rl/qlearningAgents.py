# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from backend import ReplayMemory

import nn
import model
import backend
import gridworld


import random,util,math
import numpy as np
import copy

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        
        # Dictionaries are used to store data values in key:value pairs.
        self.qvalues = {} # this is a dictionary that stores the q-states with associated q-values
        # the q-states are keys, and the q-values are associated values for the keys
        # self.qvalues = {(s1,a1): val1, (s2,a2): val2, ...} # pseudo code

        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        # just filled in what the comments at bottom that were already in file
        # makes sense to me. idk?

        if (state,action) in self.qvalues: # (state,action) is the key; (s,a) is the key (s,a): 0.5
            test = 0 # just for testing

            # return the associated q-value
            return self.qvalues[(state,action)]

        else:
            test = 0 # just for testing

            # add this (s,a) pair to dictionary and set its q value to 0
            self.qvalues[(state,action)] = 0
            
            # return its value which is 0
            return self.qvalues[(state,action)]

            # update the dictionary self.qvalues with this unseen (s,a) and initialize its value as 0.0
            # self.qvalues[(s,a)]=0.0
            # return this q-value     
            

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action) # which is V(state)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # returns V(state) by iterating over legal actions (a') and getting the greatest Q(state,a')

        # create a list of all legal actions from state
        legal_actions = self.getLegalActions(state)

        # if no legal actions (terminal state) return 0.0
        if not (legal_actions):
          return 0.0

        # initialize Q value with first legal action as 'max'
        max_dummy = self.getQValue(state, legal_actions[0])

        # for all legal actions after the first
        # if its Q value is greater than the current max then make it the max
        # (dont have to worry about choosing from multiple because it just wants the value)
        for i in legal_actions[1:]:
          if self.getQValue(state,i) > max_dummy:
            max_dummy = self.getQValue(state,i)

        # return the max Q value (aka V(state))
        return max_dummy
          
        #util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # returns best action by iterating over all legal actions and populating a list of actions that all
        # have the same Q value from state and choosing a random one

        #sets current max action and list of possible action candidates to empties
        max_act = None
        candidate_actions = []

        # create a list of all legal actions from state
        legal_actions = self.getLegalActions(state)

        # if no legal actions (terminal state) return None
        if not (legal_actions):
          return None

        # set first possible action to max action and add action to candiate actions
        candidate_actions.append(legal_actions[0])
        max_dummy = self.getQValue(state,legal_actions[0])

        #for every actions starting after the first
        for i in legal_actions[1:]:

          # if value for i has same as max then add it to candidate actions
          if self.getQValue(state,i) == max_dummy:
            candidate_actions.append(i)

          # if value for i is greater than value for candidate actions
          elif self.getQValue(state,i) > max_dummy:

            # set new max value to current actions value and clear the list of candidates
            # and add new max action to candidate actions
            max_dummy = self.getQValue(state,i)
            candidate_actions.clear()
            candidate_actions.append(i)

        # choose a random action from candidate actions and return
        max_act = random.choice(candidate_actions)
        return max_act

        # YL: if there are multiple best actions, then choose a random one
        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        # 
        if (util.flipCoin(self.epsilon)):
          random_action = random.choice(legalActions)
          return random_action
        else:
          best_action = self.computeActionFromQValues(state)
          return best_action


        util.raiseNotDefined()

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        # get max Q(s',a') 
        # it references the gamma*max(Q(s',a')) from slides/pdf

        # create a list of legal actions from next state (to use in sample variable)
        next_legal_actions = self.getLegalActions(nextState)

        # initial max_next_q:
        # 0 if no legal actions (terminal)
        # Q value of (nextState,next_legal_actions[0]) if there are legal actions
        if not (next_legal_actions):
          max_next_q = 0
        else:
          max_next_q = self.getQValue(nextState,next_legal_actions[0])
        
        # find max Q value for all possible actions from nextState
        for next_action in next_legal_actions[1:]:
          if self.getQValue(nextState, next_action) > max_next_q:
            max_next_q = self.getQValue(nextState, next_action)

        # create sample variable
        sample = reward + self.discount * (max_next_q)

        # update Q value
        self.qvalues[(state,action)] = ((1-self.alpha) * self.getQValue(state,action)) + (self.alpha*(sample))
        #OR
        #self.qvalues[(state,action)] = self.getQValue(state,action) + self.alpha*(sample - self.getQValue(state,action))
      
        #util.raiseNotDefined()
        
        # self.qvalues[(state,action)] = ...

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
