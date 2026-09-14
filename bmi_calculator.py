import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# Database Initialization
def init_db():
    conn = None
    try:
        conn = sqlite3.connect('bmi_records.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date_recorded TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
    finally:
        if conn:
            conn.close()

def save_record(user_name, weight, height, bmi, category):
    conn = None
    try:
        conn = sqlite3.connect('bmi_records.db')
        cursor = conn.cursor()
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO records (user_name, weight, height, bmi, category, date_recorded)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_name, weight, height, bmi, category, date_str))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save record: {e}")
    finally:
        if conn:
            conn.close()

def fetch_records(user_name):
    conn = None
    try:
        conn = sqlite3.connect('bmi_records.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date_recorded, bmi FROM records 
            WHERE user_name = ? ORDER BY date_recorded ASC
        ''', (user_name,))
        records = cursor.fetchall()
        return records
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch records: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Application Class
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Style options
        font_title = ("Helvetica", 20, "bold")
        font_large = ("Helvetica", 14)
        font_normal = ("Helvetica", 12)

        # UI Elements
        tk.Label(root, text="BMI Calculator", font=font_title, fg="#333").pack(pady=15)

        # User Name
        tk.Label(root, text="User Name:", font=font_normal).pack()
        self.entry_name = tk.Entry(root, font=font_normal, justify="center")
        self.entry_name.pack(pady=5)

        # Weight
        tk.Label(root, text="Weight (kg):", font=font_normal).pack()
        self.entry_weight = tk.Entry(root, font=font_normal, justify="center")
        self.entry_weight.pack(pady=5)

        # Height
        tk.Label(root, text="Height (m):", font=font_normal).pack()
        self.entry_height = tk.Entry(root, font=font_normal, justify="center")
        self.entry_height.pack(pady=5)

        # Calculate Button
        btn_calc = tk.Button(root, text="Calculate BMI", font=font_large, bg="#4CAF50", fg="white", 
                             activebackground="#45a049", cursor="hand2", command=self.calculate_bmi)
        btn_calc.pack(pady=15, fill="x", padx=50)

        # Result Label
        self.lbl_result = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
        self.lbl_result.pack(pady=10)

        # History Button
        btn_history = tk.Button(root, text="View BMI History", font=font_normal, bg="#2196F3", fg="white", 
                                activebackground="#1976D2", cursor="hand2", command=self.view_history)
        btn_history.pack(pady=10, fill="x", padx=50)

    def calculate_bmi(self):
        name = self.entry_name.get().strip()
        weight_str = self.entry_weight.get().strip()
        height_str = self.entry_height.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a user name.")
            return

        try:
            weight = float(weight_str)
            height = float(height_str)
            
            if weight <= 0 or height <= 0:
                raise ValueError("Values must be positive.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid positive numeric values for weight and height.")
            return

        # BMI Formula: weight / (height²)
        bmi = weight / (height ** 2)
        bmi_rounded = round(bmi, 2)

        # Classification and Color Coding
        if bmi < 18.5:
            category = "Underweight"
            color = "#FFA500" # Orange
        elif 18.5 <= bmi <= 24.9:
            category = "Normal"
            color = "#008000" # Green
        elif 25 <= bmi <= 29.9:
            category = "Overweight"
            color = "#FF8C00" # Dark Orange
        else:
            category = "Obese"
            color = "#FF0000" # Red

        # Update Result Label
        result_text = f"BMI: {bmi_rounded}\n{category}"
        self.lbl_result.config(text=result_text, fg=color)

        # Save to DB
        save_record(name, weight, height, bmi_rounded, category)

    def view_history(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a user name to view history.")
            return

        records = fetch_records(name)
        if not records:
            messagebox.showinfo("History", f"No records found for user '{name}'.")
            return

        dates = [rec[0] for rec in records]
        bmis = [rec[1] for rec in records]

        # Use matplotlib to plot the data
        plt.figure(figsize=(8, 5))
        plt.plot(dates, bmis, marker='o', linestyle='-', color='#2196F3', linewidth=2, markersize=8)
        
        # Add a baseline for Normal BMI
        plt.axhspan(18.5, 24.9, color='#008000', alpha=0.2, label="Normal Range")

        plt.title(f"BMI History for {name}", fontsize=14)
        plt.xlabel("Date Recorded", fontsize=12)
        plt.ylabel("BMI", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
