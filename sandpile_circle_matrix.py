from random import randint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

class Sandpile:
    """
    Class representing sandpile model for Self-Organized Criticality


    number_radial = number representing r values (must be odd number)
    umber_angles = numer representing theta values
    array = array representing sandpile with r and theta
    max_peak = maximum sand grains on position [r][theta]
    topple_count = sums how many topples occured during simulation
    mass_count = sums whole mass gathered during simulation
    mass_fallen_count = sums mass that was thrown out outside disk
    mass_left_count = sums mass left on disk
    mass_when_iteration = array consisting of mass during every iteration
    when_topple = array consisting of iteration when topple occured

    angles_array = angles array for plotting (required by matplotlib)
    radial_array = radial array for plotting (required by matplotlib)
    """

    #initialization of sandpile
    def __init__(self, number_radial, number_angles, max_peak, force=False, addition_random=False):
        """
        Initialisation function for Sandpile class
        :param number_radial:
        :param number_angles:
        :param max_peak:
        """
        self.number_radial = number_radial
        self.number_angles = number_angles
        self.array = np.zeros((self.number_radial, self.number_angles))
        self.max_peak = max_peak
        self.topple_count = 0
        self.mass_count = 0
        self.mass_fallen_count = 0
        self.mass_left_count = 0
        self.mass_when_iteration = []
        self.when_topple = []

        self.number_of_simulations = 0

        self.force = force
        self.addition_random = addition_random

        self.angles_array = np.linspace(0, 2 * np.pi, number_angles + 1)
        self.radial_array = np.linspace(0, number_radial, number_radial + 1)

    def count_mass_left(self):
        """
        Function for counting how much mass is left on disk
        :return:
        """
        self.mass_left_count = int(np.sum(self.array))

    def add_grain(self, radial_position):
        """
        Adds grain to chosen radial position and random angle position
        :param radial_position:
        :return:
        """

        self.mass_count += 1
        if self.addition_random:
            self.array[randint(0, self.number_radial - 1)][randint(0, self.number_angles - 1)] += 1
        else:
            self.array[radial_position][randint(0, self.number_angles - 1)] += 1

    def topple_sumulate_centrifugal_force(self, radial_position, angle_position, iteration, direction='right'):

        #gather data
        self.topple_count += 1
        self.when_topple.append(iteration)

        #execute topple with force simulation
        taken_grains = 3
        self.array[radial_position][angle_position] -= taken_grains

        #topples right
        if angle_position == self.number_angles - 1:
            self.array[radial_position][0] += 1
        else:
            self.array[radial_position][angle_position + 1] += 1

        #topples down
        if radial_position < self.number_radial - 1:
            self.array[radial_position + 1][angle_position] += 1
        else:
            self.mass_fallen_count += 1

        #topples skos
        if radial_position < self.number_radial - 1:
            if angle_position == self.number_angles - 1:
                self.array[radial_position + 1][0] += 1
            else:
                self.array[radial_position + 1][angle_position + 1] += 1
        else:
            self.mass_fallen_count += 1

    def topple(self, radial_position, angle_position, iteration):
        """
        Topple function, gathers data, strips current sandpile location, distributes taken grains to 3 nearby locations
        :param radial_position:
        :param angle_position:
        :param iteration:
        :return:
        """
        #gather data
        self.topple_count += 1
        self.when_topple.append(iteration)
        #execute topple
        taken_grains = 3
        self.array[radial_position][angle_position] -= taken_grains

        #one grain topples downwards
        if radial_position < self.number_radial - 1:
            self.array[radial_position + 1][angle_position] += 1
        else:
            self.mass_fallen_count += 1

        #one grain topples LEFT

        if angle_position == 0:
            self.array[radial_position][self.number_angles - 1] += 1
        else:
            self.array[radial_position][angle_position - 1] += 1

        #one grain topples RIGHT

        if angle_position == self.number_angles - 1:
            self.array[radial_position][0] += 1
        else:
            self.array[radial_position][angle_position + 1] += 1

    def check_pile(self, iteration):
        """
        Function checking every sandpile location, if grains of sand exceed max topple starts
        :param iteration:
        :return:
        """

        for r in range(0, self.number_radial, 1):
            for theta in range(0, self.number_angles, 1):

                if self.array[r][theta] < self.max_peak:
                    self.array[r][theta] = self.array[r][theta]

                else:
                    if self.force:
                        self.topple_sumulate_centrifugal_force(r, theta, iteration)
                    else:
                        self.topple(r, theta, iteration)

    def plot_iteration(self, angles_array, radial_array, array, iteration):
        fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
        cb = ax.pcolormesh(angles_array, radial_array, array, edgecolors='k', linewidths=1)
        ax.set_yticks([])
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        plt.colorbar(cb, orientation='vertical')
        plt.savefig(f'animation\\{iteration}_{self.force}_{self.number_of_simulations}.png')
        plt.show()

    def simulate(self, number_of_simulations):
        """
        Main function, starts sandpile simulation
        :param number_of_simulations:
        :return:
        """
        self.number_of_simulations = number_of_simulations

        for iteration_num in range(0, number_of_simulations, 1):
            self.add_grain(0)
            self.check_pile(iteration_num)
            self.mass_when_iteration.append(self.mass_count - self.mass_fallen_count)
            self.plot_iteration(self.angles_array, self.radial_array, self.array, iteration_num)
            print(self.array)

    def plot(self, type='sandpile', bandwith=1):
        """
        Plotting function
        :param type:
        :return:
        """

        #plot sandpile after simulation
        if type == 'sandpile':
            fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
            cb = ax.pcolormesh(self.angles_array, self.radial_array, self.array, edgecolors='k', linewidths=1)
            ax.set_yticks([])
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            plt.colorbar(cb, orientation='vertical')
            plt.savefig(f'plot_{self.number_of_simulations}_sandpile_{self.force}.png')
            # plt.show()

        #plot iteration / mass of left pile on plate
        if type == 'mass':
            simulation_array = []
            for i in range(0, self.number_of_simulations, 1):
                simulation_array.append(i)

            plt.plot(self.mass_when_iteration)
            # plt.title("Left Mass on pile during iterations")
            plt.xlabel("Iteration")
            plt.ylabel("Value sum")
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
            plt.savefig(f'plot_{self.number_of_simulations}_mass_{self.force}.png')
            plt.show()

        #plot iteration / topple
        if type == 'topple':
            lists = sorted(Counter(self.when_topple).items())
            when_topple, topple_count = zip(*lists)

            print("TOPPLE COUNT")
            print(topple_count)
            print("TOPPLE COUNT LEN")
            print(len(topple_count))

            print("LISTS")
            print(lists)

            plt.bar(when_topple, topple_count)
            plt.xlabel('Iteration Number')
            plt.ylabel('Relocated value sum')
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
            plt.savefig(f'plot_{self.number_of_simulations}_topple_{self.force}.png')
            plt.show()

        if type == 'histogram':

            lists = sorted(Counter(self.when_topple).items())
            when_topple, topple_count = zip(*lists)


            if bandwith == 1:
                plt.hist(self.when_topple, color='blue',
                         bins=int(180 / bandwith))
            else:
                plt.hist(self.when_topple, color='blue', edgecolor='black',
                         bins=int(180 / bandwith))
            plt.ylabel("Relocatation amount")
            plt.xlabel("Iteration")
            plt.show()

        if type == 'pdf':

            if bandwith == 1:
                sns.distplot(self.when_topple, hist=True, kde=True, bins=int(180 / bandwith),
                             color='blue', kde_kws={'linewidth': 3})
            else:
                sns.distplot(self.when_topple, hist=True, kde=True, bins=int(180 / bandwith),
                             color='blue', hist_kws={'edgecolor': 'black'}, kde_kws={'linewidth': 3})

            plt.ylabel("Density")
            plt.xlabel("Iteration")
            plt.show()

    def analyze_data(self, bandwith=1):
        """
        Function for analyzing data and executes plotting.
        :return:
        """
        data = {"Topple Count": self.topple_count, "Fallen mass": self.mass_fallen_count}
        print(data)

        self.plot()
        self.plot(type='mass')
        self.plot(type='topple')
        self.plot(type='histogram',bandwith=bandwith)
        self.plot(type='pdf',bandwith=bandwith)





SANDPILE = Sandpile(5, 36, 5, force=True, addition_random=False)
SANDPILE.simulate(1000)
# SANDPILE.analyze_data(bandwith=1)

# SANDPILE_two = Sandpile(5, 35, 5)
# SANDPILE_two.simulate(10000)
# SANDPILE_two.analyze_data()

