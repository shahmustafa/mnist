## Insert records from DB

import psycopg2

conn = psycopg2.connect(database="starbucks_stores", user="postgres",
                        host='localhost', password="Bigv@567",
                        port=5432)

cur = conn.cursor()
cur.execute("INSERT INTO persons(id, first_name, last_name, dob, email) VALUES('1','Appy','Bigv',"
            " '2014-02-02', 'appy@bgiv.com')")
conn.commit()
cur.close()
conn.close()