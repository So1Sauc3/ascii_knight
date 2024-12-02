# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         LEYOU CHEN
# Section:      520
# Assignment:   LAB 13 GROUP ASSIGNMENT
# Date:         1 12 2024

import keyboard
from GameManager import GameManager
import GuiManager as gui
import time as t
import threading
import queue as q
from os import scandir

# constants
REFRESH_RATE = 0.04
INPUT_RATE = 0.1
HIT_PAUSE = 0.5

# global variables
keyin = q.Queue()

# input listen thread
def input_listen():
    """
    Continuously listens for keyboard input and places the key into a queue.

    This function runs in an infinite loop, reading a key press using the
    keyboard module and adding the key to the global queue `keyin`. It sleeps
    for a short duration defined by `INPUT_RATE` between each key press reading
    to manage input rate.
    """
    while True:
        char = keyboard.read_key()
        keyin.put(char)
        t.sleep(INPUT_RATE)

# setting up threads for input and actual game itself
# separate threads b/c game has stuff like hit-pauses
# while input must stay consistently active
input_thread = threading.Thread(target=input_listen)
input_thread.daemon = True
input_thread.start()
display = gui.GuiManager(10, 10)

# THE GAME ########################################################
while True:
    # MENU SCREEN #################################################
    display.menu()
    menuInput = keyboard.read_key()
    # NEW GAME ####################################################
    if menuInput == "enter" or menuInput == "l":
        # LOAD PREVIOUS SAVE ######################################
        loadGame = True
        saveID = 0
        if menuInput == "l":
            while True:
                k = keyin.get() if not keyin.empty() else None
                if k=="esc":
                    loadGame = False
                    break
                if k and k.isdigit():
                    try:
                        game = GameManager(f"saves/save{int(k)}")
                        saveID = int(k)
                        break
                    except: pass
                display.loadGame()
                t.sleep(REFRESH_RATE)
        else:
            game = GameManager()
            saveID = len([e.name for e in scandir("saves") if e.is_file()])
        
        escaped = False
        # GAME LOOP ###############################################
        while loadGame:
            # input
            k = keyin.get() if not keyin.empty() else None
            # escape menu logic
            if k=="esc": escaped = True
            if escaped and k=="enter": escaped = False
            if escaped and k=="x": break
            
            # ESCAPED #############################################
            if escaped:
                display.escaped()
            # RUNNING #############################################
            else:
                uOut, eOut = game.tick(k)
                display.game(game, uOut, eOut)
            
            if "hitEntity" in (uOut, eOut): t.sleep(HIT_PAUSE)
            if "dmged" in (uOut, eOut): t.sleep(HIT_PAUSE)
            if "dead" in (uOut, eOut): break
            t.sleep(REFRESH_RATE)
        # GAME OVER ###############################################
        if loadGame:
            game.save(saveID)
            display.gameOver(f"save{saveID}.txt", game.h, game.c)
            while keyin.get()!="esc":
                display.gameOver(f"save{saveID}.txt", game.h, game.c)
                t.sleep(REFRESH_RATE)
    # EXIT ########################################################
    if menuInput == "x":
        display.endCredits()
        break

# # UNSUSED DEBUG FUNCTION
# def printFloor(f, floorsize, roomSize):
#     for j in range(floorsize):
#         roomRow = ["" for _ in range(roomSize)]
#         for i in range(floorsize):
#             for k in range(roomSize):
#                 if f.floor[i][j]==None: roomRow[k] += "         "
#                 else: roomRow[k] += f.floor[i][j].getRoomDisplay()[k]
#         for r in roomRow: print(r)