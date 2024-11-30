from random import choice
from colorama import Fore
class Entity:
    def __init__(self, char, h, pos):
        """
        Parameters:
            char (str): Character to represent the entity in the game
            h (int): Entity's health
            pos (tuple): Entity's starting position as a (x,y) tuple
        """
        self.char = Fore.RED+char+Fore.RESET
        self.h = h
        self.pos = pos
        pass
    
    def tick(self, r, pPos):
        """
        Update the entity's position and handle collisions with the player.

        Parameters:
            r (Room): The room the entity is in
            pPos (tuple): The position of the player

        Returns:
            str: "dead" if the entity is killed, "hitPlayer" if the entity hits the player, "moved" if the entity moves to a new position, or "moveFailed" if the entity's move is blocked
        """
        if self.h<1: return "dead"
        
        # random movement
        dx, dy = choice([(-1,0),(0,-1),(1,0),(0,1)])
        nPos = (self.pos[0]+dx, self.pos[1]+dy)
        if r.isValidPos(r.room, nPos[0], nPos[1]) and nPos not in [e.pos for e in r.entities]:
            if nPos==pPos: return "hitPlayer"
            else:
                self.pos = nPos
                return "moved"
        return "moveFailed"
    
    def atb(self, atb, val, change=True):
        """
        Applies a value to one of the entity's attributes.

        Parameters:
            atb (str): The attribute to apply the value to. "h" for health.
            val (int): The value to apply to the attribute.
            change (bool): Whether to change the attribute to the given value or add the given value to it.

        Returns:
            str: "hitEntity" if the entity's health was changed, "missed" if the attribute was not changed.
        """
        match atb:
            case "h": # health
                self.h = val if not change else self.h + val
                return "hitEntity"
            case _: return "missed"