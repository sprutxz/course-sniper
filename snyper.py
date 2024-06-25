import os
import config
import clsretrieval

def main():
    if not os.path.exists('config.txt'):
        config.create_config()
    
    if not os.path.exists('class-index.txt'):
        config.create_desired_classes()

    desired_sections = config.load_desired_classes_from_file()
    
    open_sections = clsretrieval.get_open_classes()
    
    indexes = clsretrieval.check_open_classes(open_sections, desired_sections)
    
    
    print(f"Open sections: {indexes}")
    
if __name__ == '__main__':
    main()