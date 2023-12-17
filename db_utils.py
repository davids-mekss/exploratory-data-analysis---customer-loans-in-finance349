#imports in alphabetical order, and start with "from" statements
import pandas as pd
from sqlalchemy import create_engine
import yaml     # remember, two clear lines after imports


class RDSDatabaseConnector:
    # define the docstring which can be found by using help(ClassName)
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

    def __init__(self, credentials):    #initialise an instance of the class which takes in a dictionary of the credentials as a parameter 
        '''
        #Initialise an instance of the RDSDatabaseConnector class
        '''
        self.credentials = credentials
        self.engine = self.__create_engine()

    @staticmethod
    def load_credentials():
    # Load credentials from credentials.yaml file
        with open("credentials.yaml", "r") as file:
            credentials = yaml.safe_load(file)
        return credentials

    def __create_engine(self):
        #TODO add docstrings for ALL classes and ALL methods
        # Create SQLAlchemy engine
        db_url = f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        #the string names match data in the credentials.yaml file
        engine = create_engine(db_url)
        return engine

    def _extract_data_to_dataframe(self):
        # Extract data from RDS database to Pandas DataFrame
        query = "SELECT * FROM loan_payments"
        df = pd.read_sql(query, self.engine)
        return df

    def _save_dataframe_to_csv(self, df, filename):
        # Save Pandas DataFrame to CSV file
        df.to_csv(filename, index=False)


# create a class for transforming data
# recommended to create classes in .py file (here) and then work in a .ipynb file (where you can import the classes)
class DataTransform:
    '''
    #TODO docstring
    '''
    # check column data types
    # especially check dates data types
    # any excess symbols in data?
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_column_to_integer(self, column_name):
        # Convert specified columns from float to int data type to save space
        self.dataframe[column_name] = self.dataframe[column_name].astype('int64')

    def convert_column_to_category(self, column_name):
        self.dataframe[column_name] = self.dataframe[column_name].astype('category')
        #TODO try if this works
        #TODO check which columns have categorical data
        #TODO convert those columns
            
    def convert_column_to_date(self, column_name, format = '%b-%Y'):
        #to use this with another format, when calling the method, specify format = '<another_format>'
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format=format, errors='coerce')
        #TODO check if works
        #TODO if works, susbstitute the manual line in ipynb file with using a method from here
    

if __name__ == "__main__":
    credentials = RDSDatabaseConnector.load_credentials()
    connector = RDSDatabaseConnector(credentials)   #passing the credentials (loaded in as yaml) as an argument to the RDSDatabaseConnector class
    
    # Extract data from RDS and save to CSV
    data_df = connector._extract_data_to_dataframe()
    connector._save_dataframe_to_csv(data_df, "loan_payments_data.csv")

#now that we have data saved locally on our machine (loan_payments_data.csv), we can call it directly via a function:
def load_local_data_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    
    return df

#define the file path (it's in our directory, so just the file name)
file_path = 'loan_payments_data.csv'
dataframe = load_local_data_to_dataframe(file_path)

print("Shape of the dataframe:", dataframe.shape)   #.shape returns a tuple with (number_of_rows, number_of_columns)
# good to get an overview of the data without printing out all of the data

# another good idea is printing out a sample by using the .head() method
dataframe_head = dataframe.head()   # default is first 5 records
print("Dataframe head:\n", dataframe_head)

# print out all of the data IF remove #
#print(dataframe)


# before transforming the data, let's understand it better
print("\ndataframe info:\n")
print(dataframe.info())
print("\ndataframe data types:\n", dataframe.dtypes)
print("\n Percentage of missing values:\n", dataframe.isnull().sum() / len(dataframe))
print("\nNumber of unique values in each column:\n", dataframe.nunique())

# let's look at the column "term"
print("Unique items in column \"term\":", dataframe['term'].unique())
# looks like the unique items in the column are strings "36 months", "60 months" and nan
# there is potential to change this column to a name "term, months" and change it to an int64 data type

# could something similar be done to "employment_length"?


#TODO !!!!!!!!!!!!!!!!!!!!!!!!!!
#should some columns be categorical

#TODO !!!!!!!!!!!!!!!!!!!!!
# when converting data types try using .fillna if encounter errors

#TODO
# issue_date is a string in a format "Jan-2021", we could convert this to a proper data type for a date
#TODO
# earliest_credit_line is also an object in format "Oct-1987", we could convert to a date
#TODO
# same with last_payment_date
#TODO
# and next_payment_date
#TODO
# and last_credit_pull_date


#TODO
# mths_since_last_delinq and mths_since_last_record are float64 but could be int64 to save space
#TODO
print("Unique items in column \"collections_12_mths_ex_med\":", dataframe['collections_12_mths_ex_med'].unique())
# items are 0, 1, 2, 3, 4 and nan
# collections_12_mths_ex_med could be int instead of float too


#TODO
# handle null values, drop columns where over 50% nulls
# these are 1) mths_since_last_delinq, 2) mths_since_last_record, 3) mths_since_last_major_derog, 4) next_payment_date