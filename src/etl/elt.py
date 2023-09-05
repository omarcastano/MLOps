# import libraries
import pandas as pd
import sqlalchemy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class MyETL:
    def __init__(self, table_name, db_host, db_name="datasets", db_user="root", db_password="123") -> None:
        self.table_name = table_name
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_data(self, num_var, cat_var, target_var):
        ## load dataset
        dataset = self.get_table()

        if num_var[0] == "None":
            num_var = []
        if cat_var[0] == "None":
            cat_var = []

        print("######################################################333")
        print(cat_var)
        print(num_var)
        print(cat_var + num_var)
        print("######################################################333")

        ## train test split
        X_train, X_test, y_train, y_test = train_test_split(dataset[num_var + cat_var], dataset[target_var], test_size=0.2, random_state=0)

        if (y_train.dtype == str) or (y_train.dtype == object):
            label_encoder = LabelEncoder().fit(y_train)
            y_train = label_encoder.transform(y_train)
            y_test = label_encoder.transform(y_test)

        return X_train, X_test, y_train, y_test

    # get a table from MariDB and return a pandas dataframe
    def get_table(self):
        # Construct the database URL
        db_url = f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

        # Create a SQLAlchemy engine
        engine = sqlalchemy.create_engine(db_url)

        # Define the SQL query to retrieve data from the table
        query = f"SELECT * FROM {self.table_name}"

        # Load data into a pandas DataFrame
        df = pd.read_sql(query, engine)

        # Close the SQLAlchemy engine
        engine.dispose()

        return df
