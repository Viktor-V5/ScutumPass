from Functions import cryptographicfunctions, database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow,WINDOW_SIZE
import tkinter as tk
from tkinter import filedialog
import sys
import os
from scutumCreateContainerWin import ScutumCreateContainerWindow
from scutumLoginContainerWin import ScutumLoginContainerWindow
from image_loader import load_loaded_image
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

class Main(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False) 
        self.loaded_image = load_loaded_image()
        
        self.create_widgets()

    def create_widgets(self):

        tk.Label(self,image=self.loaded_image["orange_gui"]).pack()
        tk.Label(self,font=(FONT_DEFAULT,11,"bold"),fg="#818181", text="Scutum pass",bg="white").place(x=45,y=70)
        tk.Label(self,image=self.loaded_image["scutum_pass_img"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",bg="#de3800").place(x=127, y=5)

        button_grid = tk.Frame(self,width=212,bg="white")
        button_grid.place(x=otherfunctions.x_center_widget(button_grid,300), y=120)

        tk.Button(button_grid,image=self.loaded_image["scutum_pass_create_button"],borderwidth=0,bg="white",highlightbackground="white",command=self.create_containter).grid(row=0,column=0,padx=10, pady=10)
        tk.Label(button_grid,text="Create container",font=(FONT_DEFAULT,8),bg="white").grid(row=1,column=0)

        tk.Button(button_grid,image=self.loaded_image["scutum_pass_open_button"],borderwidth=0,bg="white",highlightbackground="white",command=self.login_container).grid(row=0,column=1,padx=10, pady=10)
        tk.Label(button_grid,text="Open container",font=(FONT_DEFAULT,8),bg="white").grid(row=1,column=1)

    def login_container(self):
        scutum_login = ScutumLoginContainerWindow(self,self.loaded_image)
        scutum_login.grab_set()

    def create_containter(self):
        scutum_create = ScutumCreateContainerWindow(self,self.loaded_image)
        scutum_create.grab_set()

if __name__ == "__main__":
    app = Main()
    app.mainloop()