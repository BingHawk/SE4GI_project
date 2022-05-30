import psycopg2

class Pg:

    # Configuration information. Adjust so it matches you postgres installation before running on you computer. 
    MYUSER = 'postgres'
    MYPWRD = 'qrC85Ba9Dpg'
    MYPORT = '5432'

    # list of the table names
    tables = ["cities","users","contacts"]

    # Dictionary of the create statements for each table.
    #   There has to be one key equal to every item int tables. 
    #   The name of the created table must be the same as the name of the table in the tables list 
    create = {
        "cities": '''CREATE TABLE cities(
            city_id SMALLINT GENERATED ALWAYS AS IDENTITY
            city_name CHAR(20) NOT NULL,
            longitude FLOAT,
            latitude FLOAT
        )''',
        "users": '''CREATE TABLE users(
            user_id SMALLINT GENERATED ALWAYS AS IDENTITY
            user_name CHAR(20) NOT NULL
            user_password VARCHAR NOT NULL
        ''',
        "contacts": '''CREATE TABLE users(
            contact_id SMALLINT GENERATED ALWAYS AS IDENTITY
            first_name CHAR(20) NOT NULL
            last_name CHAR(20) NOT NULL
            description TEXT
            nationality CHAR(3)
            email VARCHAR
        '''
    }

    # helper function to clean up.
    def _drop(self, table):
        return "DROP TABLE IF EXISTS {}".format(table)

    #create the database table
    def __init__(self):
        conn = psycopg2.connect(
    database="SE4G", user= self.MYUSER, password= self.MYPWRD, host='localhost', port= self.MYPORT
    )
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Creates all the tables in the list of tables. 
        for table in self.tables:
            #Doping table if already exists.
            cursor.execute(self._drop(table))

            cursor.execute(self.create['table'])
        # print("Table created successfully........")
            conn.commit()
        # Closing the connection
        conn.close()

if __name__ == "__main__":
    Pg = Pg()