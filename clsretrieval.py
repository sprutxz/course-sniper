"""
Retrieval of open classes from the SOC API and checking if the desired sections are open
"""
import requests
import time
import asyncio

import config_loader

def get_open_classes():
    """Retrieve the open classes from the SOC API"""
    
    params = config_loader.load_config_from_file() # loading the parameters to send to the SOC API
    
    if params is None:
        print("No parameters found in config.txt")
        return []
    
    url = "http://sis.rutgers.edu/soc/api/openSections.gzip" # SOC API URL
    
    count = 0
    while count < 5:
        try:
            response = requests.get(url, params=params) # sending the api request
            
            # If the request is successful, return the json response
            if response.status_code == 200:
                return response.json()
            
            print(f"Error with SOC API request: Status Code {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            print(f"ConnectionError @ {int(time.time())}")

        count += 1
        time.sleep(10)

    raise Exception("Max retries failed.")

def check_open_classes(open_sections, desired_sections):
    """Checking if the desired sections are open"""
    
    open_sections = set(open_sections)
    
    indexes = []
    
    for section in desired_sections:
        if section in open_sections:
            indexes.append(section)
            
    return indexes
