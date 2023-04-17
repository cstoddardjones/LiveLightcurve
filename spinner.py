import customtkinter as tk

class IntSpinbox(tk.CTkFrame):
    def __init__(self, master=None, min_val=None, max_val=None, init_val=None, interval=None, unit=None, **kwargs):
        # initialize the Frame widget
        tk.CTkFrame.__init__(self, master, **kwargs)

        self.interval = interval
        
        # create the Entry widget
        self.int_var = tk.IntVar()
        entry = tk.CTkEntry(self, validate='key', validatecommand=(self.register(self.validate_input), '%P'), width=60)
        if init_val is not None:
            self.int_var.set(init_val)
        entry.configure(textvariable=self.int_var)
        entry.pack(side='left')

        



        # create the increment and decrement buttons
        increment_button = tk.CTkButton(self, text='+', command=self.increment_value, width=10)
        decrement_button = tk.CTkButton(self, text='-', command=self.decrement_value, width=10)
        increment_button.pack(side='right')
        decrement_button.pack(side='right', padx=2)
        
        # add units after entry box
        unit_label = tk.CTkLabel(self, text=unit)
        unit_label.pack(side='right', padx=4)

        # set the minimum and maximum values if specified
        if min_val is not None:
            self.min_val = min_val
        if max_val is not None:
            self.max_val = max_val

    def increment_value(self):
        value = self.int_var.get()
        if hasattr(self, 'max_val') and value < self.max_val:
            self.int_var.set(value + self.interval)

    def decrement_value(self):
        value = self.int_var.get()
        if hasattr(self, 'min_val') and value > self.min_val:
            self.int_var.set(value - self.interval)

    def validate_input(self, new_value):
        if new_value == '':
            return True
        try:
            value = int(new_value)
            if hasattr(self, 'max_val') and value > self.max_val:
                return False
            if hasattr(self, 'min_val') and value < self.min_val:
                return False
            return True
        except ValueError:
            return False
    
    def get(self):
        return self.int_var.get()