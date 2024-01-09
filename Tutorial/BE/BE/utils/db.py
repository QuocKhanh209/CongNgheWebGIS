import psycopg2
from django.conf import settings
from . import postgis

def create_conf_db():
    data = postgis.get_parmas()

    host = data.get('host')
    port = data.get('port')
    username = data.get('pg_user')
    password = data.get('pg_password')
    database = data.get('db')

    return {'host': host, 'port': port, 'user': username, 'password': password, 'dbname': database}

def connection():
    db_conf = create_conf_db()
    import psycopg2 as db
    conn = db.connect(**db_conf)
    return conn

# 
def execute_command(conn, command):
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(command)

        conn.commit()

        # close the communication with db
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise error

# 
def execute_query_select(conn, query, data=None):
    '''
        Excute query
    '''
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(query, data)

        # result
        data = cur.fetchall()
        columns = [item.name for item in cur.description]

        # json data
        result = []
        for item in data:
            r = {}
            for idx, val in enumerate(columns):
                r[val] = item[idx]
            
            result.append(r)

        # close the communication with db
        cur.close()

        return result

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

# insert, update, delete
def execute_query_iud(conn, query, data):
    '''
        Excute query
        Apply to insert, update, delete
        data: [(), ...]
    '''
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        if len(data) > 1:
            cur.executemany(query, data)
        else:
            cur.execute(query, data[0])

        conn.commit()

        # result
        updated_rows = cur.rowcount

        # close the communication with db
        cur.close()

        return updated_rows

    except (Exception, psycopg2.DatabaseError) as error:
        raise error

