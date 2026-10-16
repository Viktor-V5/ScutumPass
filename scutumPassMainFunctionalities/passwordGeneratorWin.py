import os
import os.path
import string
import sys
import math
import secrets
from decimal import Decimal,ROUND_HALF_UP
from Functions import cryptographicfunctions, database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE,PASS_GEN_BUTTONS_FONT_SIZE
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class PasswordGeneratorWindow(BaseWindow):

    def __init__(self, master, loaded_image,clipboard_manager):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image

        self.generated_password_length = tk.IntVar()
        self.password_var = tk.StringVar()

        self.genrated_password_entry = None
        self.clipboard_manager = clipboard_manager
        
        self.chars = set()
        self.pool = []

        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()
        tk.Label(self,font=(FONT_DEFAULT,8,"bold"),text="Generate password",fg="#818181",bg="white").place(x=45,y=70)

        self.label_logo = tk.Label(self,image=self.loaded_image["scutum_pass_img"],activebackground="#de3800",bg="#de3800")
        self.label_logo.place(x=otherfunctions.x_center_widget(self.label_logo,400),y=5)

        self.frame_password_generator = tk.Frame(self,bg="white")
        self.frame_password_generator.place(x=45,y=120)

        self.genrated_password_entry = tk.Entry(self.frame_password_generator,bg="#dddddd",borderwidth=0,font=(FONT_DEFAULT, 10),state="disabled",textvariable=self.password_var,width=35,show="*")
        self.genrated_password_entry.grid(row=0, column=0)

        self.copy_password_button = tk.Button(self.frame_password_generator,image=self.loaded_image["copy_button"],highlightbackground="white",activebackground="white",borderwidth=0,bg="white",state=tk.DISABLED,command=self.copy_password)
        self.copy_password_button.grid(row=0,column=1,padx=2) 

        self.generate_new_password_button = tk.Button(self.frame_password_generator,image=self.loaded_image["random_button"],highlightbackground="white",activebackground="white",borderwidth=0,bg="white",state=tk.DISABLED,command=self.reset_password)
        self.generate_new_password_button.grid(row=0,column=2) 

        tk.Label(self.frame_password_generator,text="",bg="white").grid(row=1, column=0)

        self.frame_password_scale = tk.Frame(self,bg="white")
        self.frame_password_scale.place(x=45,y=150)

        tk.Label(self.frame_password_scale,font=(FONT_DEFAULT,8,"bold"),text="Length:",fg="#818181",bg="white").grid(row=0, column=0)

        self.password_slider = tk.Scale(self.frame_password_scale,from_=0,to=80,orient='horizontal',highlightthickness=0,bg="white",state=tk.DISABLED,variable=self.generated_password_length,command=self.slider_changed)
        self.password_slider.grid(row=0, column=1)

        self.entropy_label = tk.Label(self.frame_password_scale,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),bg="white",fg="red",text="0.0 bits (poor)") 
        self.entropy_label.grid(row=0, column=2,padx=10)
        

        self.frame_symbols = tk.Frame(self,bg="white")
        self.frame_symbols.place(x=45,y=210)

        self.a_z_button = tk.Button(self.frame_symbols,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),highlightbackground="white",text="a-z",bg="white",command=self.select_lower_case_letters)
        self.a_z_button.grid(row=1, column=0)


        self.A_Z_button = tk.Button(self.frame_symbols,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),highlightbackground="white",text="A-Z",bg="white",command=self.select_upper_case_letters)
        self.A_Z_button.grid(row=1, column=1)


        self.digits_button = tk.Button(self.frame_symbols,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),highlightbackground="white",text="0-9",bg="white",command=self.select_digits)
        self.digits_button.grid(row=1, column=2)


        self.punctuation_button = tk.Button(self.frame_symbols,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),highlightbackground="white",text="!#(%.])",bg="white",command=self.select_punctuation)
        self.punctuation_button.grid(row=1, column=3)

        self.reset_character_types = tk.Button(self.frame_symbols,font=(FONT_DEFAULT,PASS_GEN_BUTTONS_FONT_SIZE,"bold"),highlightbackground="white",text="reset",bg="white",command=self.reset_character_types)
        self.reset_character_types.grid(row=1, column=4)

        frame_hide_view_buttons = tk.Frame(self.frame_symbols, bg="white")
        frame_hide_view_buttons.grid(row=1, column=5,padx=5)

        self.view_button = tk.Button(frame_hide_view_buttons, font=(FONT_DEFAULT, 6, "bold"), activebackground="white",
                                         highlightbackground="white", bg="white", text="view", borderwidth=0, command=self.view_id)
        self.view_button.grid(row=0, column=0, sticky="w")
        self.hide_button = tk.Button(frame_hide_view_buttons, font=(FONT_DEFAULT, 6, "bold"), activebackground="white",
                                        highlightbackground="white", bg="white", text="hide", borderwidth=0, state="disabled", command=self.hide_id)
        self.hide_button.grid(row=0, column=1, sticky="w")

    def view_id(self):
        self.genrated_password_entry.config(show="")

        self.hide_button.config(state=tk.NORMAL)
        self.view_button.config(state=tk.DISABLED)

    def hide_id(self):
        self.genrated_password_entry.config(show="*")

        self.hide_button.config(state=tk.DISABLED)
        self.view_button.config(state=tk.NORMAL)

    def update_pool(self):
        self.pool = list(self.chars)

    def select_lower_case_letters(self):


        self.password_slider.config(state=tk.ACTIVE)
        self.genrated_password_entry.config(state="normal")
        self.copy_password_button.config(state=tk.ACTIVE)
        self.generate_new_password_button.config(state=tk.ACTIVE)
        self.a_z_button.config(state=tk.DISABLED)
        self.chars.update(string.ascii_lowercase)
        self.update_pool()

    def select_upper_case_letters(self):


        self.password_slider.config(state=tk.ACTIVE)
        self.genrated_password_entry.config(state="normal")
        self.copy_password_button.config(state=tk.ACTIVE)
        self.generate_new_password_button.config(state=tk.ACTIVE)
        self.A_Z_button.config(state=tk.DISABLED)
        self.chars.update(string.ascii_uppercase)
        self.update_pool()

    def select_digits(self):


        self.password_slider.config(state=tk.ACTIVE)
        self.genrated_password_entry.config(state="normal")
        self.copy_password_button.config(state=tk.ACTIVE)
        self.generate_new_password_button.config(state=tk.ACTIVE)
        self.digits_button.config(state=tk.DISABLED)

        self.chars.update(string.digits)
        self.update_pool()

    def select_punctuation(self):


        self.password_slider.config(state=tk.ACTIVE)
        self.genrated_password_entry.config(state="normal")
        self.copy_password_button.config(state=tk.ACTIVE)
        self.generate_new_password_button.config(state=tk.ACTIVE)
        self.punctuation_button.config(state=tk.DISABLED)
        self.chars.update(string.punctuation)
        self.update_pool()

    def reset_character_types(self):

        self.password_slider.config(state=tk.DISABLED)
        self.copy_password_button.config(state=tk.DISABLED)
        self.generate_new_password_button.config(state=tk.DISABLED)

        self.genrated_password_entry.config(state="disabled", show="*")
        self.hide_button.config(state=tk.DISABLED)
        self.view_button.config(state=tk.NORMAL)

        self.a_z_button.config(state=tk.ACTIVE, activebackground="white", bg="white")
        self.A_Z_button.config(state=tk.ACTIVE, activebackground="white", bg="white")
        self.digits_button.config(state=tk.ACTIVE, activebackground="white", bg="white")
        self.punctuation_button.config(state=tk.ACTIVE, activebackground="white", bg="white")

        self.generated_password_length.set(0)
        self.entropy_label.config(fg="red", text="0 bits (poor)")

        self.chars = set()
        self.pool = []

        self.password_var.set("")

    def copy_password(self):
        password = self.password_var.get()

        if not password:
            tk.messagebox.showerror("Error", "No password to copy.")
            return

        self.clipboard_manager.copy_clip(password, timeout=10)

        tk.messagebox.showinfo("Success","Password copied. Clipboard will be cleared after 10 seconds.")


    def reset_password(self):

        if not self.chars:
            return

        password = "".join(
            secrets.choice(self.pool)
            for _ in range(self.generated_password_length.get())
        )

        self.password_var.set(password)

        entropy_level = self.password_entropy(password)
        self.update_entropy_status(entropy_level)

    
    def slider_changed(self, event=None):
        if not self.chars:
            return

        password = "".join(
            secrets.choice(self.pool)
            for _ in range(self.generated_password_length.get())
        )

        self.password_var.set(password)

        entropy_level = self.password_entropy(password)
        self.update_entropy_status(entropy_level)


    def password_entropy(self, password):
        if not password or not self.pool:
            return Decimal("0.00")

        entropy = len(password) * math.log2(len(self.pool))

        return Decimal(str(entropy)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    def update_entropy_status(self, entropy_level):

        entropy_level = float(entropy_level)

        if 0 == entropy_level or 0 < entropy_level <= 45:
            color = "red"
            label = "poor"

        elif 45 < entropy_level <= 80:
            color = "orange"
            label = "weak"

        elif 80 < entropy_level <= 90:
            color = "green"
            label = "good"

        else:
            color = "dark green"
            label = "strong"

        self.entropy_label.config(
            fg=color,
            text=f"{entropy_level} bits ({label})"
        )
