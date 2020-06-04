__author__ = 'Narasimha Krishan Sundeep, Kilani'
__university__ = 'Harrisburg University of Science & Technology, PA.'
__huid__ = 244681
__credits__ = ['Dr. Don Mortan/Harrsburg University']
__course__ = 'CISC-614-51-B Computer Simulation'
__topic__ = """COMPARATIVE ANALYSIS OF REPRODUCTIVE NUMBER ESTIMATION 
OF COVID-19 BY WORLD HEALTH ORGANIZATION AND MATHEMATICALLY MODELED 
STUDIES APPLIED TO UNITED STATES OUTBREAK USING SIR MODEL"""


"""
SIMPLE SIR MODEL
"""

"""SETUP"""
import logging
import os
import ssl
from pprint import pformat
import pandas as pd
import matplotlib.pyplot as plt

# SSL VERIFICATION FOR HTTPS
if getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

# LOGGING CONSTANTS
LOG_LEVEL = 'INFO'
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
gamma = 0.5  # TRANSITION RATE
beta = 2  # COEFFICIENT OF INFECTION
NO_OF_DAYS_FROM_FIRST_CASE = 100 # DAYS FROM FIRST CASE

# POPULATION NUMBER
POPULATION_NUMBER = 329968629.0  # US POPULATION ESTIMATE 2019

# INITIAL NUMBER OF INFECTED PEOPLE
INFECTED_POPULATION = 1.0

# INITIAL NUMBER OF SUSCEPTIBLE PEOPLE
SUSCEPTIBLE_POPULATION = POPULATION_NUMBER - INFECTED_POPULATION

# INITIAL NUMBER OF RECOVERED PEOPLE
RECOVERED_POPULATION = 0.0


def sir_model(susceptible, infected, recovered, population_num=POPULATION_NUMBER):
    """
    SIR MATHEMATICAL MODEL PROGRAMMATIC IMPLEMENTATION
    :param susceptible: {int} Susceptible population
    :param infected: {int} Infected population
    :param recovered: {int} Recovered Population
    :param population_num: {int} Population Number
    :return: {dict} Dictionary for verification of model behaviour
    """
    susceptible_list = []
    infected_list = []
    recovered_list = []
    rate_of_increase = None
    population = None
    for d in range(1, NO_OF_DAYS_FROM_FIRST_CASE):
        ds_dt = - (beta * susceptible * infected) / population_num
        di_dt = ((beta * susceptible * infected) / population_num) - (gamma * infected)
        dr_dt = gamma * infected
        
        susceptible += ds_dt
        infected += di_dt
        recovered += dr_dt

        # APPEND DATA TO LISTS
        susceptible_list.append(abs(susceptible))
        infected_list.append(abs(infected))
        recovered_list.append(abs(recovered))
        
        # MODEL VALIDATION DATA
        rate_of_increase = ds_dt + di_dt + dr_dt
        population = susceptible + infected + recovered
        logger.debug('Susceptible: {}\nInfected: {}\nRecovered: {}'
        .format(susceptible, infected, recovered))
    return {'data': {'susceptibleList': susceptible_list,
                  'infectedList': infected_list,
                  'recoveredList': recovered_list}, 
        'rateOfIncrease': rate_of_increase, 
        'population': population}


def plot_model(infected, susceptible, recovered):
    """
    PLOT SIR MODEL
    :param infected: {List} Infected
    :param susceptible: {List} Susceptable
    :param recovered: {List} Recoverd and Deceased
    :return:
    """
    plt.plot(infected, label='infected', color='red')
    plt.plot(susceptible, label='susceptible', color='blue')
    plt.plot(recovered, label='recovered', color='green')
    plt.legend()
    plt.title('SIR MODEL BASIC\ngamma: {gamma:.2f}, beta: {beta}'
    .format(gamma=gamma, beta=beta))
    plt.xlabel('DAYS')
    plt.ylabel('POPULATION')
    plt.show()

"""
RUN MODEL
"""
model_data = sir_model(susceptible=SUSCEPTIBLE_POPULATION, 
                      infected=INFECTED_POPULATION, 
                      recovered=RECOVERED_POPULATION, 
                      population_num=POPULATION_NUMBER)

logger.debug(pformat(model_data))

"""
PLOT MODEL OUTPUT
"""
plot_model(susceptible=model_data.get('data', {}).get('susceptibleList'),
               infected=model_data.get('data', {}).get('infectedList'),
               recovered=model_data.get('data', {}).get('recoveredList'))
