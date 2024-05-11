import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the 'rent_rec' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rent_rec (
        SrNo INTEGER PRIMARY KEY,
        Name TEXT,
        Rent INTEGER,
        FromDate DATE,
        ToDate DATE,
        CurrentLightUnit INTEGER,
        PreviousLightUnit INTEGER,
        TotalUnits INTEGER,
        LightBill INTEGER,
        DueAmount INTEGER,
        Total INTEGER,
        Remarks TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'rent_rec' created.")
