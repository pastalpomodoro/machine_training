import random
import numpy as np
import time
from classes import *
import pygame

EXPLOSING = 0
EXPLOSED = 1
WAITING = 2

def take_action(s, Q, esp):
    if random.uniform(0, 1) < esp:
        action = random.randint(0, 3)
    else:
        action = np.argmax(Q[s])
    return action
env = EnvGrid(0, 2)
def generate_Q(env):
    Q = []
    for i in range(len(env.grid)):
        for j in range(len(env.grid[i])):
            Q.append([0, 0, 0, 0])
    return(Q)
def print_Q(Q):
    i = 1
    print("----------------------------")
    for q in Q:
        print(i, q)
        i+=1

scale = 100
WIDTH = len(env.grid[0])*scale
HEIGHT = len(env.grid)*scale
pygame.init()
pygame.key.set_repeat(0)
screen = pygame.display.set_mode((WIDTH, HEIGHT+40))
clock = pygame.time.Clock()
running = True

door = pygame.transform.scale(pygame.image.load("./textures/door.png"), (scale, scale))
tale_set = pygame.transform.scale(pygame.image.load("./textures/tale_set.png"), (scale, scale))
pig = pygame.transform.scale(pygame.image.load("./textures/pig/pig_0.png"), (scale, scale))

bombs = []

for i in range(len(env.grid)):
    for j in range(len(env.grid[0])):
        if env.grid[i][j] == -1:
            bombs.append(Bomb(scale, j, i))
# bomb = Bomb(scale, 1, 1)

moveTime = 0
moveTimeDelay = 0

Q = generate_Q(env)

st = env.get_st()

font = pygame.font.Font(None, 30)
trys = 1
defeat = False
defeat_time = 0
defeat_timeDelay = 1.7
at = 4
r = 0
f = "Try: waiting"

steps = 0

for i in range(300):
    st = env.reset()
    esp = max(0.01, 1 - i / 150)
    steps = 0
    while not env.is_finished():
        at = take_action(st, Q, esp)
        stp1, r = env.move(at)
        atp1 = take_action(stp1, Q, 0.0)
        Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])
        st = stp1
        steps += 1
    trys+=1

print_Q(Q)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("black")
    dt = clock.tick(60) / 1000.0
    for i in range(len(env.grid)):
        for j in range(len(env.grid[0])):
            screen.blit(tale_set, (j*scale, i*scale))
            if (env.grid[i][j] > 0):
                screen.blit(door, (j*scale, i*scale))
    for b in bombs:
        tmp = b.draw(screen, dt, env.x, env.y)
        if  tmp == EXPLOSING:
            defeat = True
        elif tmp == EXPLOSED:
            defeat = False
            st = env.reset()
            trys+=1
            print_Q(Q)

    screen.blit(pig, (env.x*scale, env.y*scale))
    texte = font.render("Try n: " + str(trys), True, (255, 255, 255))
    screen.blit(texte, (10, HEIGHT+10))
    moveTime += dt
    if moveTime >= moveTimeDelay: 
        # if not defeat and trys < 150:
        #     if (env.is_finished()):
        #         st = env.reset()
        #         trys+=1
        #         print_Q(Q)
        #     else:
        #         at = take_action(st, Q, 0.6)
        #         stp1, r = env.move(at)
        #         atp1 = take_action(stp1, Q, 0.0)
        #         Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])
        #         st = stp1
        #         if at == 0:
        #             f = "Try: UP"
        #         elif at == 1:
        #             f = "Try: DOWN"
        #         elif at == 2:
        #             f = "Try: LEFT"
        #         else:
        #             f = "Try: RIGHT"
        #         print_Q(Q)
        #     moveTime = 0
        if not defeat:
            if env.is_finished():
                st = env.reset()
            else:
                at = take_action(st, Q, 0.0)
                stp1, r = env.move(at)
                st = stp1
                # print(st, at)
            moveTime = 0
    texte = font.render(f, True, (255, 255, 255))
    screen.blit(texte, (200, HEIGHT+10))
    texte = font.render("steps: " + str(steps), True, (255, 255, 255))
    screen.blit(texte, (400, HEIGHT+10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
