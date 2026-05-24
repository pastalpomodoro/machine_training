import time
import random
from classes import *

map = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]

endpoint = Vect2(7, 3)

def print_map(map):
    for i in range(len(map)):
        print(map[i])

ai = Ai(map)
moves = []
bestTryIndex = 0
for i in range(10):
    nMove = 0
    tmp = []
    ai.vPos = Vect2(ai.initPos.x, ai.initPos.y)
    print("try: ", i+1)
    while (ai.vPos != endpoint):
        num = random.randint(0, 3)
        map[ai.vPos.y][ai.vPos.x] = 0
        if (num == 0):
            tmp.append("UP")
            ai.UP()
        elif (num == 1):
            tmp.append("DOWN")
            ai.DOWN()
        elif (num == 2):
            tmp.append("RIGHT")
            ai.RIGHT()
        else :
            tmp.append("LEFT")
            ai.LEFT()
        map[ai.vPos.y][ai.vPos.x] = 1
        # print("POS: ", ai.vPos.y, ai.vPos.x)
        nMove+=1
        if (ai.vPos.x == endpoint.x and ai.vPos.y == endpoint.y):
            tmp.append("successs")
            break
    if (i == 0):
        bestTryIndex = i
    elif nMove < len(moves[bestTryIndex]):
        bestTryIndex = i
    print("success in: ", nMove)
    moves.append(tmp)
    time.sleep(1)

for move in moves:
    print(move)
print("Best Try Index: ", bestTryIndex)
print(moves[bestTryIndex])