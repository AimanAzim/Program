import sqlite3
from tkinter import *
from tkinter import ttk, simpledialog
import subprocess
import os


def load_entries():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SrNo, Name, Rent, FromDate, ToDate, CurrentLightUnit, PreviousLightUnit, TotalUnits, LightBill, DueAmount, Total, Remarks FROM rent_rec')
    entries = cursor.fetchall()
    conn.close()
    return entries

def display_entries():
    root = Tk()
    root.title("Rent Record Entries")

    def open_expenses_module():
        subprocess.run(["python", "expenses.py"])

    def edit_entry():
        script_path = os.path.join("edit_entry.py")
        subprocess.run(["python", script_path])

    def delete_entry():
        selected_item = tree.selection()[0]  
        sr_no = tree.item(selected_item, "values")[0]  
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rent_rec WHERE SrNo = ?', (sr_no,))
        conn.commit()
        conn.close()
        tree.delete(selected_item)  

    def refresh_entries():
        for item in tree.get_children():
            tree.delete(item)  
        entries = load_entries()
        for entry in entries:
            tree.insert("", "end", values=entry)

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

    def exit_program():
        root.quit()

    tree = ttk.Treeview(root, columns=("SrNo", "Name", "Rent", "FromDate", "ToDate", "CurrentLightUnit", "PreviousLightUnit", "TotalLightUnits", "LightBill", "DueAmount", "Total", "Remarks"), show="headings")

    tree.heading("SrNo", text="Sr No")
    tree.heading("Name", text="Name")
    tree.heading("Rent", text="Rent")
    tree.heading("FromDate", text="From")
    tree.heading("ToDate", text="To")
    tree.heading("CurrentLightUnit", text="CLU")
    tree.heading("PreviousLightUnit", text="PLU")
    tree.heading("TotalLightUnits", text="TLU")
    tree.heading("LightBill", text="LBill")
    tree.heading("DueAmount", text="Due Amt")
    tree.heading("Total", text="Total")
    tree.heading("Remarks", text="Remarks")

    tree.pack(padx=20, pady=10, fill="both", expand=True)

    for entry in load_entries():
        tree.insert("", "end", values=entry)

    tree.column("SrNo", width=10, anchor="w")
    tree.column("Name", width=80, anchor="w")
    tree.column("Rent", width=40, anchor="e")
    tree.column("FromDate", width=60, anchor="e")
    tree.column("ToDate", width=60, anchor="e")
    tree.column("CurrentLightUnit", width=30, anchor="e")
    tree.column("PreviousLightUnit", width=30, anchor="e")
    tree.column("TotalLightUnits", width=30, anchor="e")
    tree.column("LightBill", width=30, anchor="e")
    tree.column("DueAmount", width=80, anchor="e")
    tree.column("Total", width=0, anchor="e")
    tree.column("Remarks", anchor="w")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))
    style.configure("Treeview", font=("Consolas", 12))

    refresh_button = Button(root, text="Refresh", command=refresh_entries)
    edit_button = Button(root, text="Add", command=edit_entry)
    delete_button = Button(root, text="Delete", command=delete_entry)
    print_button = Button(root, text="Print", command=print_entries)
    exit_button = Button(root, text="Exit", command=exit_program)
    expenses_button = Button(root, text="Expenses", command=open_expenses_module)

    refresh_button.pack(side=LEFT, padx=10)
    edit_button.pack(side=LEFT, padx=10)
    delete_button.pack(side=LEFT, padx=10)
    print_button.pack(side=LEFT, padx=10)
    expenses_button.pack(side=LEFT, padx=10)
    exit_button.pack(side=LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    display_entries()
