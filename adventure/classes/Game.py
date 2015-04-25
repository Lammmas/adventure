from classes.Player import Player
from classes.Base import Item, Dice, Container, parse
from classes.Gear import *
from classes.Map import Map
from classes.Npc import Npc

class Game:
	"""The main game functionality"""

	__weapons = {}
	__armour = {}
	__gear = {}
	__npc = {}

	def __init__(self):
		# Want to have a set "Gold" Item, because currency is the same everywhere
		self.copper = Item("Copper coin", "", 0.01, 0)
		self.silver = Item("Silver coin", "", 0.1, 0)
		self.gold = Item("Gold coin", "", 1, 0)
		self.platinum = Item("Platinum coin", "", 10, 0)

		# Same thing with items
		weapons = parse("weapons.csv")
		armour = parse("armour.csv")
		gear = parse("gear.csv")
		npc = parse("npc.csv")

		for weapon in weapons:
			# {'Name': 'Spear', 'Price': 2, 'Slots': 2, 'Roll': [1, 8], 'Range': 6, 'Ranged': 0, 'Quest': 0}
			self.__weapons[weapon['Name'].lower()] = Weapon(weapon['Name'], weapon['Price'], weapon['Quest'], weapon['Range'], weapon['Roll'], weapon['Slots'], weapon['Ranged'])

		for armor in armour:
			# {'Name': 'Tower Shield', 'Price': 30, 'Slots': 1, 'Bonus': 4, 'Class': 3, 'Quest': 0}
			self.__armour[armor['Name'].lower()] = Armour(armor['Name'], armor['Price'], armor['Bonus'], armor['Slots'], armor['Class'], armor['Quest'])

		for item in gear:
			#{'Name': 'Winter Blanket', 'Description': '', 'Value': '0.5', 'Quest': 0, 'Container': 0, 'Capacity': 0}
			if item['Container'] == 0:
				self.__gear[item['Name'].lower()] = Gear(item['Name'], item['Description'], item['Value'], 3, item['Quest'], item['Container'], item['Capacity'])
			else:
				self.__gear[item['Name'].lower()] = Container(item['Name'], item['Description'], 0, item['Capacity'])

		for creature in npc:
			#{'Attack': [4, 8, 2], 'Armor': 14, 'Effect': [1, 2, -2], 'Damage': [1, 2, -2], 'Name': 'Scorpion'}
			self.__npc[creature['Name'].lower()] = Npc(creature['Name'], creature['Description'], creature['Race'], 1, creature['Damage'], creature['Effect'], creature['Intelligence'])

		self.map = Map()

	def run(self):
		self.__setup()
		self.__intro()
		loose_items = {"map":{}}

		location = self.map.location.inspect()

		if len(location[2]) > 0:
			for k, item in enumerate(location[2]):
				# loose_items["map"]["copper"] = [50, Item Object]
				if item[1] in loose_items["map"]:
					loose_items["map"][item[1]][0] += item[0]
				else:
					loose_items["map"][item[1]] = [item[0], item[4]]

		while True:
			action = input("? ").lower()
			location = self.map.location.inspect()

			if "help" in action or action == "h":
				print("Available commands:")
				print("")
				print("Look (at) [something]")
				print("Look (at) me/self")
				print("Go [direction]")
				print("Open [something]")
				print("Open my [something]")
				print("Fight [someone]")
				print("Talk (to) [someone]")
				print("Take [something]")
				print("Drop [something]")
				print("")
				print("[quit] to Quit")
				print("")
			elif action == "quit":
				break
			else:
				action = action.split(" ")
				target = False

				if len(action) > 2:
					if action[1] == "at" or action[1] == "to":
						target = " ".join(action[2:])
					else:
						target = " ".join(action[1:])
				elif len(action) > 1:
					target = action[1]

				if "go" in action[0]:
					movement = self.map.move(action[1])

					if movement == False:
						print("You can't go there")
					else:
						# Reset the takeable loose items
						loose_items = {"map":{}}
						print("")
						print(movement[0])
						print("")
						print(movement[1])

						location = self.map.location.inspect()
						if len(location[2]) > 0:
							for k, item in enumerate(location[2]):
								# loose_items["map"]["copper"] = [50, Item Object]
								if item[1] in loose_items["map"]:
									loose_items["map"][item[1]][0] += item[0]
								else:
									loose_items["map"][item[1]] = [item[0], item[4]]

				elif "look" in action[0]:
					if len(action) == 1 or (len(action) == 2 and action[1] == "at"):
						print("")
						print(location[0])
						print("")
						print(location[1])
						print("")

						if len(location[2]) > 0:
							print("You can see these items: ")

							for k, item in enumerate(location[2]):
								print("%dx %s" % (item[0], item[1]))

							print("")

						if len(location[3]) > 0:
							print("Here are: ")

							for k, item in enumerate(location[3]):
								print("%dx level %d %s" % (item[0], item[3], item[1]))

					elif target == "self" or target == "me":
						items = self.player.bag.open()

						print("You have:")

						for k, item in enumerate(items):
							print("%dx %s" % (item[0], item[1]))

					else:
						item = self.map.location.find(target)
						if not item:
							print("That's not here")
						else:
							print("%dx %s" % (item[0], item[1]))
							print(item[2])

				elif "open" in action[0]:
					if "my " in target:
						t = target.split(" ")
						items = self.player.bag.open()
						found = False

						for k, item in enumerate(items):
							if t[1] == item[1].lower():
								found = True
								if isinstance(item[3], Container):
									gear = item[3].open()

									if not gear:
										print("It's empty")
									else:
										print("Inside you find:")

										for k, g in enumerate(gear):
											print("%dx %s" % (g[0], g[1]))
											print(item[2])
								else:
									print("You can't open tahat")

						if not found:
							print("You don't have this")

					else:
						item = self.map.location.find(target)

						if item == False:
							print("That isn't here")
						else:
							result = item[3].open()
							if not result:
								print("It's empty")
							else:
								print("Inside you find:")

								for k, item in enumerate(result):
									print("%dx %s" % (item[0], item[1]))
									print(item[2])

									if target not in loose_items:
										loose_items[target] = {}

									# loose_items["chest"]["copper"] = [50, Item Object]
									if item[1] in loose_items[target]:
										loose_items[target][item[1]][0] += item[0]
									else:
										loose_items[target][item[1]] = [item[0], item[3]]

				elif "take" in action[0]:
					item = False

					for location in loose_items:
						for name, i in loose_items[location].items():
							if name.lower() == target:
								item = i
								break

					bag = self.player.bag.open()
					bag = bag[0][3]

					if item == False:
						print("That isn't here")
					else:
						bag.add_item(item[1], item[0])
						print("Put %s in your bag" % item[1].name)

				elif "drop" in action[0]:
					bag = self.player.bag.open()
					bag = bag[0][3]
					item = self.__gear[target]

					if bag.remove_item(item, 1):
						print("Dropped %s" % item.name)
						self.map.location.add_item(item, 1)
					else:
						print("Don't have %s to drop" % item.name)

				elif "fight" in action[0] or "attack" in action[0]:
					print(target)
					foe = self.__npc[target]
					print(foe)
					print(foe.name)

				elif "talk" in action[0]:
					# TODO: ?????
					print(target)
					npc = self.__npc[target]

			print("")

	def __setup(self):
		name = ""
		while len(name) == 0:
			name = input("What is your name ? ")

		print("Who are you?")
		print("I'm a...")

		race = 0
		while True:
			print("1) Human")
			print("2) Elf")
			print("3) Dwarf")
			print("4) Halfling")

			try:
				race = int(input("? "))
				if race < 1 or race > 4:
					raise ValueError
			except ValueError:
				print("Not a valid number!")
				continue
			else:
				break 

		cls = 0
		while True:
			print("1) Fighter")
			print("2) Rogue")
			print("3) Mage")
			print("4) Cleric")

			try:
				cls = int(input("? "))
				if cls < 1 or cls > 4:
					raise ValueError
			except ValueError:
				print("Not a valid number!")
				continue
			else:
				break 

		self.player = Player(name, "", Dice.roll(6, 3), Dice.roll(6, 3), Dice.roll(6, 3), race, cls)

		# Starting gold
		if cls == 1:
			self.player.currency("Gold", 150)
		elif cls == 2:
			self.player.currency("Gold", 125)
		elif cls == 3:
			self.player.currency("Gold", 75)
		elif cls == 4:
			self.player.currency("Gold", 120)

		bag = self.__gear["backpack"]
		self.player.bag.add_item(bag, 1)

		self.map = Map()

	def __intro(self):
		chest = Container("Old chest", "A ruggedy old chest, half-buried in the sand", 0, 10)
		chest.add_item(self.__gear["bell"], 1)

		self.map.location.add_item(chest, 1)

		print("Welcome Adventurer!")
		print("If you need help, just type in [h] or [help].")
		print("Quit with [quit] and move around with 'Go [direction]'")
		print("Usable stuff is brought out by '[' and ']'.")

		location = self.map.location.inspect()

		print("")
		print(location[0])
		print("")
		print(location[1])