import pygame
import time

EXPLOSING = 0
EXPLOSED = 1
WAITING = 2

class EnvGrid:
    def __init__(self, init_x, init_y):
        self.grid = [
            [0,  0,  0,  0,  0, 0, 1],
            [0,  0,  0,  0,  0, 0, 0],
            [0,  0,  0,  0,  0, 0, 0],
            [0,  0,  0,  0,  0, 0, 0]
        ]
        #start pos
        self.init_x = init_x
        self.init_y = init_y
        self.x = init_x
        self.y = init_y
        self.actions = [
            [-1, 0], #up
            [1, 0], #down
            [0, -1], #left
            [0, 1] #right
        ]
    def show(self):
        print("-----------------------------")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == self.y and j == self.x:
                    print('X  ', end="")
                else:
                    print(self.grid[i][j], " ", end="")
            print("")
    def move(self, at):
        self.y = max(0, min(self.y+self.actions[at][0], len(self.grid)-1))
        self.x = max(0, min(self.x+self.actions[at][1], len(self.grid[0])-1))
        return (self.y*len(self.grid[0])+self.x), (self.grid[self.y][self.x])
    def is_finished(self):
            return self.grid[self.y][self.x] > 0
    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        return self.y * len(self.grid[0]) + self.x
    def get_st(self):
        return self.y * len(self.grid[0]) + self.x

class Bomb:
    def __init__(self, scale, x, y):
        self.x = x
        self.y = y
        self.time_scale = 0
        self.bomb_timePerFrame = 0.086*self.time_scale
        self.bomb_timeFrame = 0
        self.bomb_indexFrame = 0
        self.boom_timePerFrame = 0.035*self.time_scale
        self.boom_timeFrame = 0
        self.boom_indexFrame = 0
        self.bomb_active = False
        self.scale = scale
        self.bombTex = []
        for i in range(5):
            self.bombTex.append(pygame.transform.scale(pygame.image.load("./textures/bomb/bomb_" + str(i) + ".png"), (scale, scale)))
        self.boomTex = []
        for i in range(6):
            self.boomTex.append(pygame.transform.scale(pygame.image.load("./textures/bomb/boom_" + str(i) + ".png"), (scale, scale)))
    def draw(self, screen, dt, ax, ay):
        tmp = False
        if ax == self.x and ay == self.y:
            tmp = True
            if not self.bomb_active:
                self.bomb_timeFrame += dt
                if self.bomb_timeFrame >= self.bomb_timePerFrame:
                    self.bomb_indexFrame+=1
                    self.bomb_timeFrame = 0
                    if self.bomb_indexFrame == len(self.bombTex):
                        self.bomb_active = True
                        self.bomb_indexFrame = 0
            else:
                self.boom_timeFrame += dt
                if self.boom_timeFrame >= self.boom_timePerFrame:
                    self.boom_indexFrame+=1
                    self.boom_timeFrame = 0
                    if self.boom_indexFrame == len(self.boomTex):
                        self.bomb_active = False
                        self.boom_indexFrame = 0
                        return EXPLOSED
        if not self.bomb_active:
            screen.blit(self.bombTex[self.bomb_indexFrame], (self.x*self.scale, self.y*self.scale))
        else:
            screen.blit(self.boomTex[self.boom_indexFrame], (self.x*self.scale, self.y*self.scale))
        if tmp:
            return EXPLOSING
        return WAITING