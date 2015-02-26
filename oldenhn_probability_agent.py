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
    

def is_item_in_list(item,list):
    try:
        list.index(item)
        return True
    except ValueError:
        return False

def find_weakest_guy(team):
    returnme = -1
    val = float("inf")
    for i in range(4):
        if(team[i].statuses[0]): continue
        if(team[i].hp[0] < val):
            val = team[i].hp
            returnme = i
    return returnme

    
def find_most_injured_guy(team):
    returnme = -1
    val = float("-inf")
    for i in range(4):
        if(team[i].statuses[0]): continue
        x = team[i].hp[1] - team[i].hp[0]
        if(x > val):
            val = x
            returnme = i
    return returnme

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
    def __init__(self,depth=64,aggressive=0,defensive=1,nominal=0):
    
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


    def get_good_options(self,game,x):
        
        #Reduce the list of possible actions in accordance with the following principles:

        #Only One person at a time should shield anyone

        #

        #
        current_state = game.OfficialState
        state = current_state

        MyActions = [current_state.get_actions(x,i) for i in range(4)]
        TheirActions = [current_state.get_actions((x+1)%2,i) for i in range(4)]

        MyResults = []
        TheirResults = []
        
        for a in MyActions[0]:
            for b in MyActions[1]:
                for c in MyActions[2]:
                    for d in MyActions[3]:
                        guardcount = 0
                        shieldcount = 0
                        yay = True
                        LIST = [a,b,c,d]
                        for i in range(4):
                            if yay:
                                #printf("IJGOEGJOEGHJ %s  %s\n",x,i)
                                guy = state.Teams[x][i]
                                Z = LIST[i]
                                if(Z is None): continue
                                if(Z[1] == 2):
                                    shieldcount += 1
                                    if(guardcount > 0 or shieldcount > 1):
                                        yay = False
                                if(Z[1] == 1):
                                    guardcount += 1
                                    #If Not Capable of Dying
                                    list = state.getDamagePotential(x)
                                    sum = list[0]+list[2]+list[4]+list[6]
                                    if(sum >= guy.hp[0]):
                                        yay = False
                                if(Z[1] == 0):
                                    if(guy.mp[0] > 0 and guy.actions[8] != 0 and state.Teams[Z[2][0]][Z[2][1]].statuses[3]):
                                        yay = False
                                if(Z[1] == 0 or Z[1] == 3):
                                    if(Z[2][1] != find_most_injured_guy(state.Teams[Z[2][0]])):
                                       yay = False
                                       
                        #end for
                        if(yay):
                            MyResults.append(LIST)
                                       
        for a in TheirActions[0]:
            for b in TheirActions[1]:
                for c in TheirActions[2]:
                    for d in TheirActions[3]:
                        guardcount = 0
                        shieldcount = 0
                        yay = True
                        LIST = [a,b,c,d]
                        for i in range(4):
                            if yay:
                                guy = state.Teams[(x+1)%2][i]
                                Z = LIST[i]
                                if(Z is None): continue
                                if(Z[1] == 2):
                                    shieldcount += 1
                                    if(guardcount > 0 or shieldcount > 1):
                                        yay = False
                                if(Z[1] == 1):
                                    guardcount += 1
                                    #If Not Capable of Dying
                                    list = state.getDamagePotential(x)
                                    sum = list[0]+list[2]+list[4]+list[6]
                                    if(sum >= guy.hp[0]):
                                        yay = False
                                if(Z[1] == 0):
                                    if(guy.mp[0] > 0 and guy.actions[8] != 0 and state.Teams[Z[2][0]][Z[2][1]].statuses[3]):
                                        yay = False
                                if(Z[1] == 0 or Z[1] == 3):
                                    if(Z[2][1] != find_most_injured_guy(state.Teams[Z[2][0]])):
                                       yay = False
                                    
                                    

                        #end for
                        if(yay):
                            TheirResults.append(LIST)


        return [MyResults,TheirResults]                                

        


    # This agent summates all possible of my actions (With heuristics) against
    # 128 randomly chosen among their (+Heuristic) choices
    def choose(self,game,x):
    
        #Debug stuff
        game.OfficialState.report_teams()
    
        current_state = game.OfficialState
        FinalAnswer = [None,None,None,None]

        #printf("GOD DAMN IT!!!    %s\n\n\n\n",x)

        TheActions = self.get_good_options(game,x)
        
        MyActions = TheActions[0]
        TheirActions = TheActions[1]

        random.shuffle(TheirActions)

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

     
        analysis = []
        
        
        #printf("ALERT! THE PERMUTATION POOL IS (%d * %d * %d * %d) * (%d * %d * %d * %d) = %d * %d = %d!!!\n\n", a,b,c,d,e,f,g,h,myproduct, theirproduct, lolproduct)

        #contenders = snag_choices(TheirActions,self.depth)
        
        ide = 0
        for lol in MyActions:
            ide += 1
            if(ide % 50 == 0):
                printf("ding %s/%s!\n",ide,len(MyActions))
            best = float("-inf")
            worst = float("inf")
            average = 0
            util = 0
            
            for act in TheirActions[:self.depth]:

                #printf('OH COME ON %s    %s\n\n\n\n',lol,act)
                temp = None
                if (x ==0):
                    temp = current_state.apply_action([lol,act])
                elif (x == 1):
                    temp = current_state.apply_action([act,lol])
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
            analysis.append((lol,util))
            #printf("Oh come on %s decomposing into %s  %s\n",analysis[-1],analysis[-1][0],analysis[-1][1])
        
        optkey = [None,None,None,None]
        #if(len(analysis) == 0):
            #printf("NO NO NO NO NOOOO!!!!!\n\n\n")
            #raw_input()
        optval = float("-inf")
        for item in analysis:
            #printf("wgwegwoij %s\n",item)
            key = item[0]
            val = item[1]
            if(val > optval):
                optkey = key
                optval = val

        printf("OPTKEY IS %s\n\n",optkey)
        #raw_input()
        return optkey
#This is a simple agent meant to play the game, well, simply.
