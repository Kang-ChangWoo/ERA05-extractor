# import python built-in libraries
import os.path

# import external libraries
import netCDF4 
import pandas as pd
import numpy as np
import yaml
from datetime import datetime, timedelta
from cftime import num2date, date2num
from metpy.calc import wind_speed, wind_direction #it 
from metpy.units import units

def print_what_is_in_source_directory():
    print("testing")
    