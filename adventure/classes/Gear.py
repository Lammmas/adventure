from classes.Base import Item, Container

class Gear(Item):
	"""Gear management"""
	
	def __init__(self, name, description, value, cat, quest):
		super().__init__(name, description, value, cat, quest)

class Armour(Gear):
	"""Armour management - protection etc"""
	
	def __init__(self, name, value, bonus=0, slots=0, cls=0, quest=0):
		self.bonus = bonus
		self.slots = slots
		self.classification = cls

		super().__init__(name, "", value, 2, quest, 0)

class Weapon(Gear):
	"""Weapon management - damage etc"""

	def __init__(self, name, value, quest, area=0, damage=[1, 6], slots=1, ranged=0):
		self.range = area
		self.damage = damage
		self.slots = slots
		self.ranged = ranged == 1

		super().__init__(name, "", value, 1, quest, 0)