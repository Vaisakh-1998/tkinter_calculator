import tkinter as tk
from math import sin, cos, tan, pi, sqrt

MAX_LEN = 14 #calc size restriction

LARGE_FONT_STYLE = ("Arial", 30, "bold")
UPDATE_FONT = ("Arial", 18, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 20, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
TRIG_FONT_STYLE = ("Arial", 15)

LIGHT_GRAY = "#F5F5F5"
WHITE = "#FFFFFF"
LABEL_COLOR = "#25265E"
OFF_WHITE = "#F8FAFF"
BLUE = "#0096FF"
GRAY = "#CECECE"

class Calculator:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Calculator")
		self.window.geometry("900x1600")
		self.window.resizable(1,1)
		
		self.upper_expression = ""
		self.lower_expression = ""
		self.display_frame = self.create_display_frame()
		
		self.upper_label, self.lower_label = self.create_display_labels()		
		
		self.digits = {			
			7: (1, 1), 8: (1, 2), 9: (1, 3),
			4: (2, 1), 5: (2, 2), 6: (2, 3),
			1: (3, 1), 2: (3, 2), 3: (3, 3),
			'.': (4, 2), 0: (4, 3)
		}
		self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
		self.buttons_frame = self.create_buttons_frame()
		
		self.buttons_frame.rowconfigure(0, weight=1)
		for i in range(1,5):
			self.buttons_frame.rowconfigure(i, weight=1)
			self.buttons_frame.columnconfigure(i, weight=1)
				
		self.create_buttons()
		self.collapse_button = self.create_collapsible_button()	
			
		self.collapse = True
		self.collapsible_frame = self.create_collapsible_frame()
		self.collapsible_frame.rowconfigure(0, weight=1)
		self.collapsible_frame.rowconfigure(1, weight=1)
		for i in range(1, 5):
			self.collapsible_frame.columnconfigure(i, weight=1)
			
		self.create_parentheses_buttons()
		self.create_square_button()					
		self.create_percent_button()				
		self.create_trigonometry_buttons()			
		self.create_sqrt_button()
		self.create_pi_num_button()
										
	def create_buttons(self):
		self.create_digit_buttons()
		self.create_operator_buttons()
		self.create_clear_button()
		self.create_equals_button()
					
	def create_display_labels(self):
		up_label = tk.Label(self.display_frame,
                                    text=self.upper_expression, 
                                    anchor=tk.E, bg=LIGHT_GRAY, 
                                    fg=GRAY, font=SMALL_FONT_STYLE)
		up_label.pack(expand=True, fill='both')
		
		low_label = tk.Label(self.display_frame, 
                                     text=self.lower_expression,
                                     anchor=tk.E, bg=LIGHT_GRAY,  
                                     fg=LABEL_COLOR, font=LARGE_FONT_STYLE)
		low_label.pack(expand=True, fill='both')
		
		low_label.config(text="0")
		
		return up_label, low_label
	
	def create_display_frame(self):
		frame = tk.Frame(self.window,bg=LIGHT_GRAY)
		frame.pack(expand=True, fill='both')
		return frame
	
	def add_to_expression(self, value):
		if len(self.lower_expression) <= MAX_LEN:
			self.lower_expression += str(value)
			self.update_lower_label()
	
	def create_digit_buttons(self):
		for digit, grid_value in self.digits.items():
			button = tk.Button(self.buttons_frame,
                                           text=str(digit),bg=WHITE, 
                                           fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, boderwidth=0,
                                           command=lambda x=digit: self.add_to_expression(x))
			button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
	
	def create_operator_buttons(self):		
		i = 0
		for operator, symbol in self.operations.items():
			button = tk.Button(self.buttons_frame,
                                           text=symbol,bg=OFF_WHITE, fg=BLUE, 
                                           font=DEFAULT_FONT_STYLE, borderwidth=0,
                                           command=lambda x=operator: self.add_to_expression(x))
			button.grid(row=i, column=4, sticky=tk.NSEW)
			i+=1
	
	def create_parentheses_buttons(self):
		i = 2
		for el in ["(", ")"]:
			button = tk.Button(self.buttons_frame,
                                           text=el, bg=OFF_WHITE, 
                                           fg=BLUE, font=DEFAULT_FONT_STYLE, borderwidth=0,  
                                           command=lambda x=el:self.add_to_expression(x))
			button.grid(row=0, column=i, sticky=tk.NSEW)				
			i += 1
					
	def clear(self):
		self.upper_expression = ""
		self.lower_expression = ""
		self.update_lower_label()
		self.update_upper_label()
	
	def create_clear_button(self):
		button = tk.Button(self.buttons_frame, 
                                   text="C", bg=OFF_WHITE, 
                                   fg=BLUE, font=DEFAULT_FONT_STYLE,
                                   borderwidth=0, command=self.clear)
		button.grid(row=0, column=1, sticky=tk.NSEW)
	
	def evaluate(self):
		self.upper_expression = self.lower_expression
		exp = self.lower_expression
		if ("sin" in exp) or ("cos" in exp) or \
                   ("tan" in exp) or ("cot" in exp) or ("sqrt" in exp):
			self.add_to_expression(")")
		try:
			value = round(eval(self.lower_expression), 5)
			value = int(value) if value == int(value) else value #1.0 changes to 1
			self.lower_expression = str(value)
		except:
			self.lower_expression = "Error"
		self.update_upper_label()
		self.update_lower_label()
		
	def create_equals_button(self):
		button = tk.Button(self.buttons_frame, text="=", bg=BLUE,
                                   fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                                   borderwidth=0, command=self.evaluate)
		button.grid(row=4, column=4, sticky=tk.NSEW)
	
	def expand(self):
		if self.collapse:
			self.collapse_button.config(text="\u21F2")
			self.collapsible_frame.pack(expand=True, fill="both")
			self.collapse = False
		else:
			self.collapse_button.config(text="\u21F1")
			self.collapsible_frame.forget()
			self.collapse = True
	
	def create_collapsible_button(self):
		button = tk.Button(self.buttons_frame, text="\u21F1", 
                                   bg=OFF_WHITE, fg=BLUE, font=DEFAULT_FONT_STYLE, 
                                   borderwidth=0, command=self.expand)
		button.grid(row=4, column=1, sticky=tk.NSEW)
		return button
	
	def create_buttons_frame(self):
		frame = tk.Frame(self.window, bg=WHITE)
		frame.pack(expand=True, fill='both')
		return frame
	
	def pi(self):
		self.add_to_expression("+"+str(round(pi, 5)))
		self.evaluate()
	
	def create_pi_num_button(self):
		button = tk.Button(self.collapsible_frame, text="π",
                                   bg=OFF_WHITE, fg=BLUE, font=DEFAULT_FONT_STYLE, 
                                   borderwidth=0, command=self.pi)
		button.grid(row=0, column=4, sticky=tk.NSEW)
	
	def create_sqrt_button(self):
		button = tk.Button(self.collapsible_frame, text="\u00B2\u221A",
                                   bg=OFF_WHITE, fg=BLUE,
                                   font=DEFAULT_FONT_STYLE, borderwidth=0, 
                                   command=lambda : self.add_to_expression("sqrt("))
		button.grid(row=0, column=3, sticky=tk.NSEW)
	
	def create_trigonometry_buttons(self):
		trig = ["sin", "cos", "tan", "cot"]
		trig_op = ["sin(", "cos(", "tan(", "cot("]
		for i in range(1, 5):
			button = tk.Button(self.collapsible_frame,
                                           text=trig[i-1],bg=OFF_WHITE,
                                           fg=BLUE, font=TRIG_FONT_STYLE, borderwidth=0,
                                           command=lambda x=trig_op[i-1]: self.add_to_expression (x))
			button.grid(row=1, column=i, sticky=tk.NSEW)
					
	def percent(self):
		try:
			self.lower_expression = str(eval(f"{self.lower_expression}/100"))
		except:
			self.lower_expression = "Error"
		self.update_lower_label()
	
	def create_percent_button(self):
		button= tk.Button(self.collapsible_frame, text="%", 
                                  bg=OFF_WHITE, fg=BLUE, font=DEFAULT_FONT_STYLE, 
                                  borderwidth=0,  command=self.percent)
		button.grid(row=0, column=2, sticky=tk.NSEW)
		
	def square(self):
		try:
			expression = str(eval(f"{self.lower_expression}**2"))
		except:
			expression = "Error"
			
		if len(expression) <= MAX_LEN:
			self.lower_expression = expression
			self.update_lower_label()
	
	def create_square_button(self):
		button = tk.Button(self.collapsible_frame, text=" x\u00b2",
                                   bg=OFF_WHITE, fg=BLUE, 
                                   font=DEFAULT_FONT_STYLE, borderwidth=0,
                                   command=self.square, width=2)
		button.grid(row=0, column=1, sticky=tk.NS)
	
	def create_collapsible_frame(self):
		frame = tk.Frame(self.window,bg=LIGHT_GRAY)
		#frame.pack(expand=True, fill='both')
		return frame
	
	def update_upper_label(self):
		expression = self.upper_expression
		for operator, symbol in self.operations.items():
			expression = expression.replace(operator, symbol)
		expression = expression.replace("sqrt(", "√")
		self.upper_label.config(text=expression)		
	
	def update_lower_label(self):
		expression = self.lower_expression[:MAX_LEN]
		for operator, symbol in self.operations.items():
			expression = expression.replace(operator, symbol)
		expression = expression.replace("sqrt(", "√")
		self.lower_label.config(text=expression)
		#reduce size with length
		if len(expression) > 8:
			self.lower_label.config(font=UPDATE_FONT)
		else:
			self.lower_label.config(font=LARGE_FONT_STYLE)			
						
	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	cal = Calculator()
	cal.run()
