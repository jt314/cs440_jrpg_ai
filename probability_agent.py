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
        
    def get_potential(self,game,x,action):
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]

        for act in actions:
            pass

        
    def snag_potential(self,game,x):
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]


    # This agent summates all possible of my actions (With heuristics) against
    # 128 randomly chosen among their (+Heuristic) choices
    def choose(self,game,x):
    
        #Debug stuff
        game.OfficialState.report_teams()
        
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]
        
        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]

        AllActions = []        
        if(x == 0):
            AllActions = [MyActions,TheirActions]
        else:
            AllActions = [TheirActions,MyActions]

        #MUST REDUCE HERE
        
        """
        Ideas for reduction:
        
        (1) Mages, Wizards, and Healers will NOT basic-attack if they have mana
        (2) Thieves will only poison OR attack, never both.
        
        
        """

                
        j1 = [current_state.Teams[x][i].job for i in range(4)]
        j2 = [current_state.Teams[(x+1)%2][i].job for i in range(4)]
        
        #printf("ME: %s  %s  %s  %s\n",j1[0],j1[1],j1[2],j1[3])
        #printf("THEM: %s  %s  %s  %s\n",j2[0],j2[1],j2[2],j2[3])
        
        for i in range(2):
            for j in range(4):
                if(AllActions[i][j] == [None]): continue
                #printf("WHat the hell %d %d\n",i,j)
                #printf("Surprise! It's %s\n", AllActions[i][j])
            
            
                guy = current_state.Teams[i][j]
                if (guy.job == "Wizard" or guy.job == "Healer" or guy.job == "Mage"):
                    if(guy.mp[0] > 0):
                        c1 = len(AllActions[i][j])
                        list_tuple_truncate(AllActions[i][j],1,0) #Truncate all Attack commands
                        c2 = len(AllActions[i][j])
                        if(c1 == c2):
                            printf("OH SHIT!!!!\n")
                   
                if(guy.job == "Thief" and guy.mp[0] > 0):
                    
                
                    for k in range(4):
                        if(current_state.Teams[(i+1)%2][k].statuses[0]): continue
                    
                        #if poisoned, kill Poison
                        if (current_state.Teams[(i+1)%2][k].statuses[3]): 
                            AllActions[i][j].remove(((i,j),8,((i+1)%2,k))) #If Poisoned, drop Poison
                    
                        #else if max HP above 150, then drop Attack
                        else:
                        #elif (current_state.Teams[(i+1)%2][k].hp[1] >= 150): 
                            AllActions[i][j].remove(((i,j),0,((i+1)%2,k)))
                    
                        #else drop Poison
                        #else: 
                            #AllActions[i][j].remove(((i,j),8,((i+1)%2,k)))
        
        #end for
        
     
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

        contenders = snag_choices(TheirActions,self.depth)
        
        for a in MyActions[0]:
            printf("ding!\n")
            for b in MyActions[1]:
                #printf("dong!\n")
                for c in MyActions[2]:
                    for d in MyActions[3]:
                        
                        best = float("-inf")
                        worst = float("inf")
                        average = 0
                        util = 0
                       
                        for act in contenders:
                            temp = None
                            if (x ==0):
                                temp = current_state.apply_action([[a,b,c,d],act])
                            elif (x == 1):
                                temp = current_state.apply_action([act,[a,b,c,d]])
                            util = temp[0].utility(x)
                            #printf("GOD DAMN IT %d\n\n",util)
                            if(util > best): 
                                best = util
                            if(util < worst): 
                                worst = util
                            average = average + util
                        
                        average /= self.depth
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
