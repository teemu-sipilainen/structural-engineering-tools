from sympy import symbols, Eq, solve, latex

class Beam:
    def __init__(self, moment, shear, length, width, height, cover, left_support, right_support):
        self.moment = moment
        self.shear = shear
        self.length = length
        self.width = width
        self.height = height
        self.cover = cover
        self.left_support = left_support
        self.right_support = right_support

        # Calculate effective depth (d)
        self.d = self.height - self.cover

        # Calculate required area of reinforcement (A_s)
        self.calculate_reinforcement()

    def calculate_reinforcement(self):
        # Concrete and steel properties
        f_ck = 30  # Concrete compressive strength (MPa)
        f_yk = 500  # Yield strength of reinforcement (MPa)
        gamma_c = 1.5  # Partial safety factor for concrete
        gamma_s = 1.15  # Partial safety factor for steel

        f_cd = f_ck / gamma_c
        f_yd = f_yk / gamma_s

        # Reinforcement area calculation
        A_s = symbols('A_s')
        formula = Eq(self.moment * 1e6, 0.87 * f_yd * self.d * A_s * (1 - (f_cd * self.width * self.d) / (f_yd * A_s)))
        self.A_s = solve(formula, A_s)[0]
    
    def get_results(self):
        return (f"Effective Depth (d): {self.d:.2f} mm\n"
                f"Required Reinforcement Area (A_s): {self.A_s:.2f} mm²")

    def get_formula_latex(self):
        """Return the formula in LaTeX format with A_s solved."""
        A_s = symbols('A_s')
        f_ck = 30
        f_yk = 500
        gamma_c = 1.5
        gamma_s = 1.15

        f_cd = f_ck / gamma_c
        f_yd = f_yk / gamma_s

        formula = Eq(self.moment * 1e6, 0.87 * f_yd * self.d * A_s * (1 - (f_cd * self.width * self.d) / (f_yd * A_s)))
        A_s_solved = solve(formula, A_s)[0]

        # LaTeX representation with units
        return (f"A_s = \\frac{{{latex(self.moment * 1e6)} \\, \\text{{Nm}}}}{{0.87 \\cdot {latex(f_yd)} \\, \\text{{MPa}} \\cdot {latex(self.d)} \\, \\text{{mm}} \\, \\left(1 - \\frac{{{latex(f_cd)} \\, \\text{{MPa}} \\cdot {latex(self.width)} \\, \\text{{mm}} \\cdot {latex(self.d)} \\, \\text{{mm}}}}{{{latex(f_yd)} \\, \\text{{MPa}} \\cdot A_s}}\\right)}}")
