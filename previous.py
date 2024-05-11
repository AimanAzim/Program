import tkinter as tk
from datetime import datetime
import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the 'rent_rec' table if it doesn't exist
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

# Function to save the entered values into the database
def save_to_database():
    try:
        sr_no = sr_no_entry.get()
        name = name_entry.get()
        rent = rent_entry.get()
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()
        current_units = current_light_units_entry.get()
        previous_units = previous_light_units_entry.get()
        total_units = total_light_units_entry.get()
        light_bill = light_bill_entry.get()
        due_amount = due_amount_entry.get()
        total = total_entry.get()
        remarks = remarks_entry.get("1.0", "end-1c")  # Get text from the text box

        cursor.execute("INSERT INTO rent_rec (SrNo, Name, Rent, FromDate, ToDate, CurrentLightUnit, PreviousLightUnit, TotalUnits, LightBill, DueAmount, Total, Remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (sr_no, name, rent, from_date, to_date, current_units, previous_units, total_units, light_bill, due_amount, total, remarks))

        conn.commit()

        # Clear the entry fields and text box after saving
        for entry in entry_fields:
            entry.delete(0, tk.END)
            remarks_entry.delete(1.0, tk.END)


        # Update the datetime label
        update_datetime_label()

    except ValueError:
        error_label.config(text="Please enter valid numbers for input fields.")
    except sqlite3.Error as e:
        error_label.config(text=f"Database Error: {str(e)}")

def calculate_bill():
    try:
        current_units = int(current_light_units_entry.get())
        previous_units = int(previous_light_units_entry.get())
        rent = int(rent_entry.get())
        due_amount = int(due_amount_entry.get())

        total_units = current_units - previous_units
        light_bill = total_units * 12
        total = rent + light_bill + due_amount

        total_light_units_entry.delete(0, tk.END)
        light_bill_entry.delete(0, tk.END)
        total_entry.delete(0, tk.END)

        total_light_units_entry.insert(0, total_units)
        light_bill_entry.insert(0, light_bill)
        total_entry.insert(0, total)
    except ValueError:
        error_label.config(text="Please enter valid numbers for input fields.")

def update_datetime_label():
    current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    datetime_label.config(text=f"Current Date and Time: {current_datetime}")

root = tk.Tk()
root.title("Edit entries")

# Entry fields
entry_fields = []

sr_no_label = tk.Label(root, text="Sr No:")
sr_no_label.grid(row=0, column=0, sticky='w')
sr_no_entry = tk.Entry(root)
sr_no_entry.grid(row=0, column=1)
entry_fields.append(sr_no_entry)

name_label = tk.Label(root, text="Name:")
name_label.grid(row=1, column=0, sticky='w')
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)
entry_fields.append(name_entry)

rent_label = tk.Label(root, text="Rent:")
rent_label.grid(row=1, column=3, sticky='w')
rent_entry = tk.Entry(root)
rent_entry.grid(row=1, column=4)
entry_fields.append(rent_entry)

from_date_label = tk.Label(root, text="From Date:")
from_date_label.grid(row=3, column=0, sticky='w')
from_date_entry = tk.Entry(root)
from_date_entry.grid(row=3, column=1)
entry_fields.append(from_date_entry)

to_date_label = tk.Label(root, text="To Date:")
to_date_label.grid(row=3, column=3, sticky='w')
to_date_entry = tk.Entry(root)
to_date_entry.grid(row=3, column=4)
entry_fields.append(to_date_entry)

current_light_units_label = tk.Label(root, text="Current Light Units:")
current_light_units_label.grid(row=5, column=0, sticky='w')
current_light_units_entry = tk.Entry(root)
current_light_units_entry.grid(row=5, column=1)
entry_fields.append(current_light_units_entry)

previous_light_units_label = tk.Label(root, text="Previous Light Units:")
previous_light_units_label.grid(row=5, column=3, sticky='w')
previous_light_units_entry = tk.Entry(root)
previous_light_units_entry.grid(row=5, column=4)
entry_fields.append(previous_light_units_entry)

total_light_units_label = tk.Label(root, text="Total Light Units:")
total_light_units_label.grid(row=6, column=0, sticky='w')
total_light_units_entry = tk.Entry(root)
total_light_units_entry.grid(row=6, column=1)
entry_fields.append(total_light_units_entry)

light_bill_label = tk.Label(root, text="Light Bill:")
light_bill_label.grid(row=6, column=3, sticky='w')
light_bill_entry = tk.Entry(root)
light_bill_entry.grid(row=6, column=4)
entry_fields.append(light_bill_entry)

due_amount_label = tk.Label(root, text="Due Amount:")
due_amount_label.grid(row=7, column=0, sticky='w')
due_amount_entry = tk.Entry(root)
due_amount_entry.grid(row=7, column=1)
entry_fields.append(due_amount_entry)

total_label = tk.Label(root, text="Total Amount:")
total_label.grid(row=7, column=3, sticky='w')
total_entry = tk.Entry(root)
total_entry.grid(row=7, column=4)
entry_fields.append(total_entry)

remarks_label = tk.Label(root, text="Remarks:")
remarks_label.grid(row=8, column=0, sticky='w')
remarks_entry = tk.Text(root, height=5, width=40)
remarks_entry.grid(row=8, column=1, columnspan=4)
entry_fields.append(remarks_entry)

# Buttons
calculate_button = tk.Button(root, text="Calculate", command=calculate_bill)
calculate_button.grid(row=18, column=2, columnspan=2)

save_button = tk.Button(root, text="Save", command=save_to_database)
save_button.grid(row=18, column=4, columnspan=2)

error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=14, column=0, columnspan=2)

datetime_label = tk.Label(root, text="")
datetime_label.grid(row=0, column=3, columnspan=5)

update_datetime_label()  # Start updating the date and time

root.geometry('600x400')
root.mainloop()
