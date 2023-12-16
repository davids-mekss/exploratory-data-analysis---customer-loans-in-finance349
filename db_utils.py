import yaml
import pandas as pd
from sqlalchemy import create_engine


class RDSDatabaseConnector:     # define docstring which can be found by using help(ClassName)
    '''
    A class that connects to an AWS RDS database to retrieve data related to customer loans in finance from the cloud.

    Parameters:
    ----------
    credentionals_dictionary: dict
        A dictionary containing credentials for accessing the RDS database
 
    Attributes:
    ----------

    Methods:
    -------
    load_yaml_file()
        Load database credentials from a YAML file

        Returns:
        -------
        dict
            A dictionary containing credentials for accessing the RDS database.
    '''

    def __init__(self, credentials_dictionary):
        '''
        #Initialise an instance of the RDSDatabaseConnector class
        '''
        self.credentials_dictionary = credentials_dictionary

    @staticmethod
    def load_yaml_file():
        '''
        Load database credentials from a YAML file
        '''
        with open('credentials.yaml', 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials['database']
    
    def initialise_sqlalchemy(self):
        '''
        Initialise an SQLAlchemy engine using the credentials.
        '''
        db_credentials = self.credentials_dictionary
        db_url = f"postgresql+psycopg2://{db_credentials['RDS_USER']}:{db_credentials['RDS_PASSWORD']}@{db_credentials['RDS_HOST']}:{db_credentials['RDS_PORT']}/{db_credentials['RDS_DATABASE']}"

connector_instance = RDSDatabaseConnector.load_yaml_file()
print(connector_instance)


with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
    pass