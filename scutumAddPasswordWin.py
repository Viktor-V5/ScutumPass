from Functions import cryptographicfunctions, database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE
import tkinter as tk
import datetime
from tkinter import filedialog, messagebox
from scutumPassMainFunctionalities.passwordGeneratorWin import PasswordGeneratorWindow
from Classes.Accounts import (
    ContainerRow,
    ContainerRowContainer
)



class ScutumAddPasswordWindow(BaseWindow):

    def __init__(self, master, loaded_image,password_list_widget,clipboard_manager):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image
        
        self.master_widget = master
        self.clipboard_manager = clipboard_manager
        self.password_list_widget = password_list_widget

        session = ContainerRowContainer.get_session()


        if session is None:
            self.destroy()
            return

        self.db_location = session.db_location
        self.key_bytes = session.key_bytes

        self.group_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.pass_var = tk.StringVar()


        self.created_at = None
        
        self.master_widget.withdraw()

        self.create_widgets()

    def password_generator_program(self):
        password_generator_win = PasswordGeneratorWindow(self,self.loaded_image,self.clipboard_manager)
        password_generator_win.grab_set()

    def add_password(self):


        string_group = self.group_var.get()

        string_title = self.title_var.get()
        string_password = self.pass_var.get()
        string_email = self.email_var.get()

        self.created_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.edited_at = self.created_at

        try:


            if string_title == "" or string_password == "":
                tk.messagebox.showerror("Error","Password and title are required")
                return

            if string_group == "":
                string_group = "none_group"

            if string_email == "":
                string_email = "none_email"

            if not database.password_name_check(self.db_location,self.key_bytes , string_title):
                tk.messagebox.showerror("Error","This password name row is already used")
                return


            # Vars  


            database.insert_password_row(string_group,string_title,string_email, string_password,self.created_at,self.edited_at,self.db_location,self.key_bytes)
            row = f"{string_group},{string_title},{string_email},{self.created_at},{self.edited_at}"
            

            self.password_list_widget.insert(tk.END,row)

            tk.messagebox.showinfo("Success",f"{string_title} has successfully added")        

        except ValueError and FileNotFoundError as e:

            tk.messagebox.showerror("Error",e)      

    def copy_to_clipboard(self, text, timeout=10):

        if self.clipboard_timer is not None:
            self.after_cancel(self.clipboard_timer)
            self.clipboard_timer = None

        self.clipboard_clear()
        self.clipboard_append(str(text))
        self.update_idletasks()

        self.clipboard_timer = self.after(
            timeout * 1000,
            self.clear_clipboard
        )

    def create_widgets(self):

        tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()


        tk.Label(self,font=(FONT_DEFAULT,8,"bold"),text="Add password row",fg="#818181",bg="white").place(x=45,y=70)


        self.frame_add_password = tk.Frame(self,bg="white")
        self.frame_add_password.place(x=45,y=120)

        tk.Label(self.frame_add_password,font=(FONT_DEFAULT,8),text="*Group:",bg="white").grid(row=0 , column=0)

        self.entry_title = tk.Entry(self.frame_add_password,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.group_var,width=20)
        self.entry_title.grid(row=0 , column=1)


        tk.Label(self.frame_add_password,font=(FONT_DEFAULT,8),text="Name:",bg="white").grid(row=1 , column=0)

        self.entry_title = tk.Entry(self.frame_add_password,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.title_var,width=20)
        self.entry_title.grid(row=1 , column=1)

        tk.Label(self.frame_add_password,font=(FONT_DEFAULT,8),text="*Email:",bg="white").grid(row=2 , column=0)

        self.entry_email = tk.Entry(self.frame_add_password,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.email_var,width=20)
        self.entry_email.grid(row=2 , column=1)

        tk.Label(self.frame_add_password,font=(FONT_DEFAULT,8),text="Password:",bg="white").grid(row=3 , column=0)

        self.entry_pass = tk.Entry(self.frame_add_password,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.pass_var,width=20)
        self.entry_pass.grid(row=3 , column=1)

        tk.Button(self.frame_add_password,font=(FONT_DEFAULT,8),text="Add password",command=self.add_password,width=12).grid(row=4,column=1,pady=10)

        self.button_logo = tk.Button(self,image=self.loaded_image["scutum_pass_img"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",command=self.go_back,bg="#de3800")
        self.button_logo.place(x=otherfunctions.x_center_widget(self.button_logo,400),y=5)

        self.generate_password_button = tk.Button(self.frame_add_password,image=self.loaded_image["random_button"],highlightbackground="white",borderwidth=0,command=self.password_generator_program)
        self.generate_password_button.grid(row=3,column=2,padx=8)