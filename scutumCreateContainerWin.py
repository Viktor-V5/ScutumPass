from Functions import cryptographicfunctions, database
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


class ScutumCreateContainerWindow(BaseWindow):

    def __init__(self, master, loaded_image):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image

        self.container_name = tk.StringVar()

        self.container_db_path = None 

        self.create_widgets()

    def create_widgets(self):
        try:

            self.hide()

            tk.Label(self, image=self.loaded_image["orange_landscape_gui"]).pack()

            tk.Label(
                self,
                font=(FONT_DEFAULT, 11, "bold"),
                fg="#818181",
                text="Create container",
                bg="white"
            ).place(x=45, y=70)

            frame_register = tk.Frame(self, bg="white")
            frame_register.place(x=45, y=110)

            tk.Label(frame_register, font=(FONT_DEFAULT, 8), text="Name: ", bg="white").grid(row=0, column=0)

            self.location = tk.Label(frame_register, font=(FONT_DEFAULT, 8, "bold"), bg="white")
            self.location.grid(row=0, column=3, padx=5)

            container_name_entry = tk.Entry(
                frame_register,
                bg="#dddddd",
                borderwidth=0,
                font=(FONT_DEFAULT, 8),
                textvariable=self.container_name
            )
            container_name_entry.grid(row=0, column=1)

            self.select_location_button = tk.Button(
                frame_register,
                image=self.loaded_image["search_location"],
                borderwidth=0,
                bg="white",
                highlightbackground="white",
                command=self.select_db_location
            )
            self.select_location_button.grid(row=0, column=2, padx=5)


            tk.Button(
                frame_register,
                font=(FONT_DEFAULT, 8),
                text="Create",
                width=10,
                command=self.create_files
            ).grid(row=3, column=1, pady=10)


            tk.Button(
                self,
                image=self.loaded_image["scutum_pass_img"],
                highlightbackground="#de3800",
                borderwidth=0,
                activebackground="#de3800",
                command=self.go_back,
                bg="#de3800"
            ).place(x=177, y=5)

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    def select_db_location(self):
        self.container_db_path = tk.filedialog.askdirectory(initialdir='/')

        if not self.container_db_path:
            return

        self.select_location_button.config(text=self.container_db_path)
        self.location.config(text="Location set")

    def create_files(self):

        container_name = self.container_name.get().strip().replace(" ", "_")

        # Verifiaction 

        if not container_name:
            raise ValueError("Container name is required.")

        if len(container_name) >= 20:
            raise ValueError("Container name must be fewer than 20 characters.")

        if not self.container_db_path:
            raise ValueError("Please select a container location.")


        container_folder = os.path.join(
            self.container_db_path,
            f"Container {container_name}"
        )

        container_key_path = tk.filedialog.askdirectory(title="Select key location")

        if not container_key_path:
            raise ValueError("No key location selected.")

        container_file_path = os.path.join(
            container_folder,
            f"{container_name}.db"
        )

        container_key = os.path.join(
            container_key_path,
            f"Container_key_{container_name}.key"
        )

        os.mkdir(container_folder)

        cryptographicfunctions.create_key(container_key)

        key = cryptographicfunctions.get_key(container_key)

        with cryptographicfunctions.SecureKey(key) as key_db:
            key_db_bytes = key_db.get()

        database.create_password_Managerdb(container_file_path,key_db_bytes)

        tk.messagebox.showinfo(
            "Success",
            f"Container '{container_name}' has been created."
        )

        self.go_back()
