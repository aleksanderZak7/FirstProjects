import PyPDF2
from tkinter import * # type: ignore
from tkinter import filedialog
from tkinter import messagebox

class PDFConverterApp(Frame):
    """Main application class for converting PDF files to text.
    
    Inherits from the Frame class from tkinter, creating a GUI interface
    for selecting a PDF file, converting it to text, and saving the result.
    """
    def __init__(self, master):
        """Initializes the application, sets up the main window, and creates widgets."""
        super().__init__(master)
        self.grid()
        self._pdf_file_path = None
        self._create_widgets()

    def _create_widgets(self):
        """Creates all the GUI widgets, including the menu, buttons, and labels."""
        self._main_menu = Menu(self)
        self._file_menu = Menu(self._main_menu, tearoff=0)
        self._about_menu = Menu(self._main_menu, tearoff=0)
        self.master.config(menu=self._main_menu)  # type: ignore
        self._main_menu.add_cascade(label="File", menu=self._file_menu)
        self._file_menu.add_command(label="Open", command=self._pick_pdf_file)
        self._file_menu.add_command(label="Exit", command=self.master.destroy)

        self._main_menu.add_cascade(label="About", menu=self._about_menu)
        self._about_menu.add_command(label="Help", command=self._help_me)

        self._welcome_label = Label(self, text="Convert PDF to Text:", font=("Calibri", 14, "bold"), pady=5)
        self._welcome_label.grid(row=0, pady=(0, 5), padx=10)

        self._choose_file_button = Button(self, text="Choose PDF File", font=("Calibri", 12), pady=5, padx=10, command=self._pick_pdf_file)
        self._choose_file_button.grid(row=1, pady=(0, 5))

        self._pdf_file_label = Label(self, text="", font=("Calibri", 8), anchor="w", wraplength=300, padx=5)
        self._pdf_file_label.grid(row=2, pady=(0, 5), padx=10)

        self._change_button = Button(self, text="Convert to Text", font=("Calibri", 12), pady=5, padx=10, command=self._change_format)
        self._change_button.grid(row=3, pady=(0, 5))

    def _pick_pdf_file(self):
        """Allows the user to select a PDF file using a file dialog."""
        file = filedialog.askopenfile(parent=self.master, mode="rb", title="Choose a PDF file:", filetypes=[("PDF Files", "*.pdf")])
        if file:
            self._pdf_file_path = file.name
            self._pdf_file_label.config(text=f"Selected: {self._pdf_file_path}", wraplength=300)
            file.close()

    def _help_me(self):
        """Displays a help message, informing the user how to use the application."""
        if not self._pdf_file_path:
            messagebox.showinfo("Help", "Please select a PDF file first using File -> Open or the 'Choose PDF File' button.")
        else:
            messagebox.showinfo("Help", "Click 'Convert to Text' to convert the selected PDF file into a text file.")

    def _change_format(self):
        """Converts the selected PDF file to a text file and saves the result."""
        if not self._pdf_file_path:
            messagebox.showerror("File Error", "Please select a PDF file first!")
            return

        try:
            with open(self._pdf_file_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                extracted_text = "".join(page.extract_text() for page in pdf_reader.pages)

            txt_file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("Microsoft Word", "*.doc"), ("OpenDocument", "*.odt"), ("All files", ".*")])

            if txt_file:
                with open(txt_file.name, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                messagebox.showinfo("Success!", f"The PDF has been converted to text successfully and saved at:\n{txt_file.name}")
                self._reset()
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while converting the file: {str(e)}")

    def _reset(self):
        """Resets the PDF file path and clears the file label."""
        self._pdf_file_path = None
        self._pdf_file_label.config(text="")

if __name__ == "__main__":
    root = Tk()
    root.title("PDF to Text Converter")
    root.geometry("350x175")
    root.resizable(False, False)
    app = PDFConverterApp(root)
    app.pack(padx=5, pady=5)
    root.mainloop()