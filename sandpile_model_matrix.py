import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

MAX = 4  # maximum heigght of sandpile
width = 50
height = 50
SANDPILE = np.zeros((width, height))  # array generation
NUM_ITER = 10000
print(SANDPILE)
mass_whole = 0
mass_during_iteration = []
dislocated_count = 0
when_discolaction = []

iteration_array = []
for i in range(0,NUM_ITER,1):
    iteration_array.append(i)

for i in range(NUM_ITER):
    print(f"iteration: {i}")
    SANDPILE[int(width/2)][int(height/2)] += 1
    mass_whole += 1
    print(f"{i}: mass {mass_whole}")
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            print(f"cell: ({x}, {y})")

            if SANDPILE[x][y] >= MAX:
                SANDPILE[x][y] = SANDPILE[x][y] - 4
                dislocated_count += 1
                when_discolaction.append(i)

                if x + 1 < width:
                    SANDPILE[x + 1][y] += 1
                else:

                    mass_whole -= 1

                if x - 1 >= 0:
                    SANDPILE[x - 1][y] += 1
                else:

                    mass_whole -= 1

                if y + 1 < height:
                    SANDPILE[x][y + 1] += 1
                else:

                    mass_whole -= 1

                if y - 1 >= 0:
                    SANDPILE[x][y - 1] += 1
                else:

                    mass_whole -= 1


            print(SANDPILE)
    mass_during_iteration.append(mass_whole)

print("Final Sandpile")
print(SANDPILE)

plt.plot(iteration_array, mass_during_iteration)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlabel("Iteration")
plt.ylabel("Value sum")
plt.show()

lists = sorted(Counter(when_discolaction).items())
when_discolaction, dislocated_count = zip(*lists)
plt.bar(when_discolaction, dislocated_count)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.xlabel("Iteration")
plt.ylabel("Relocated value sum")
plt.show()