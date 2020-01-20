from random import random
from time import time
from sys import setrecursionlimit
import pygame
import maze

setrecursionlimit(2000)

pygame.display.init()
pygame.font.init()
window = pygame.display.set_mode((200, 200), flags=pygame.RESIZABLE)
font = pygame.font.Font(None, 30)
gameClock = pygame.time.Clock()
running = True
successPrinted = False
fCount = 0

maze = maze.Maze(2, 2, window)
solveRate = 1
solveSteps = 1 # Account of steps executed each `solveRate` frames
print("Stepping {} times each {} frames".format(solveSteps, solveRate))

print(maze)

while running:
    gameClock.tick(60)
    fCount += 1
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        running = False
    if e.type == pygame.VIDEORESIZE:
        #maze.setCsize(e=e)
        maze.cw = 30
        maze.ch = 30
        window.fill((255, 255, 255))
        maze.show_unoptimized()
        pygame.display.flip()
        
    if (not maze.isPerfect()) and fCount % solveRate == 0:
        for _i in range(solveSteps):
            maze.step()
        pygame.display.set_caption("{}/{}".format(maze.openWalls, len(maze.cells)))
        window.fill((255, 255, 255))
        maze.show_unoptimized()
        pygame.display.flip()
        
    elif maze.isPerfect():
        if not successPrinted:
            successPrinted = True
            print("Created perfect maze !")    