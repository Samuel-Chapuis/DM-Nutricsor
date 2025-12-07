import tkinter as tk
from tkinter import ttk, messagebox

class NutriScoreEngine:
    """
    Calculates the Nutri-Score .
    """
    COLORS = {
        'A': '#038141', 'B': '#85BB2F', 'C': '#FECB02', 'D': '#EE8100', 'E': '#E63E11'
    }

    @staticmethod
    def get_points_n(energy, sat_fat, sugar, salt):
        # Calculates Negative Points (N)
        
        # Energy (kJ)
        if energy > 3350: p_en = 10
        elif energy <= 335: p_en = 0
        else: p_en = int((energy - 1) // 335)

        # Saturated Fat (g)
        if sat_fat > 10: p_fa = 10
        elif sat_fat <= 1: p_fa = 0
        else: p_fa = int(sat_fat)

        # Sugars (g)
        if sugar > 51: p_su = 15
        elif sugar > 48: p_su = 14
        elif sugar > 44: p_su = 13
        elif sugar > 41: p_su = 12
        elif sugar > 37: p_su = 11
        elif sugar > 34: p_su = 10
        elif sugar > 31: p_su = 9
        elif sugar > 27: p_su = 8
        elif sugar > 24: p_su = 7
        elif sugar > 20: p_su = 6
        elif sugar > 17: p_su = 5
        elif sugar > 14: p_su = 4
        elif sugar > 10: p_su = 3
        elif sugar > 6.8: p_su = 2
        elif sugar > 3.4: p_su = 1
        else: p_su = 0

        # Salt (g)
        if salt > 4.0: p_sa = 20
        elif salt > 0.2: p_sa = int(salt / 0.2)
        else: p_sa = 0
        
        return p_en + p_fa + p_su + p_sa

    @staticmethod
    def get_points_p(fiber, protein, fruit):
        # Calculates Positive Points (P)

        # Fiber (g)
        if fiber > 7.4: p_fi = 5
        elif fiber > 6.3: p_fi = 4
        elif fiber > 5.2: p_fi = 3
        elif fiber > 4.1: p_fi = 2
        elif fiber > 3.0: p_fi = 1
        else: p_fi = 0

        # Protein (g)
        if protein > 17: p_pr = 7
        elif protein > 14: p_pr = 6
        elif protein > 12: p_pr = 5
        elif protein > 9.6: p_pr = 4
        elif protein > 7.2: p_pr = 3
        elif protein > 4.8: p_pr = 2
        elif protein > 2.4: p_pr = 1
        else: p_pr = 0

        # Fruit/Veg (%)
        if fruit > 80: p_fr = 5
        elif fruit > 60: p_fr = 2
        elif fruit > 40: p_fr = 1
        else: p_fr = 0

        return p_fi, p_pr, p_fr

    @staticmethod
    def calculate(vals):
        score_n = NutriScoreEngine.get_points_n(
            vals['energy'], vals['sat_fat'], vals['sugar'], vals['salt']
        )
        p_fi, p_pr, p_fr = NutriScoreEngine.get_points_p(
            vals['fiber'], vals['protein'], vals['fruit']
        )
        
        score_p_raw = p_fi + p_pr + p_fr

        # If N >= 11 AND Fruit <= 80%, Protein is not counted 
        if score_n >= 11 and vals['fruit'] <= 80:
            score_p = p_fi + p_fr
            protein_msg = "Proteins excluded (N >= 11)"
        else:
            score_p = score_p_raw
            protein_msg = "Proteins included"

        final_score = score_n - score_p

        # Classification
        if final_score <= 0: grade = 'A'
        elif final_score <= 2: grade = 'B'
        elif final_score <= 10: grade = 'C'
        elif final_score <= 18: grade = 'D'
        else: grade = 'E'

        return {
            'score': final_score, 'grade': grade, 'color': NutriScoreEngine.COLORS[grade],
            'n_total': score_n, 'p_total': score_p, 'msg': protein_msg
        }

class RoundedFrame(tk.Canvas):
    """
    Custom widget to draw a rounded rectangle background.
    """
    def __init__(self, parent, width, height, color, bg_color, radius=25):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.color = color
        self.create_rounded_rect(0, 0, width, height, radius, fill=color)
        self.inner = tk.Frame(self, bg=color)
        self.create_window(width/2, height/2, window=self.inner, anchor="center")

    def update_bg(self, new_bg_color):
        # Updates the external corner color to match the window background
        self.configure(bg=new_bg_color)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

class ProNutriApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nutri-Score Calculator")
        self.geometry("1050x750")
        self.resizable(False, False)
        
        self.default_bg = "#F4F6F8" 
        self.current_bg = self.default_bg

        self.setup_styles()
        self.create_interface()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.card_bg = "#FFFFFF"     
        self.text_col = "#2C3E50"    
        self.accent_neg = "#E74C3C" 
        self.accent_pos = "#27AE60" 
        self.btn_color = "#3498DB"   
        self.font_main = ("Helvetica", 10)
        
        self.configure(bg=self.default_bg)
        style.configure("TLabel", background=self.card_bg, foreground=self.text_col, font=self.font_main)
        style.configure("Calc.TButton", font=("Helvetica", 12, "bold"), background=self.btn_color, foreground="white", borderwidth=0)
        style.map("Calc.TButton", background=[('active', '#2980B9')])

    def create_interface(self):
        # Header Section
        self.header_frame = tk.Frame(self, bg=self.current_bg)
        self.header_frame.pack(pady=35)
        
        self.header_label = tk.Label(self.header_frame, text="Nutri-Score Analysis Tool", font=("Helvetica", 26, "bold"), 
                 bg=self.current_bg, fg="#2C3E50")
        self.header_label.pack()

        # Main Layout Container
        self.main_frame = tk.Frame(self, bg=self.current_bg)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Left Column: Inputs
        self.left_col = tk.Frame(self.main_frame, bg=self.current_bg)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 30))

        # Negative Component Panel
        self.neg_panel = RoundedFrame(self.left_col, width=450, height=260, color=self.card_bg, bg_color=self.current_bg)
        self.neg_panel.pack(pady=10)
        self.create_form_section(self.neg_panel.inner, "Negative Component", self.accent_neg, [
            ("Energy (kJ/100g)", "energy"), ("Sugars (g/100g)", "sugar"),
            ("Sat. Fat (g/100g)", "sat_fat"), ("Salt (g/100g)", "salt")
        ])

        # Positive Component Panel
        self.pos_panel = RoundedFrame(self.left_col, width=450, height=220, color=self.card_bg, bg_color=self.current_bg)
        self.pos_panel.pack(pady=10)
        self.create_form_section(self.pos_panel.inner, "Positive Component", self.accent_pos, [
            ("Fibers (g/100g)", "fiber"), ("Proteins (g/100g)", "protein"),
            ("Fruits/Veg (%)", "fruit")
        ])

        # Action Button
        btn = ttk.Button(self.left_col, text="CALCULATE SCORE", style="Calc.TButton", command=self.validate_and_calculate, cursor="hand2")
        btn.pack(fill="x", pady=20, ipady=10)

        # Right Column: Results
        self.right_col = tk.Frame(self.main_frame, bg=self.current_bg)
        self.right_col.pack(side="right", fill="both", expand=True)

        self.res_panel = RoundedFrame(self.right_col, width=450, height=520, color=self.card_bg, bg_color=self.current_bg)
        self.res_panel.pack()
        
        res_inner = self.res_panel.inner
        tk.Label(res_inner, text="Nutritional Grade", font=("Helvetica", 14), bg=self.card_bg, fg="#95A5A6").pack(pady=(0, 20))
        
        # Canvas for the Score Bar
        self.canvas_res = tk.Canvas(res_inner, width=320, height=100, bg=self.card_bg, highlightthickness=0)
        self.canvas_res.pack()
        self.draw_bar() 

        self.lbl_grade = tk.Label(res_inner, text="-", font=("Helvetica", 80, "bold"), bg=self.card_bg, fg="#BDC3C7")
        self.lbl_grade.pack(pady=10)

        self.lbl_score = tk.Label(res_inner, text="Score: --", font=("Helvetica", 16), bg=self.card_bg, fg="#34495E")
        self.lbl_score.pack(pady=5)
        
        # Details Section
        ttk.Separator(res_inner, orient="horizontal").pack(fill="x", pady=20)
        self.lbl_n = tk.Label(res_inner, text="Negative Points: -", bg=self.card_bg, font=("Helvetica", 10))
        self.lbl_n.pack()
        self.lbl_p = tk.Label(res_inner, text="Positive Points: -", bg=self.card_bg, font=("Helvetica", 10))
        self.lbl_p.pack()
        self.lbl_msg = tk.Label(res_inner, text="", bg=self.card_bg, font=("Helvetica", 9, "italic"), fg="#BDC3C7")
        self.lbl_msg.pack(pady=5)

    def create_form_section(self, parent, title, accent_color, fields):
        head = tk.Frame(parent, bg=self.card_bg)
        head.pack(fill="x", pady=(0, 15))
        tk.Frame(head, bg=accent_color, width=5, height=20).pack(side="left", padx=(0, 10))
        tk.Label(head, text=title, font=("Helvetica", 12, "bold"), bg=self.card_bg, fg=self.text_col).pack(side="left")

        self.entries = getattr(self, 'entries', {})
        for label, key in fields:
            row = tk.Frame(parent, bg=self.card_bg)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, bg=self.card_bg, width=22, anchor="w").pack(side="left")
            ent = ttk.Entry(row, width=15, font=("Helvetica", 10), justify="center")
            ent.insert(0, "0")
            ent.pack(side="right")
            self.entries[key] = ent

    def draw_bar(self, active=None):
        self.canvas_res.delete("all")
        colors = ['#038141', '#85BB2F', '#FECB02', '#EE8100', '#E63E11']
        letters = ['A', 'B', 'C', 'D', 'E']
        start_x, w, gap = 10, 55, 5
        
        for i, (col, let) in enumerate(zip(colors, letters)):
            x = start_x + i*(w+gap)
            is_active = (active == let)
            fill = col if is_active else "#F0F3F4"
            text_col = "white" if is_active else "#BDC3C7"
            h_offset = 10 if is_active else 0
            
            self.create_round_rect_canvas(self.canvas_res, x, 20-h_offset, x+w, 80+h_offset, 8, fill=fill, outline="")
            f_size = 24 if is_active else 18
            self.canvas_res.create_text(x+w/2, 50, text=let, fill=text_col, font=("Helvetica", f_size, "bold"))

    def create_round_rect_canvas(self, canvas, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        canvas.create_polygon(points, smooth=True, **kwargs)

    def update_background(self, color):
        """Updates the main window background color dynamically."""
        self.configure(bg=color)
        
        self.header_frame.configure(bg=color)
        self.header_label.configure(bg=color)
        
        # Adjust text color based on background darkness
        if color in ['#038141', '#E63E11', '#EE8100']: 
             self.header_label.configure(fg="white")
        else:
             self.header_label.configure(fg="#2C3E50")

        self.main_frame.configure(bg=color)
        self.left_col.configure(bg=color)
        self.right_col.configure(bg=color)

        self.neg_panel.update_bg(color)
        self.pos_panel.update_bg(color)
        self.res_panel.update_bg(color)

    def validate_and_calculate(self):
        vals = {}
        limited_keys = ['sugar', 'sat_fat', 'salt', 'fiber', 'protein', 'fruit']
        
        for k, v in self.entries.items():
            try:
                val = float(v.get())
                if val < 0:
                    messagebox.showerror("Input Error", f"Value for {k} cannot be negative.")
                    return
                if k in limited_keys and val > 100:
                    messagebox.showerror("Input Constraint", f"Value for '{k}' cannot exceed 100.")
                    return
                vals[k] = val
            except ValueError:
                messagebox.showerror("Input Error", f"Please enter a valid number for {k}.")
                return

        res = NutriScoreEngine.calculate(vals)
        
        # Trigger dynamic visual feedback
        self.update_background(res['color'])

        self.draw_bar(res['grade'])
        self.lbl_grade.config(text=res['grade'], fg=res['color'])
        self.lbl_score.config(text=f"Score: {res['score']}")
        self.lbl_n.config(text=f"Negative Points: {res['n_total']}")
        self.lbl_p.config(text=f"Positive Points: {res['p_total']}")
        self.lbl_msg.config(text=res['msg'])

if __name__ == "__main__":
    app = ProNutriApp()
    app.mainloop()