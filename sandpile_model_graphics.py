import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random

MAX = 5


def init(width, height, start_x, start_y):
    SANDPILE = np.zeros((width, height))
    print(type(SANDPILE))
    SANDPILE[start_x][start_y] = 5
    return SANDPILE

def init_random(width, height):
    SANDPILE = np.zeros((width, height))
    random.seed(int)
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            SANDPILE[x][y] = random.randint(0,4)


    return SANDPILE

def update(SANDPILE, width, height, topple):
    SANDPILE[int(width / 2)][int(height / 2)] += 1
    for x in range(0, width, 1):
        for y in range(0, height, 1):

            if SANDPILE[x][y] < MAX:
                SANDPILE[x][y] = SANDPILE[x][y]

            elif SANDPILE[x][y] >= MAX:
                topple += 1
                print("Topple started")
                print(f"Topple Sum:{topple}")

                SANDPILE[x][y] -= 5
                if x + 1 < width:
                    SANDPILE[x + 1][y] += 1
                if x - 1 >= 0:
                    SANDPILE[x - 1][y] += 1
                if y + 1 < height:
                    SANDPILE[x][y + 1] += 1
                if y - 1 >= 0:
                    SANDPILE[x][y - 1] += 1
    print("Sandpile Now:")
    print(SANDPILE)


    return SANDPILE

def update_multiple(SANDPILE, width, height, topple, num_update_places):
    random.seed(int)
    for i in range(0,num_update_places):
        SANDPILE[random.randint(0, width)][random.randint(0, height)] += 1

    print(SANDPILE[random.randint(0, width)][random.randint(0, height)])
    for x in range(0, width, 1):
        for y in range(0, height, 1):

            if SANDPILE[x][y] < MAX:
                SANDPILE[x][y] = SANDPILE[x][y]

            elif SANDPILE[x][y] >= MAX:
                topple += 1
                print("Topple started")
                print(f"Topple Sum:{topple}")

                SANDPILE[x][y] -= 5
                if x + 1 < width:
                    SANDPILE[x + 1][y] += 1
                if x - 1 >= 0:
                    SANDPILE[x - 1][y] += 1
                if y + 1 < height:
                    SANDPILE[x][y + 1] += 1
                if y - 1 >= 0:
                    SANDPILE[x][y - 1] += 1
    print("Sandpile Now:")
    print(SANDPILE)


    return SANDPILE

populated = False
# print("Populated or not (Y/N)")
# populated = str(input())

# if populated == "Y":
#     populated = True

width = 9
height = 9
topple = 0

if populated:
    sandpile = init_random(width, height)
else:
    sandpile = init(width, height, int(width / 2), int(height / 2))

def animate(frames):

    # if populated:
    #     im.set_array(update_multiple(sandpile, width, height, topple, 15))
    # else:
    im.set_array(update(sandpile, width, height, topple))

    return im,


fig = plt.figure()
im = plt.imshow(sandpile, animated=True)


anim = animation.FuncAnimation(fig, animate, frames=10000, interval=0.1, blit=True, repeat=True)
plt.show()
#anim.save("sandpile.gif")