from os import path
from Floor import Floor

class GameManager:
    ENTITYTICKDELAY = 20
    ATTACKCOOLDOWN = 5
    
    def __init__(self, fileName=None):
        """
        Constructor for GameManager.

        Initializes the game by creating a new floor and player.
        Sets player's health, mana, and coins to 10, 20, and 0, respectively.
        Sets entity and attack timers to 0.
        """
        if fileName!=None:
            self.load(fileName)
            pass
        else:
            self.dungeon = [Floor(0, "f0")]
            self.fPos = 0
            self.f = self.dungeon[self.fPos]
            self.rPos = (Floor.STARTINGROOMX, Floor.STARTINGROOMY)
            self.r = self.f.floor[self.rPos[0]][self.rPos[0]]
            self.pPos = (len(self.r.room)//2, len(self.r.room)//2)
            self.h, self.m, self.c = 10, 20, 0
            self.entityTimer, self.attackTimer = 1, 1
    
    def load(self, fileName):
        with open(fileName, "r") as f:
            data = f.read().split("\n\n")
            stats = [row.split(":")[1] for row in data[1].split("\n")] # h m c
            pos = [row.split(":")[1] for row in data[2].split("\n")] # fPos rPos pPos
            timers = [row.split(":")[1] for row in data[3].split("\n")] # entityTimer attackTimer
            floorGrid = [row.split(" ") for row in data[4].split("\n")[1:-1]] # floor layout, id:roomType
            
            self.h, self.m, self.c = int(stats[0]), int(stats[1]), int(stats[2])
            self.fPos = int(pos[0])
            self.rPos = (int(pos[1].split(",")[0]), int(pos[1].split(",")[1]))
            self.pPos = (int(pos[2].split(",")[0]), int(pos[2].split(",")[1]))
            self.entityTimer, self.attackTimer = int(timers[0]), int(timers[1])
            
            # load floor
            self.dungeon = [Floor(0, "f0", floorGrid)]
            self.f = self.dungeon[self.fPos]
            self.r = self.f.floor[self.rPos[0]][self.rPos[0]]
        return
    
    def atb(self, atb, val, change=True):
        """
        Applies a value to one of the player's attributes.

        Parameters:
            atb (str): The attribute to apply the value to. "h" for health, "m" for mana, "c" for coins.
            val (int): The value to apply to the attribute.
            change (bool): Whether to change the attribute to the given value or add the given value to it.

        Returns:
            str: "dead" if the player's health was reduced to 0, "dmged" if the player's health was changed, "broke mf" if the player's coins were reduced below 0, or False if the attribute was not changed.
        """
        match atb:
            case "h": # health
                if self.h<1: return "dead"
                self.h = val if not change else self.h + val
                return "dmged"
            case "m": # mana
                if self.m<1: return self.atb("h", -1) # use health when out of mana
                else: self.m = val if not change else self.m + val
            case "c": # coins
                self.c = val if not change else self.c + val
                if self.c<0:
                    self.c = 0
                    return "broke mf" # not possible by normal means lol
            case _: return False
    
    def movePlayer(self, key):
        """
        Moves the player in the direction of the given key.

        Parameters:
            key (str): The direction to move the player in. "w" for up, "a" for left, "s" for down, "d" for right.

        Returns:
            str: "moved" if the player moved to a new position, "dmged" if the player collided with an entity, "enteredRoom" if the player entered a new room, or "moveFailed" if the player's move was blocked.
        """
        dx, dy = {'w':(-1,0), 'a':(0,-1), 's':(1,0), 'd':(0,1)}[key]
        nPos = (self.pPos[0]+dx, self.pPos[1]+dy)
        
        # basic move logic
        if self.r.isValidPos(self.r.room, nPos[0], nPos[1]):
            if nPos not in [e.pos for e in self.r.entities]:
                self.pPos = nPos
                return "moved"
            else:
                # player collides with an entity
                return self.atb("h", -1)
        
        # door entering logic
        if self.r.room[nPos[0]][nPos[1]].id=="d" and self.f.enterDoor(self.rPos[0], self.rPos[1], dy, dx, key):
            self.rPos = (self.rPos[0]+dy, self.rPos[1]+dx)
            self.r = self.f.floor[self.rPos[0]][self.rPos[1]]
            l = len(self.r.room)
            self.pPos = (l//2-dx*(l//2-1), l//2-dy*(l//2-1))
            
            # remove entity if noclipping into player, janky solution!
            for e in self.r.entities:
                if e.pos==self.pPos:
                    self.r.entities.remove(e)
            return "enteredRoom"
        return "moveFailed"
    
    def attack(self):
        """
        Attack in the four cardinal directions.

        Returns:
            str: "attackFailed" if no entities were hit, "hitEntity" if an entity was hit, or "cantAttack" if the player is on cooldown.
        """
        # basic attack logic, may implement spells in future
        if self.attackTimer%self.ATTACKCOOLDOWN==0:
            eOuts = "attackFailed"
            for e in self.r.entities:
                for d in [(-1,0),(0,-1),(1,0),(0,1)]:
                    if e.pos==(self.pPos[0]+d[0], self.pPos[1]+d[1]): eOuts = e.atb("h", -10)
            self.attackTimer = 1
            self.atb("m", -1) # *eOuts.count("hitEntity")
            return eOuts
        return "cantAttack"
    
    def userInput(self, key):        
        """
        Processes the player's input and executes the corresponding action.

        Parameters:
            key (str): The input key pressed by the player.

        Returns:
            str: The result of the action taken based on the input key.
                - "moved", "dmged", "enteredRoom", or "moveFailed" if the player moves.
                - "hitEntity", "attackFailed", or "cantAttack" if the player attacks.
                - None if no valid action is performed.
        """
        if key==None: return None
        if key.lower() in "wasd": return self.movePlayer(key)
        match key.lower():
            case "space": return self.attack()
    
    def tick(self, key):
        # update player
        """
        Updates the game state based on the player's input and other events.

        Parameters:
            key (str): The input key pressed by the player.

        Returns:
            tuple: A tuple of two strings. The first is the result of the player's action, and the second is the result of the entities' actions.
                - The first element may be "moved", "dmged", "enteredRoom", or "moveFailed" if the player moves.
                - The first element may be "hitEntity", "attackFailed", or "cantAttack" if the player attacks.
                - The first element will be None if no valid action is performed.
                - The second element may be "hitPlayer" if an entity hits the player, or "dead" if an entity is killed.
        """
        uOut, eOut = self.userInput(key), ""
        
        # update entities
        self.entityTimer += 1
        if self.entityTimer%self.ENTITYTICKDELAY==0:
            entityOut = self.r.tickEntities(self.pPos)
            for out in entityOut:
                if out=="hitPlayer": eOut = self.atb("h", -1)
                if out=="dead": self.atb("c", 1)
            self.entityTimer = 1
        
        # update attack timer
        if self.attackTimer<self.ATTACKCOOLDOWN: self.attackTimer += 1
        
        return uOut, eOut
    
    def save(self, counter):
        """
        Saves the game state to a file named "save<counter>.txt" in the "saves" directory.

        Parameters:
            counter (int): The number of the save to write.

        Returns:
            None
        """
        with open(f"saves/save{str(counter)}.txt", "w") as f:
            f.write(f"Save #{str(counter)}\n\n")
            f.write(f"Health:{self.h}\nMana:{self.m}\nCoins:{self.c}\n\n")
            f.write(f"Floor Position:{self.fPos}\nRoom Position:{self.rPos[0]},{self.rPos[1]}\nPlayer Position:{self.pPos[0]},{self.pPos[1]}\n\n")
            f.write(f"Entity Timer:{self.entityTimer}\nAttack Timer:{self.attackTimer}\n\n")
            f.write("Floor Layout:\n")
            for r in self.f.floor:
                for room in r:
                    if room: f.write(f"{room.id}:{room.roomType}:{("".join(room.connections)+"____")[:4]} ")
                    else: f.write("0:NONE:NONE ")
                f.write("\n")