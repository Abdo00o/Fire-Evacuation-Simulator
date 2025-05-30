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

        # Validate start and exit
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
        self.exit =[]
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
                        self.exit.append((i, j)) 
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


    def Print(self):
        print(self.solution[0])
        print(self.solution[1])


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

            # If node is a exit, then we have a solution
            if node.state in self.exit:
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

    def mix_colors(self, color1, color2, weight1=0.5, weight2=0.5):
        return tuple(
            round(c1 * weight1 + c2 * weight2)
            for c1, c2 in zip(color1, color2)
        )

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

        
        for i, row in enumerate(self.contents):
            for j, col in enumerate(row):
                
                # Walls
                if col=="#":
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (0, 191, 255)

                # Exit
                elif (i, j) in self.exit:
                    fill = (0, 171, 28)

                # Solution
                else : 
                    
                    fire = fs.fireAt[i][j]<=self.arriveAt[i][j] and fs.fireAt[i][j]!= 1e9
                    smoke = fs.smokeAt[i][j]<=self.arriveAt[i][j]and fs.smokeAt[i][j]!= 1e9
                    obstacle = self.contents[i][j]=='O' 
                    flameObject = self.contents[i][j]=='A' ; 
                    solu = (i,j) in self.solution[1] 

                    if fire and smoke  :
                        if solu :fill=self.mix_colors((178, 34, 34),(144, 238, 144))
                        else :fill = (178, 34, 34)
                    elif obstacle and smoke :  
                        if solu :fill=self.mix_colors((90, 70, 50),(144, 238, 144))
                        else :fill = (90, 70, 50)
                    elif flameObject and smoke : 
                        if solu :fill=self.mix_colors((184, 134, 11),(144, 238, 144))
                        else :fill = (184, 134, 11)
                        
                    elif fire : 
                        if solu :fill=self.mix_colors((255, 69, 0),(144, 238, 144))
                        else :fill = (255, 69, 0)
                    elif flameObject : 
                        if solu :fill=self.mix_colors((255, 215, 0),(144, 238, 144))
                        else :fill = (255, 215, 0)
                    elif smoke : 
                        if solu :fill=self.mix_colors((105, 105, 105),(144, 238, 144))
                        else :fill = (105, 105, 105)
                    elif obstacle : 
                        if solu :fill=self.mix_colors((160, 82, 45),(144, 238, 144))
                        else :fill = (160, 82, 45)
                    else : 
                        if (i,j) in self.solution[1] :
                            fill = (144, 238, 144)
                        elif (i,j) in  self.explored :
                            fill = (255, 255, 153)  
                        else :  
                            fill = (237, 240, 252)

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

        
        m.solve(fs=Fs)
        print("States Explored:", m.num_explored)
        print("Solution of the safest path :")
        m.Print()
        m.output_image("Safest_Exit_Map.png" , Fs)
        print()



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

