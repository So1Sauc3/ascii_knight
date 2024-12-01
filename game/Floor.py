from random import choice, randint
from Room import Room

class Floor:
    # constants
    MAXDEPTH = 3
    MAXFLOORSIZE = MAXDEPTH*2+1
    STARTINGROOMX = MAXFLOORSIZE//2
    STARTINGROOMY = MAXFLOORSIZE//2
    
    def __init__(self, id, floorType, floorGrid=None):
        """
        Parameters:
            id (int): id of the floor
            floorType (str): type of the floor (not used right now)
        Attributes:
            id (int): id of the floor
            floorType (str): type of the floor (not used right now)
            floor (list): 2d list of Room objects
            playerPos (tuple): position of the player on the floor
        """
        self.id = id
        self.floorType = floorType
        self.floor = self.loadFloor(floorGrid) if floorGrid!=None else self.generateFloor()
    
    def generateFloor(self):
        """
        Generate the floor layout by recursively calling recurseRooms on the grid.
        
        Returns:
            list: 2d list of Room objects
        """
        roomGrid = [[None for _ in range(self.MAXFLOORSIZE)] for _ in range(self.MAXFLOORSIZE)]
        self.recurseRooms(roomGrid, list(Room.roomDict.keys()), self.STARTINGROOMX, self.STARTINGROOMY, 0)
        return roomGrid
    
    def loadFloor(self, floorGrid):
        """
        Loads a floor layout from a 2d list of strings. Each string should be in the format "id:roomType:connections"
        where id is the id of the room, roomType is the type of room (e.g. "f0r0"), and connections is a string of
        directions (e.g. "N E S W") indicating which directions the room connects to other rooms.
        
        Parameters:
            floorGrid (list): 2d list of strings, each string representing a room in the format "id:roomType:connections"
        
        Returns:
            list: 2d list of Room objects, representing the loaded floor layout
        """
        roomGrid = [[None for _ in range(self.MAXFLOORSIZE)] for _ in range(self.MAXFLOORSIZE)]
        for r in range(len(floorGrid)):
            for c in range(len(floorGrid[0])-1):
                print(floorGrid[r][c])
                print(floorGrid[r][c].split(":")[1])
                id, roomType, connections = floorGrid[r][c].split(":")
                if roomType=="NONE": continue
                roomGrid[r][c] = Room(id, roomType)
                roomGrid[r][c].addConnections(connections)
        return roomGrid
    
    def recurseRooms(self, grid, roomDict, x, y, depth=0, oldDir=None):
        """
        Recursively generate the floor by calling itself on adjacent positions.
        
        Parameters:
            grid (list): 2d list of Room objects
            roomDict (list): list of room types
            x (int): x position of the room
            y (int): y position of the room
            depth (int): current level of recursion
            oldDir (str): direction of the room that lead to the current room
        """
        if not (self.isValidPos(grid, x, y) and grid[x][y]==None) or depth>self.MAXDEPTH: return
        if depth==0: grid[x][y] = Room(depth, "f0r0") # starting room
        else:
            grid[x][y] = Room(depth, choice(roomDict)) # random room
            grid[x][y].addConnections(oldDir) # add connection to room made by the "previous" recurse call
        
        doorDict = {(0,1):'S', (0,-1):'N', (1,0):'E', (-1,0):'W'} # N/S is "flipped" b/c the grid is "flipped" by nature
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]: # chance to create a door and recurse in all directions
            if all([self.isValidPos(grid, x+dx, y+dy) and grid[x+dx][y+dy]==None, depth<self.MAXDEPTH, depth==0 or randint(0,1)]):
                grid[x][y].addConnections(doorDict[(dx,dy)])
                self.recurseRooms(grid, roomDict, x+dx, y+dy, depth+1, doorDict[(-dx,-dy)])
    
    def isValidPos(self, grid, x, y):
        """
        Checks if a given position is valid in the grid.
        
        Parameters:
            grid (list): 2d list of objects
            x (int): x position of the object
            y (int): y position of the object
        
        Returns:
            bool: True if the position is valid, False otherwise
        """
        return (-1<x<len(grid)) and (-1<y<len(grid[0]))
    
    def enterDoor(self, x, y, dx, dy, key):
        """
        Checks if the player can enter the room at x+dx, y+dy by pressing the given key.
        
        Parameters:
            x (int): x position of the player
            y (int): y position of the player
            dx (int): x direction of the door
            dy (int): y direction of the door
            key (str): key pressed by the player
        
        Returns:
            bool: True if the player can enter the room, False otherwise
        """
        if not (self.isValidPos(self.floor, x+dx, y+dy) and self.floor[x+dx][y+dy]!=None): return False
        # uses dict to convert player movement into room movement b/c they are always opposite
        return {'w':'S','s':'N','a':'E','d':'W'}[key] in self.floor[x+dx][y+dy].connections