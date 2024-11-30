from colorama import Fore, Back, Style
from random import choice
import os
# game width is 22

class GuiManager:
    PLAYERCHAR = Fore.GREEN+chr(9829)+Fore.RESET
    
    with open('display_templates.txt', 'r') as f:
        displays = [i.split('\n') for i in f.read().split('\n\n')]
        displayDict = {i[0]:i[1:] for i in displays}
    with open('tile_data.csv', 'r') as f:
        tileData = [t.split(',') for t in f.readlines()]
        tileDict = {t[0]: t[1:] for t in tileData}
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')
    
    def convert(self, s):
        if s in self.tileDict:
            t = self.tileDict[s][0]
            if len(str(t))==1: return t
            return chr(int(t))
        return s
    
    def getScreen(self, screenID):
        return ["".join([self.convert(t) for t in row]) for row in self.displayDict[screenID]]
    
    def menu(self):
        self.cls()
        prt = self.getScreen("menu")
        for r in prt: print(r)
    
    def game(self, game, uOut, eOut):
        self.cls()
        
        r, pPos, h, m, c = game.r, game.pPos, game.h, game.m, game.c
        
        roomDisplay = ["".join([t.char for t in row]) for row in r.room]
        
        # debug depth
        roomDisplay[2] = roomDisplay[2][:1] + f"{r.id:2}" + roomDisplay[2][3:]
        
        # door display
        if "N" not in r.connections: roomDisplay[0] = roomDisplay[0].replace(chr(9015), chr(9552))
        if "E" not in r.connections: roomDisplay[len(roomDisplay)//2] = roomDisplay[len(roomDisplay)//2][:-1] + chr(9553)
        if "W" not in r.connections: roomDisplay[len(roomDisplay)//2] = chr(9553) + roomDisplay[len(roomDisplay)//2][1:]
        if "S" not in r.connections: roomDisplay[-1] = roomDisplay[-1].replace(chr(9015), chr(9552))
        
        # dynamic positions of all entities, sorted by row col
        movingPositions = sorted([(e.pos, e.char) for e in r.entities]+[(pPos, self.PLAYERCHAR)], key=lambda ps: ps[0][1])
        
        # inserting entity chars and adjusting for colorama code lengths
        for p in movingPositions:
            x, y = p[0]
            ch = p[1]
            y+=10*len([p for p in movingPositions if p[0][0]==x and p[0][1]<y]) # correcting entity colorama code offset
            roomDisplay[x] = roomDisplay[x][:y]+ch+roomDisplay[x][y+1:]
        
        # GUI sections
        top = self.getScreen("gameScreenTop")
        top[1] = top[1].replace("_", f"{str(h):>18}")
        top[2] = top[2].replace("_", f"{str(m):>18}")
        top[3] = top[3].replace("_", f"{str(c):>18}")
        edge = self.getScreen("gameScreenEdge")
        bottom = self.getScreen("gameScreenBottom")
        
        # stitch together
        for i in range(len(roomDisplay)):
            eXs = len([p for p in movingPositions if p[0][0]==i])
            #if i==x: eXs+=1
            width = 22+10*eXs
            roomDisplay[i] = edge[0] + roomDisplay[i].center(width) + edge[0]
        
        # print
        for r in top: print(r)
        for r in roomDisplay: print(r)
        for r in bottom: print(r)
        
        # special events (during hit pauses)
        if uOut:
            if "hitEntity" in uOut: print("Attack landed!") # player attacked entity
            if "dmged" in uOut: print("You were hit!") # player collided into entity
            if "cantAttack" in uOut: print("Attack on cool down") # player can't attack
        if eOut:
            if "dmged" in eOut: print("You were hit!") # entity collided into player
            
    def escaped(self):
        self.cls()
        for r in self.getScreen("gamePaused"): print(r)
    
    def gameOver(self):
        self.cls()
        for r in self.getScreen("gameOver"): print(r)
    
    def endCredits(self):
        self.cls()
        for r in self.getScreen("endCredits"): print(r)