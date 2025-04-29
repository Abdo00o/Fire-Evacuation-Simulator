import Fire_SpreadingAndSmoke 
from queue import PriorityQueue
class Node():
    def __init__(self,cost,state, parent, action):
        self.cost = cost 
        self.state = state
        self.parent = parent
        self.action = action
    def __lt__(self, other):
        return self.cost < other.cost
class Map():

    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            self.contents = f.read()

        # Validate start and goal
        if self.contents.count("C") != 1:
            raise Exception("map must have exactly one start point")
        if self.contents.count("E") ==0 :
            raise Exception("map must have at least 1 Exit")

        # Determine height and width of maze
        self.contents = self.contents.splitlines()  #return list of string split with /n
        self.height = len(self.contents)
        self.width = max(len(line) for line in self.contents)

        # Keep track of walls
        self.walls = []
        self.goal =[]
        self.arriveAt = []
        for i in range(self.height):
            row = []
            arrive=[]
            for j in range(self.width):
                try:
                    if self.contents[i][j] == "#" : 
                        arrive.append(1e9) 
                        row.append(True) 
                    elif self.contents[i][j] == "C":
                        arrive.append(0) 
                        self.start = (i, j)
                        row.append(False)
                    elif self.contents[i][j] == "E":
                        arrive.append(1e9)
                        self.goal.append((i, j)) 
                        row.append(False)
                    else:
                        arrive.append(1e9)
                        row.append(False)
                except IndexError:
                    arrive.append(1e9)
                    row.append(False)
            self.arriveAt.append(arrive)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self,fs):
        """ Find the Safest path to any Exit no mater the distance is """

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(cost=0,state=self.start, parent=None, action=None)
        frontier = PriorityQueue() #UCS
        frontier.put(start)

        calc = {"F":10 , 
                "S":5 , 
                "O":1,
                ".":0,
                "A":0,
                "E":0,
                "C":0}

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("There is no way out of here ToT !....")

            # Choose a node from the frontier
            node = frontier.get() #node = removed node
            
            self.num_explored += 1

            # If node is a goal, then we have a solution
            if node.state in self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return  # This explicitly ends the function, returning None implicitly

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    self.arriveAt[state[0]][state[1]] = self.arriveAt[node.state[0]][node.state[1]]+1 
                    child_cost = node.cost 

                    if self.contents[state[0]][state[1]] == "O" :  child_cost+=calc["O"] 
                    if fs.fireAt[state[0]][state[1]] <= self.arriveAt[state[0]][state[1]] : child_cost+=calc["F"]
                    if fs.smokeAt[state[0]][state[1]] <= self.arriveAt[state[0]][state[1]] : child_cost+=calc["S"]

                    child = Node(cost=child_cost,state=state, parent=node, action=action)
                    frontier.put(child)


    def output_image(self, filename , fs ):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None

        for i, row in enumerate(self.contents):
            for j, col in enumerate(row):
                """print(i,j)
                print(fs.fireAt[i][j])
                print(fs.smokeAt[i][j])
                print(self.arriveAt[i][j])"""
                # Walls
                if col=="#":
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 102, 102)

                # Exit
                elif (i, j) in self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and (i, j) in solution:
                    if fs.fireAt[i][j]<=self.arriveAt[i][j] and fs.smokeAt[i][j]<=self.arriveAt[i][j] : 
                        fill= (200, 170, 123)
                    elif fs.fireAt[i][j]<=self.arriveAt[i][j] : 
                        fill = (142, 119, 72)
                    elif fs.smokeAt[i][j]<=self.arriveAt[i][j] : 
                         fill =(195, 242, 195)
                    else :fill =  (144, 238, 144)   # Light lime green

                # Explored
                elif solution is not None and (i, j) in self.explored:
                    if fs.fireAt[i][j]<=self.arriveAt[i][j] and fs.smokeAt[i][j]<=self.arriveAt[i][j] : 
                        fill= (238, 169, 108)
                    elif fs.fireAt[i][j]<=self.arriveAt[i][j] : 
                        fill = (180, 118, 57)
                    elif fs.smokeAt[i][j]<=self.arriveAt[i][j] : 
                         fill =(233, 240, 179)
                    else :fill = (220, 235, 113)   # Shade of red

                # Empty cell
                else:
                    fill = (237, 240, 252)  # Very Light Blue

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


class main():
    def __init__(self,file):
        Fs = Fire_SpreadingAndSmoke.Map(file)
        m = Map(file)

        Fs.solve()

        print("Maze:")
        m.print()
        print("Solving...")
        m.solve(fs=Fs)
        print("States Explored:", m.num_explored)
        print("Solution:")
        m.print()
        m.output_image("Safest_Exit_Map.png" , Fs)



"""
Map entities 

# --->> wall 
O --->> obstacle 
F --->> fire
S --->> smoke
A --->> flammable objects 

C --->> my currunt position 
E --->> exit

. --->> empty cell 

every map should be a rectangle (every row have the same columns as the others)

"""
print("HI")

