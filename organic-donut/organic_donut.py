#!/usr/bin/env python

import random
import sys
import collections

class character:
    def __init__(self, HP, AC, name):
        self.HP = HP
        self.AC = AC
        self.name = name	
        self.inventory = []

    def list_inventory():
        self.counted_inventory = collections.Counter(self.inventory)
        for x in self.counted_inventory:
            thing = x
            num = self.counted_inventory[x]
            if num < 2:
                print self.name + " has " + str(num) + " " + thing
            else:
                print self.name + " has " + str(num) + " " + thing + "s" #this is bad and I feel bad about it

class inv_item:
    def __init__(self, size=1):
        self.size = size

#keep inventory as a list, and check len(inventory) to make sure we're not over?
#each item in the list is an object (an instance of a class)
#if we're going to just get len(inventory), we'll need to override len for the inventory data type to sum all item sizes
class sword(inv_item):
    def __init__(self, name, add_hp):
        inv_item(self, 2)
        

def attack(attacker, defender):
    '''Takes two objects, makes them fight. Returns victor'''
    #roll for AC
    ac_Roll = random.randint(1,10)
    if ac_Roll>defender.AC:
        #roll for damage
        damage_Roll = random.randint(1,5)
        print attacker.name + " hit " + defender.name + " for " + str(damage_Roll) + " points."
        #deduct damage from HP
        defender.HP = defender.HP - damage_Roll
        
        if defender.HP <= 0: #defender loses
            print defender.name + " loses."
            return attacker, defender
 
        if defender.HP > 0: #defender doesn't lose
            return attacker, defender

    else:
        print attacker.name + " missed their attack."
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
    while player.HP > 0 and not_player.HP > 0:
        #decide whether we want to fight (choose run/fight)
        action = str(raw_input("Do you want to [F]ight or [R]un?"))
        #should we choose who attacks first, or randomize it?
        #do we always allow the player to chose whether they're going to fight?
        #can they be attacked without warning?
        if "f" in action.lower():
            attack(player, not_player)
            if not_player.HP > 0:
                attack(not_player, player)
        if "r" in action.lower():
            run_away(player, not_player)
    if not_player.HP <= 0:
        print(not_player.name + " Died.\n")
    else:
        print("\033[1;31;40mYou Died.\n") 


#create your characters
michael = character(10, 4, "Michael")
ognut = character(10, 4, "Ognut")
	
fight(michael, ognut)

#####
#NOTES SECTION
#####
#right now we're stuck in an endless fight/run loop until someone dies.
#That's an allegory or something, but I guess we need some concept of location(?)
#so that you can run _away_.
#Thoughts on location:
#each room object has four directions (NSEW), and directions with doorways/other rooms have those rooms listed.
#Directions that are blocked should list what is blocking them (wall, locked door, etc)
#Each room can have a method for getting the inventory of the room (most will just list inventory, some may start a fight, or list inventory that can be interacted with?)
#
###
#upon entering a room for the first time, give a quick inventory. Entering the room subsequent times will not?
#'look' command will give you full inventory of a room
#'inventory' (or just 'i'?) command will show your inventory
