from tkinter import * # type: ignore
from tkinter import messagebox

class BMICalculator(Frame):
    """Main application class for calculating BMI."""

    def __init__(self, master):
        """Initializes the application, sets up the main window, and creates widgets."""
        super().__init__(master)
        self._bmi = '0.0'
        self._bmi_status = ''
        self.grid(sticky=N+S+E+W)
        self._create_widgets()
    
    def _create_widgets(self):
        """Creates all the GUI widgets, including the menu, labels, entries, and buttons."""
        self.grid_columnconfigure(0, minsize=120)
        self.grid_columnconfigure(1, minsize=200)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)
        
        self._main_menu = Menu(self)
        self._sub_menu = Menu(self._main_menu, tearoff=0)
        self.master.configure(menu=self._main_menu) # type: ignore
        
        self._main_menu.add_cascade(label='About program', menu=self._sub_menu)
        self._sub_menu.add_command(label='Help', command=self._help_me)
        self._sub_menu.add_command(label='Exit', command=self.master.destroy)
        
        self._height_label = Label(self, text='Your height (cm):', font=('Calibri', 12), pady=5)
        self._height_label.grid(row=2, column=0, sticky=E, padx=(10, 0))
        self._entry_for_height = Entry(self)
        self._entry_for_height.grid(row=2, column=1, padx=5, sticky=W)
        
        self._mass_label = Label(self, text='Your mass (kg):', font=('Calibri', 12), pady=5)
        self._mass_label.grid(row=3, column=0, sticky=E, padx=(10, 0))
        self._entry_for_mass = Entry(self)
        self._entry_for_mass.grid(row=3, column=1, padx=5, sticky=W)
        
        self._bmi_label = Label(self, text='Your BMI:', font=('Calibri', 12), pady=2)
        self._bmi_label.grid(row=4, column=0, sticky=E, padx=(10, 0))
        self._your_bmi = Label(self, text=self._bmi, font=('Calibri', 12), pady=5)
        self._your_bmi.grid(row=4, column=1, sticky=W, padx=5)
        
        self._status_label = Label(self, text='Your BMI status:', font=('Calibri', 12), pady=5)
        self._status_label.grid(row=5, column=0, sticky=E, padx=(10, 0))
        self._your_bmi_status = Label(self, pady=5, font=('Calibri', 12))
        self._your_bmi_status.grid(row=5, column=1, sticky=W, padx=5)
        
        self._calculate_button = Button(self, text='Calculate!', font=('Calibri', 12), command=self._calculate)
        self._calculate_button.grid(row=6, column=0, padx=5, sticky=E, pady=5)
        
        self._reset_button = Button(self, text='Reset', font=('Calibri', 12), command=self._reset)
        self._reset_button.grid(row=6, column=1, padx=40, sticky=W, pady=5)
        
    def _calculate(self):
        """Calculates BMI based on user input and updates the display."""
        user_height = self._entry_for_height.get().replace(',', '.')
        user_mass = self._entry_for_mass.get().replace(',', '.')
        
        if not user_height or not user_mass:
            messagebox.showerror('Input error!', "You can't leave a blank in any field!")
            return
        
        try:
            user_height = float(user_height) / 100
            user_mass = float(user_mass)
            user_bmi = round(user_mass / user_height ** 2, 2)
            
            self._your_bmi['text'] = user_bmi
            
            if user_bmi < 16:
                self._your_bmi_status['text'] = 'Starvation < 16'
            elif user_bmi < 17:
                self._your_bmi_status['text'] = 'Emaciation [16,17)'
            elif user_bmi < 18.5:
                self._your_bmi_status['text'] = 'Underweight [17,18.5)'
            elif user_bmi < 25:
                self._your_bmi_status['text'] = 'Optimum [18.5,25)'
            elif user_bmi < 30:
                self._your_bmi_status['text'] = 'Overweight [25,30)'
            else:
                self._your_bmi_status['text'] = 'Obesity 30 ≤'
        except ValueError:
            messagebox.showerror('Input error!', 'Input must be numbers!')
    
    def _help_me(self):
        """Displays a help message with instructions on how to use the application."""
        messagebox.showinfo('Help!', "First, enter your height and mass, then click on the 'Calculate!' button to check your BMI!")
    
    def _reset(self):
        """Resets the input fields and clears the BMI and status display."""
        self._entry_for_height.delete(0, END)
        self._entry_for_mass.delete(0, END)
        self._your_bmi['text'] = self._bmi
        self._your_bmi_status['text'] = self._bmi_status

if __name__ == "__main__":
    root = Tk()
    root.title('BMI Calculator')
    root.geometry('300x200')
    root.resizable(False, False)
    calculator = BMICalculator(root)
    calculator.pack(padx=10, pady=10, fill=BOTH, expand=True)
    root.mainloop()