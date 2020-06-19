__author__ = 'Narasimha Krishan Sundeep, Kilani'
__university__ = 'Harrisburg University of Science & Technology, PA.'
__huid__ = 244681
__credits__ = ['Dr. Don Mortan/Harrsburg University']
__course__ = 'CISC-614-51-B Computer Simulation'
__topic__ = """COMPARATIVE ANALYSIS OF REPRODUCTIVE NUMBER ESTIMATION 
OF COVID-19 BY WORLD HEALTH ORGANIZATION AND MATHEMATICALLY MODELED 
STUDIES APPLIED TO UNITED STATES OUTBREAK USING SIR MODEL"""


import logging
import ssl

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate

"""MODULE SETUP"""

# SSL VERIFICATION FOR HTTPS
if getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

# LOGGING CONSTANTS
LOG_LEVEL = 'DEBUG'
LOGGING_FORMAT = "%(asctime)s {app} [%(thread)d] %(levelname)-5s %(name)s - %(message)s. [file=%(filename)s:%(lineno)d]"
DATE_FORMAT = None

# LOGGING SETUP
LOGGING_FORMAT = LOGGING_FORMAT.format(app='CARN')
logging.basicConfig(format=LOGGING_FORMAT)
logger = logging.getLogger()
logger.setLevel(level=LOG_LEVEL)

"""
SIR MODEL VARIABLES AND CONSTANTS
"""
# POPULATION NUMBER
POPULATION_NUMBER = 329968629

# REPRODUCTION NUMBER
ro_values = [3.28, 2.0, 1.95]   # 3.28: RESEARCH LETTER CUMULATIVE, 2.0: MEDIAN RO, 1.95: WHO RO

GAMMA = 1 / 21  # THE RATE OF RECOVERY

# beta = 0.00003  # THE RATE OF INFECTION
t = np.linspace(0, 500, 100)  # Time

# INITIAL NUMBER OF INFECTED PEOPLE
INFECTED_POPULATION = 1

# INITIAL NUMBER OF RECOVERED PEOPLE
RECOVERED_POPULATION = 0

# INITIAL NUMBER OF SUSCEPTIBLE PEOPLE
SUSCEPTIBLE_POPULATION = POPULATION_NUMBER - INFECTED_POPULATION - RECOVERED_POPULATION


def sir_model(pop_list, time, beta, gamma, verification=False):
    """
    SIR MATHEMATICAL MODEL PROGRAMMATIC IMPLEMENTATION
    :param pop_list: {list} List of S, I, R
    :param beta: {float} Infected Rate
    :param gamma: {float} Recovery rate
    :param time: {obj} time
    :param verification: {bool} True if verification else False
    :return: {list/dict} Derivatives S, I, R over time and Rate of Increase
    """

    susceptible, infected, recovered = pop_list

    ds_dt = - (beta * susceptible * infected) / POPULATION_NUMBER
    di_dt = ((beta * susceptible * infected) / POPULATION_NUMBER) - (gamma * infected)
    dr_dt = (gamma * infected)
    response = [ds_dt, di_dt, dr_dt]
    logger.debug('TIME(t): {}'.format(time))
    logger.debug('[susceptible, infected, recovered]: {}'.format(pop_list))
    logger.debug('Derivatives of [susceptible, infected, recovered]: {}'.format(response))
    if verification:
        response = {'data': [ds_dt, di_dt, dr_dt], 'rateOfIncrease': ds_dt + di_dt + dr_dt}
        logger.info('RATE of Increase: ds_dt + di_dt + dr_dt = {}'.format(response.get('rateOfIncrease', 'ERROR')))
    return response


def calculate_beta(ro, gamma):
    beta = (ro * gamma)
    logger.debug('BETA: {beta}'.format(beta=beta))
    return beta


def solve_differential_equations(susceptible, infected, recovered, beta, gamma):
    sol = scipy.integrate.odeint(sir_model,
                                 [susceptible, infected, recovered],
                                 t,
                                 args=(beta, gamma))
    logger.debug('SOLUTION: {sol}'.format(sol=sol))
    return sol


def plot_model(sol, title='SIR MODEL'):
    """
    PLOT MODEL
    """
    plt.plot(t, sol[:, 0], label="Susceptible", color='blue')
    plt.plot(t, sol[:, 1], label="Infected", color='red')
    plt.plot(t, sol[:, 2], label="Recovered", color='green')
    plt.grid()
    plt.legend(loc=1)
    plt.xlabel("TIME")
    plt.xlim(0, 300)
    plt.ylabel("POPULATION - (1.0*e8 = 100 Million)")
    plt.title(title)
    plt.show()


def run_model():
    for r in ro_values:
        beta = calculate_beta(ro=r, gamma=GAMMA)
        model_data = solve_differential_equations(susceptible=SUSCEPTIBLE_POPULATION,
                                                  infected=INFECTED_POPULATION,
                                                  recovered=RECOVERED_POPULATION,
                                                  beta=beta,
                                                  gamma=GAMMA)
        plot_title = "SIR MODEL - REPRODUCTION NUMBER Ro: {}".format(r)
        plot_model(sol=model_data, title=plot_title)


"""
RUN SIR MODEL
"""
run_model()


"""SIR MODEL VERIFICATION"""

"""
VERIFICATION 1 - RATE OF INCREASE
"""
"""VERIFY SUM OF RATE OF INCREASE IS EQUAL TO 0"""


def verify_sir_model_by_rate_of_increase():
    """
    Verify Sum of Rate of Increase is equal to 0
    :return: Model Verification
    """
    rt_of_infection = calculate_beta(ro=ro_values[1], gamma=GAMMA)
    rate_of_increase = sir_model(pop_list=[SUSCEPTIBLE_POPULATION, INFECTED_POPULATION, RECOVERED_POPULATION],
                                 time=0,
                                 beta=rt_of_infection,
                                 gamma=GAMMA,
                                 verification=True).get('rateOfIncrease')
    assert int(rate_of_increase) == 0


"""
VERIFICATION 2 - PLOT INFECTION RATE AS 0
"""


def plot_infection_rate_verification_model():
    """
    PLOT VERIFICATION BY INFECTION RATE AS 0
    """
    beta = 0.0
    model_data = solve_differential_equations(susceptible=SUSCEPTIBLE_POPULATION,
                                              infected=INFECTED_POPULATION,
                                              recovered=RECOVERED_POPULATION,
                                              beta=beta,
                                              gamma=GAMMA)
    plot_title = "SIR MODEL VERIFICATION 2 - RATE OF INFECTION: {}\n" \
                 "".format(beta)
    plot_model(sol=model_data, title=plot_title)


def verify_sir_model_by_infection_rate_plot():
    plot_infection_rate_verification_model()


"""
VERIFICATION 3 - PLOT RECOVERY RATE 0
"""


def plot_recovery_rate_verification_model():
    """
    PLOT VERIFICATION BY RECOVERY RATE 0
    """
    gamma = 0.0
    beta = calculate_beta(ro=ro_values[0], gamma=GAMMA)
    model_data = solve_differential_equations(susceptible=SUSCEPTIBLE_POPULATION,
                                              infected=INFECTED_POPULATION,
                                              recovered=RECOVERED_POPULATION,
                                              beta=beta,
                                              gamma=gamma)
    plot_title = "SIR MODEL VERIFICATION 3 - RATE OF RECOVERY: {}\n".format(gamma)
    plot_model(sol=model_data, title=plot_title)


def verify_sir_model_by_recovery_rate_plot():
    plot_recovery_rate_verification_model()


"""
VERIFICATION 4 - PLOT INITIAL INFECTED POPULATION IS 0
"""


def plot_initial_infection_zero_verification_model():
    """
    PLOT VERIFICATION BY INITIAL INFECTED POPULATION AS 0
    """
    initial_infected_population = 0
    beta = calculate_beta(ro=ro_values[0], gamma=GAMMA)
    model_data = solve_differential_equations(susceptible=SUSCEPTIBLE_POPULATION,
                                              infected=initial_infected_population,
                                              recovered=RECOVERED_POPULATION,
                                              beta=beta,
                                              gamma=GAMMA)
    plot_title = "SIR MODEL VERIFICATION 4 - INITIAL INFECTED POPULATION AS : {}\n".format(initial_infected_population)
    plot_model(sol=model_data, title=plot_title)


def verify_sir_model_by_initial_infection_rate_plot():
    plot_initial_infection_zero_verification_model()


"""RUN VERIFICATIONS"""

verify_sir_model_by_rate_of_increase()
verify_sir_model_by_infection_rate_plot()
verify_sir_model_by_recovery_rate_plot()
verify_sir_model_by_initial_infection_rate_plot()
