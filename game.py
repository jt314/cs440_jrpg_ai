from __future__ import print_function
import unit
import ability
from ability import printf
import random
import os

#Classes = [unit.Knight,unit.Wizard,unit.Medic,unit.Mage,unit.Thief]
#Classes = [unit.Thief,unit.Thief,unit.Thief,unit.Thief,unit.Thief]

TeamNames = ('RED','BLU')


class Game:
    def __init__(self):
        self.Agents = [None,None]
        self.Actions = [[None,None,None,None],[None,None,None,None]]
        self.PlayByPlay = []
        self.OfficialState = None
        self.Verbose = False
        
    def playGame(self,redagent,blueagent,verbose = False):
        self.Verbose = verbose
        self.Agents[0] = redagent
        self.Agents[1] = blueagent
        self.OfficialState = GameState()
        
        while(self.OfficialState.teamscore(0) > 0 and self.OfficialState.teamscore(1) > 0): #While not a terminal state
            self.PlayByPlay = []

            for i in range(2):
                for j in range(4):
                    self.OfficialState.Teams[i][j].statuses[1] = None
                    self.OfficialState.Teams[i][j].statuses[2] = None    

            
            self.Actions[0] = self.Agents[0](self,0)
            self.Actions[1] = self.Agents[1](self,1)            
            
            temp = self.OfficialState.apply_action(self.Actions)
            
            self.OfficialState = temp[0]
            self.PlayByPlay = temp[1]
            
            if(verbose):
                os.system('cls' if os.name == 'nt' else 'clear')
                for item in self.PlayByPlay:
                    if(item[0] is None):
                        printf("ALERT: %s takes %d damage from poison!\n",item[3][0],item[4][0])
                    else:
                        printf("%s uses %s!\n",item[0],ability.Names[item[1]])
                        
                        if(item[1] == 1): #if guard 
                            continue
                        
                        for i in range(len(item[3])):
                            if(item[2][i] != item[3][i]):
                                printf("    %s is protected by %s!\n",item[2][i],item[3][i])
                            if(item[4][i] is True):
                                if(item[1] == 2): #if Cover
                                    printf("    %s protects %s!\n",item[0],item[3][i])

                            else:
                                if(item[4][i] > 0):
                                    printf("    %s takes %d damage!\n",item[3][i],item[4][i])
                                    if(item[1] == 8): #if Poison
                                        printf("        %s is poisoned!\n",item[3][i])
                                    if(item[3][i].statuses[0]):
                                        printf("        %s has fallen!\n",item[3][i])
                                
                                if(item[4][i] < 0):
                                    printf("    %s heals %d HP!\n",item[3][i],-item[4][i])
                                    if(item[3][i].statuses[0]):
                                        printf("        Unfortunately, %s remains dead.\n",item[3][i])
                                
                blah = raw_input('Press ENTER to continue: ')
                os.system('cls' if os.name == 'nt' else 'clear')
            
                
        if(self.OfficialState.teamscore(0) > 0):
            return 0
        if(self.OfficialState.teamscore(1) > 0):
            return 1
        return -1
            




class GameState:

    def copy(self,other):
        for j in range(4):
            for i in range(2):
                self.Teams[i][j] = unit.Unit(other.Teams[i][j])    #COPY!!!    


            
    def __init__(self,other = None):
        self.Teams = [[None,None,None,None],[None,None,None,None]]
        self.FirstMove = 0
        
        if(other is None):
            self.Teams = [[None,None,None,None],[None,None,None,None]]
            for j in range(4):
                for i in range(2):
                    self.Teams[i][j] = unit.Unit(j)#random.randint(0,4))
                    self.Teams[i][j].assign_name(TeamNames[i] + " " + str(j) + " the " + self.Teams[i][j].job)
        else:
            self.copy(other)





    def get_actions(self,x,y):
        x = x % 2
        y = y % 4
        returnme = []
        
        if(self.Teams[x][y].statuses[0]): return [None]
        
        for z in range(9):
            if(self.Teams[x][y].actions[z] == 0): continue
            if(ability.Costs[z] > self.Teams[x][y].mp[0]): continue
            
            a = ability.targetingType(z)
            b = (x+1)%2
            
            
            
            
            if a == 0: #self only
                returnme.append(((x,y),z,(x,y)))
                
            elif a == 1: #Target Ally
                for i in range(4):
                    if(not self.Teams[x][i].statuses[0]):
                        returnme.append(((x,y),z,(x,i)))    
            
            elif a == 2: #All Allies
                returnme.append(((x,y),z,(x,)))
            
            elif a == 3:
                for i in range(4):
                    if(not self.Teams[b][i].statuses[0]):
                        returnme.append(((x,y),z,(b,i)))
            
            elif a == 4:
                returnme.append(((x,y),z,(b,)))
                
            elif a == 5: #Target Dead Ally
                for i in range(4):
                    if(self.Teams[x][i].statuses[0]):
                        returnme.append(((x,y),z,(x,i)))
                
                
        if (len(returnme) == 0): return [None]
        return returnme


    def numAlive(self,x):
        #printf("NOOOO!!!!! %s\n\n",x)
        n = 4
        for guy in self.Teams[x]:
            if(guy.statuses[0]):
                n -= 1
        return n

    def getDamagePotential(self,x):

        #printf("NOOOwdfwfO!!!!! %s\n\n",x)

        returnme = [0,0,0,0,0,0,0,0]
        for i in range(4):
            for item in self.get_actions(x,i):
                if(item is None): continue
                if(item[1] == 1 or item[1] == 2 or item[1] == 5 or item[1] == 6 or item[1] == 7): continue
                if(item[1] == 0 or item[1] == 8):
                    Z = self.Teams[x][i].patk
                    if(Z > returnme[2*i]):
                        returnme[2*i] = Z
                    if(returnme[2*i+1] < Z):
                        returnme[2*i+1] = Z
                if(item[1] == 3):
                    Z = 3*self.Teams[x][i].matk
                    if(returnme[2*i] < Z):
                        returnme[2*i] = Z
                    if(returnme[2*i+1] < Z ):
                        returnme[2*i+1] = Z

                if(item[1] == 4):
                    Z = self.Teams[x][i].matk
                    #printf("HMM... %s\n",self.numAlive((x+1)%2))
                    if(returnme[2*i] < Z):
                        returnme[2*i] = Z
                    if(returnme[2*i+1] <  Z*self.numAlive((x+1)%2) ):
                        returnme[2*i+1] = Z*self.numAlive((x+1)%2)
        return returnme



    def report_teams(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for guy in self.Teams[0]+self.Teams[1]:
            printf("%s:    HP:%d/%d    MP:%d/%d    ",guy.name,guy.hp[0],guy.hp[1],guy.mp[0],guy.mp[1])
            if(guy.statuses[0]):
                printf("DEAD ")
            if(guy.statuses[3]):
                printf("POISONED ")
            if(guy.statuses[4]):
                printf("LOCKED")
            printf("\n")
        printf("\n\n")
        
    def teamscore(self,x):
        multy = 4
        total = 0
        for guy in self.Teams[x]:
            if(guy.statuses[0]):
                multy -= 1
            else:
                total = guy.hp[0] #+ 10*guy.mp[0]
        return total*multy
        
    def score(self):
        return (teamscore(0),teamscore(1))
        
    def utility(self,x):
        return self.teamscore(x) - self.teamscore((x+1)%2)
    
    # This function returns the state that would result after applying this action.
    # Its return value is a list of two elements
    # the first element is the new state
    # the second state is the associated Play-By-Play (readout of what happened)
    def apply_action(self,actions):
        #printf("WOOO! WOOO!    %s\n",actions)
        returnme = GameState(self)
        returnme.FirstMove = (self.FirstMove + 1)%2
        KNIGHTS = []
        WIZARDS = []
        MEDICS = []
        MAGES = []
        THIEVES = []
        PREEMPT = []

        teamorder = []
        
        if(self.FirstMove%2 == 0):
            teamorder.append(0)
            teamorder.append(1)
            
        else:
            teamorder.append(1)
            teamorder.append(0)
        
        
        
        
        for j in range(4):
            for i in teamorder:
                #printf("OH NO!!!! %s %s\n\n",actions[0],actions[1])
                #printf("OH NO!!!! %s %s %s\n\n",i,j,actions[0])
                if(actions[i][j] is None): continue
                if(returnme.Teams[i][j].hp[0] > 0 and not returnme.Teams[i][j].statuses[0]):
                    if(actions[i][j][1] in [1,2,7]):
                        PREEMPT.append((i,j))
                    elif(returnme.Teams[i][j].job == "Knight"):
                        KNIGHTS.append((i,j))
                    elif(returnme.Teams[i][j].job == "Wizard"):
                        WIZARDS.append((i,j))
                    elif(returnme.Teams[i][j].job == "Healer"):
                        MEDICS.append((i,j))
                    elif(returnme.Teams[i][j].job == "Mage"):
                        MAGES.append((i,j))
                    elif(returnme.Teams[i][j].job == "Thief"):
                        THIEVES.append((i,j))
        
        TODO = PREEMPT+THIEVES+MAGES+KNIGHTS+WIZARDS+MEDICS
        PlayByPlay = []
        
        #printf("%s\n",TODO)

        for doit in TODO:            
            #Translate into pointers
            #printf("ALERT! ALERT!    %s\n\n",doit)
            #printf("ALERT! ALERT!    %s\n\n",returnme.Teams)
            subject = returnme.Teams[doit[0]][doit[1]]
            action = actions[doit[0]][doit[1]][1]
            target = None
            
            targetinglist = actions[doit[0]][doit[1]][2]
            
            
            
            #printf("WOOO WOOO %s\n",targetinglist)
            if(len(targetinglist) == 1):
                target = returnme.Teams[targetinglist[0]]
            else:
                target = [returnme.Teams[targetinglist[0]][targetinglist[1]]]
            
            #activate the ability
            PlayByPlay.append(ability.doAbility(subject,action,target))
    
        for i in range(2):
            for j in range(4):
                if(returnme.Teams[i][j].statuses[3]):
                    pdmg = returnme.Teams[i][j].hp[1]/5
                    if(returnme.Teams[i][j].statuses[1]):
                        pdmg *= 3
                    returnme.Teams[i][j].receive_damage(pdmg)
                    PlayByPlay.append([None,None,None,[returnme.Teams[i][j]],[ability.reportDamage(pdmg,returnme.Teams[i][j])],None])
        
        return (returnme,PlayByPlay)

def isuint(s):
    try:
        return (int(s) >= 0)
    except ValueError:
        return False

def namedisplay(state, listoftargets):
    #printf("LALALALALA %s\n\n\n",listoftargets)
    if(listoftargets == (0)):
        return 'RED'
    if(listoftargets == (1)):
        return 'BLU'
    return str(state.Teams[listoftargets[0]][listoftargets[1]])

def list_tuple_find(list, index, value):
    for item in list:
        if(item[index] == value):
            return True
    return False
    
    
def manual_choice(game,team):
    returnme = [None,None,None,None]
    
    # Now to actually describe the actions
    thestate = game.OfficialState
    for i in range(4):
        os.system('cls' if os.name == 'nt' else 'clear')

        
        
        for guy in thestate.Teams[0]+thestate.Teams[1]:
            printf("%s:    HP:%d/%d    MP:%d/%d    ",guy.name,guy.hp[0],guy.hp[1],guy.mp[0],guy.mp[1])
            if(guy.statuses[0]):
                printf("DEAD ")
            if(guy.statuses[3]):
                printf("POISONED ")
            if(guy.statuses[4]):
                printf("LOCKED")
            printf("\n")

        printf("\n\n")
    
    
        if(thestate.Teams[team][i].hp < 0 or thestate.Teams[team][i].statuses[0]):
            pass
        else: #if actual thingie
        
            blahlist = thestate.get_actions(team,i)
        
            a = thestate.Teams[team][i]
            printf("%s's Turn: \n\n", a)
            for j in range(10):
                if(a.actions[j] != 0 and ability.Costs[j] <= a.mp[0] and list_tuple_find(blahlist,1,j)):
                    printf("%d: %s\n",j,ability.Names[j])
            validaction = False
            s = -1
            while(not validaction):
                printf("Pick Ability");
                s = raw_input(': ')
                if(not isuint(s)):
                    s = '9999'
                s = int(s)
                validaction = (s < 10 and a.actions[s] != 0 and ability.Costs[s] <= a.mp[0] and list_tuple_find(blahlist,1,s))

            #Now that the action has been made:
            
            
            
            if(ability.targetingType(s) == 0):
                returnme[i] = ((team,i),s,(team,i))
                
            elif(ability.targetingType(s) == 2): #AE ally
                returnme[i] = ((team,i),s,(team,))
                
            elif(ability.targetingType(s) == 4): #AE enemy
                returnme[i] = ((team,i),s,((team+1)%2,))
                
            else: #Begin Selection of targets
            
                validtarget = False
                
                blahlist = thestate.get_actions(team,i)
                
                targetlist = []
                for item in blahlist:
                    #printf("%s\n",item)
                    if(item[1] == s):
                        targetlist.append(item)
                #now that the target list is cleaned
                
                
                for j in range(len(targetlist)):
                    #printf("%s\n",targetlist[j])
                    printf("%d: %s\n",j,namedisplay(thestate,targetlist[j][2]))
                t = -1
                
                
                while(not validtarget):
                    printf("Pick Target",);
                    t = raw_input(': ')
                    if(not isuint(t)):
                        t = '9999'
                    t = int(t)
                    validtarget = (t < len(targetlist))
                returnme[i] = (targetlist[t])

    return returnme


