import Fire_SpreadingAndSmoke 
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

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


    def solve(self):
        """ Find the shortest path to any exit , no matter the fires ,smoke or obstacles"""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier() #BFS
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("There is no way out of here ToT !....")

            # Choose a node from the frontier
            node = frontier.remove() #node = removed node
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
                if not frontier.contains_state(state) and state not in self.explored:
                    self.arriveAt[state[0]][state[1]] = self.arriveAt[node.state[0]][node.state[1]]+1 
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def Print(self) :  
        print(self.solution[0]) 
        print(self.solution[1])

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
        f= Fire_SpreadingAndSmoke
        Fs = f.Map(file) 
        m = Map(file)
        
        Fs.solve()
        
        #m.print()
        #print("Solving...")
        m.solve()
        print("States Explored:", m.num_explored)
        print("Solution of the nearest path:")
        m.Print()
        m.output_image("Nearest_Exit_Map.png" , Fs)
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


