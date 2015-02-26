import game
import os
import unit
import ability
import random
import itertools


from ability import printf

def list_tuple_truncate(list, index, value):
    temp = []
    for item in list:
        if(item[index] == value):
            temp.append(item)
            
    for item in temp:
        #printf("KILLING %s!!\n",item)
        list.remove(item)
    

    
def snag_choices(listoflists,x):
    returnme = []
    
    for e in listoflists[0]:
        for f in listoflists[1]:
            for g in listoflists[2]:
                for h in listoflists[3]:
                    returnme.append([e,f,g,h])
    random.shuffle(returnme)
    
    return returnme[:x]
    

class Agent:
    def __init__(self,depth=64,aggressive=1,defensive=1,nominal=1):
    
        self.AggressiveWeight = aggressive
        self.DefensiveWeight = defensive
        self.NominalWeight = nominal
        self.depth = depth
        
        
    # This agent summates all possible of my actions (With heuristics) against
    # 128 randomly chosen among their (+Heuristic) choices
    def choose(self,game,x):
    
        #Debug stuff
        game.OfficialState.report_teams()
    
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
		
        for i in range(4):
            random.shuffle(MyActions[i])
            FinalAnswer[i] = MyActions[i][0]
			
        return FinalAnswer

#This is a simple agent meant to play the game, well, simply.
