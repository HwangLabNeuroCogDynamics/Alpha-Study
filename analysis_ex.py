# data analysis of behavioral pilot results for Hwang Lab alpha study
# ver 01, sept 09 2018

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, log10, pi, average, sqrt, std
from numpy.random import random, randint, normal, shuffle,uniform
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd  
import matplotlib
print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)


#path to .csv result files with subject data 
where_files = r'C:\Users\dillc\University of Iowa\Hwang Lab - Documents\Alpha Paradigm\scripts\data'
file = pd.read_csv(where_files +r'\99_alpha_pilot_01_2018_Sep_25_1011.csv')
print(file.head(10))