"""
A module containing helper methods to load configs from files.
"""
import os
import json

def load_config_from_file(file='config.json'):
    """Used to load the parameters to send to the SOC API from provided file."""
    
    config = {}
    
    if not os.path.exists(file):
        return None
    
    with open(file, 'r') as f:
        config = json.load(f)
        
    return config

def load_desired_classes_from_file(file='class-index.json'):
    """Load the desired classes to snipe from the provided file."""
    if not os.path.exists(file):
        return None
    
    with open(file, 'r') as f:
        desired_classes = json.load(f)
        
    return desired_classes

