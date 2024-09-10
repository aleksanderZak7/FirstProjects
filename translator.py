"""
How to run the Text Translator:

This program translates text using the DeepL API, https://www.deepl.com/pl/pro-api.

Usage:
  python translator.py <api_key>

Options:
  <api_key>  (required) DeepL API key for authentication.

Example:
  python translator.py your_deepl_api_key
"""

import deepl
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

class TranslatorApp(tk.Frame):
    """Main application class for translating text using DeepL."""

    def __init__(self, master, api_key):
        """Initializes the application, sets up the main window, and creates widgets."""
        super().__init__(master)
        self.grid()
        self._language_dict = {"English": "EN", "Dutch": "NL", "French": "FR", "German": "DE", "Italian": "IT", "Japanese": "JA", "Polish": "PL", "Russian": "RU", "Spanish": "ES", "Chinese": "ZH"}
        self._previous_source_lang = "English"
        self._previous_target_lang = "Polish"
        self._create_widgets()
        self._translator = deepl.Translator(api_key)

    def _create_widgets(self):
        """Creates all the GUI widgets."""
        self._main_menu = tk.Menu(self)
        self.master.config(menu=self._main_menu)  # type: ignore

        self._file_menu = tk.Menu(self._main_menu, tearoff=0)
        self._main_menu.add_cascade(label="File", menu=self._file_menu)
        self._file_menu.add_command(label="Open File", command=self._open_file)
        self._file_menu.add_command(label="Save Translation", command=self._save_translation)
        self._file_menu.add_command(label="Exit", command=self.master.destroy)

        self._about_menu = tk.Menu(self._main_menu, tearoff=0)
        self._main_menu.add_cascade(label="Help", menu=self._about_menu)
        self._about_menu.add_command(label="Help", command=self._show_help)

        lang_frame = tk.Frame(self)
        lang_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        
        self._source_lang_var = tk.StringVar(value=self._previous_source_lang)
        self._source_lang_menu = tk.OptionMenu(lang_frame, self._source_lang_var, *sorted(self._language_dict.keys()), command=self._handle_language_change)
        self._source_lang_menu.config(width=15, bg='lightgray')
        self._source_lang_menu.grid(row=0, column=0, padx=5)

        self._switch_button = tk.Button(lang_frame, text="↔", font=("Calibri", 16), command=self._swap_languages, bg='lightblue', width=6)
        self._switch_button.grid(row=0, column=1, padx=5)

        self._target_lang_var = tk.StringVar(value=self._previous_target_lang)
        self._target_lang_menu = tk.OptionMenu(lang_frame, self._target_lang_var, *sorted(self._language_dict.keys()), command=self._handle_language_change)
        self._target_lang_menu.config(width=15, bg='lightgray')
        self._target_lang_menu.grid(row=0, column=2, padx=5)

        self._text_input = tk.Text(self, height=12, width=45)
        self._text_input.grid(row=1, column=0, padx=(15, 5), pady=(10, 15))

        self._text_output = tk.Text(self, height=12, width=45)
        self._text_output.grid(row=1, column=1, padx=(5, 15), pady=(10, 15))

        self._translate_button = tk.Button(self, text="Translate", font=("Calibri", 14), command=self._translate_text, bg='lightblue')
        self._translate_button.grid(row=2, column=0, columnspan=2, pady=(5, 10))

    def _open_file(self):
        """Opens a *.txt file and loads its content into the text input field."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()
                self._text_input.delete("1.0", tk.END)
                self._text_input.insert(tk.END, file_content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def _handle_language_change(self, *_):
        """Checks if both languages are the same and swaps them if necessary."""
        source_lang = self._source_lang_var.get()
        target_lang = self._target_lang_var.get()

        if source_lang == target_lang:
            self._source_lang_var.set(self._previous_source_lang)
            self._target_lang_var.set(self._previous_target_lang)
            self._swap_languages()
        else:
            self._previous_source_lang = source_lang
            self._previous_target_lang = target_lang

    def _swap_languages(self):
        """Swaps the source and target languages and updates text fields."""
        self._source_lang_var.set(self._previous_target_lang)
        self._target_lang_var.set(self._previous_source_lang)
        self._previous_source_lang = self._source_lang_var.get()
        self._previous_target_lang = self._target_lang_var.get()

        input_text = self._text_input.get("1.0", tk.END).strip()
        output_text = self._text_output.get("1.0", tk.END).strip()

        self._text_input.delete("1.0", tk.END)
        self._text_output.delete("1.0", tk.END)
        self._text_input.insert(tk.END, output_text)
        self._text_output.insert(tk.END, input_text)

    def _translate_text(self):
        """Translates the input text using DeepL."""
        text = self._text_input.get("1.0", tk.END).strip()
        source_lang_code = self._language_dict.get(self._source_lang_var.get())
        target_lang_code = self._language_dict.get(self._target_lang_var.get())
        
        if target_lang_code == "EN":
            target_lang_code = "EN-US"

        if not text:
            messagebox.showwarning("Error", "The text input field cannot be empty.")
            return

        try:
            result = self._translator.translate_text(text, source_lang=source_lang_code, target_lang=target_lang_code) # type: ignore
            translated_text = result.text  # type: ignore
            self._text_output.delete("1.0", tk.END)
            self._text_output.insert(tk.END, translated_text)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

    def _save_translation(self):
        """Saves the translated text to a .txt file."""
        translated_text = self._text_output.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning("Error", "No translated text to save.")
            return

        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            with open(file.name, "w", encoding="utf-8") as f:
                f.write(translated_text)
            messagebox.showinfo("Success", f"Translated text saved to:\n{file.name}")

    def _show_help(self):
        """Displays a help message."""
        messagebox.showinfo("Help", "Enter text, select languages, and click 'Translate' to get the translation.")

def main():
    parser = argparse.ArgumentParser(description='Translate text using DeepL.')
    parser.add_argument('api_key', help='DeepL API key for authentication.')
    args = parser.parse_args()

    root = tk.Tk()
    root.title("Text Translator")
    root.geometry("800x360")
    root.resizable(False, False)
    app = TranslatorApp(root, args.api_key)
    app.pack(padx=10, pady=10)
    root.mainloop()

if __name__ == '__main__':
    main()