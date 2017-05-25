#!/usr/bin/env python

import random
import sys

class character:
    def __init__(self, HP, AC, name):
        self.HP = HP
        self.AC = AC
        self.name = name
	
def attack(attacker, defender):
    '''Takes two objects, makes them fight. Returns victor'''
    #roll for AC
    ac_Roll = random.randint(1,10)
    if ac_Roll>defender.AC:
        #roll for damage
        damage_Roll = random.randint(1,10)
        print attacker.name + " hit " + defender.name + " for " + str(damage_Roll) + " points."
        #deduct damage from HP
        defender.HP = defender.HP - damage_Roll
        
        if defender.HP <= 0: #defender loses
            print defender.name + " loses."
            sys.exit()
        
        if defender.HP > 0: #defender doesn't lose
            return attacker, defender

    else:
        print "You missed, sucka."
        return attacker, defender

def run_away(runner, striker):
    ac_Roll = random.randint(1,5)
    if ac_Roll>runner.AC:
        damage_Roll = random.randint(1,15)
        print striker.name + " hit " + runner.name + " for " + str(damage_Roll) + " points."
        runner.HP = runner.HP - damage_Roll
    else:
        print "You escaped, you coward."

def fight(player, not_player):
    while player.HP > 0:
        #decide whether we want to fight (choose run/fight)
        action = str(raw_input("Do you want to fight or run? [Fight/Run]"))
        #should we choose who attacks first, or randomize it?
        #do we always allow the player to chose whether they're going to fight?
        #can they be attacked without warning?
        if "fight" in action.lower():
            attack(player, not_player)
        if "run" in action.lower():
            run_away(player, not_player)
    print ("\033[1;31;40mYou Died.\n") 


#create your characters
michael = character(10, 4, "michael")
ognut = character(10, 2, "ognut")
	
fight(michael, ognut)

#####
#NOTES SECTION
#####
#right now we're stuck in an endless fight/run loop until someone dies.
#That's an allegory or something, but I guess we need some concept of location(?)
#so that you can run _away_.
###
#we also need the computer to fight back - turns.
