import psycopg2


def get_db(): #authentication for database
    return psycopg2.connect(host="localhost", dbname="authme" , user="loki", password="4prez")

def get_db_instance():  #creating an session 
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 



if __name__ == "__main__":
    db, cur = get_db_instance()

    cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute("create table music ( song_name varchar(255), rating int);")
    db.commit()




