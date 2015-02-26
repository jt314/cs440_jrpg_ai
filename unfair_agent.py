import game
import sys
import unit
import ability
import random

from ability import printf

def list_tuple_truncate(list, index, value):
    temp = []
    for item in list:
        if(item[index] == value):
            temp.append(item)
            
    for item in temp:
        #printf("KILLING %s!!\n",item)
        list.remove(item)
    return


class Agent:
    def __init__(self,depth=16,aggressive=0,defensive=0,nominal=1):
    
        self.AggressiveWeight = aggressive
        self.DefensiveWeight = defensive
        self.NominalWeight = nominal

    def choose(self,game,x):
    
        if x == 0:
            return
            
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]

        AllActions = []        
        if(x == 0):
            AllActions = [MyActions,TheirActions]
        else:
            AllActions = [TheirActions,MyActions]

        
        j1 = [current_state.Teams[x][i].job for i in range(4)]
        j2 = [current_state.Teams[(x+1)%2][i].job for i in range(4)]
        
        printf("ME: %s  %s  %s  %s\n",j1[0],j1[1],j1[2],j1[3])
        printf("THEM: %s  %s  %s  %s\n",j2[0],j2[1],j2[2],j2[3])
       
        
        analysis = []
        
        myproduct = len(MyActions[0])*len(MyActions[1])*len(MyActions[2])*len(MyActions[3])
        theirproduct = len(TheirActions[0])*len(TheirActions[1])*len(TheirActions[2])*len(TheirActions[3])
        lolproduct = myproduct * theirproduct
        
        a = len(MyActions[0])
        b = len(MyActions[1])
        c = len(MyActions[2])
        d = len(MyActions[3])
        
        e = len(TheirActions[0])
        f = len(TheirActions[1])
        g = len(TheirActions[2])
        h = len(TheirActions[3])
        
        
        #printf("ALERT! THE PERMUTATION POOL IS (%d * %d * %d * %d) * (%d * %d * %d * %d) = %d * %d = %d!!!\n\n", a,b,c,d,e,f,g,h,myproduct, theirproduct, lolproduct)
        
        for a in MyActions[0]:
            #printf("ding!\n")
            for b in MyActions[1]:
                #printf("dong!\n")
                for c in MyActions[2]:
                    for d in MyActions[3]:
                        
                        best = float("-inf")
                        worst = float("inf")
                        average = 0
                        util = 0
                        

                        temp = current_state.apply_action([game.Actions[0],[a,b,c,d]])
                                        
                        util = temp[0].utility(x)
                            
                        if(util > best): 
                            best = util
                        if(util < worst): 
                            worst = util
                        average = average + util
                        
                        #average /= (len(e)*len(f)*len(g)*len(h))
                        #printf("WHYYYY %d %d %d\n",best,worst,average)
                        util = self.AggressiveWeight*best + self.DefensiveWeight*worst + self.NominalWeight*average
                        #analysis[[a,b,c,d]] = util
                        analysis.append(([a,b,c,d],util))
                        #printf("Oh come on %s decomposing into %s  %s\n",analysis[-1],analysis[-1][0],analysis[-1][1])



        optkey = [None,None,None,None]
        optval = float("-inf")
        for item in analysis:
            key = item[0]
            val = item[1]
            if(val > optval):
                optkey = key
                optval = val

        printf("OPTKEY IS %s\n\n",optkey)
        return optkey
#This is a simple agent meant to play the game, well, simply.
