import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from IPython.display import Image
import matplotlib.pyplot as plt
from PIL import Image
import PIL
import datetime

import os
import requests
import functions

def get_vaccinations_dataset():
    '''
    Gets vaccinations dataset from the url or get it from the local dataset
    '''
    
    return pd.read_csv("dataset/vaccinations.csv")

    covid_vaccinations_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"

    ## Get the dataset from the API
    try:
        country_vaccinations_df = pd.read_csv(covid_vaccinations_url)
        country_vaccinations_df.to_csv('dataset/vaccinations.csv')

    except Exception as e:
        ## Use the local dataset if any issue occur with downloading it
        
        if os.path.exists("dataset/vaccinations.csv"):
            country_vaccinations_df = pd.read_csv("dataset/vaccinations.csv")
        else:
            functions.error_log("Local dataset opening: Local vaccinations dataset not found")
        
        ## Log the issue for troubleshooting later
        functions.error_log("API opening: " + str(e))

    print("Returning vacinnation dataset")
    return country_vaccinations_df


def delete_file(file_path):
    '''
    Delete temporary files
    '''
    if os.path.exists(file_path):
        os.remove(file_path)


## Create global variables
country_vaccinations_df = get_vaccinations_dataset()
country_vaccinations_df['country'] = country_vaccinations_df['location'] 
country_list = country_vaccinations_df['country'].unique()
today_date = datetime.datetime.now()


def get_dataset_by_history(history_days = 90):
    '''
        Returns the country_vaccinations_df dataset filtered by length of days required

    '''
    
    # start_date = today_date.strftime("%Y-%m-%d")

    start_date = (today_date - datetime.timedelta(history_days)).strftime("%Y-%m-%d")
    date_view = history_days

    
    return country_vaccinations_df[country_vaccinations_df["date"] > start_date]

def compare_vaccinations_between_countries(country_1, country_2, days, metrics = 'total_vaccinations', the_user=''):
    '''
        Compares vaccinations history between 2 countries as defined by the metrics.
        Default metrics is 'total_vaccinations'
        the_user is the Discord user
        returns the image path for the visualization
    '''

    if country_1 not in country_list or country_2 not in country_list:
        pass

    country_df = get_dataset_by_history(days)
    
    condition = (country_df['country'] == country_1) | (country_df['country'] == country_2)
    country_df = country_df[condition]
    
    fig = go.Figure()
    
    fig = px.line(country_df, x="date", y=metrics, color='country', symbol="country",
                title= "Comparing monthly {} between \n {} and {} across the last {} days".format(metrics, country_1, country_2, days),
                labels={"total_vaccinations": "Total Vaccinations", 
                        "total_vaccinations_per_hundred": "Total Vaccinations Per Hundred", 
                        "date":"Months"
                        
                    }
                        )
    print("Sent fig to image generator")
    return functions.generate_vizualization_img(fig, the_user)

def get_top_bottom_vaccinated_countries(top_bottom, number_of_records, days, metrics = 'total_vaccinations', the_user=''):
    '''
        Get visualization of top or bottom vaccinated countries as defined by the user
        Default metrics is 'total_vaccinations'
        the_user is the Discord user
        returns the image path for the visualization
    '''

    metrics = 'total_vaccinations' ## Default sort values

    compare_values = ["people_vaccinated", "people_fully_vaccinated"] ## Default compare values

    if metrics == "total_vaccinations_per_hundred":
        compare_values = ["people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred"]

    ascending_value = False ## Get top countries by default
    if top_bottom.lower() == "bottom": ## True to get bottom countries
        ascending_value = True    


    vaccinated_by_country = country_vaccinations_df.groupby('country').max().sort_values(metrics, ascending=ascending_value).head(int(number_of_records))
    vaccinated_by_country = vaccinated_by_country[vaccinated_by_country["iso_code"].str.contains('OWID') == False]

    country_index = vaccinated_by_country.index
    

    fig = px.bar(vaccinated_by_country, x = country_index, y = compare_values, 
                title='Compare monthly {} by {} and {} across the last {} days '.format(metrics, compare_values[0], compare_values[1], days),
                labels={"value":"Total People", "country":'Country', 
                        "variable":"Vaccinated People"
                        })

    print("Sent fig to image generator")
    return functions.generate_vizualization_img(fig, the_user)