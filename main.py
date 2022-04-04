from scipy import integrate, optimize


class SIRModel:
    def __init__(self, daily_deaths, daily_births, population):
        self.population = population
        self.death_rate = daily_deaths / population
        self.birth_rate = daily_births / population
        pass

    def model(self, y, t, beta, gamma):
        """
        Model to use, currently the basic SIR model
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

    def fit_curve(self, x, y, beta, gamma):
        pass
