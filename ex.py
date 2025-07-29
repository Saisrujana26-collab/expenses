import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

file_name = "expenses.json"

def load_expenses():
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_expenses(expenses):
    with open(file_name, "w") as file:
        json.dump(expenses, file, indent=4)

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Expense Tracker")

        self.expenses = load_expenses()

        # --- Widgets ---
        # Amount
        tk.Label(root, text="Amount ($):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        tk.Label(root, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        # Description
        tk.Label(root, text="Description:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        # Date
        tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        # Buttons
        add_btn = tk.Button(root, text="Add Expense", command=self.add_expense)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        view_btn = tk.Button(root, text="View All Expenses", command=self.view_expenses)
        view_btn.grid(row=5, column=0, columnspan=2, pady=5)

        summary_btn = tk.Button(root, text="Show Summary by Category", command=self.show_summary)
        summary_btn.grid(row=6, column=0, columnspan=2, pady=5)

        # Text box for output
        self.output_text = tk.Text(root, width=50, height=15)
        self.output_text.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for amount.")
            return

        category = self.category_entry.get().strip().capitalize()
        if not category:
            messagebox.showerror("Invalid input", "Please enter a category.")
            return

        description = self.desc_entry.get().strip()
        date = self.date_entry.get().strip()

        # Validate date format
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Please enter date in YYYY-MM-DD format.")
            return

        expense = {"amount": amount, "category": category, "description": description}

        if date not in self.expenses:
            self.expenses[date] = []
        self.expenses[date].append(expense)

        save_expenses(self.expenses)

        messagebox.showinfo("Success", f"Added expense of ${amount} on {date}.")

        # Clear input fields
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

    def view_expenses(self):
        self.output_text.delete("1.0", tk.END)
        if not self.expenses:
            self.output_text.insert(tk.END, "No expenses recorded yet.\n")
            return

        for date, entries in sorted(self.expenses.items()):
            self.output_text.insert(tk.END, f"Date: {date}\n")
            for e in entries:
                desc = e['description'] if e['description'] else "No description"
                self.output_text.insert(tk.END, f"  ${e['amount']} - {e['category']} - {desc}\n")
            self.output_text.insert(tk.END, "\n")

    def show_summary(self):
        category_totals = {}
        for entries in self.expenses.values():
            for e in entries:
                category = e['category']
                category_totals[category] = category_totals.get(category, 0) + e['amount']

        self.output_text.delete("1.0", tk.END)
        if not category_totals:
            self.output_text.insert(tk.END, "No expenses to summarize.\n")
            return

        self.output_text.insert(tk.END, "Expense Summary by Category:\n")
        for cat, total in category_totals.items():
            self.output_text.insert(tk.END, f"{cat}: ${total:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
