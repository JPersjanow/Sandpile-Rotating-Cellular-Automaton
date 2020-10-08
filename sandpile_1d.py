import numpy as np
import matplotlib.pyplot as plt

N = 50
E = 0.1
critical_slope = 5.
n_iter = 1000000

sand = np.zeros(N)
tsav = np.zeros(n_iter)
mass = np.zeros(n_iter)

for iterate in range(0, n_iter):
    move = np.zeros(N)

    for j in range(0, N - 1):
        slope = abs(sand[j+1] - sand[j])
        if slope >= critical_slope:
            print("UNSTABLE")
            avrg = (sand[j] + sand[j+1])/2.
            move[j] += (avrg - sand[j])/2.
            move[j+1] += (avrg - sand[j+1])/2.
            tsav[iterate] += slope/4.

    if tsav[iterate] > 0:
        sand += move

    else:
        j = np.random.random_integers(0,N-1)
        sand[j] += np.random.uniform(0,E)

    sand[N-1] = 0.
    mass[iterate] = np.sum(sand)

    print(f"{iterate}, mass: {mass[iterate]}, sand: {sand}")


plt.plot(range(0,n_iter),mass)
plt.ylabel("Value Sum")
plt.xlabel("Iteration")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.show()
plt.plot(range(0,n_iter),tsav)
plt.ylabel("Relocated value sum")
plt.xlabel("Iteration")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.show()
