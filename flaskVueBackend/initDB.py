import psycopg2

# Class that creates all tables in postgres database when initialized. Your installation of postgres has to have a database called "SE4G"

# Import to other files and initialize by typing: 
# from initDB import Pg
# Pg = Pg(user = "my username", password = "my password", port = "my port")
# if no keywords are inputed, default MYUSER, MYPWRD and MYPORT below will be used. 


class Pg:

    # Configuration information. Adjust so it matches you postgres installation before running on you computer. 
    MYUSER = 'postgres'
    MYPWRD = '123456'
    MYPORT = '5433'

    # Dictionary of the create statements for each table.
    #   There has to be one key equal to every item int tables. 
    #   The name of the created table must be the same as the name of the table in the tables list 
    create = {
        "city": '''CREATE TABLE city(
            city_id SMALLINT GENERATED ALWAYS AS IDENTITY,
            city_name CHAR(20) NOT NULL,
            longitude FLOAT,
            latitude FLOAT
        )''',
        "users": '''CREATE TABLE users(
            user_id SMALLINT GENERATED ALWAYS AS IDENTITY,
            user_name CHAR(20) NOT NULL,
            user_password VARCHAR NOT NULL
        )''',
        "contacts": '''CREATE TABLE contacts(
            contact_id SMALLINT GENERATED ALWAYS AS IDENTITY,
            first_name CHAR(20) NOT NULL,
            last_name CHAR(20) NOT NULL,
            description TEXT,
            nationality CHAR(3),
            email VARCHAR
        )'''
    }

    createTable ='''CREATE TABLE CITY(
    CITY_NAME CHAR(20) NOT NULL,
    NORTH FLOAT,
    EAST FLOAT
    )'''

    # helper function to clean up.
    def _drop(self, table):
        return "DROP TABLE IF EXISTS {}".format(table)

    #create the database table
    def __init__(self, user = None, password = None, port = None):

        if user is None: 
            user = self.MYUSER
        if password is None: 
            password = self.MYPWRD
        if port is None: 
            port = self.MYPORT

        conn = psycopg2.connect(
    database="SE4G", user = user, password= password, host='localhost', port= port
    )
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Creates all the tables in the list of tables. 
        for table in self.create.keys():
            #Doping table if already exists.
            cursor.execute(self._drop(table))

            cursor.execute(self.create[table])
            print("Table created successfully........")
            conn.commit()
        # Closing the connection
        conn.close()

if __name__ == "__main__":
    Pg = Pg()