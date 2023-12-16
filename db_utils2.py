import yaml
import pandas as pd
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    '''
    A class that connects to an AWS RDS database to retrieve data related to customer loans in finance from the cloud.

    Parameters:
    ----------
    credentials_dictionary: dict
        A dictionary containing credentials for accessing the RDS database
 
    Attributes:
    ----------
    credentials_dictionary: dict
        A dictionary containing credentials for accessing the RDS database.
    engine: sqlalchemy.engine.base.Engine
        SQLAlchemy engine for database connection.

    Methods:
    -------
    load_yaml_file()
        Load database credentials from a YAML file.

        Returns:
        -------
        dict
            A dictionary containing credentials for accessing the RDS database.
    initialise_sqlalchemy()
        Initialize an SQLAlchemy engine using the credentials.
    execute_query(query: str)
        Execute a SQL query and return the result as a Pandas DataFrame.
    '''

    def __init__(self, credentials_dictionary):
        '''
        Initialise an instance of the RDSDatabaseConnector class.
        '''
        self.credentials_dictionary = credentials_dictionary
        self.engine = None  # Initialize the engine as None

    @staticmethod
    def load_yaml_file():
        '''
        Load database credentials from a YAML file.

        Returns:
        -------
        dict
            A dictionary containing credentials for accessing the RDS database.
        '''
        with open('credentials.yaml', 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials['database']

    def initialise_sqlalchemy(self):
        '''
        Initialise an SQLAlchemy engine using the credentials.
        '''
        db_credentials = self.credentials_dictionary

        # Create an SQLAlchemy engine
        db_url = f"postgresql+psycopg2://{db_credentials['RDS_USER']}:{db_credentials['RDS_PASSWORD']}@{db_credentials['RDS_HOST']}:{db_credentials['RDS_PORT']}/{db_credentials['RDS_DATABASE']}"
        self.engine = create_engine(db_url)

    def execute_query(self, query: str):
        '''
        Execute a SQL query and return the result as a Pandas DataFrame.

        Parameters:
        -----------
        query: str
            SQL query to be executed.

        Returns:
        --------
        pd.DataFrame
            Result of the query as a Pandas DataFrame.
        '''
        with self.engine.connect() as connection:
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

# Example usage:
connector_instance = RDSDatabaseConnector.load_yaml_file()

# Create an instance of RDSDatabaseConnector and initialize SQLAlchemy engine
connector = RDSDatabaseConnector(connector_instance)
connector.initialise_sqlalchemy()

# Execute a query
query = "SELECT * FROM your_table"
result_df = connector.execute_query(query)
print(result_df)
