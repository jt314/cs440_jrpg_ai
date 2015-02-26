import game
import exhaustive_agent
import search_agent
import probability_agent
import enhn_probability_agent
import oldenhn_probability_agent
import reduction_agent
import unfair_agent
import random_agent
import os

if (__name__ == '__main__'):
    os.system('cls' if os.name == 'nt' else 'clear')
    print "Hello World!"
    lolgame = game.Game()
    x = lolgame.playGame(enhn_probability_agent.Agent(64,0,1,0).choose, unfair_agent.Agent(16,0,1,0).choose,False)
    #x = lolgame.playGame(enhn_probability_agent.Agent(32,0,1,0).choose, probability_agent.Agent(64,0,1,0).choose,False)
    #x = lolgame.playGame(game.manual_choice, unfair_agent.Agent(32,0,1,0).choose,True)
    #x = lolgame.playGame(game.manual_choice, probability_agent.Agent().choose,True)
    #x = lolgame.playGame(game.manual_choice, game.manual_choice,True)
    print str(x) + " WINS!"
    
