import psycopg2


def authenticate(username, password, *args):

    #The authentication
    #Checking whether he is already in the DB|registered
    conn = psycopg2.connect(
    database="SE4G", user = args[0], password= args[1], host='localhost', port= args[2]
    )
    cur = conn.cursor()
    cur.execute(
    'SELECT user_id FROM users WHERE user_name = %s AND user_password= %s', (username, password))
    # The user is registered then is verified
    if cur.fetchone() is not None:
        cur.execute(
        'SELECT * FROM users WHERE user_name = %s AND user_password= %s', (username, password))
        res= cur.fetchone()
        responde= {
            "user": {
                "username": res[1],
                "userID": res[0],
            },
            "access": True,
            "lastSearch": res[3]
            }
        print('the user is being verified to be registered, hence it has been authenticated')
        print("Authenticate recieved")
        cur.close()
    # If he is not registered then the authentication fails    
    else:
        responde={
            "user": {
                "username": None,
                "userID": None,
            },
            "access": False,
            "lastSearch": None
            }
        print('the user is not being verified to be registered, hence it has to register first')
        print("Authenticate not being granted")
        # cur.execute(

    conn.commit()
    conn.close()
    # flash(error)
    return responde 

def register(username, password, *args):
    conn = psycopg2.connect(
    database="SE4G", user = args[0], password= args[1], host='localhost', port= args[2]
    )
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO users (user_name,user_password) VALUES ('{username}','{password}') RETURNING user_id;")

        output= {
        'user':{
            'user_id': cur.fetchone()[0],
            'username': username,
        },
        'register': True
        }  
    except psycopg2.errors.UniqueViolation:
        print("not a new username")
        output= {
        'user':{
            'user_id': None,
            'username': username,
        },
        'register': False
        }

    conn.commit()
    conn.close()
    return output  

def logout(username, lastsearch, *args):
    conn = psycopg2.connect(
            database="SE4G", user = args[0], password= args[1], host='localhost', port= args[2]
            )
    cur = conn.cursor()

    cur.execute(f"UPDATE users SET last_search = '{lastsearch}' WHERE user_name = '{username}'")
    conn.commit()
    cur.execute(f"SELECT user_id FROM users WHERE user_name = '{username}'")
    output = {
            'user':{
                'user_id': cur.fetchone()[0],
                'username': username
                },
            'saved': bool(id)}       
    conn.commit()
    conn.close()

    return output