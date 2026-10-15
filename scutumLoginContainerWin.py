import os
import sys
import sqlite3
from Functions import cryptographicfunctions, database
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE
import tkinter as tk
from tkinter import filedialog, messagebox
from scutumMainMenuWin import ScutumMainMenuWindow
from Classes.Accounts import (
    ContainerRow,
    ContainerRowContainer
)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


class ScutumLoginContainerWindow(BaseWindow):

    def __init__(self, master, loaded_image):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image

        self.container_path = tk.StringVar()
        self.container_key_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):

        try:
            self.hide()
            
            tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()
            tk.Label(self,font=(FONT_DEFAULT,11,"bold"),fg="#818181", text="Open vault",bg="white").place(x=45,y=70)


            frame_login = tk.Frame(self,bg="white")
            frame_login.place(x=45,y=110)

            tk.Label(frame_login,font=(FONT_DEFAULT,8), text="Name: ",bg="white").grid(row=0, column=0)

            container_entry = tk.Entry(frame_login,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.container_path)
            container_entry.grid(row=0, column=1)

            tk.Button(frame_login,image=self.loaded_image["open_folder_icon"],highlightbackground="white",borderwidth=0,bg="white",command=self.select_container_file).grid(row=0,column=2,padx=5)
        
            tk.Label(frame_login,font=(FONT_DEFAULT,8), text="Key: ",bg="white").grid(row=1, column=0)

            key_entry = tk.Entry(frame_login,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT,8),textvariable=self.container_key_path)
            key_entry.grid(row=1, column=1)

            tk.Button(frame_login,
            image=self.loaded_image["open_folder_icon"],
            highlightbackground="white",
            borderwidth=0,
            bg="white",
            command=self.select_key_file
            ).grid(row=1,column=2,padx=5)

            tk.Button(frame_login,
            font=(FONT_DEFAULT,8),
            text="Open",
            width=10,
            command=self.unlock_container
            ).grid(row=2,column=1)

            tk.Button(self,
            image=self.loaded_image["scutum_pass_img"],
            highlightbackground="#de3800"
            ,borderwidth=0,
            activebackground="#de3800",
            command=self.go_back,
            bg="#de3800"
            ).place(x=177,y=5)

        except Exception as e:
            tk.messagebox.showerror("Error",e)

    def unlock_container(self):

        container_db = os.path.basename(f"{self.container_path.get()}")
        container_path = self.container_path.get()
        container_key_path = self.container_key_path.get()

        if not container_path or not container_key_path:
            tk.messagebox.showerror("Error", "All fields are required")
            return

        try:
            key = cryptographicfunctions.get_key(container_key_path)

            with cryptographicfunctions.SecureKey(key) as db_key:
                db_key_bytes = db_key.get()

                try:

                    database.select_db_data(container_path, db_key_bytes)

                except sqlite3.DatabaseError:
                    tk.messagebox.showerror(
                        "Wrong Key",
                        "The encryption key is incorrect or the database is corrupted."
                    )
                    return

                result = ContainerRow(
                    db_location=container_path,
                    key_bytes=db_key_bytes
                )

                if isinstance(result, ContainerRow):
                    ContainerRowContainer.set_session(result)

                parent = self.master
                loaded_image = self.loaded_image

                self.destroy()

                ScutumMainMenuWindow(parent, loaded_image)

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))


    def select_key_file(self):

        continer_key_file = tk.filedialog.askopenfilename(defaultextension =".key",initialdir='/',filetypes=[("Key file","*.key")])
        self.container_key_path.set(continer_key_file)

    def select_container_file(self):

        continer_file = filedialog.askopenfilename(defaultextension =".db",initialdir='/',filetypes=[("database file","*.db")])
        self.container_path.set(continer_file)
