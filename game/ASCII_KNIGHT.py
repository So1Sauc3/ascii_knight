import keyboard
from GameManager import GameManager
import GuiManager as gui
import time as t
import threading
import queue as q

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

with open("saves/save0.txt", "w") as f:
    f.write("test")

# THE GAME ########################################################
while True:
    gCounter = 0
    # MENU SCREEN #################################################
    display.menu()
    match keyboard.read_key():
        # NEW GAME ################################################
        case "enter":
            game = GameManager()
            escaped = False
            # GAME LOOP ###########################################
            while True:
                # input
                k = keyin.get() if not keyin.empty() else None
                # escape menu logic
                if k=="esc": escaped = True
                if escaped and k=="enter": escaped = False
                if escaped and k=="x": break
                
                # ESCAPED #########################################
                if escaped:
                    display.escaped()
                # RUNNING #########################################
                else:
                    uOut, eOut = game.tick(k)
                    display.game(game, uOut, eOut)
                
                if "hitEntity" in (uOut, eOut): t.sleep(HIT_PAUSE)
                if "dmged" in (uOut, eOut): t.sleep(HIT_PAUSE)
                if "dead" in (uOut, eOut): break
                t.sleep(REFRESH_RATE)
            # GAME OVER ###########################################
            gCounter+=1
            game.save(gCounter)
            display.gameOver(f"save{gCounter}.txt", game.h, game.c)
            while keyin.get()!="esc":
                display.gameOver(f"save{gCounter}.txt", game.h, game.c)
                t.sleep(REFRESH_RATE)
        # EXIT ####################################################
        case "x":
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