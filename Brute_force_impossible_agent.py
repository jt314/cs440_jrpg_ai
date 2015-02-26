import game
import unit
import ability
import random

class Agent:
    def __init__(self,moolol=10,aggressive=0,defensive=0,nominal=1):
    
        self.AggressiveWeight = aggressive
        self.DefensiveWeight = defensive
        self.NominalWeight = nominal

    def choose(self,game,x):
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]
        
        analysis = []
        
        for a in MyActions[0]:
            printf("ding!\n")
            for b in MyActions[1]:
                printf("dong!\n")
                for c in MyActions[2]:
                    for d in MyActions[3]:
                        
                        best = float("-inf")
                        worst = float("inf")
                        average = float("-inf")
                        util = 0
                        
                        for e in TheirActions[0]:
                            for f in TheirActions[1]:
                                for g in TheirActions[2]:
                                    for h in TheirActions[3]:
                                        temp = current_state.apply_action([[a,b,c,d],[e,f,g,h]])
                                        util = temp[0].utility(x)
                                        if(best > util): best = util
                                        if(worst < util): worst = util
                                        average += util
                        
                        average /= (len(e)*len(f)*len(g)*len(h))
                        util = self.AggressiveWeight*best + self.DefensiveWeight*worst + self.NominalWeight*average
                        #analysis[[a,b,c,d]] = util   
                        analysis.append(([a,b,c,d],util))
        
        optkey = [None,None,None,None]
        optval = float("-inf")
        for item in analysis:
            key = item[0]
            val = item[1]
            if(val > optval):
                optkey = key
                optval = val

        return optkey
#This is a simple agent meant to play the game, well, simply.
