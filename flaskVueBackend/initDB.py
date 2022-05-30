import psycopg2

MYUSER = 'postgres'
MYPWRD = ''
MYPORT = '5432'


#create the database table
def initCities():
    conn = psycopg2.connect(
   database="SE4G", user= MYUSER, password= MYPWRD, host='localhost', port= MYPORT
)
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS CITY")

    #Creating table as per requirement
    createTable ='''CREATE TABLE CITY(
    CITY_NAME CHAR(20) NOT NULL,
    NORTH FLOAT,
    EAST FLOAT
    )'''
    cursor.execute(createTable)
    #print("Table created successfully........")
    conn.commit()
    #Closing the connection
    conn.close()

if __name__ == "__main__":
    initCities()