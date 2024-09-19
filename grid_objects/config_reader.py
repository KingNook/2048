import typing
import yaml

def load_config(
        file_name: str = 'main',
        folder_path: str = './config/',
        file_extension: str = 'yaml'
):
    '''load the config file at given path; by default loads ./config/main.yaml'''
    
    path = f'{folder_path}{file_name}.{file_extension}'
    with open(path, 'r') as config:

        return yaml.safe_load(config)
        

if __name__ == '__main__':
    # debugging purposes

    print(load_config())