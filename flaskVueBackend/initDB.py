import psycopg2


#create the database table
def addCitiesToDatabase(cities):
    conn = psycopg2.connect(
   database="SE4G", user='postgres', password='123456', host='localhost', port= '5433'
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