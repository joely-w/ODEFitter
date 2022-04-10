import csv

import matplotlib.pyplot as plt
import numpy
from scipy import integrate, optimize

# Render LaTeX in plt
plt.rcParams['text.usetex'] = True


# https://stackoverflow.com/questions/34422410/fitting-sir-model-based-on-least-squares


class SIRModel:
    def __init__(self, daily_deaths, daily_births, population, y_data, t_data):
        # Initial conditions
        self.population = population
        self.death_rate = daily_deaths / population
        self.birth_rate = daily_births / population
        self.I0 = y_data[0]
        self.y = numpy.array(y_data)
        self.t = numpy.array(t_data)
        self.I0 = y_data[0]
        self.S0 = population
        self.R0 = 0.00

    def model(self, y, t, beta, gamma):
        """
        Model to use, currently the basic SIR model. Our ODEs are autonomous and
        so have no dependence on t.
        :param y:(float,float,float) - Tuple containing previous values for S,I,R
        :param t: int - Time at which to calculate model
        :param beta: float - Infectivity parameter
        :param gamma: float -  Recovery rate parameter
        :return: (float, float, float) - Tuple containing new values for S,I,R
        """
        s = self.birth_rate * self.population - self.death_rate * y[0] - beta * y[0] * y[1] / self.population
        i = beta * y[0] * y[1] / self.population - gamma * y[1] - self.death_rate * y[1]
        r = gamma * y[1] - self.death_rate * y[2]
        return s, i, r

    def calculate_curve(self, t, beta, gamma):
        """
        Calculate infected curve at given value(s), given parameters
        :param t: int
        :param beta: float
        :param gamma: float
        :return:
        """
        return integrate.odeint(self.model, (self.S0, self.I0, self.R0), t, args=(beta, gamma))[:, 1]

    def calculate_model(self, t, beta, gamma):
        return integrate.odeint(self.model, (self.S0, self.I0, self.R0), t, args=(beta, gamma))

    def calculate_error(self, fitted):
        """
        Calculate error between fitted model and data points at each interval
        :param fitted: numpy.array
        :return:
        """
        error = []
        for i in range(len(fitted)):
            error.append(abs(fitted[i] - self.y[i]))
        return error

    def fit(self):
        """
        Find least squares best fit of parameters and plot
        :return:
        """
        popt, pcov = optimize.curve_fit(self.calculate_curve, self.t, self.y)
        # Parameters are stored in array popt
        fitted_model = self.calculate_model(self.t, *popt)
        # Plot infected data points
        plt.plot(self.t, self.y, 'o')

        # Susceptible
        plt.plot(self.t, fitted_model[:, 0], 'b')
        # Infected
        plt.plot(self.t, fitted_model[:, 1], 'r')

        # Recovered
        plt.plot(self.t, fitted_model[:, 2], 'g')

        plt.title(rf"SIR Model with $\beta = {popt[0]}$, $\gamma = {popt[1]}$")
        plt.ylim(0, max(fitted_model[:, 2]))
        print("Parameters estimated at: ")
        print(f"Beta = {str(popt[0])}, Gamma = {str(popt[1])}")
        plt.show()


def driver(filepath):
    with open(filepath) as csv_file:
        print("Loading data...")
        csv_reader = csv.reader(csv_file, delimiter=',')
        population = float(next(csv_reader)[0])
        births_per_day = float(next(csv_reader)[0])
        deaths_per_day = float(next(csv_reader)[0])
        csv_y = []
        csv_t = []
        for row in csv_reader:
            csv_t.append(int(row[0]))
            csv_y.append(float(row[1]))
        print("Data loaded!")
        sir = SIRModel(daily_deaths=deaths_per_day, daily_births=births_per_day,
                       population=population, y_data=csv_y, t_data=csv_t)
        print("Fitting dataset to model...")
        sir.fit()


driver('./datasets/sars/processed_sars.csv')
