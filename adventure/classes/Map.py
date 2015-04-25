from classes.Base import Container, Item, parse
import random

class Room(Container):
	"""Single room in the world"""

	directions = {
		"n": 0,
		"e": 1,
		"s": 2,
		"w": 3,
		"ne": 4,
		"se": 5,
		"sw": 6,
		"nw": 7
	}
	
	def __init__(self, name="", description="", exits=[-1,-1,-1,-1,-1,-1,-1,-1]):
		self.exits = exits
		self.npc_count = 0

		super().__init__(name, description, 0, 999999999)

		self.description += "\n\nYou can go "

		if self.exits[0] != -1:
			self.description += "[N] North "
		if self.exits[4] != -1:
			self.description += "[NE] North-East "
		if self.exits[1] != -1:
			self.description += "[E] East "
		if self.exits[5] != -1:
			self.description += "[SE] South-East "
		if self.exits[2] != -1:
			self.description += "[S] South "
		if self.exits[6] != -1:
			self.description += "[SW] South-West "
		if self.exits[3] != -1:
			self.description += "[W] West "
		if self.exits[7] != -1:
			self.description += "[NW] North-West "

		self.description += "\n"

	def add_npc(self, npc, amount=1):
		self.npc_count += 1
		self.add_item(npc, amount)

	def remove_npc(self, npc, amount=1):
		self.npc_count -= 1
		self.remove_item(npc, amount)

	def inspect(self):
		result = [self.name, self.description, [], []]

		if len(self.items) > 0:
			items = []
			npc = []

			for item in self.items:
				if isinstance(item[0], Item):
					items.append([item[1], item[0].name, item[0].description, item[0].value, item[0]])
				elif isinstance(item[0], Container):
					items.append([item[1], item[0].name, item[0].description, item[0].destructable, item[0]])
				else:
					npc.append([item[1], item[0].name, item[0].description, item[0].level, item[0]])

			result[2] = items
			result[3] = npc

		return result

class Map:
	"""The world map"""
	
	def __init__(self, size=10):
		self.position = 22
		self.rooms = {}

		rooms = parse("map.csv")

		for room in rooms:
			# {'N': '-1', 'W': '-1', 'E': '-1', 'Description': 'You are ...', 'Name': 'Sheltered Outcropping', 'ID': 26, 'S': 23}
			self.rooms[room['ID']] = Room(
				room['Name'], 
				room['Description'], 
				[int(room["N"]), int(room["E"]), int(room["S"]), int(room["W"]),
				int(room["NE"]), int(room["SE"]), int(room["SW"]), int(room["NW"])]
				)

		self.location = self.rooms[self.position]

	def move(self, direction):
		room = self.rooms[self.position]
		direction = direction.lower()

		if direction not in room.directions:
			return False

		if room.exits[room.directions[direction]] == -1:
			return False
		
		self.position = room.exits[room.directions[direction]]
		room = self.rooms[self.position]

		return [room.name, room.description]