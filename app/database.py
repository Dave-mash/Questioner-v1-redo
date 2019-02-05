import psycopg2
import os

class InitializeDb:
    """ This class sets up database connection and creates tables """


    def __init__(self, url):
        try:
            self.connection = psycopg2.connect(url)
            self.cursor = self.connection.cursor()
            print('A connection to questioner_db database was established!')
        except:
            print('A problem occured while connecting to the database')


    def create_tables(self):
        """ This method creates tables """

        # users
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                other_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number INT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                isAdmin BOOLEAN NOT NULL,
                date_registered INT NOT NULL
                );
            """
        )

        # meetups
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS meetups (
                id serial PRIMARY KEY NOT NULL,
                admin_id INT unique NOT NULL,
                location TEXT NOT NULL,
                topic TEXT NOT NULL,
                created_on TIMESTAMP NOT NULL,
                description TEXT NOT NULL,
                schedule INT NOT NULL,
                tags VARCHAR NOT NULL
                );
            """
        )


        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS posts (
                id serial PRIMARY KEY NOT NULL,
                topic TEXT NOT NULL,
                description TEXT NOT NULL
                );
            """
        )
        
        self.connection.commit()
        # self.cursor.close()

    
    def execute(self, query):
        """ This method saves values into the db """
        
        self.cursor.execute(query)
        self.connection.commit()
        print('executed')
    
    
    def fetch_all(self, query):
        """ This method fetches all items """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
    def fetch_one(self, query):
        """ This method fetches a single item """
        
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    
    def update(self, query):
        """ This method executes update queries """
        print(query)
        self.cursor.execute(query)
        self.connection.commit()


# TIME
# from datetime import datetime

    # normal time --> timestamp
     # time = datetime.now()
     # datetime.timestamp(time)

    # timestamp --> normal time
     # timestamp = 34103718234.89098
     # time = datetime.fromtimestamp(timestamp)
 
# DICTIONARIES
# b = {
#    "one": 1,
#    "two": 2
# }
# list(b) --> 'one', 'two'
# list(b.values()) --> 1, 2