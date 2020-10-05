import maze

m = maze.Maze(50, 50)

while not m.isPerfect():
    m.step()

for row in m.asGrid():
    for c in row:
        print("[X]" if c else "   ", end="")
    print("")