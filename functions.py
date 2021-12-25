import config
import datetime
import os
import requests
import pandas as pd

## Check for images directory and create it if it does not exist
if not os.path.exists("images"):
    os.mkdir("images")

def error_log(the_error_message):
    '''
    Function to log error messages for troubleshooting.
    It saves the error message and the timestamp in a location defined in the config file
    '''

    error_log_file = config.error_log_file
    if not os.path.exists(error_log_file):
        file_object = open(error_log_file, "w+")

    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    file_object  = open(error_log_file, "a+")

    the_string = the_error_message + " | " + timestamp
    file_object.write(the_string)

    file_object.close()

def log_message(the_message, the_user):
    '''
    Function to log every message received from the user.
    It saves the user name, the message and the timestamp in a location defined in the config file
    '''

    message_log_file = config.message_log_file
    if not os.path.exists(message_log_file):
        file_object = open(message_log_file, "w+")

    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    file_object  = open(message_log_file, "a+")

    the_string = "{}: {} - {} \n".format(str(the_user), str(the_message), timestamp)
    file_object.write(the_string)

    file_object.close()


def get_vaccinations_dataset():
    '''
    Gets vaccinations dataset from the url or get it from the local dataset
    '''
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
            error_log("Local dataset opening: Local vaccinations dataset not found")
        
        ## Log the issue for troubleshooting later
        error_log("API opening: " + str(e))

    return country_vaccinations_df


def generate_vizualization_img(fig, the_user = 'temp_user'):
    '''
    Converts plotly figure to image 
    returns image path 
    '''

    img_path = "images/temp_{}.jpeg".format(the_user)
    fig.write_image(img_path)#, width=4000, height=4000)

    print("Returning img_path after generating")
    return img_path

def delete_file(file_path):
    '''
    Delete temporary files
    '''
    if os.path.exists(file_path):
        os.remove(file_path)
