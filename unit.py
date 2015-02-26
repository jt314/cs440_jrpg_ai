from __future__ import print_function
import random

def printf(str, *args):
    print(str % args, end='')


# Status Index
# 0 means death
# 1 means guarding
# 2 means covered by
# 3 means Poison
# 4 means Locked


class Unit:
    ClassNames = ("Knight","Wizard","Healer","Mage","Thief")
    HP_Options = (240,100,120,180,80)
    MP_Options = (5,13,30,8,4)
    PATK_Options = (20,5,10,15,40)
    MATK_Options = (0,25,20,15,0)
    Allowable_Actions = ([1,1,1,0,0,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,0],[1,1,0,0,0,1,1,1,0,0],[1,1,0,0,1,1,0,0,0,0],[1,1,0,0,0,0,0,0,1,0])
    
    def __init__(self,x):
    
        #here for paranoia
        self.hp = []
        self.mp = []
        self.patk = 0
        self.matk = 0
        self.actions = []
        self.statuses = []
    
        if(x.__class__ == Unit):
            self.copy(x)
        else:
            self.name = "BullyBob"
            self.job = self.ClassNames[x]
            
            self.hp = [self.HP_Options[x],self.HP_Options[x]]
            self.mp = [self.MP_Options[x],self.MP_Options[x]]
            self.patk = self.PATK_Options[x]
            self.matk = self.MATK_Options[x]
        
            self.actions = self.Allowable_Actions[x]
            self.statuses = [0,0,0,0,0]
                
        
    def copy(self,other):
        self.name = other.name
        self.job = other.job
        self.hp = [other.hp[0],other.hp[1]]
        self.mp = [other.mp[0],other.mp[1]]
        self.patk = other.patk
        self.matk = other.matk
        self.actions = [other.actions[i] for i in range(len(other.actions))]
        self.statuses = [other.statuses[i] for i in range(len(other.statuses))]
    
    def assign_name(self,s="BullyBob"):
        self.name=s

    def receive_damage(self, x):
        if(self.statuses[0]):
            return
        if(self.statuses[1] and x >= 0):
            x /= 3
        self.hp[0] -= x
        if(self.hp[0] > self.hp[1]): 
            self.hp[0] = self.hp[1] + 0
        if(self.hp[0] <= 0):
            #printf("        %s has fallen!\n",self.name)
            self.hp[0] = 0
            self.statuses[0] = True

    def __str__(self):
        return self.name
