from classes.Base import Actor, Dice
from math import floor

class Player(Actor):
	"""The Player class"""

	# 0 = no armor, 1 = light armor, 2 = medium armor, 3 = heavy armor & shields
	armor_level = 0

	classes = [
		"None",
		"Fighter",
		"Rogue",
		"Mage",
		"Cleric"
	]

	races = [
		"Special"
		"Human",
		"Elf",
		"Dwarf",
		"Halfling",
	]

	def __init__(self, name, description, strength=10, dexterity=10, mind=10, race=1, classification=1):
		self.level = 1
		self.experience = 0

		# Initial bonuses
		self.bonuses = {
			"roll": {
				'attack': 0,
				'damage': 0,
				'save': 0,
				'luck': 0
			},
			'stats': {
				'strength': floor((strength - 10) / 2),
				'dexterity': floor((dexterity - 10) / 2),
				'mind': floor((mind - 10) / 2),
				'armor': 0
			}
		}

		if self.bonuses['stats']['strength'] > 0:
			strength += self.bonuses['stats']['strength']
		if self.bonuses['stats']['dexterity'] > 0:
			dexterity += self.bonuses['stats']['dexterity']
		if self.bonuses['stats']['mind'] > 0:
			mind += self.bonuses['stats']['mind']

		if classification == 1:
			self.bonuses['roll']['attack'] = 1
			self.bonuses['roll']['damage'] = 1
		if classification == 3 or classification == 3:
			self.mana = self.mind + Dice.roll()

		self.__set_stats(strength, dexterity, mind, race, classification)
		self.health = self.strength + Dice.roll()

		# Race Bonuses
		if race == 2:
			self.mind += 2
		elif race == 3:
			self.strength += 2
		elif race == 4:
			self.dexterity += 2
		
		super().__init__(name, description)

	def __set_stats(self, strength, dexterity, mind, race, classification):
		# Base stats
		self.strength = strength
		self.dexterity = dexterity
		self.mind = mind
		self.race = self.races[race]
		self.classification = self.classes[classification]

		# Skills
		self.physical = self.level
		self.superfuge = self.level
		self.knowledge = self.level
		self.communication = self.level

		# Class bonuses
		if classification == 1:
			self.armor_level = 3
			self.physical += 3 + floor(self.level / 5)
		elif classification == 2:
			self.armor_level = 1
			self.superfuge += 3
		elif classification == 3:
			self.armor_level = 0
			self.knowledge += 3
		elif classification == 4:
			self.armor_level = 2
			self.communication += 3

		self.armor = 10 + self.bonuses['stats']['dexterity'] + self.bonuses['stats']['armor']

	def level_up():
		self.level += 1
		self.experience = 0

		self.health += Dice.roll()
		self.bonuses['roll']['attack'] += 1

		if self.level % 3 == 0:
			# Ask user if add +1 to STR, DEX or MIND
			selection = 0
			while True:
				print("Add +1 stat to...")
				print("1) Strength")
				print("2) Dexterity")
				print("3) Mind")

				try:
					selection = int(input("? "))
					if selection < 1 or selection > 3:
						raise ValueError
				except ValueError:
					print("Not a valid number!")
					continue
				else:
					break 
			
			if selection == 1:
				self.strength += 1
			elif selection == 2:
				self.dexterity += 1
			elif selection == 3:
				self.mind += 1