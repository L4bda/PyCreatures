


class CornConfig:
    seedCycle = 4
    cornSymbol = 'C'

class MouseConfig:
    maxStarving = 5000
    maxAge = 5000
    offspringCycle = 1
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
        # 2D arrar
        self.map = list()
        a = list()
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

    def out(self):
        for y in reversed(range(self.max_y)):
            for x in range(self.max_x):
                if self.map[x][y] is None:
                    print(".", end="")
                else:
                    print(self.map[x][y], end="")
            print()
        print()

    def get(self, x, y):
        if inbound(self, x, y):
            if self.map[x][y] is None:
                    print(".")
            else:
                    print(self.map[x][y])

    def spawn(self, thing):
        if not inbound(self, thing.x, thing.y):
            coordinates = normalize(self, thing.x, thing.y)
            #print(f"x,y oob: {x} {y}")
            x = coords.x
            y = coords.y
        else:
            x = thing.x 
            y = thing.y 
        self.map[x][y] = thing.symbol
        self.things[ctod(x, y)] = thing

                
    def freeNeighbour(self, thing): # TODO: Change that to return some direction randomly
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

                if not inbound(self, x, y):
                    coords = normalize(self, x, y)
                    x = coords.x
                    y = coords.y
        
                if self.things[ctod(x, y)] == None: # If this throws an error fix inbound or normalize
                    return Coordinates(x,y, True)
            return Coordinates(None, None, False)

    def foodNearMe(self, thing):
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
            if not inbound(self, x, y):
                coords = normalize(self, x, y)
                x = coords.x
                y = coords.y
    
            if self.things[ctod(x, y)] in thing.eatable: # If this throws an error fix inbound or normalize
                return Coordinates(x,y, True)
        return Coordinates(None, None, False)
    def kill(self, thing): #TODO: Kill the children of Thing
        x = thing.x 
        y = thing.y 
        self.map[x][y] = None
        self.things[ctod(x, y)] = None
    
    def randomFreeCoordinates(self):
        things = list(self.things.items())
        random.shuffle(things)
        for k, v in things:
            if v == None:
                return dtoc(k)
        print("Map is full")
        exit()
    def replace(self, old, new):
        thing = self.things[ctod(old.x, old.y)]
        self.things[ctod(old.x, old.y)] = None
        self.things[ctod(new.x, new.y)] = thing
        self.map[old.x][old.y] = None
        self.map[new.x][new.y] = self.things[ctod(new.x, new.y)].symbol 

    
    def computeLifeCycle(self):
        things = self.things.values()
        random.shuffle(list(things))
        for v in things:
            if v != None:
                v.call()
        self.out()



def tryDieGeliebteImBeischlafVerführen(thing): #TODO: Lowercase for idiomacy
    #TODO: Find a free freeNeighbour, randomly
    #TODO: Spawn a rat at the returned postion
    # Wie reproduzieren die sich eigentlich asexuell
    c = map.freeNeighbour(thing)
    if c.valid: # Map hier vlt. in die Funktion einfügen, aber runtime ist eh schon aus dem Fenster geflogen
        match type(thing).__name__:
            case "Creature":
                map.spawn(Creature(thing.symbol, c.x, c.y)) #TODO: Creature hier durch wahre klasse ersetzen 
            case "Plant":
                print("corn spawned")
                map.spawn(Plant(thing.symbol, c.x, c.y))
            case _:
                raise Exception("Non class called")
    else:
        print("No valid spawnpoint")
    
    

def ctod(x, y):
    return "{},{}".format(x, y)
def dtoc(xy):
    
    xy = xy.split(",")
    return Coordinates(int(xy[0]), int(xy[1]), True)
def normalize(map, x, y): # ts still fucked
    if map.max_x == 0:
        x = 0
    else:
        if x < 0:
            if x == -1:
                x = map.max_x - 1
            else:
                x = map.max_x + x + 1
        if x >= map.max_x:
            #print("Fucked?")
            try:
                x %= map.max_x
            except ZeroDivisionError:
                x = 0
    # print(f"x after fuck {x}")

    if map.max_y == 0:
        y = 0
    else:
        if y < 0:
            if y == -1:
                y = map.max_y - 1
            else:
                y = map.max_y + y + 1
        if y >= map.max_y :
           # print("Fucked?")
            try:
                y %= map.max_y
            except ZeroDivisionError:
                y = 0
    # print(f"Y after fuck {y}")
    return Coordinates(x, y, True)

def inbound(map, x,y):
    if x < 0:
        return False
    if y < 0:
        return False
    if y >= map.max_y:
        return False
        
    if x >= map.max_x:
        return False
    return True

class Thing:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.age = 0
        self.x = x 
        self.y = y
        self.age = 0
    def performAction():
        pass

class Creature(Thing):
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
    def call(self):
        self.age += 1
        self.starving += 1
        self.currentCycle += 1

        if self.age == self.maxAge:
            self.dead = True
            map.kill(self)
        elif self.starving == self.maxStarving:
            self.dead = True
            map.kill(self) 
        if not self.dead and self.currentCycle >= self.offspringCycle: 
            tryDieGeliebteImBeischlafVerführen(self)
            self.currentCycle = 0
        
        # Move
        if not self.dead:
            new_field = map.foodNearMe(self)
            if not new_field.valid:
                new_field = map.freeNeighbour(self)
            if new_field.valid:
                map.replace(self, new_field)
                self.x = new_field.x 
                self.y = new_field.y 
            else:
                pass # Useless btw
class Plant(Thing):
    def __init__(self, symbol, x, y):
        super().__init__(
            symbol = symbol,
            x = x,
            y = y,
        )
        self.age += 1
        self.currentCycle = 0
        self.seedCycle = CornConfig.seedCycle
 
        
    def call(self):
        print("corn called")
        self.currentCycle += 1
        if self.currentCycle >= CornConfig.seedCycle:
            tryDieGeliebteImBeischlafVerführen(self)

map = World(79, 29)

def mainLoop(map):
    while True:
        map.out()
        while True:
            command = input("Enter command: ")
            if len(command) == 0:
                map.computeLifeCycle()
                continue
            elif len(command) == 1:
                match command:
                    case "h":
                        print("Lorem ipsum in dolor sit amet")
                        break
                    case "q":
                        exit()
            command = command.split()
            match command[0]:
                case "spawn":
                        if len(command) != 3:
                            continue
                        match command[1]: 
                            case "mouse":
                                try:
                                    n = int(command[2])
                                except:
                                    n = 0
                                    continue
                                for _ in range(n):
                                    c = map.randomFreeCoordinates()
                                    mouse = Creature(MouseConfig.mouseSymbol, c.x, c.y)
                                    map.spawn(mouse)
                            case "corn":
                                try:
                                    n = int(command[2])
                                except:
                                    n = 0
                                    continue
                                for _ in range(n):
                                    c = map.randomFreeCoordinates()
                                    corn = Plant(CornConfig.cornSymbol, c.x, c.y)
                                    map.spawn(corn)
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
                        continue
                    for _ in range(n):
                        map.computeLifeCycle()
                        

mainLoop(map)

    
