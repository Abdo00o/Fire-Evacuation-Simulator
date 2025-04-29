import sys 
import Search_For_The_Nearest_Exit
import Uninformed_Cost_Search

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

BFS = Search_For_The_Nearest_Exit
BFS.main(sys.argv[1])

UCS = Uninformed_Cost_Search 

UCS.main(sys.argv[1]) 
