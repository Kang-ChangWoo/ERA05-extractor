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


class WindInfoCalculator:
    def __init__(self, u_column = 'u10', v_column = 'v10'):
        self.u_column = u_column       
        self.v_column = v_column

    def calculate(self, record):
        u = float(record[self.u_column]) * units.meter / units.second
        v = float(record[self.v_column]) * units.meter / units.second
        return [wind_direction(u,v), wind_speed(u,v)]


def measure_wind_info( pandas_df ):
    keys = pandas_df.columns.tolist()
    df_list = []
    
    if ('u10' in keys) and ('v10' in keys):
        wind_calculator = WindInfoCalculator(u_column = 'u10', v_column = 'v10')
        wind_information = pandas_df.apply(wind_calculator.calculate, axis=1)
        
        column_0 = wind_calculator.u_column + '_' + wind_calculator.v_column + '_' + 'wind_direction'
        column_1 = wind_calculator.u_column + '_' + wind_calculator.v_column + '_' + 'wind_speed'
        
        tmp_array = pandas_df.apply(wind_calculator.calculate, axis=1)
        tmp_df = pd.DataFrame(tmp_array.tolist(), columns = [column_0, column_1])

        df_list.append(tmp_df)
        
    if ('u100' in keys) and ('v100' in keys):
        wind_calculator = WindInfoCalculator(u_column = 'u100', v_column = 'v100')
        wind_information = pandas_df.apply(wind_calculator.calculate, axis=1)
        
        column_0 = wind_calculator.u_column + '_' + wind_calculator.v_column + '_' + 'wind_direction'
        column_1 = wind_calculator.u_column + '_' + wind_calculator.v_column + '_' + 'wind_speed'
        
        tmp_array = pandas_df.apply(wind_calculator.calculate, axis=1)
        tmp_df = pd.DataFrame(tmp_array.tolist(), columns = [column_0, column_1])

        df_list.append(tmp_df)
    
    calculated_num = len(df_list)
    
    if calculated_num > 1:
        concated_df = pd.concat([pandas_df] + df_list, axis=1)
        return concated_df
        
    elif calculated_num == 1:
        concated_df = pd.concat([pandas_df, df_list[0]], axis=1)
        return concated_df
        
    elif calculated_num == 0:
        return pandas_df
    
    
def save_df( pandas_df, fname ):
    pandas_df.to_csv(fname,index=True, header=True)
    