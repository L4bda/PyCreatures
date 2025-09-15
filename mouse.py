from enum import Enum
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

    def spawn(self, thing, x, y):
        if not inbound(self, x, y):
            coordinates = normalize(self, x, y)
            #print(f"x,y oob: {x} {y}")
            x = coordinates[0]
            y = coordinates[1]       
        self.map[x][y] = thing.symbol
        self.things[ctod(x, y)] = thing

                
    def neighbour(self, x, y, direction):
        match direction:
            case "N":
                y += 1
            case "S":
                y -= 1
            case "E":
                x += 1
            case "W":
                x -= 1
            case _:
                print("Somthings ducked")
        if inbound(self, x, y):
          # print(f"neighbour in {x} {y}")
            return [x, y]
        else:
           # print(f"from neigbour { normalize(self, x, y)}")
           # print(f"{x}, {y}")
           # print(f"neighbour out { normalize(self, x, y)}")
            return normalize(self, x, y)        

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
    def __init__(self, symbol):
        self.symbol = symbol
        self.age = 0
    def performAction():
        pass

class Creature(Thing):
    def __init__(self, symbol, offspringCycle, maxStarving, maxAge):
        super().__init__(
            symbol = symbol
        )
        self.offspringCycle = offspringCycle
        self.starving = False
        self.maxStarving = maxStarving
        self.maxAge = maxAge

class Plant(Thing):
    def __init__(symbol, seedCycle):
        super().__init__(
            symbol = symbol
        )
        self.seedCycle = seedCycle


map = World(79, 29)
mouse = Creature("M", 3, 12, 144)
map.spawn(mouse, 14, 13)
print(map.max_y, map.max_x)
map.out()
