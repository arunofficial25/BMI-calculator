import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pickle
import os

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.data = self.load_data()

        # Create input fields
        self.weight_label = tk.Label(root, text="Weight (kg):")
        self.weight_label.pack()
        self.weight_entry = tk.Entry(root)
        self.weight_entry.pack()

        self.height_label = tk.Label(root, text="Height (m):")
        self.height_label.pack()
        self.height_entry = tk.Entry(root)
        self.height_entry.pack()

        # Create buttons
        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.pack()

        self.view_history_button = tk.Button(root, text="View History", command=self.view_history)
        self.view_history_button.pack()

        # Create result display
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def load_data(self):
        if os.path.exists("bmi_data.pkl"):
            with open("bmi_data.pkl", "rb") as f:
                return pickle.load(f)
        else:
            return []

    def save_data(self):
        with open("bmi_data.pkl", "wb") as f:
            pickle.dump(self.data, f)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight < 0 or height < 0:
                messagebox.showerror("Invalid input", "Weight and height must be non-negative.")
                return

            bmi = weight / (height ** 2)
            category = self.categorize_bmi(bmi)

            self.data.append((weight, height, bmi, category))
            self.save_data()

            self.result_label.config(text=f"BMI: {bmi:.2f}, Category: {category}")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for weight and height.")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def view_history(self):
        if not self.data:
            messagebox.showinfo("No history", "No BMI data available.")
            return

        weights = [x[0] for x in self.data]
        heights = [x[1] for x in self.data]
        bmis = [x[2] for x in self.data]
        categories = [x[3] for x in self.data]

        plt.plot(bmis)
        plt.xlabel("Entry")
        plt.ylabel("BMI")
        plt.title("BMI History")
        plt.show()

        history_text = ""
        for i, (weight, height, bmi, category) in enumerate(self.data):
            history_text += f"Entry {i+1}: Weight={weight}kg, Height={height}m, BMI={bmi:.2f}, Category={category}\n"

        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        history_label = tk.Label(history_window, text=history_text)
        history_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()