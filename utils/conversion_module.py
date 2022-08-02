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
# #1. shape이 n,1,1인 경우로 가정하고 작성.
def netCDF4_to_CSV( netCDF4_file ):
    tmp_dict = {}
    meta_dict = {}

    for key in ["latitude","longitude"]:
        init_value = netCDF4_file[key][:].data
        meta_dict[key] = init_value      

    for key in ['time']:
        masked_array_dtime = [str(i) for i in netCDF4.num2date(netCDF4_file['time'],netCDF4_file['time'].units)] # it return masked_array
        length = len(masked_array_dtime)
        array_format = np.array(masked_array_dtime).T.reshape([length,1])

        tmp_dict[key] = array_format

    # TODO expver..?
    for key in netCDF4_file.variables.keys():
        if key not in ["time","latitude","longitude",'expver']:
            init_value = netCDF4_file[key][:].data
            array_format = np.array(init_value)
            array_format = array_format.T.reshape([length,1])
            
            tmp_dict[key] = array_format
    
    return tmp_dict, meta_dict


def dict_to_dataframe( info_dict, meta_dict  ):
    column_names = [ ]
    array_list = [ ]
    
    length = len(list(info_dict.items())[0][1])

    for key_, val_ in list(meta_dict.items()):
        repeated_array = np.repeat(val_[0], length, axis=0)
        repeated_array = repeated_array.reshape(length, -1)
        column_names.append(key_)
        array_list.append(repeated_array)
    
    
    for key_, val_ in list(info_dict.items()):
        column_names.append(key_)
        array_list.append(val_)
    
    concated_array = np.concatenate(array_list, axis=1)
    concated_df =  pd.DataFrame(concated_array, columns =column_names)

    
    return concated_df


def measure_wind_info( tmpDict ):
    
    
    print("test")
    
    return calculatedDict