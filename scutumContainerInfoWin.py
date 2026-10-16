import datetime
import csv
import os
from Functions import cryptographicfunctions, database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE
import tkinter as tk
from scutumPassMainFunctionalities.passwordGeneratorWin import PasswordGeneratorWindow
from Classes.Accounts import (
    ContainerRow,
    ContainerRowContainer
)



class ScutumContainerInfoWindow(BaseWindow):

    def __init__(self, master, loaded_image,password_widget):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image
        self.master_widget = master

        self.password_list_widget = password_widget

        session = ContainerRowContainer.get_session()

        if session is None:
            self.destroy()
            return

        self.db_location = session.db_location
        self.key_bytes = session.key_bytes

        ctime = os.path.getctime(self.db_location)
        self.time_created = datetime.datetime.fromtimestamp(ctime)
        self.container_name = otherfunctions.file_name(self.db_location)

        self.master_widget.withdraw()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()

        button_logo = tk.Button(self,image=self.loaded_image["scutum_pass_img"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",command=self.go_back,bg="#de3800")
        button_logo.place(x=otherfunctions.x_center_widget(button_logo,400),y=5)

        tk.Label(self,font=(FONT_DEFAULT,11,"bold"),fg="#818181",text=f"Container information",bg="white").place(x=45,y=70)
        tk.Label(self,image=self.loaded_image["database_icon"],bg="white").place(x=290,y=80)

        frame_main_container = tk.Frame(self,bg="white")
        frame_main_container.place(x=45,y=130)
        frame_name_container = tk.Frame(frame_main_container,bg="white")
        frame_name_container.grid(row=0,column=0,sticky=tk.W)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Name:",bg="white").grid(row=0,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=self.container_name,bg="white").grid(row=0,column=1,pady=1)

        frame_date_created_container = tk.Frame(frame_main_container,bg="white")
        frame_date_created_container.grid(row=1,column=0,sticky=tk.W)

        tk.Label(frame_date_created_container,font=(FONT_DEFAULT,8,"bold"),text=f"Date created:",bg="white").grid(row=0,column=0,pady=1,sticky=tk.W)
        tk.Label(frame_date_created_container,font=(FONT_DEFAULT,8),text=f"{self.time_created} ",bg="white").grid(row=0,column=1,pady=1)

        button_option_frame = tk.Frame(self,bg="white")
        button_option_frame.place(x=220,y=220)

        tk.Button(button_option_frame,image=self.loaded_image["export_csv"],bg="white",highlightbackground="white",borderwidth=0,command=self.export_to_csv).grid(row=0,column=0,padx=5)
        tk.Button(button_option_frame,image=self.loaded_image["import_csv"],bg="white",highlightbackground="white",borderwidth=0,command=self.import_from_csv).grid(row=0,column=1,padx=5)
        tk.Button(button_option_frame,image=self.loaded_image["change_key"],bg="white",highlightbackground="white",borderwidth=0,command=self.change_key).grid(row=0,column=2,padx=5)

    def change_key(self):

        key_path = tk.filedialog.asksaveasfilename(
            defaultextension=".key",
            initialfile=f"Container_key_{self.container_name}.key",
            title="Save new key",
            filetypes=[("Key file", "*.key")]
        )

        if not key_path:
            return

        try:

            cryptographicfunctions.create_key(key_path)
            key = cryptographicfunctions.get_key(key_path)

            with cryptographicfunctions.SecureKey(key) as key_db:
                new_key_bytes = key_db.get()


            success = database.change_db_key(
                self.db_location,
                self.key_bytes,
                new_key_bytes
            )

            if not success:
 
                if os.path.exists(key_path):
                    os.remove(key_path)

                tk.messagebox.showerror("Error", "Key swap was not successful.")
                return

            self.key_bytes = new_key_bytes

            tk.messagebox.showinfo("Success", "Database key changed successfully.")
            self.destroy()

        except Exception as e:
            if os.path.exists(key_path):
                os.remove(key_path)

            tk.messagebox.showerror("Error", f"Key change failed: {e}")

    def export_to_csv(self):

        question = tk.messagebox.askquestion(
            "Warning",
            "Are you sure you want to export your passwords? This will write them in plain text."
        )

        if question == "no":
            return

        # Select directory for CSV export

        csv_location = tk.filedialog.askdirectory(title="CSV export file location", initialdir="/")
        if not csv_location:
            return 

        try:

            records, column_names = database.select_all_db_data(self.db_location,self.key_bytes)

            # Export data to CSV
            csv_file = os.path.join(csv_location, f'{self.container_name}.csv')
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  
                writer.writerows(records)  

            tk.messagebox.showinfo("Success", f"Data exported successfully to {csv_file}")

        except Exception as e:
            tk.messagebox.showerror("Error",f"{e}")

    def import_from_csv(self):

        # Ask user to select a CSV file
        csv_location = tk.filedialog.askopenfilename(defaultextension=".csv",title="CSV import file location", filetypes=[("Comma-separated values", "*.csv")])
        
        if not csv_location:
            tk.messagebox.showerror("Error", "No CSV file selected")
            return
        try:

                
            with open(csv_location, 'r', newline='', encoding='utf-8-sig') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Extract data from CSV row
                    group_password = row['grp']
                    title = row['name']
                    email = row['email']
                    password = row['password']
                    created_at = row['createdAt']
                    updated_at = row['updatedAt']


                    if not database.password_name_check(self.db_location,self.key_bytes , title.strip()):
                        tk.messagebox.showerror("Error", f"Record '{title}' already exists in the database")
                        return



                    database.insert_password_row(group_password,title,email,password,created_at,updated_at,self.db_location,self.key_bytes)
                    row = f"{group_password},{title},{email},{created_at},{updated_at}"
            

                    self.password_list_widget.insert(tk.END,row)
            
            tk.messagebox.showinfo("Success", "Data imported successfully from CSV to SQLite database")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    