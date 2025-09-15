offspringCycle = 4
maxStarving = 3
maxStarving = 10
mouse = 'M'
corn = 'C'
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

    def get(self, x, y):
        if inbound(self, x, y):
            if self.map[x][y] is None:
                    print(".")
            else:
                    print(self.map[x][y])

    def spawn(self, thing):
        print(thing.x, thing.y)
        if not inbound(self, thing.x, thing.y):
            coordinates = normalize(self, thing.x, thing.y)
            #print(f"x,y oob: {x} {y}")
            x = coordinates[0]
            y = coordinates[1]
        else:
            x = thing.x 
            y = thing.y 
        self.map[x][y] = thing.symbol
        self.things[ctod(x, y)] = thing

                
    def neighbour(self, thing): # TODO: Change that to return some direction randomly
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
                    x = coords[0]
                    y = coords[1]
        
                if self.map[ctod(x, y)] == None: # If this throws an error fix inbound or normalize
                    return[x, y]
            return[]    
            
    def kill(self, thing): #TODO: Kill the children of Thing
        x = thing.x 
        y = thing.y 
        self.map[x][y] = None
        self.things[ctod(x, y)] = None

    
    def computeLifeCycle(self):
        things = self.things.values()
        random.shuffle(list(things))
        for v in things:
            if v != None:
                v.call()



def TryDieGeliebteImBeischlafVerführen(thing, x, y):
    #TODO: Find a free neighbour, randomly
    #TODO: Spawn a rat at the returned postion
    # Wie reproduzieren die sich eigentlich asexuell
    
    if len(neighbour(map, thing)) > 0: # Map hier vlt. in die Funktion einfügen, aber runtime ist eh schon aus dem Fenster geflogen
        map.spawn(Creature(mouse, offspringCycle, maxStarving, maxAge, x, y))


    
    

def ctod(x, y):
    return "{},{}".format(x, y)
def dtoc(xy):
    return[xy[0], xy[1]]
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
    return [x, y]

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
    def performAction():
        pass

class Creature(Thing):
    def __init__(self, symbol, offspringCycle, maxStarving, maxAge, x, y):
        super().__init__(
            symbol = symbol,
            x = x,
            y = y,
        )
        self.offspringCycle = offspringCycle
        self.starving = 0
        self.maxStarving = maxStarving
        self.maxAge = maxAge
        self.currentCycle = 0
    def call(self):
        self.offspringCycle += 1
        self.age += 1
        self.starving += 1
        self.currentCycle += 1
        if self.starving == self.maxStarving:
            self.age = self.maxAge # This should kill it
        if self.age == self.maxAge:
            map.kill(self)
        if self.offspringCycle == self.currentCycle:
            TryDieGeliebteImBeischlafVerführen(self)
          
class Plant(Thing):
    def __init__(symbol, seedCycle):
        super().__init__(
            symbol = symbol
        )
        self.seedCycle = seedCycle
    def call(self):
        self.seedCycle += 1

map = World(79, 29)
def mainLoop(map):
    map.out()
    while True:
        command = input("Enter command: ")
        if len(command) == 0:
            break
        elif len(command) == 1:
            match command:
                case "h":
                    print("Lorem ipsum in dolor sit amet")
                    break
                case "q":
                    exit()
        elif len(command) > 5:
            if command[:5] == "spawn":
                pass #TODO: Create random coordinate generator, match pattern for spawn <type> <number>




