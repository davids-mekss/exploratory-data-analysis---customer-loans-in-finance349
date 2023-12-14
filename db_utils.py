import yaml


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

    def load_yaml_file(self):
        '''
        Load database credentials from a YAML file
        '''
        filename = 'credentials.yaml'

        with open(filename, 'r') as file:
            credentials_dictionary = yaml.safe_load(file)
        return credentials_dictionary

connector_instance = RDSDatabaseConnector({})
loaded_credentials = connector_instance.load_yaml_file()
print(loaded_credentials)
