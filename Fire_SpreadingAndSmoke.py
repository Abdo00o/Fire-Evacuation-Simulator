

class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Map():

    def __init__(self, filename):

        # Read file and set height and width of map
        with open(filename) as f:
            self.contents = f.read()
        
        # Get the rows and columns
        self.contents = self.contents.splitlines()  #return list of string split with /n
        self.height = len(self.contents)
        self.width = max(len(line) for line in self.contents)

        # Keep track of walls
        self.fireAt = []
        self.smokeAt = [] 
        self.frontier = QueueFrontier() 
        for i in range(self.height):
            rowFire = []
            rowSmoke = []
            for j in range(self.width):
                try:
                    if self.contents[i][j] == "F" :  
                        self.frontier.add((i,j)) 
                        rowSmoke.append(1e9) 
                        rowFire.append(0) 
                    elif self.contents[i][j] == "S" :  
                        rowSmoke.append(0) 
                        rowFire.append(1e9) 
                    else:
                        rowFire.append(1e9) 
                        rowSmoke.append(1e9) 
                except IndexError:
                    rowFire.append(1e9)
                    rowSmoke.append(1e9) 
            
            self.fireAt.append(rowFire)
            self.smokeAt.append(rowSmoke) 

    def neighborsFires(self, state):
        row, col = state
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        result = []
        for r,c in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and self.contents[r][c]=="A":
                result.append((r,c))
        return result

    def neighborsSomke(self, state):
        row, col = state
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        result = []
        for r,c in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.contents[r][c]=="#":
                result.append((r,c))
        return result


    def solve(self):
        """ Handels the fire spread ,
          and calculate the units of times which the fire will reach this cell (if Possible )"""


        # Initialize an empty explored set
        exploredFire = set()
        exploredSmoke = set()
        # Keep looping until no new updates
        while not self.frontier.empty():

            # Choose a node from the frontier
            node = self.frontier.remove() #node = removed node
            # Mark node as explored
            exploredFire.add(node)

            # Add neighbors to frontier
            # Check the fire Spread
            for state in self.neighborsFires(node):
                if not self.frontier.contains_state(state) and state not in exploredFire and self.fireAt[state[0]][state[1]]!=0:
                    self.fireAt[state[0]][state[1]] = self.fireAt[node[0]][node[1]]+1 
                    self.frontier.add(state)
            
            for state in self.neighborsSomke(node):
                if not self.frontier.contains_state(state) and state not in exploredSmoke and self.smokeAt[state[0]][state[1]]!=0:
                    self.smokeAt[state[0]][state[1]] = self.smokeAt[node[0]][node[1]]+1 
                    exploredSmoke.add(state)
            
            

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