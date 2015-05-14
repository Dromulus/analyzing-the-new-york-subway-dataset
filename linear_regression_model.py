import numpy as np
import pandas
import scipy
import statsmodels.api as sm

def predictions(weather_turnstile):
	
	#dependant variable
    ridership =  weather_turnstile['ENTRIESn_hourly']
    
    #create counter to select columns from data frame
    col_count_weather_turnstile = len(weather_turnstile)
    col_counter = range(col_count_weather_turnstile)
    
    #initiate lists for independant variables to use
    name_list = list()
    slope_list = list()
    intercept_list = list()
    r_value_list = list()
    
   #compute statistics for each column and append useful ones to each list, if errors while attempting statistics skip that column
    for count in col_counter:
        try:
            x = weather_turnstile.ix[:, count]
            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, ridership)
            if p_value <= 0.05 and r_value != 0 and x.name != 'ENTRIESn_hourly' and x.name != 'Unnamed: 0':
                name_list.append(x.name)
                slope_list.append(slope)
                intercept_list.append(intercept)
                r_value_list.append(r_value)
        except:
            pass
    
    #create counter to cycle through lists of independant variables, empty list for storing predictions
    row_count_weather_turnstile = len(weather_turnstile.index)
    row_counter = range(row_count_weather_turnstile)
    prediction = list()
    
    #generate predictions
    for count in row_counter:
        predict = 0
        for item in name_list:
            data_col_loc = list(weather_turnstile.columns.values).index(item)
            list_col_loc = name_list.index(item)
            model_intercept = intercept_list[list_col_loc]
            model_slope = slope_list[list_col_loc]
            model_x = weather_turnstile.iat[count, data_col_loc]
            model_weight = r_value_list[list_col_loc] / sum(r_value_list)
            predict += (model_intercept + (model_slope * model_x)) * model_weight
            
    #Generate column of predicted entries
        prediction.append(predict)
    prediction = pandas.Series(prediction, name = 'prediction')

    return prediction
