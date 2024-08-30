import random
import string
from tkinter import *
from tkinter import messagebox

class PasswordGenerator(Frame):
    """Application class for generating random passwords with various options."""
    
    def __init__(self, master):
        """Initializes the application, sets up the main window, and creates widgets."""
        super().__init__(master)
        self.grid(padx=20, pady=20)
        self._password_length = IntVar(value=18)
        self._include_symbols = BooleanVar(value=True)
        self._include_numbers = BooleanVar(value=True)
        self._include_lowercase = BooleanVar(value=True)
        self._include_uppercase = BooleanVar(value=True)
        self._no_similar_chars = BooleanVar(value=False)
        self._no_duplicate_chars = BooleanVar(value=False)
        self._no_sequential_chars = BooleanVar(value=False)
        self._create_widgets()
        self._generate_passwords()

    def _create_widgets(self):
        """Creates all the GUI widgets, including labels, buttons, checkboxes, and text areas."""
        Label(self, text="Generated Password:", font=("Calibri", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        self._password_display = Entry(self, font=("Calibri", 14), width=35, bd=2, justify="center", state="readonly")
        self._password_display.grid(row=1, column=0, columnspan=2, pady=5)
        
        button_frame = Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="Generate", width=10, command=self._generate_passwords).pack(side=LEFT, padx=10)
        Button(button_frame, text="Copy All", width=10, command=self._copy_password).pack(side=LEFT, padx=10)
        
        Label(self, text="Password Length:").grid(row=3, column=0, sticky=E, padx=10, pady=5)
        self._length_scrollbar = Scale(self, from_=6, to=30, orient=HORIZONTAL, variable=self._password_length, command=self._generate_passwords, length=230)
        self._length_scrollbar.grid(row=3, column=1, sticky=W, padx=10, pady=5)

        Checkbutton(self, text="Include Symbols", variable=self._include_symbols, command=self._generate_passwords).grid(row=4, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="Include Numbers", variable=self._include_numbers, command=self._generate_passwords).grid(row=5, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="Include Lowercase Characters", variable=self._include_lowercase, command=self._generate_passwords).grid(row=6, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="Include Uppercase Characters", variable=self._include_uppercase, command=self._generate_passwords).grid(row=7, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="No Similar Characters", variable=self._no_similar_chars, command=self._generate_passwords).grid(row=8, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="No Duplicate Characters", variable=self._no_duplicate_chars, command=self._generate_passwords).grid(row=9, column=0, columnspan=2, sticky=W, padx=20)
        Checkbutton(self, text="No Sequential Characters", variable=self._no_sequential_chars, command=self._generate_passwords).grid(row=10, column=0, columnspan=2, sticky=W, padx=20)

    def _generate_passwords(self, event=None):
        """Generates a password based on user options and displays it."""
        password = self._generate_password()
        self._password_display.config(state=NORMAL)
        self._password_display.delete(0, END)
        self._password_display.insert(0, password)
        self._password_display.config(state="readonly")

    def _generate_password(self):
        """Generates a single password based on user options."""
        length = self._password_length.get()
        characters = ''
        
        if self._include_lowercase.get():
            characters += string.ascii_lowercase
        if self._include_uppercase.get():
            characters += string.ascii_uppercase
        if self._include_numbers.get():
            characters += string.digits
        if self._include_symbols.get():
            characters += string.punctuation
        if self._no_similar_chars.get():
            characters = characters.translate({ord(i): None for i in 'il1LoO0'})
        if not characters:
            return "No character sets selected!"

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def _copy_password(self):
        """Copies the generated password to the clipboard."""
        password = self._password_display.get()
        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Copied", "Password has been copied to clipboard.")

if __name__ == "__main__":
    root = Tk()
    root.title("Password Generator")
    root.geometry("420x375")
    root.resizable(False, False)
    app = PasswordGenerator(root)
    app.pack()
    root.mainloop()