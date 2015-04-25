from random import randint
import os, csv, re

class Base:
    """Base class for my classes"""
    
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description

class Container(Base):
    """Container of items"""
    
    def __init__(self, name="", description="", destructable=0, capacity=0):
        self.destructable = destructable
        self.items = []
        self.capacity = capacity
        super().__init__(name, description)
        
    def add_item(self, item, amount):
        if (len(self.items)) >= self.capacity:
            print("Cannot add anything here, try removing something first")
            return False

        if amount < 0:
            return self.remove_item(item)

        # Not making a copy because items are moved not copied over
        for index, element in enumerate(self.items):
            if element[0] == item:
                self.items[index][1] += amount

                return True
            
        self.items.append([item, amount])
        return True

    def remove_item(self, item, amount):
        if amount < 0:
            return self.add_item(item, amount)

        for index, element in enumerate(self.items):
            if element[0] == item:
                self.items[index][1] -= amount

                if self.items[index][1] < 1:
                    del self.items[index]

                return True

        return False

    def open(self):
        items = []

        for index, element in enumerate(self.items):
            items.append([element[1], element[0].name, element[0].description, element[0]])

        if len(items) < 1:
            return False # AKA empty

        return items

    def find(self, name):
        for index, element in enumerate(self.items):
            if element[0].name.lower() == name.lower():
                return [element[1], element[0].name, element[0].description, element[0]]
        return False

class Actor(Base):
    """NPC or PC, element that can interact with others"""
    
    def __init__(self, name="", description=""):
        # Maybe bag is not the right var name, but fudge it
        self.bag = Container("Outfit", destructable=0, capacity=5)

        self.copper = 0
        self.silver = 0
        self.gold = 0
        self.platinum = 0
        
        super().__init__(name, description)

    def currency(self, name="gold", amount=0):
        name = name.lower()

        if name == "copper":
            self.copper += amount
        elif name == "silver":
            self.silver += amount
        elif name == "gold":
            self.gold += amount
        elif name == "platinum":
            self.platinum += amount

class Spell(Base):
    """Castable by using Mana or if that's 0 -> Health"""

    types = [
        "Passive",
        "Armor",
        "Attack",
        "Illusion"
    ]
    
    def __init__(self, name, description, cls=0, level=0, duration=1, area=1, damage=False, bonus=False, target=0, divine=False):
        self.type = types[cls]
        self.level = level
        self.duration = duration
        self.range = area
        self.target = target # Target 0 = Player
        self.divine = divine
        
        if damage is not False:
            self.damage = damage
        
        if bonus is not False:
            self.bonus = bonus

        # TODO: Proper implementation

        super().__init__(name, description)

class Item(Base):
    """Items in the world"""
    
    __types = [
        "Currency",
        "Weapon",
        "Armor",
        "Gear"
        ]
    
    def __init__(self, name="", description="", value=1, cat=5, quest=0):
        self.value = value
        self.category = cat
        self.quest_item = quest == 1
        super().__init__(name, description)
    
    def get_type(self):
        return self.__types[self.category]

    def inspect(self):
        return [self.name, self.description, self.value, self.get_type()]

class Dice:
    """Dice rolling (helper) class"""

    def roll(dice=6, amount=1):
        total = 0

        for i in range(0, amount):
            total += randint(1, dice)

        return total

def parse(filename):
        path = os.path.join(os.path.dirname(__file__), os.pardir, "data", filename)
        result = []
        r = re.compile('(\d)d(\d)([+-]\d)*')
        
        with open(path) as file:
            reader = csv.DictReader(file)

            for row in reader:
                parsed = {}

                for k, v in row.items():
                    if isinstance(v, list):
                        v = v[0]

                    if r.match(v) is not None:
                        parsed[k] = [int(var) for var in r.split(v) if var]
                    else:
                        # Because in some cases random arrays were thrown in, out of the blue
                        if isinstance(v, list):
                            v = v[0]

                        if v.isdigit():
                            parsed[k] = round(float(v), 2)
                        else:
                            parsed[k] = v
                result.append(parsed)

        return result

class Weather:
    seasons = [
        "Unknown",
        "Spring",
        "Summer",
        "Autumn",
        "Winter"
    ]

    __weathers = [
        {},
        {
            3: "Hot",
            4: "Sunny",
            5: "Sunny",
            6: "Bright",
            7: "Bright",
            8: "Breezy",
            9: "Dull",
            10: "Dull",
            11: "Mist",
            12: "Windy",
            13: "Overcast",
            14: "Light Rain",
            15: "Light Rain",
            16: "Heavy Rain",
            17: "Fog",
            18: "Sleet"
        },
        {
            3: "Heatwave",
            4: "Hot",
            5: "Hot",
            6: "Sunny",
            7: "Sunny",
            8: "Bright",
            9: "Bright",
            10: "Breezy",
            11: "Dull",
            12: "Mist",
            13: "Windy",
            14: "Overcast",
            15: "Light Rain",
            16: "Light Rain",
            17: "Heavy Rain",
            18: "Fog"
        },
        {
            3: "Hot",
            4: "Sunny",
            5: "Bright",
            6: "Breezy",
            7: "Dull",
            8: "Dull",
            9: "Mist",
            10: "Mist",
            11: "Windy",
            12: "Overcast",
            13: "Light Rain",
            14: "Heavy Rain",
            15: "Heavy Rain",
            16: "Fog",
            17: "Fog",
            18: "Sleet"
        },
        {
            3: "Sunny",
            4: "Bright",
            5: "Breezy",
            6: "Dull",
            7: "Mist",
            8: "Windy",
            9: "Overcast",
            10: "Overcast",
            11: "Light Snow",
            12: "Heavy Snow",
            13: "Heavy Snow",
            14: "Fog",
            15: "Fog",
            16: "Sleet",
            17: "Snowstorm",
            18: "Snowstorm"
        },
    ]

    def __init__(self, day=1, season=1):
        self.season = season
        self.day = day

    def get():
        roll = Dice.roll(6, 3)
        return self.seasons[self.season] + ": " + self.__weathers[self.season][roll]

    def advance(amount=1):
        self.day += amount

        if self.day % 50 == 0:
            self.season += 1