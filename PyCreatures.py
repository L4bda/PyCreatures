import random

class CornConfig:
    seedCycle = 6
    cornSymbol = '§'
    maxAge = 25
class MouseConfig:
    maxStarving = 7
    maxAge = 25
    offspringCycle = 12
    mouseSymbol = "M"
    eatable = [CornConfig.cornSymbol] # Maybe imoprt classes to fix undefined class error when added in wrong order or change fully if two fighting classes should be added
class Coordinates:
    def __init__(self, x, y, valid):
        if valid:
            self.x = x 
            self.y = y
            self.valid = True
        else:
            self.valid = False
import random
class World:
    def __init__(self, width, height):
        # 2D array
        self.map = list()
        a = list()
        # Dictionary
        self.things = dict()
        for x in range(width):
            a = []
            for y in range(height):
                a.append(None)
                self.things[ctod(x, y)] = None
            self.map.append(a)
        self.max_y = len(self.map[0])
        try:
            self.max_x = len(self.map)
        except IndexError:
            self.max_x = 0

    def out(self): # Prints the map as a x*y grid, where None will be printed as '.'
        for y in reversed(range(self.max_y)):
            for x in range(self.max_x):
                if self.map[x][y] is None:
                    print(".", end="")
                else:
                    print(self.map[x][y], end="")
            print()
        print()

    def get(self, x, y): # Same as out(), but for a single coordinate. Only used for debug purposes
        c = normalize(self, x, y)
        if self.map[c.x][c.y] is None:
                print(".")
        else:
                print(self.map[c.x][c.y])
        
    def spawn(self, thing): # Adds a Thing to the map and dictionary
        #  Unnecessary Boilerplate
            # coords = normalize(self, thing.x, thing.y) 
            # x = coords.x
            # y = coords.y
        self.map[thing.x][thing.y] = thing.symbol
        self.things[ctod(thing.x, thing.y)] = thing
    
    def freeNeighbour(self, thing): # Finds a random grid with in 1 Space of vertical or horizontal movement of the parsed in thing. If this is free it returns it as a valid coordinate 
            x = thing.x 
            y = thing.y 
            directions = ["N", "E", "S", "W"]
            random.shuffle(directions)
            for direction in directions:
                match direction:
                    case "N":
                        y += 1
                    case "S":
                        y -= 1
                    case "E":
                        x += 1
                    case "W":
                        x -= 1 
                
                coords = normalize(self, x, y)
                x = coords.x
                y = coords.y
                if self.things[ctod(x, y)] == None: # If this throws an error fix normalize
                    return Coordinates(x,y, True)
            return Coordinates(None, None, False)

    def foodNearMe(self, thing): # Same as freeNeighbour() but for food
        x = thing.x 
        y = thing.y 
        directions = ["N", "E", "S", "W"]
        random.shuffle(directions)
        for direction in directions:
            match direction:
                case "N":
                    y += 1
                case "S":
                    y -= 1
                case "E":
                    x += 1
                case "W":
                    x -= 1 
            coords = normalize(self, x, y)
            x = coords.x
            y = coords.y
            if self.things[ctod(x, y)] != None:
                if self.things[ctod(x, y)].symbol in thing.eatable: # If this throws an error fix normalize
                    return Coordinates(x,y, True)
        return Coordinates(None, None, False)

    def kill(self, thing): # Opposite of spawn, removes object
        x = thing.x 
        y = thing.y 
        self.map[x][y] = None
        self.things[ctod(x, y)] = None

    def countFreeSpaces(self): # Counts all None spaces in the cictionary
        counter = 0
        for v in list(self.things.values()):
            if v == None:
                counter += 1
        return counter

    def randomFreeCoordinates(self): # Returns a random space on the map with a None value. Used to spawn objects randomly
        things = list(self.things.items())
        random.shuffle(things)
        for k, v in things:
            if v == None:
                return dtoc(k)
        raise Exception ("Can not spawn more Things then Spaces on the map ({self.max_x} * {self.max_y} - (amount of things))")

    def replace(self, old, new): # Replaces two Things or one Thing and one None in the map and dict. Used for movement and eating
        thing = self.things[ctod(old.x, old.y)]
        self.things[ctod(old.x, old.y)] = None
        self.things[ctod(new.x, new.y)] = thing
        self.map[old.x][old.y] = None
        self.map[new.x][new.y] = self.things[ctod(new.x, new.y)].symbol 
    
    
    def computeLifeCycle(self): # Iterates over all Things, let's them perform their actions
        things = self.things.values()
        random.shuffle(list(things))
        for v in things:
            if v != None:
                v.call(map)
        self.out()

def tryDieGeliebteBeimBeischlafVerführen(thing, map): # Handles reproduction # Reference  
    # Wie reproduzieren die sich eigentlich asexuell
    match type(thing).__name__:
        case "Creature":
            c = map.freeNeighbour(thing)
            if c.valid:
                map.spawn(Creature(thing.symbol, c.x, c.y))
                return
            c = map.foodNearMe(thing)
            if c.valid:
                map.spawn(Creature(thing.symbol, c.x, c.y))
                return
        case "Plant":
            c = map.freeNeighbour(thing)
            if c.valid:
                map.spawn(Plant(thing.symbol, c.x, c.y))
                return
        case _:
            raise Exception("Non class called") 
def ctod(x, y): # Coordinates to the format of a map.things key
    return "{},{}".format(x, y)
def dtoc(xy): # A map.things key to a coordinate
    xy = xy.split(",")
    return Coordinates(int(xy[0]), int(xy[1]), True)

def normalize(map, x, y): # Sets the coordinates to be wrapped around the plane
# Normalize X coordinate
    if map.max_x == 0:
        x = 0
    else:
        if x < 0:
            if x == -1:
                x = map.max_x - 1
            else:
                x = map.max_x + x + 1
        if x >= map.max_x:
            try:
                x %= map.max_x
            except ZeroDivisionError:
                x = 0
# Normalize Y coordinate
    if map.max_y == 0:
        y = 0
    else:
        if y < 0:
            if y == -1:
                y = map.max_y - 1
            else:
                y = map.max_y + y + 1
        if y >= map.max_y :
            try:
                y %= map.max_y
            except ZeroDivisionError:
                y = 0
    return Coordinates(x, y, True)

class Thing: # Parent class. Stores Age, Coordinate
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.age = 0
        self.x = x 
        self.y = y
        self.age = 0

class Creature(Thing): # Living, moving, eating Creature
    def __init__(self, symbol, x, y):
        super().__init__(
            symbol = symbol,
            x = x,
            y = y,
        )
        self.offspringCycle = MouseConfig.offspringCycle
        self.starving = 0
        self.maxStarving = MouseConfig.maxStarving
        self.maxAge = MouseConfig.maxAge
        self.currentCycle = 0
        self.dead = False
        self.eatable = MouseConfig.eatable

    def call(self, map): # Personal cycle
        self.age += 1
        self.starving += 1
        self.currentCycle += 1
        if not self.dead and self.currentCycle >= self.offspringCycle: 
            tryDieGeliebteBeimBeischlafVerführen(self, map)
            self.currentCycle = 0
        if self.age >= self.maxAge:
            self.dead = True
            map.kill(self)
        elif self.starving > self.maxStarving:
            self.dead = True
            map.kill(self)         
        # Move
        if not self.dead:
            new_field = map.foodNearMe(self)
            if not new_field.valid:
                new_field = map.freeNeighbour(self)
            else:
                self.starving = 0
            if new_field.valid:
                map.replace(self, new_field)
                self.x = new_field.x 
                self.y = new_field.y 
    
class Plant(Thing): # Non moving, non eating Thing
    def __init__(self, symbol, x, y):
        super().__init__(
            symbol = symbol,
            x = x,
            y = y,
        )
        self.age += 1
        self.currentCycle = 0
        self.seedCycle = CornConfig.seedCycle

    def call(self, map): # Personal cycle
        self.currentCycle += 1
        if self.currentCycle >= CornConfig.seedCycle:
            tryDieGeliebteBeimBeischlafVerführen(self, map)
        if self.age >= CornConfig.maxAge:
            map.kill(self)

def initWorld() -> World: # Creates and returns World
    print("This simulation shows mice(M) and corn(§) in a spherical plane. Both Mice and Corn try to reproduce and can die. Mice will also try to eat corn when next to it.")
    print("Change the parameters set in CornConfig and MouseConfig to alter the outcome")
    while True:
        size = input("Please input the size of your simulation in the format of <width>,<height>")
        try:
            coords = dtoc(size)
            break
        except:
            print("Please enter the size in the correct format")
    return World(coords.x, coords.y)

def mainLoop(map):
    while True:
        map.out()
        command = input("Enter command <'h' for help, <Enter> for next cycle>: ")
        if len(command) == 0:
            map.computeLifeCycle()
            continue
        elif len(command) == 1:
            match command:
                case "h":
                    print("This simulation shows mice(M) and corn(§) in a spherical plane. Both Mice and Corn try to reproduce and can die. Mice will also try to eat corn when next to it.")
                    print("Change the parameters set in CornConfig and MouseConfig to alter the outcome")
                    print("--Keybinds--")
                    print("Return : Next cycle")
                    print("<number> : Complete <number> cycles ")
                    print("q : quit")
                    print("h : show this menu")
                    print("spawn <number> <type> : Randomly spawns <number ∈ ℕ> of <type> where type may be corn or mouse")
                    print("free : shows amount of free spaces on the plane")
                    print("debug : shows the dictionary and map as raw object")
                    print("Press Enter to continue")
                    input() 
                    break
                case "q":
                    exit()
        command = command.split()
        match command[0]:
            case "free":
                print(f"{map.countFreeSpaces()}")
            case "spawn":
                    if len(command) != 3:
                        continue
                    match command[2]: 
                        case "mouse":
                            try:
                                n = int(command[1])
                            except:
                                print("Press h for help")
                                continue
                            for _ in range(n):
                                c = map.randomFreeCoordinates()
                                mouse = Creature(MouseConfig.mouseSymbol, c.x, c.y)
                                map.spawn(mouse)
                        case "corn":
                            try:
                                n = int(command[1])
                            except:
                                n = 0
                                continue
                            for _ in range(n):
                                c = map.randomFreeCoordinates()
                                corn = Plant(CornConfig.cornSymbol, c.x, c.y)
                                map.spawn(corn)
                        case _:
                            print(f"{command[2]} is not implemented. Press h for help")
            case "debug":
                print(map.things)
                print("-"*50)
                print(map.map)
                print("-"*50)
                map.out()
            case _:
                try:
                    n = int(command[0])
                except:
                    print("Press h for help")
                    continue
                for _ in range(n):
                    map.computeLifeCycle()
map = initWorld()
mainLoop(map)
