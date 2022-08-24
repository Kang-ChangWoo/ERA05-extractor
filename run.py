# import python built-in libraries
import os.path

# import external libraries
import netCDF4 
import pandas as pd
import numpy as np
import yaml
from datetime import datetime, timedelta
from cftime import num2date, date2num

# import user libraries
from utils import description_module
from utils import conversion_module

# load configuration file
with open('config.yml') as f:
    cfg = yaml.load(f, Loader = yaml.FullLoader)
    

dataPath = "./data/"
# dataPath = "./raw_data/Maebong_and_Moonam/"
 
files = os.listdir(dataPath)

datasetDict = {}
for idx,nc_type_file in enumerate(files):
    if nc_type_file.split(".")[-1] == 'nc':
        datasetDict[nc_type_file] = netCDF4.Dataset(dataPath+nc_type_file,mode="r")
        
for fname, netCDF4 in list(datasetDict.items()):

    info_dict, meta_dict, desc_dict = conversion_module.netCDF4_to_CSV(netCDF4)
    data_df = conversion_module.dict_to_dataframe(info_dict, meta_dict)
    data_df = conversion_module.measure_wind_info(data_df)

    tmp_fname = fname.split('.')[-2] + '(located_in_' + str(meta_dict['latitude'][0])+"lat "+str(meta_dict['longitude'][0])+"lon"+').csv'
    conversion_module.save_df(data_df, cfg['project_title'], tmp_fname)
