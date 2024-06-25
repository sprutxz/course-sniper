def create_config():
    year = input('Enter the year:')

    while True:
        term = input('Enter the term (spring, summer, fall, winter):').lower()

        if term == 'spring':
            term = str(1)
            break
            
        elif term == 'summer':
            term = str(7)
            break
        
        elif term == 'fall':
            term = str(9)
            break

        elif term == 'winter':
            term = str(0)
            break

        else :
            print('Invalid term. Please eneter a valid term. (Maybe spelling error?)')
            continue

    while True:
        campus = input('Enter desired campus (New Brunswick, Newark, Camden):').lower()
        
        if campus == 'new brunswick':
            campus = 'NB'
            break
        
        elif campus == 'newark':
            campus = 'NK'
            break
        
        elif campus == 'camden':
            campus = 'CM'
            break
        
        else:
            print('Invalid campus. Please enter a valid campus. (Maybe spelling error?)')
            continue


    config = {
        'year': year,
        'term': term,
        'campus': campus,
    }
    
    with open('config.txt', 'w') as f:
        for key, value in config.items():
            f.write(key + ':' + value + '\n')

def create_desired_classes():
    section_indexes = []

    text = '''
    Enter the index number of the class you want to track.
    The smaller the number of classes to track, the faster the open sections check will be.

    Enter "-1" when finished.
    '''

    print(text)

    while True:
        
        index = int(input('Enter index number: '))
        if index != -1:
            section_indexes.append(index)
            
        else:
            break

    with open('class-index.txt', 'w') as f:
        for index in section_indexes:
            f.write(str(index) + '\n')
        
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