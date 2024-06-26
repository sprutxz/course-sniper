def load_config_from_file(file='config.txt'):
    with open(file, 'r') as f:
        lines = f.readlines()
        
    config = {}
    
    for line in lines:
        key, value = line.split(':')
        config[key] = value.strip()
        
    return config

def load_desired_classes_from_file(file='class-index.txt'):
    with open(file, 'r') as f:
        lines = f.readlines()
        
    desired_classes = []
    
    for line in lines:
        desired_classes.append(line.strip())
        
    return desired_classes

