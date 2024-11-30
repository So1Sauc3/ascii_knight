class Tile:
    with open('tile_data.csv', 'r') as f:
        tileData = [t.split(',') for t in f.readlines()]
        tileDict = {t[0]: t[1:] for t in tileData}
    def __init__(self, id):
        """
        Parameters:
            id (str): The ID of the tile to generate.

        Attributes:
            id (str): The ID of the tile.
            char (str): The character to represent the tile in the game.
            dura (int): The durability of the tile.
        """
        self.id = id
        self.char = self.tileDict[id][0] if len(self.tileDict[id][0])==1 else chr(int(self.tileDict[id][0]))
        self.dura = int(self.tileDict[id][1])
    
    def update(self):
        """
        Updates the tile and returns a boolean indicating whether the tile was changed.
        
        Returns:
            bool: True if the tile was changed, False otherwise.
        """
        return True # WIP, update the tile if needed like for trap tiles