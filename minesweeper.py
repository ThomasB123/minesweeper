from pygame_functions import *
import time
import random

def draw():
    screenSize(size*100+20+size*20,size*100+20)
    setBackgroundColour(background)
    for i in range(gridSize+1):
        drawLine(i*size*100/gridSize+10,10,i*size*100/gridSize+10,size*100+10,lines)
        drawLine(10,i*size*100/gridSize+10,size*100+10,i*size*100/gridSize+10,lines)

def createGrid():
    grid = [0 for i in range(gridSize**2)]
    while grid.count(1) != mines and grid.count(1) != len(grid):
        grid[random.randint(0,len(grid)-1)] = 1
    return grid

def createFlags():
    flags = {}
    for x in range(gridSize):
        for y in range(gridSize):
            flags[(x,y)] = None # None for no flag
    return flags

def numberMines(x,y): # given an (x,y) coordinate, return number of mines in vicinity
    out = 0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if 0 <= i < gridSize and 0 <= j < gridSize:
                out += grid[i+j*gridSize]
    return out - grid[x+y*gridSize]

def numberAll():
    #number = []
    number = {}
    for x in range(len(grid)):
        number[x] = numberMines(x%gridSize,x//gridSize)
        #number.append(numberMines(x%gridSize,x//gridSize))
    return number

def state():
    states = {}
    for x in range(gridSize):
        for y in range(gridSize):
            states[(x,y)] = 0 # 0 for hidden
    return states

def show(x,y):
    global alive
    global left
    if states[(x,y)] == 0 and flags[(x,y)] is None:
        if grid[x+y*gridSize] == 1:
            drawRect(x*size*100/gridSize+10+2,y*size*100/gridSize+10+2,size*100/gridSize-2,size*100/gridSize-2,discovered)
            mine = makeSprite('mine.jpg')
            transformSprite(mine,0,0.3*size/gridSize)
            moveSprite(mine,x*size*100/gridSize+size*50/gridSize+10,y*size*100/gridSize+size*50/gridSize+10,True)
            showSprite(mine)
            alive = False
        elif number[x+y*gridSize] == 0:
            flood(x,y)
        else:
            drawRect(x*size*100/gridSize+10+2,y*size*100/gridSize+10+2,size*100/gridSize-2,size*100/gridSize-2,discovered)
            showLabel(makeLabel(str(number[x+y*gridSize]),50*size//gridSize,x*size*100/gridSize+30*size//gridSize+10,y*size*100/gridSize+30*size//gridSize+10,colours[number[x+y*gridSize]],background=discovered))
            left -= 1
        states[(x,y)] = 1

def flag(x,y):
    global mines
    if states[(x,y)] == 0:
        if flags[(x,y)] is None:
            if mines > 0:
                flag = makeSprite('flag.png')
                transformSprite(flag,0,0.3*size/gridSize)
                moveSprite(flag,x*size*100/gridSize+size*50/gridSize+10,y*size*100/gridSize+size*50/gridSize+10,True)
                showSprite(flag)
                flags[(x,y)] = flag
                mines -= 1
        else:
            killSprite(flags[(x,y)])
            flags[(x,y)] = None
            mines += 1

def showAll():
    for i in range(gridSize):
        for j in range(gridSize):
            show(i,j)

def flood(x,y):
    global left
    q = [(x,y)]
    index = 0
    while index < len(q):
        (x,y) = q[index]
        if states[(x,y)] == 0 and flags[(x,y)] is None:
            # if it's a zero
            drawRect(x*size*100/gridSize+10+2,y*size*100/gridSize+10+2,size*100/gridSize-2,size*100/gridSize-2,discovered)
            #showLabel(makeLabel(str(number[x+y*gridSize]),50*size//gridSize,x*size*100/gridSize+30*size//gridSize+10,y*size*100/gridSize+30*size//gridSize+10,colours[number[x+y*gridSize]],background=discovered))
            states[(x,y)] = 1
            left -= 1
            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if 0 <= i < gridSize and 0 <= j < gridSize and states[(i,j)] == 0 and flags[(i,j)] == None:
                        if number[i+j*gridSize] == 0:
                            q.append((i,j))
                        else:
                            show(i,j)
        index += 1

def main():
    while left > 0:
        if not alive:
            showAll()
            return None
        pygame.event.clear()
        mouseState = pygame.mouse.get_pressed()
        if mouseState[2]: # right click
            x = mouseX()
            y = mouseY()
            x = (x-10)*gridSize//(size*100)
            y = (y-10)*gridSize//(size*100)
            if 0 <= x < gridSize and 0 <= y < gridSize:
                flag(x,y)
        elif mouseState[0]: # left click
            x = mouseX()
            y = mouseY()
            x = (x-10)*gridSize//(size*100)
            y = (y-10)*gridSize//(size*100)
            if 0 <= x < gridSize and 0 <= y < gridSize:
                show(x,y)
        changeLabel(minesLeft,str(mines))
        pause(50)

if __name__ == '__main__':
    # Parameters #
    ####################
    gridSize = 10 # how big the grid is (number of squares = gridSize x gridSize)
    size = 8 # relative size of the window
    mines = 10 # number of mines in the grid 0-100 inclusive
    colours = {0:'white',1:'blue',2:'green',3:'red',4:'purple',5:'maroon',6:'turquoise',7:'black',8:'gray'} # colours of numbers
    lines = 'black' # colour of lines of grid
    background = 'light grey' # colour of background
    discovered = 'white' # colour of square once discovered
    ####################

    left = gridSize*gridSize - mines
    grid = createGrid()
    number = numberAll()
    states = state()
    flags = createFlags()
    draw()
    minesLeft = makeLabel(str(mines),size*10,size*100+20,size*5)
    showLabel(minesLeft)
    alive = True
    start = time.time()
    main()
    end = time.time()
    showLabel(makeLabel(str(round(end-start,1)),size*10,size*100+20,size*50))

    endWait()

# idea
# precompute graphs of chains of paths to be revealed by flood
# to make flood faster
# probably best use breadth first search

# records
# 30 x 30 grid
# 100 mines
# 509 seconds

# 10 x 10 grid
# 10 mines
# 20.6 seconds
