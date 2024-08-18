"""
If you encounter issues logging in with your real email, it may be due to security settings in your email account.
Specifically, if you use a Google account and have 2-step verification enabled, you will need to use an app-specific password.
For more information on how to create an app-specific password, visit:
https://support.google.com/accounts/answer/185833?hl=pl
"""

import os
import re
import smtplib
import mimetypes
from tkinter import *  # type: ignore
from email import encoders # type: ignore
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from tkinter import messagebox, filedialog
from email.mime.multipart import MIMEMultipart

class EmailApp(Frame):
    """
    Main application class for email login and sending functionality.
    """

    _trials = 0

    def __init__(self, master):
        """Initializes the application, sets up the main window, and creates widgets."""
        super().__init__(master)
        self._server = None
        self._username = None
        self._password = None
        self._attachment_path = None
        self._create_widgets()
        self.grid(sticky='nsew')
        self._show_login()

    def _create_widgets(self):
        """Creates all the GUI widgets for both login and email sending views."""
        self._main_menu = Menu(self)
        self._sub_menu = Menu(self._main_menu, tearoff=0)
        self.master.config(menu=self._main_menu)  # type: ignore
        self._main_menu.add_cascade(label='About program', menu=self._sub_menu)
        self._sub_menu.add_command(label='Help', command=self._help_me)
        self._sub_menu.add_command(label='Exit', command=self.master.destroy)

        self._login_widgets = Frame(self, bg='#f0f0f0', padx=20, pady=20)
        self._login_widgets.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self._welcome_label = Label(self._login_widgets, text='Enter your email and password:', font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self._welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

        self._enter_your_email = Label(self._login_widgets, text='Email:', font=('Arial', 12), bg='#f0f0f0')
        self._enter_your_email.grid(row=1, column=0, sticky=E, pady=5)

        self._entry_for_email = Entry(self._login_widgets, width=35)
        self._entry_for_email.grid(row=1, column=1, pady=5, padx=(0, 10))

        self._enter_your_password = Label(self._login_widgets, text='Password:', font=('Arial', 12), bg='#f0f0f0')
        self._enter_your_password.grid(row=2, column=0, sticky=E, pady=5)

        self._entry_for_password = Entry(self._login_widgets, show='*', width=35)
        self._entry_for_password.grid(row=2, column=1, pady=5, padx=(0, 10))

        self._show_password_var = BooleanVar()
        self._show_password_check = Checkbutton(self._login_widgets, text='Show password',variable=self._show_password_var, command=self._toggle_password_visibility, bg='#f0f0f0')
        self._show_password_check.grid(row=3, column=1, pady=5, padx=(0, 10), sticky=W)

        self._login_button = Button(self._login_widgets, text='Login', font=('Arial', 14, 'bold'), bg='#007bff', fg='white', command=self._login)
        self._login_button.grid(row=4, column=0, columnspan=2, pady=10)

        self._email_widgets = Frame(self, bg='#f0f0f0', padx=20, pady=20)
        self._email_widgets.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._email_widgets.grid_forget()

        self._logout_button = Button(self._email_widgets, text='Logout', bg='#dc3545', fg='white', command=self._logout)
        self._logout_button.grid(row=0, column=2, sticky=E, pady=10, padx=(5, 0))

        self._new_email_label = Label(self._email_widgets, text="Creating new email:", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self._new_email_label.grid(row=0, column=0, columnspan=3, pady=10)

        self._recipients_email_label = Label(self._email_widgets, text="Recipient's email:", bg='#f0f0f0')
        self._recipients_email_label.grid(row=1, column=0, sticky=E, pady=5)

        self._entry_for_recipients_email = Entry(self._email_widgets)
        self._entry_for_recipients_email.grid(row=1, column=1, columnspan=2, pady=5, padx=(0, 10), sticky='ew')

        self._email_subject_label = Label(self._email_widgets, text="Email subject:", bg='#f0f0f0')
        self._email_subject_label.grid(row=2, column=0, sticky=E, pady=5)

        self._entry_for_email_subject = Entry(self._email_widgets)
        self._entry_for_email_subject.grid(row=2, column=1, columnspan=2, pady=5, padx=(0, 10), sticky='ew')

        self._email_message_label = Label(self._email_widgets, text="Email message:", bg='#f0f0f0')
        self._email_message_label.grid(row=3, column=0, sticky=E, pady=5)

        self._text_frame = Frame(self._email_widgets)
        self._text_frame.grid(row=3, column=1, columnspan=2, pady=5, padx=(0, 10), sticky='nsew')

        self._entry_for_email_message = Text(self._text_frame, wrap='word', height=10)
        self._entry_for_email_message.pack(side=LEFT, fill=BOTH, expand=True)

        self._attach_file_button = Button(self._email_widgets, text='Attach File', command=self._attach_file)
        self._attach_file_button.grid(row=4, column=0, pady=5, padx=(0, 10))

        self._file_label = Label(self._email_widgets, text='No file selected', bg='#f0f0f0')
        self._file_label.grid(row=4, column=1, columnspan=2, pady=5, padx=(0, 10), sticky=W)

        self._reset_button = Button(self._email_widgets, text='Reset', bg='#ffc107', fg='white', command=self._reset_fields)
        self._reset_button.grid(row=5, column=1, pady=10,padx=(5, 5), sticky='e')

        self._send_email_button = Button(self._email_widgets, text='Send email!', bg='#28a745', fg='white', command=self._send_email)
        self._send_email_button.grid(row=5, column=2, pady=10, padx=(5, 5), sticky='w')

        self._message_label = Label(self._email_widgets, font=('Arial', 14), bg='#f0f0f0')
        self._message_label.grid(row=6, column=0, columnspan=3, pady=5)

        self._email_widgets.grid_columnconfigure(0, weight=1)
        self._email_widgets.grid_columnconfigure(1, weight=0)
        self._email_widgets.grid_columnconfigure(2, weight=1)
        self._email_widgets.grid_rowconfigure(4, weight=1)
        self._email_widgets.grid_rowconfigure(5, weight=0)

    def _toggle_password_visibility(self):
        """Toggles the visibility of the password."""
        if self._show_password_var.get():
            self._entry_for_password.config(show='')
        else:
            self._entry_for_password.config(show='*')

    def _attach_file(self):
        """Opens a file dialog to select a file and updates the file path."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self._attachment_path = file_path
            self._file_label.config(text=file_path.split('/')[-1])

    def _show_login(self):
        """Shows the login widgets and hides the email sending widgets."""
        self._login_widgets.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._email_widgets.grid_forget()

    def _show_email(self):
        """Shows the email sending widgets and hides the login widgets."""
        self._login_widgets.grid_forget()
        self._email_widgets.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def _help_me(self):
        """Displays a help message, informing the user how to use the application."""
        if not self._username:
            messagebox.showinfo('Help!', "To send an email you must:\n1) Log in using your real email and password.\n2) Fill in all fields.\n3) Provide a valid recipient's email.\n4) Click 'Send email!'")
        else:
            messagebox.showinfo('Help!', "Click 'Send email!' to send the email.")

    def _login_verification(self):
        """Verifies the login credentials."""
        email = self._entry_for_email.get()
        password = self._entry_for_password.get()

        if not email or not password:
            messagebox.showerror('Login error!', "You can't leave any field blank!")
            return False

        if not re.match(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$', email):
            messagebox.showerror('Login error!', 'Enter a valid email!')
            return False

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            server.quit()
            return True
        except Exception:
            messagebox.showerror('Login error!', 'Enter a valid password!')
            return False

    def _login(self):
        """Handles user login and switches to email sending interface if successful."""
        EmailApp._trials += 1
        if self._login_verification():
            self._username = self._entry_for_email.get()
            self._password = self._entry_for_password.get()
            try:
                self._server = smtplib.SMTP('smtp.gmail.com', 587)
                self._server.starttls()
                self._server.login(self._username, self._password)
                self._show_email()
                self.master.update_idletasks()
                self.master.geometry(f'{self._email_widgets.winfo_reqwidth()}x{self._email_widgets.winfo_reqheight()}')  # type: ignore
                self.master.resizable(False, False)  # type: ignore
            except Exception as e:
                messagebox.showerror('Login error!', f'Failed to log in: {str(e)}')
        else:
            if EmailApp._trials >= 2:
                messagebox.showinfo('Help message!', "If you entered your real email and can't log in, make sure to use an app-specific password.\nFor more info, visit:\nhttps://support.google.com/accounts/answer/185833?hl=pl")
                EmailApp._trials = 0

    def _message_verification(self):
        """Verifies the email message fields."""
        recipient_email = self._entry_for_recipients_email.get()
        subject_text = self._entry_for_email_subject.get()
        message_text = self._entry_for_email_message.get("1.0", END).strip()

        if not recipient_email or not subject_text or not message_text:
            messagebox.showerror('Email error!', "You can't leave any field blank!")
            return False

        if not re.match(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$', recipient_email):
            messagebox.showerror('Email error!', "Check the recipient's email address again!")
            return False

        return True

    def _logout(self):
        """Logs out the user and returns to the login screen."""
        try:
            if self._server:
                self._server.quit()
            self._show_login()
            self._entry_for_email.delete(0, END)
            self._entry_for_password.delete(0, END)
            self.master.geometry('400x400')  # type: ignore
            self.master.resizable(False, False)  # type: ignore
        except Exception as e:
            messagebox.showerror('Logout error!', f'Error occurred while logging out: {str(e)}')

    def _reset_fields(self):
        """Resets the recipient email, subject, and message fields."""
        self._entry_for_recipients_email.delete(0, END)
        self._entry_for_email_subject.delete(0, END)
        self._entry_for_email_message.delete("1.0", END)
        self._file_label.config(text='No file selected')
        self._attachment_path = None
        self._message_label.config(text='')

    def _send_email(self):
        """Sends an email if all fields are valid."""
        if self._message_verification():
            recipient = self._entry_for_recipients_email.get()
            subject = self._entry_for_email_subject.get()
            message_content = self._entry_for_email_message.get("1.0", END)
            msg = MIMEMultipart()
            msg['From'] = self._username  # type: ignore
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message_content, 'plain'))
            if self._attachment_path:
                try:
                    mime_type, _ = mimetypes.guess_type(self._attachment_path)
                    if mime_type is None:
                        mime_type = 'application/octet-stream'
                    maintype, subtype = mime_type.split('/', 1)
                    with open(self._attachment_path, 'rb') as attachment:
                        part = MIMEBase(maintype, subtype)
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        filename = os.path.basename(self._attachment_path)
                        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                        msg.attach(part)
                except Exception as e:
                    messagebox.showerror('Attachment error!', f'Error attaching file: {str(e)}')
                    return
            try:
                self._server.send_message(msg)  # type: ignore
                self._message_label.config(text='Email sent!', fg='green')
            except Exception as e:
                messagebox.showerror('Sending error!', f'Error sending email: {str(e)}')

if __name__ == "__main__":
    root = Tk()
    root.title('Email Sender App')
    root.geometry('400x400')
    root.resizable(False, False)
    app = EmailApp(root)
    root.mainloop()