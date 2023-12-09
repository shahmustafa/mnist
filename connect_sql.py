# Installation of psycopg2
# `sudo apt-get install libpq-dev python3-dev`
# `pip install psycopg2`

## Print all records from PostgreSQL DB

# import psycopg2
#
# conn = psycopg2.connect(database="starbucks_stores", user="postgres",
#                         host='localhost', password="Bigv@567",
#                         port=5432)
#
# cur = conn.cursor()
# cur.execute('SELECT * FROM persons;')
# rows = cur.fetchall()
# conn.commit()
# conn.close()
# for row in rows:
#     print(row)

import mysql

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3200',
    'database': 'digit'
}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
query = "SELECT * FROM classification_data;"
cursor.execute(query)
rows = cursor.fetchall()
connection.commit()
cursor.close()
connection.close()

for row in rows:
    print(row)
