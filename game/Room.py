from Tile import Tile
from Entity import Entity
from random import randrange, choice

class Room:
    ENEMYDENSITY = 5
    ENTITYCHARS = [chr(u) for u in [9824, 9827, 9830]]
    NOENTITYROOMS = [] # "f0r0"
    
    with open('room_templates.txt', 'r') as f:
        rooms = [i.split('\n') for i in f.read().split('\n\n')][1:]
        roomDict = {r[0]: r[1:] for r in rooms}
    
    def __init__(self, id, roomType):
        """
        Parameters:
            id (int): id of the room
            roomType (str): type of the room (e.g. "f0r0")
        Attributes:
            id (int): id of the room
            room (list): 2d list of Tile objects
            roomType (str): type of the room (e.g. "f0r0")
            connections (list): list of connections to other rooms
            entities (list): list of Entity objects
        """
        self.id = id # room number as it generates in the floor; DEPTH
        self.room = self.generateRoom(roomType)
        self.roomType = roomType
        self.connections = []
        self.entities = []
        if self.id!=0: self.entities = self.placeEntities() if roomType not in self.NOENTITYROOMS else []
    def generateRoom(self, roomType):
        """
        Generates a room based on the given roomType. The roomType should be
        a string that corresponds to a room ID in the roomDict dictionary.

        Parameters:
            roomType (str): The ID of the room to generate.

        Returns:
            list: A 2d list of Tile objects, representing the generated room.
        """
        try: return [[Tile(c) for c in row] for row in self.roomDict[roomType]]
        except: return "Room ID not found"
    def placeEntities(self):
        """
        Places entities in the room based on the ENEMYDENSITY constant. Randomly
        places entities in empty spaces in the room.

        Returns:
            list: List of Entity objects placed in the room.
        """
        entities = []
        # row col traverse, place entity according to density
        for x in range(len(self.room)):
            for y in range(len(self.room[x])):
                if self.room[x][y].id==" " and randrange(0,100)<Room.ENEMYDENSITY:
                    entities.append(Entity(choice(Room.ENTITYCHARS), 10, (x,y))) # assign random char
        return entities
    def addConnections(self, directions):
        """
        Adds the given directions to the room's connections. The given directions
        are added after removing any duplicates.

        Parameters:
            directions (str): A string of directions to add to the room's connections.
        """
        if directions==None: return # maybe a try catch here
        for d in set(directions):
            if d.upper() in "NESW": self.connections.append(d.upper())
    
    def removeConnections(self, directions):
        """
        Removes the given directions from the room's connections. The given directions
        are removed after removing any duplicates.

        Parameters:
            directions (str): A string of directions to remove from the room's connections.
        """
        if directions==None: return # maybe a try catch here
        for d in set(directions): self.connections.remove(d.upper())
    
    def isValidPos(self, grid, x, y):
        """
        Checks if a given position is valid in the grid and has a tile with 0 durability.

        Parameters:
            grid (list): A 2d list of Tile objects.
            x (int): The x position of the tile to check.
            y (int): The y position of the tile to check.

        Returns:
            bool: True if the position is valid and the tile has 0 durability, False otherwise.
        """
        if 0<=x<len(grid) and 0<=y<len(grid[0]):
            if grid[x][y].dura==0: return True # could add more conditions in future
    
    def updateTiles(self, tiles):
        """
        Updates all the tiles in the room and returns a list of the outputs from
        each tile's update method. The outputs will be in the same order as the
        tiles in the input list.

        Parameters:
            tiles (list): A list of Tile objects to update.

        Returns:
            list: A list of the outputs from each tile's update method.
        """
        outputs = [t.update() for t in tiles] # WIP for when I need to update tiles
        return outputs

    def tickEntities(self, pPos):
        """
        Updates all the entities in the room and returns a list of their outputs.

        Parameters:
            entities (list): A list of Entity objects to update.

        Returns:
            bool: Whether or not the room should be updated again.
        """
        outputs = []
        for e in self.entities:
            if e.h<1: # prune dead entities
                self.entities.remove(e)
                outputs.append("dead")
            else: outputs.append(e.tick(self, pPos)) # tick entity
        return outputs