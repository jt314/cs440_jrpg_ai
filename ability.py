from __future__ import print_function
from unit import *
import random

#def printf(str, *args):
 #   print(str % args, end='')

Names = ["Attack","Guard","Cover","SpotNuke","AENuke","Heal","Heal2","Revive","Poison","INVALID_ACTION"]

DisplayNames = ["Attack","Guard","Cover","SpotNuke","AENuke","Heal1","Heal2","Revive","Attack","Attack","GET OUT OF JAIL FREE!",]

Costs = [0,0,0,2,1,1,5,5,1,5,0,0,0,0]

# This function determines if an ability is retargetable,
# i.e. if Cover works on it.

def isCoverable(action):
    returnables = [True,False,False,True,True,False,False,False,True,True,False]
    return returnables[action]

def targetingType(action):
    #Return Values:
    # 0 for self
    # 1 for ST Ally
    # 2 for AE Ally
    # 3 for ST Enemy
    # 4 for AE Enemy
    # 5 for Target Dead Ally
    returnables = [3,0,2,3,4,1,2,5,3,3]
    return returnables[action]

    
def resolveCover(target):
    for i in range(len(target)):
        if(target[i].statuses[2]):
            target[i] = target[i].statuses[2]


def reportDamage(x,guy):
    if(guy.statuses[1] and x >= 0):
        return x/3
    return x

# This function will handle the act of subjects
# performing their abilities against their targets.
# 
# subject - Unit, the person acting
# action - the action being performed, symbolized by an int
# target - list of targets, also Units
#
# Return Value
# [subject, action,[intended targets], [actual targets],[results]]
def doAbility(subject, action, target):

    if(subject.statuses[0] or(subject.statuses[4] and action != 10)):
        #printf("%s can't move!\n",subject)
        return [subject,-1,[],[],[],-1]

    returnme = [subject,action,[],[],[]]


    for item in target:
        returnme[2].append(item)
        returnme[3].append(item)
    
    if(isCoverable(action)):
        resolveCover(returnme[3])

    #returnme[3] = target

    #printf("%s uses %s!\n",subject,DisplayNames[action])

    a = subject
    a.mp[0] -= Costs[action]

    for b in returnme[3]:
        
        if action == 0: #basic attack       
            dmg = a.patk
            b.receive_damage(dmg)
            returnme[4].append(reportDamage(dmg,b))
            
        elif action == 1: #guard
            a.statuses[1] = True
            returnme[4].append(True)
            
        elif action == 2: #Cover
            b.statuses[2] = a
            returnme[4].append(True)
            pass
            
        elif action == 3: #Nuke1
            dmg = 3*(a.matk)
            b.receive_damage(dmg)
            returnme[4].append(reportDamage(dmg,b))

            
        elif action == 4: #Nuke2
            dmg = a.matk  
            b.receive_damage(dmg)
            returnme[4].append(reportDamage(dmg,b))
            
        elif action == 5: #Heal1
            dmg = -2*a.matk
            b.receive_damage(dmg)
            returnme[4].append(dmg)


        elif action == 6: #Heal2
            dmg = -3*a.matk
            b.receive_damage(dmg)
            returnme[4].append(dmg)
            
        elif action == 7: #Revive
            b.statuses[0] = None
            b.receive_damage(-1*b.hp[1])
            returnme[4].append(-1*b.hp[1])
            
        elif action == 8: #Poison
            b.statuses[3] = True
            dmg = a.patk
            b.receive_damage(dmg)
            returnme[4].append(reportDamage(dmg,b))
          
    return returnme
        
            
    
