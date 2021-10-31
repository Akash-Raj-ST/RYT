import psycopg2
from credentials import DB_USER_NAME,DB_PASSWORD,DB

def connect():

    try:
        conn = psycopg2.connect(
                database=DB,
                user=DB_USER_NAME,
                password=DB_PASSWORD,
                host='localhost'
                )

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return None

if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()
    sql = "SELECT * FROM api_review"
    cur.execute(sql)

    row = cur.fetchone()

    while row is not None:
        print(row)
        row = cur.fetchone()
    cur.close()
    conn.close()