import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the login table with id and password columns
cursor.execute('CREATE TABLE IF NOT EXISTS login (id NUMBER, password TEXT)')

# Insert the sample record
sample_id = '1234567890'
sample_password = '1234567890'
cursor.execute('INSERT INTO login (id, password) VALUES (?, ?)', (sample_id, sample_password))

conn.commit()
conn.close()
