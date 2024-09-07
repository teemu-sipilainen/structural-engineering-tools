import tkinter as tk
from tkinter import ttk
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from beam import Beam
import io
from PIL import Image, ImageTk
import atexit
import tempfile

class BeamDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reinforced Concrete Beam Design")
        self.root.geometry("600x800")

        # Title
        title_label = ttk.Label(root, text="Reinforced Concrete Beam Design", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Input fields
        self.moment_entry = self.create_entry("Design Moment (kNm):", default_value="50")
        self.shear_entry = self.create_entry("Design Shear Force (kN):", default_value="20")
        self.length_entry = self.create_entry("Beam Length (m):", default_value="6")
        self.width_entry = self.create_entry("Width (mm):", default_value="300")
        self.height_entry = self.create_entry("Height (mm):", default_value="500")
        self.cover_entry = self.create_entry("Concrete Cover (mm):", default_value="30")
        self.support_left_entry = self.create_entry("Left Support Length (mm):", default_value="0")
        self.support_right_entry = self.create_entry("Right Support Length (mm):", default_value="0")

        # Concrete properties
        self.f_ck_entry = self.create_entry("Concrete Compressive Strength (MPa):", default_value="30")
        self.gamma_c_entry = self.create_entry("Partial Safety Factor for Concrete:", default_value="1.5")

        # Steel properties
        self.f_yk_entry = self.create_entry("Yield Strength of Reinforcement (MPa):", default_value="500")
        self.gamma_s_entry = self.create_entry("Partial Safety Factor for Steel:", default_value="1.15")

        # Calculate button
        calculate_button = ttk.Button(root, text="Calculate", command=self.calculate)
        calculate_button.pack(pady=20)

        # Save to PDF button
        self.save_button = ttk.Button(root, text="Save to PDF", command=self.save_to_pdf, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        # Display results
        self.result_label = ttk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

        # Display formula
        self.formula_canvas = tk.Canvas(root, width=500, height=100)
        self.formula_canvas.pack(pady=10)

        # Register cleanup function
        atexit.register(self.cleanup)

    def create_entry(self, label_text, default_value=""):
        """Helper function to create a labeled entry widget with default value."""
        label = ttk.Label(self.root, text=label_text)
        label.pack()
        entry = ttk.Entry(self.root)
        entry.pack(pady=5)
        entry.insert(0, default_value)
        return entry

    def calculate(self):
        """Performs the calculation and displays the result."""
        # Input values
        moment = float(self.moment_entry.get())  # Design moment
        shear = float(self.shear_entry.get())    # Design shear force
        length = float(self.length_entry.get())  # Beam length (not used in calculation)
        width = float(self.width_entry.get())    # Width of the beam
        height = float(self.height_entry.get())  # Total height of the beam
        cover = float(self.cover_entry.get())    # Concrete cover
        left_support = float(self.support_left_entry.get())  # Length of the left support
        right_support = float(self.support_right_entry.get()) # Length of the right support

        # Concrete properties
        f_ck = float(self.f_ck_entry.get())  # Concrete compressive strength
        gamma_c = float(self.gamma_c_entry.get())  # Partial safety factor for concrete

        # Steel properties
        f_yk = float(self.f_yk_entry.get())  # Yield strength of reinforcement
        gamma_s = float(self.gamma_s_entry.get())  # Partial safety factor for steel

        # Create Beam object
        self.beam = Beam(moment, shear, length, width, height, cover, left_support, right_support)
        self.beam.f_ck = f_ck
        self.beam.gamma_c = gamma_c
        self.beam.f_yk = f_yk
        self.beam.gamma_s = gamma_s

        # Display results
        result_text = self.beam.get_results()
        self.result_label.config(text=result_text)

        # Display formula
        formula_latex = self.beam.get_formula_latex()
        self.display_formula_graphically(formula_latex)

        # Enable Save to PDF button
        self.save_button.config(state=tk.NORMAL)

    def display_formula_graphically(self, formula_latex):
        """Display the formula graphically using matplotlib."""
        fig = Figure(figsize=(5, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"${formula_latex}$", fontsize=16, ha='center', va='center')
        ax.axis('off')

        # Convert matplotlib figure to a Tkinter-compatible image
        canvas = FigureCanvasTkAgg(fig, master=self.formula_canvas)
        canvas.draw()
        self.formula_canvas.create_window((0, 0), window=canvas.get_tk_widget(), anchor="nw")

    def save_to_pdf(self):
        """Saves the calculation result and formula to a PDF file."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Reinforced Concrete Beam Design", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Design Moment: {self.moment_entry.get()} kNm", ln=True)
        pdf.cell(200, 10, txt=f"Design Shear Force: {self.shear_entry.get()} kN", ln=True)
        pdf.cell(200, 10, txt=f"Beam Length: {self.length_entry.get()} m", ln=True)
        pdf.cell(200, 10, txt=f"Width: {self.width_entry.get()} mm", ln=True)
        pdf.cell(200, 10, txt=f"Height: {self.height_entry.get()} mm", ln=True)
        pdf.cell(200, 10, txt=f"Concrete Cover: {self.cover_entry.get()} mm", ln=True)
        pdf.cell(200, 10, txt=f"Left Support Length: {self.support_left_entry.get()} mm", ln=True)
        pdf.cell(200, 10, txt=f"Right Support Length: {self.support_right_entry.get()} mm", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Concrete Compressive Strength: {self.f_ck_entry.get()} MPa", ln=True)
        pdf.cell(200, 10, txt=f"Partial Safety Factor for Concrete: {self.gamma_c_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Yield Strength of Reinforcement: {self.f_yk_entry.get()} MPa", ln=True)
        pdf.cell(200, 10, txt=f"Partial Safety Factor for Steel: {self.gamma_s_entry.get()}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=self.beam.get_results(), ln=True)

        # Add the formula to the PDF
        formula_latex = self.beam.get_formula_latex()
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Formula:")
        
        # Convert the LaTeX formula to an image
        fig = Figure(figsize=(5, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"${formula_latex}$", fontsize=16, ha='center', va='center')
        ax.axis('off')

        # Save matplotlib figure to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_filename = temp_file.name
            fig.savefig(temp_filename, format='png', bbox_inches='tight')
        
        # Add the image to the PDF
        pdf.image(temp_filename, x=10, y=pdf.get_y(), w=180)

        # Remove the temporary file
        import os
        os.remove(temp_filename)

        # Save the PDF file
        pdf_name = "beam_design_calculation.pdf"
        pdf.output(pdf_name)

        self.result_label.config(text=f"Calculation saved as {pdf_name}")


    def cleanup(self):
        """Cleanup function to ensure proper resource management."""
        plt.close('all')  # Close all matplotlib figures

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BeamDesignApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup)  # Ensure cleanup on window close
    root.mainloop()
