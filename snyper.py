import config
import clsretrieval
import apscheduler

def main():
    desired_sections = config.load_desired_classes_from_file()
    
    open_sections = clsretrieval.get_open_classes()
    
    indexes = clsretrieval.check_open_classes(open_sections, desired_sections)
    
    print(f"Open sections: {indexes}")
    
if __name__ == '__main__':
    main()