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
	#decide whether we want to fight (choose run/fight)
	fight = raw_input("You wanna fight? [Y/N]")

	if fight == "Y":
		#roll for AC
		ac_Roll = random.randint(1,10)
		if ac_Roll>defender.AC:
			#roll for damage
			damage_Roll = random.randint(1,50)
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
	
	if fight == "N":
		#run away
		print "You run away like a bitch."
		
	else:
		print "I didn't understand that input. Choose Y or N."
	
michael = character(10, 4, "michael")
ognut = character(10, 2, "ognut")
	
attack(michael, ognut)