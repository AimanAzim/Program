import sqlite3
from tkinter import *
from tkinter import ttk, simpledialog
import subprocess
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

def load_entries():
    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Fetch all entries from the 'rent_rec' table
    cursor.execute('SELECT SrNo, Name, Rent, FromDate, ToDate, CurrentLightUnit, PreviousLightUnit, TotalLightUnits, LightBill, DueAmount, Total, Remarks FROM rent_rec')
    entries = cursor.fetchall()

    # Close the database connection
    conn.close()
    return entries

def calculate_grand_total():
    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Calculate the sum of the 'Total' column from the 'rent_rec' table
    cursor.execute('SELECT SUM(Total) FROM rent_rec')
    total = cursor.fetchone()[0]

    # Close the database connection
    conn.close()
    return total if total else 0.0

def display_entries():
    # Create the main Tkinter window
    root = Tk()
    root.title("Rent Record Entries")

    # Function to open the expenses module
    def open_expenses_module():
        subprocess.run(["python", "expenses.py"])

    # Function to edit a selected entry
    def edit_entry():
        # Path to the script for editing entries
        script_path = os.path.join("D:/Notes/Projects/Rent calculation app/Rent-calculation-application/edit_entry.py")
        subprocess.run(["python", script_path])

    # Function to delete a selected entry
    def delete_entry():
        selected_item = tree.selection()[0]  # Get the selected item
        sr_no = tree.item(selected_item, "values")[0]  # Get the SrNo of the selected row

        # Connect to the SQLite database
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        # Delete the selected entry from the 'rent_rec' table
        cursor.execute('DELETE FROM rent_rec WHERE SrNo = ?', (sr_no,))
        conn.commit()

        # Close the database connection
        conn.close()

        # Remove the selected row from the Treeview
        tree.delete(selected_item)
        update_grand_total_label()

    # Function to refresh the entries in the Treeview
    def refresh_entries():
        for item in tree.get_children():
            tree.delete(item)  # Clear all existing rows
        entries = load_entries()
        for entry in entries:
            tree.insert("", "end", values=entry)
        update_grand_total_label()

    # Function to generate a PDF report of the entries
    def print_entries():
        month = simpledialog.askstring("Input", "Enter the month:")
        pdf_filename = f"{month}_rent_record.pdf"
        entries = load_entries()
        pdf = canvas.Canvas(pdf_filename, pagesize=landscape(A4))
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawString(150, 570, f"Recorded entries for the month of: {month}")
        pdf.setFont("Helvetica", 15)
        col_widths = [40, 150, 50, 80, 80, 40, 40, 40, 40, 60, 50, 90]
        row_height = 20
        x = 10
        y = 550
        for col, width in zip(["Sr No", "Name", "Rent", "From", "To", "CLU", "PLU", "TLU", "LBill", "Due Amt", "Total", "Remarks"], col_widths):
            pdf.drawString(x, y, col)
            x += width
        y -= row_height
        for entry in entries:
            if not entry:
                continue
            x = 10
            for value, width in zip(entry, col_widths):
                pdf.drawString(x, y, str(value))
                x += width
            y -= row_height
        pdf.save()
        subprocess.Popen(["start", "", pdf_filename], shell=True)

    # Function to exit the program
    def exit_program():
        root.quit()

    # Function to update the label displaying the grand total
    def update_grand_total_label():
        total = calculate_grand_total()
        total_label.config(text=f'Grand Total Rent: ${total:.2f}')

    # Create the Treeview for displaying entries
    tree = ttk.Treeview(root, columns=("SrNo", "Name", "Rent", "FromDate", "ToDate", "CurrentLightUnit", "PreviousLightUnit", "TotalLightUnits", "LightBill", "DueAmount", "Total", "Remarks"), show="headings")

    # ... (existing code)

    # Configure the Treeview columns and style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))
    style.configure("Treeview", font=("Consolas", 12))

    # Create buttons for various actions
    refresh_button = Button(root, text="Refresh", command=refresh_entries)
    edit_button = Button(root, text="Add", command=edit_entry)
    delete_button = Button(root, text="Delete", command=delete_entry)
    print_button = Button(root, text="Print", command=print_entries)
    exit_button = Button(root, text="Exit", command=exit_program)
    expenses_button = Button(root, text="Expenses", command=open_expenses_module)

    # Pack the buttons into the window
    refresh_button.pack(side=LEFT, padx=10)
    edit_button.pack(side=LEFT, padx=10)
    delete_button.pack(side=LEFT, padx=10)
    print_button.pack(side=LEFT, padx=10)
    expenses_button.pack(side=LEFT, padx=10)
    exit_button.pack(side=LEFT, padx=10)

    # Create and pack the label for displaying the grand total
    total_label = Label(root, text="Grand Total Rent: $0.00")
    total_label.pack(side=RIGHT, padx=10)

    # Insert existing entries into the Treeview
    for entry in load_entries():
        tree.insert("", "end", values=entry)

    # Set column widths and anchors
    tree.column("SrNo", width=10, anchor="w")
    tree.column("Name", width=80, anchor="w")
    tree.column("Rent", width=40, anchor="e")
    # ... (configure other columns)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    display_entries()
