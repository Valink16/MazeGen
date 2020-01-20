import unionfind as uf
try:
    from pygame import draw, font, Rect
except ImportError:
    print("[WARNING] Could not import pygame, GUI will be disabled")

from random import randint, random

try:
    font.init()
    textFont = font.Font(None, 30)
except NameError:
    pass

# TODO: Add an array of indexes to choose from for the walls

class Maze:
    def __init__(self, w, h, window=None):
        self.w = w
        self.h = h
        self.window = window

        if window: self.setCsize()

        self.cells = [uf.Node(i) for i in range(w * h)]
        verticalWalls = [True for _i in range((w + 1) * h)]
        horizontalWalls = [True for _i in range((h + 1) * w)]
        self.hwStartIndex = len(verticalWalls) # all walls from 0 to self.hwStartIndex - 1 are vertical walls, rest is horizontal
        self.walls = verticalWalls + horizontalWalls
        self.openWalls = 0 

        # All indexes of walls which are openables        
        self.openable = [i for i in range(1, self.hwStartIndex) if i % (self.w + 1) > 0 and i % (self.w + 1) < self.w] + \
                        [i for i in range(self.hwStartIndex + self.w, len(self.walls) - self.w)]

    def __repr__(self):
        return str("Maze: {} cells, {} vertical walls, {} horizontal walls".format(len(self.cells), self.hwStartIndex, len(self.walls) - self.hwStartIndex))

    # Opens wall at i and updates self.openWalls
    def openWall(self, i):
        self.walls[i] = False
        self.openWalls += 1

    def setCsize(self, e=None):
        if not e:
            ww, wh = self.window.get_size()
            self.cw = ww / self.w
            self.ch = wh / self.h
        else:
            self.cw = e.w / self.w
            self.ch = e.h / self.h

    def show_unoptimized(self): # Requires pygame, will crash if launched without it
        for i in range(len(self.walls) - self.hwStartIndex):
            if self.walls[i]:
                pos = Rect(i % (self.w + 1) * self.cw, i // (self.w + 1) * self.ch, 0, 0)
                draw.line(self.window, (0,0,0), pos[:2], pos.move(0, self.ch)[:2])
        
        for i in range(self.hwStartIndex, len(self.walls)):
            if self.walls[i]:
                a = (i - self.hwStartIndex)
                pos = Rect(a % self.w * self.cw, a // self.w * self.ch, 0, 0)
                draw.line(self.window, (0,0,0), pos[:2], pos.move(self.cw, 0)[:2])

    def step(self):
        # Choosing a wall randomly which is not already open
        if len(self.openable) > 0:
            i = self.openable.pop(randint(0, len(self.openable) - 1))
        else:
            return

        # Get the right type of walls
        wallType = ("hor", "vert") [i < self.hwStartIndex]

        #print("i: {}, walls len: {}, openable: {}".format(i, len(self.walls), len(self.openable)))
        
        a = (i, i - self.hwStartIndex) [i >= self.hwStartIndex]
        if self.walls[i] == True:
            c1Index, c2Index = None, None
            if wallType == "vert":
                c1Index = a - (i // (self.w + 1) + 1)
                c2Index = a - i // (self.w + 1)

            elif wallType == "hor":
                c1Index = a-self.w
                c2Index = a

            else:
                raise Exception("WallType is neither vertical nor horizontal")
            
            c1, c2 = self.cells[c1Index], self.cells[c2Index]
            #print("Accessing cells {}-{}".format(c1.id, c2.id))

            if not c1.find() == c2.find():
            #    print("Opening wall {}".format(i))
                self.openWall(i)
                c1.unite(c2)
            #else:
            #    print("{} and {} are already connected".format(c1.id, c2.id))
        else:
            print("big BRUH")

    def isPerfect(self):
        return self.w * self.h - 1 == self.openWalls

    # Generates a 2D grid with (or non-)navigeable "cells", represented by booleans
    def asGrid(self):
        gridW = self.w * 2 + 1
        gridH = self.h * 2 + 1
        grid = [[True for i in range(gridW)] for j in range(gridH)]

        for y in range(len(grid)): # Freeing up the cells
            for x in range(len(grid[y])):
                if y % 2 == 1 and x % 2 == 1: # Is a cell
                    grid[y][x] = False

        for wIndex in range(self.hwStartIndex): # Vertical walls
            x = wIndex % (self.w + 1) * 2
            y = wIndex // (self.w + 1) * 2 + 1
            #print("Setting vertical wall @ {} to {}".format((x, y), self.walls[wIndex]))
            grid[y][x] = self.walls[wIndex]

        for wIndex in range(0, len(self.walls) - self.hwStartIndex): # Horizontal walls
            x = wIndex % (self.w) * 2 + 1
            y = wIndex // (self.w) * 2
            #print("Setting horizontal wall @ {} to {}".format((x, y), self.walls[wIndex + self.hwStartIndex]))
            grid[y][x] = self.walls[wIndex + self.hwStartIndex]
            
        return grid