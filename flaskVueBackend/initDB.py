import flask_cors
import psycopg2

from osm import Osm

# Class that creates all tables in postgres database when initialized. Your installation of postgres has to have a database called "SE4G"

# Import to other files and initialize by typing: 
# from initDB import Pg
# Pg = Pg(user = "my username", password = "my password", port = "my port")
# if no keywords are inputed, default MYUSER, MYPWRD and MYPORT below will be used. 


class Pg:

    # Configuration information. Adjust so it matches you postgres installation before running on you computer. 
    MYUSER = 'postgres'
    MYPWRD = 'postgres'
    MYPORT = '5432'

    # Dictionary of the create statements for each table.
    #   There has to be one key equal to every item int tables. 
    #   The name of the created table must be the same as the name of the table in the tables list 
    tables = {
        "city": '''CREATE TABLE city(
            city_id SMALLINT GENERATED ALWAYS AS IDENTITY,
            city_name VARCHAR NOT NULL,
            longitude FLOAT,
            latitude FLOAT
        )''',
        "users": '''CREATE TABLE users(
            user_id SMALLINT GENERATED ALWAYS AS IDENTITY,
            user_name CHAR(20) UNIQUE NOT NULL,
            user_password VARCHAR NOT NULL,
            last_search VARCHAR
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
        for table in self.tables.keys():
            #Doping table if already exists.
            cursor.execute(self._drop(table))

            cursor.execute(self.tables[table])
            print("Table created successfully........")
            conn.commit()

        # Getting the coordinates for cities
        cityCoords = Osm.getCities()

        # Adding the city data
        for city in cityCoords:
            city['name'] = city['name'].replace("'", "''") #using double tics to escape from postgres reserved character '. 
            sql = '''
            INSERT INTO city (city_name, longitude, latitude)
            VALUES('{}', {}, {});
            '''.format(city['name'], city['coordinates'][0], city['coordinates'][1])
            cursor.execute(sql)
        conn.commit()

        # Closing the connection
        conn.close()

if __name__ == "__main__":
    Pg = Pg()