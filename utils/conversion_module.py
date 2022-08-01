# import python built-in libraries
import os.path

# import external libraries
import netCDF4 
import pandas as pd
import numpy as np
import yaml
from datetime import datetime, timedelta
from cftime import num2date, date2num


# convert netCDF4 file into CSV file!
### input: <class 'netCDF4._netCDF4.Dataset'>
### return: <class 'pandas.DataFrame'>
def netCDF4_to_CSV( netCDF4_file ):
    tmpDict = {}
    metaDict = {}
    
    output_list = []
    meta_data = []
    column_name = []

    for key in ["latitude","longitude"]:
        init_value = netCDF4_file[key][:].data
        metaDict[key] = init_value      

    for key in ['time']:
        masked_array_dtime = [str(i) for i in netCDF4.num2date(netCDF4_file['time'],netCDF4_file['time'].units)] # it return masked_array
        length = len(masked_array_dtime)
        array_ = np.array(masked_array_dtime).T.reshape([length ,1,1])

        tmpDict[key] = array_

    # TODO expver..?
    for key in netCDF4_file.variables.keys():
        if key not in ["time","latitude","longitude",'expver']:
            init_value = netCDF4_file[key][:].data
            array_ = np.array(init_value)
            
            tmpDict[key] = array_
            #output_list.append(output_dataset.variables[key][:].data)
            #column_name.append(key)
    
    return tmpDict, metaDict

