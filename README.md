# BMI Calculator

An advanced Body Mass Index (BMI) calculator built with Python, featuring a complete graphical user interface, local data persistence, and interactive data visualization. 

## Features
- **Graphical User Interface:** Clean and intuitive UI built with `tkinter`.
- **Accurate Calculations:** Computes BMI based on user height and weight and categorizes the result (Underweight, Normal, Overweight, Obese).
- **Color-Coded Feedback:** Instant visual feedback with color coding based on the health category.
- **Data Persistence:** Automatically saves every record securely using `sqlite3` so you can track progress over time.
- **Trend Visualization:** Generates historical line charts of your BMI journey using `matplotlib`.
- **Input Validation:** Built-in safeguards to prevent crashes from negative values or non-numeric inputs.

## Prerequisites
- Python 3.6 or higher
- Matplotlib

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sumithanagandi7-art/sumit_Task2.git
   cd "sumit task 2"
   ```

2. **Install the dependencies:**
   The only external dependency is `matplotlib`. Install it via pip:
   ```bash
   pip install matplotlib
   ```

3. **Run the application:**
   ```bash
   python bmi_calculator.py
   ```

## Usage
1. Open the application.
2. Enter your **Name**, **Weight** (in kilograms), and **Height** (in meters).
3. Click **Calculate BMI** to view your current BMI and health category.
4. To see your historical data, enter your Name and click **View BMI History**. A line chart will pop up showing your trend over time!

## Data Storage
Your data is stored locally in an auto-generated SQLite database file named `bmi_records.db`. It is completely private and remains on your device.
