import sqlite3
from tkinter import *
from tkinter import ttk

def create_expenses_table():
    conn = sqlite3.connect('expenses_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       note TEXT,
                       amount REAL)''')
    conn.commit()
    conn.close()

def save_expense(note, amount):
    conn = sqlite3.connect('expenses_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (note, amount) VALUES (?, ?)', (note, amount))
    conn.commit()
    conn.close()

def load_expenses():
    conn = sqlite3.connect('expenses_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT note, amount FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def calculate_total_expenses():
    conn = sqlite3.connect('expenses_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0.0

def expenses_module():
    create_expenses_table()

    def save_expense_entry():
        note = note_entry.get()
        amount = amount_entry.get()
        if note and amount:
            save_expense(note, amount)
            update_expenses_list()
            update_total_label()

    def update_expenses_list():
        for item in expenses_tree.get_children():
            expenses_tree.delete(item)
        expenses = load_expenses()
        for expense in expenses:
            expenses_tree.insert("", "end", values=expense)

    def update_total_label():
        total = calculate_total_expenses()
        total_label.config(text=f'Total Expenses: {total:.2f}Rupees')

    root = Tk()
    root.title("Expenses Module")

    note_label = Label(root, text="Note:")
    note_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    note_entry = Entry(root)
    note_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    amount_label = Label(root, text="Amount:")
    amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    amount_entry = Entry(root)
    amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    save_button = Button(root, text="Save Expense", command=save_expense_entry)
    save_button.grid(row=2, column=0, columnspan=2, pady=10)

    expenses_tree = ttk.Treeview(root, columns=("Note", "Amount"), show="headings")
    expenses_tree.heading("Note", text="Note")
    expenses_tree.heading("Amount", text="Amount")
    expenses_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    total_label = Label(root, text="Total Expenses: $0.00")
    total_label.grid(row=4, column=0, columnspan=2, pady=10)

    update_expenses_list()
    update_total_label()

    root.mainloop()

if __name__ == "__main__":
    expenses_module()
