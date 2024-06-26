import requests
import time

import config_loader

def get_open_classes():
    
    params = config_loader.load_config_from_file()
    
    url = "http://sis.rutgers.edu/soc/api/openSections.gzip"
    
    count = 0
    while count < 5:
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            print(f"Error with SOC API request: Status Code {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"ConnectionError @ {int(time.time())}")

        count += 1
        time.sleep(10)

    raise Exception("Max retries failed.")

def check_open_classes(open_sections, desired_sections):
    open_sections = set(open_sections)
    
    indexes = []
    
    for section in desired_sections:
        if section in open_sections:
            indexes.append(section)
            
    return indexes