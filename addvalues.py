import sqlite3
import random
import datetime

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Generate and insert random values into the "rent_rec" table
for sr_no in range(1, 11):  # Generate random data for 10 entries
    name = f"Tenant{sr_no}"
    rent = random.randint(5000, 10000)
    from_date = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))
    to_date = from_date + datetime.timedelta(days=random.randint(30, 365))
    current_light_unit = random.randint(100, 500)
    previous_light_unit = random.randint(50, 99)
    rate_rs = 15  # Default rate
    total_light_units = current_light_unit - previous_light_unit
    light_bill = total_light_units * rate_rs
    due_amount = rent + light_bill
    total = rent + light_bill
    remarks = f"Random entry for Sr No {sr_no}"

    cursor.execute("INSERT INTO rent_rec (SrNo, Name, Rent, FromDate, ToDate, CurrentLightUnit, PreviousLightUnit, TotalUnits, LightBill, DueAmount, Total, Remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (sr_no, name, rent, from_date, to_date, current_light_unit, previous_light_unit, total_light_units, light_bill, due_amount, total, remarks))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Random data inserted into the 'rent_rec' table.")
