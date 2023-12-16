import yaml
from sqlalchemy import create_engine
import pandas as pd


class RDSDatabaseConnector:
    # define docstring which can be found by using help(ClassName)
    '''
    #TODO finish the docstring
    A class that connects to an AWS RDS database to retrieve data related to customer loans in finance from the cloud.

    Parameters:
    ----------
    #credentials?

 
    Attributes:
    ----------
    #credentials?

    
    Methods:
    -------
    #create_engine

    #extract_data_to_dataframe

    #save_dataframe_to_csv

    #get_table_overview

    load_yaml_file()
        Load database credentials from a YAML file

        Returns:
        -------

        
    '''

    def __init__(self, credentials):    #takes in as a parameter a dictionary of the credentials
        '''
        #Initialise an instance of the RDSDatabaseConnector class
        '''
        self.credentials = credentials
        self.engine = self.create_engine()

    def load_credentials():
    # Load credentials from credentials.yaml file
        with open("credentials.yaml", "r") as file:
            credentials = yaml.safe_load(file)
        return credentials

    def create_engine(self):
        #TODO add docstrings for ALL methods
        # Create SQLAlchemy engine
        db_url = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        engine = create_engine(db_url)
        return engine

    def extract_data_to_dataframe(self):
        # Extract data from RDS database to Pandas DataFrame
        query = "SELECT * FROM loan_payments"
        df = pd.read_sql(query, self.engine)
        return df

    def save_dataframe_to_csv(self, df, filename):
        # Save Pandas DataFrame to CSV file
        df.to_csv(filename, index=False)

    def get_table_overview(self, table_name):
        # Get an overview of the specified table in the database
        query = f"SELECT * FROM information_schema.columns WHERE table_name = '{table_name}';"
        overview_df = pd.read_sql(query, self.engine)
        return overview_df


if __name__ == "__main__":
    credentials = load_credentials()
    connector = RDSDatabaseConnector(credentials)   #passing the credentials (loaded in as yaml) as an argument to the RDSDatabaseConnector class

    # Test query: Select the first 5 rows from the loan_payments table
    test_query = "SELECT * FROM loan_payments LIMIT 5"
    test_df = pd.read_sql(test_query, connector.engine)

    # Display the results for the test query
    print("Test Query Results:")
    print(test_df)
    
    # Extract data from RDS and save to CSV
    data_df = connector.extract_data_to_dataframe()
    connector.save_dataframe_to_csv(data_df, "loan_payments_data.csv")

   