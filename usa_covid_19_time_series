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


"""DATA SOURCE: https://github.com/CSSEGISandData/COVID-19/
tree/master/csse_covid_19_data/csse_covid_19_time_series  [4]."""

# DATA FORMAT CONSTANTS
CSV_FORMAT = 'csv'
JSON_FORMAT = 'json'

base_uri = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/' \
           'csse_covid_19_data/csse_covid_19_time_series'

CONFIRMED_CSV = 'time_series_covid19_confirmed_global.csv'
RECOVERED_CSV = 'time_series_covid19_recovered_global.csv'
DECEASED_CSV =  'time_series_covid19_deaths_global.csv'

infected_uri = '{base_uri}/{confirmed}'.format(base_uri=base_uri, 
                                               confirmed=CONFIRMED_CSV)

recovered_uri = '{base_uri}/{recovered}'.format(base_uri=base_uri, 
                                                recovered=RECOVERED_CSV)

deceased_uri = '{base_uri}/{deceased}'.format(base_uri=base_uri, 
                                              deceased=DECEASED_CSV)

def get_data_frame(data_source, data_format=CSV_FORMAT, error_bad_lines=False):
    """
    GET DATA FROM DATA SOURCE
    :param data_source: {str} url or filepath of data source
    :param data_format: {str} data format Example: csv(default) or json
    :param error_bad_lines: {Boolean} False(default) - Bad are dropped.
    :return: {object} Pandas DataFrame object
    """
    df = None
    try:
        if data_format == CSV_FORMAT:
            df = pd.read_csv(filepath_or_buffer=data_source, 
                             error_bad_lines=error_bad_lines)
            logger.debug(df.head())
        else:
            raise Exception('INVALID DATA FORMAT')
    except Exception as ex:
        logger.exception('EXCEPTION IN READING DATA: {}'.format(ex))
    return df


"""GET DATA FROM DATA SOURCE"""

# INFECTED DATA FRAME
infected_data_frame = get_data_frame(data_source=infected_uri)
# RECOVERED DATA FRAME
recovered_data_frame = get_data_frame(data_source=recovered_uri)
# DECEASED DATA FRAME
deceased_data_frame = get_data_frame(data_source=deceased_uri)


def process_covid_19_data(data_frame, column_name):
    """
    PROCESSES DATA FRAMES
    :param data_frame: {object} Data Frame Object
    :param column_name: {str} column to create
    :return: {Object} Cleaned DataFrame Object
    """
    # DROP COLUMNS
    data = data_frame.drop(['Lat', 'Long'], axis=1)
    # MERGE DATA
    data = data.melt(id_vars=['Province/State', 'Country/Region'],
                     value_name=column_name,
                     var_name='date').astype({'date': 'datetime64[ns]', 
                                              column_name: 'Int64'}, 
                                             errors='ignore')
    # FILL NA
    data['Province/State'].fillna('', inplace=True)
    data[column_name].fillna(0, inplace=True)
    return data


def plot_data_frame(data_frame, title=''):
    """
    PLOTTING OF DATA
    :param data_frame: {Object} DataFrame Object to Plot
    :return: None
    """
    # PLOT DATA FRAME
    data_frame.plot()
    plt.title(title)
    plt.xlabel('MONTHS')
    plt.ylabel('POPULATION')
    plt.grid()
    plt.show()


# CONSOLIDATE DATA SETS
complete_data = process_covid_19_data(infected_data_frame, "confirmed").merge(
    process_covid_19_data(deceased_data_frame, "deceased")).merge(
    process_covid_19_data(recovered_data_frame, "recovered"))

"""
['Province/State', 'Country/Region', 'date', 'cumConfirmed', 
'cumDeaths', 'cumRecovered']
"""

# CONSOLIDATED COMPLETE DATA
usa_complete_data = complete_data[complete_data['Country/Region'] == 'US']

# SETTING DATE AS INDEX
usa_complete_data = usa_complete_data.set_index('date')

# LOGGING DATA TAIL
logger.info(usa_complete_data.tail())


# PLOTTING USA COVID-19 DATA
plot_data_frame(data_frame=usa_complete_data, title='DEC 2019 - JUN 2020 USA COVID-19')
