import threading
import time as t
import queue as q
import keyboard as kb


queue = q.Queue()
def input_listen():
    while True:
        char = kb.read_key()
        queue.put(char)

input_thread = threading.Thread(target=input_listen)
input_thread.daemon = True
input_thread.start()

while True:
    t.sleep(1)
    print(f"Queue values: {queue.queue}")