from classes.Base import Actor, Dice

class Npc(Actor):
	"""General NPCs or Monsters"""

	def __init__(self, name="", description="", race="animal", level=0, damage=[0,0,0], effect=[0,0,0], intelligence=0, text=""):
		self.intelligence = intelligence
		self.damage = damage
		self.poison = effect
		self.set_level(level)
		self.text = text

		super().__init__(name, description)

	def set_level(self, level):
		dice_count = self.damage[0] + level - 1
		dice_size = self.damage[1]

		if dice_count / self.damage[0] >= 2:
			dice_size += int(dice_count / self.damage[0])
			dice_count = int(dice_count / 2)

		self.hit = Dice.roll(dice_size, dice_count) + self.damage[2] + self.intelligence

		# Skills
		self.physical = self.hit + dice_count + self.intelligence
		self.superfuge = self.hit + dice_count + self.intelligence
		self.knowledge = self.hit + dice_count
		self.communication = self.hit + dice_count
		self.level = level