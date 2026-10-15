import os
import sys
from Functions import cryptographicfunctions, database
from Classes.baseGUI import FONT_DEFAULT,BaseWindow,WINDOW_SIZE, WINDOW_SIZE_LANDSCAPE
import tkinter as tk
from ScutumEditPasswordWin import ScutumEditPasswordWindow
from Classes.Accounts import (
    ContainerRow,
    ContainerRowContainer
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


class ScutumViewRecordWindow(BaseWindow):

    def __init__(self, master, loaded_image,extracted_data,password_list_widget,clipboard_manager):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image
        self.extracted_data = extracted_data
        self.master_widget = master
        self.password_list_widget = password_list_widget

        session = ContainerRowContainer.get_session()


        if session is None:
            self.destroy()
            return

        self.db_location = session.db_location
        self.key_bytes = session.key_bytes

        
        self.clipboard_manager = clipboard_manager
        self.extracted_data = extracted_data


        self.select_group = None
        self.select_title = None
        self.select_email = None
        self.select_password = None
        self.created_at = None
        self.updated_at = None

        self.formated_record_get = None

        self.password_label = None
        
        self.master_widget.withdraw()
        self.extract_data()

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()

        tk.Button(self,
        image=self.loaded_image["scutum_pass_img"],
        highlightbackground="#de3800"
        ,borderwidth=0,
        activebackground="#de3800",
        command=self.go_back,
        bg="#de3800"
        ).place(x=177,y=5)

        frame_name_container = tk.Frame(self,bg="white", width=240)
        frame_name_container.place(x=55, y=110)

        tk.Label(self, font=(FONT_DEFAULT, 11, "bold"), text="Password details", fg="#818181", bg="white").place(x=45, y=80)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Group:",bg="white").grid(row=0,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=f"{self.select_group}",bg="white").grid(row=0,column=1,pady=1,sticky=tk.W)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Name:",bg="white").grid(row=1,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=f"{self.select_title}",bg="white").grid(row=1,column=1,pady=1,sticky=tk.W)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Email:",bg="white").grid(row=2,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=f"{self.select_email}",bg="white").grid(row=2,column=1,pady=1,sticky=tk.W)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Password:",bg="white").grid(row=3,column=0,pady=1,sticky=tk.W) 
        self.password_label = tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text="*"*32,bg="white")
        self.password_label.grid(row=3,column=1,pady=1,sticky=tk.W)


        frame_hide_view_buttons = tk.Frame(frame_name_container, bg="white")
        frame_hide_view_buttons.grid(row=4, column=0, sticky=tk.W)

        self.view_button = tk.Button(frame_hide_view_buttons, font=(FONT_DEFAULT, 6, "bold"), activebackground="white",
                                         highlightbackground="white", bg="white", text="view", borderwidth=0, command=self.view_id)
        self.view_button.grid(row=0, column=0, sticky="w")
        self.hide_button = tk.Button(frame_hide_view_buttons, font=(FONT_DEFAULT, 6, "bold"), activebackground="white",
                                        highlightbackground="white", bg="white", text="hide", borderwidth=0, state="disabled", command=self.hide_id)
        self.hide_button.grid(row=0, column=1, sticky="w")

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Created at:",bg="white").grid(row=5,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=f"{self.created_at}",bg="white").grid(row=5,column=1,pady=1,sticky=tk.W)

        tk.Label(frame_name_container,font=(FONT_DEFAULT,8,"bold"),text=f"Updated at:",bg="white").grid(row=6,column=0,pady=1,sticky=tk.W) 
        tk.Label(frame_name_container,font=(FONT_DEFAULT,8),text=f"{self.updated_at}",bg="white").grid(row=6,column=1,pady=1,sticky=tk.W)


        tk.Button(self,font=(FONT_DEFAULT,8),text="Edit record",command=self.edit_record).place(x=250, y=220)


    def view_id(self):
        self.password_label.config(text=self.select_password)
        self.hide_button.config(state="active")
        self.view_button.config(state="disabled")

    def hide_id(self):
        self.password_label.config(text="*" * 32)
        self.hide_button.config(state="disabled")
        self.view_button.config(state="active")

    def extract_data(self):
        try:
            record = self.extracted_data.split(",")

            if len(record) < 2:
                print("Not enough fields!", record)
                return False

            self.select_title = record[1].strip()

            rows = database.load_data(self.db_location, self.key_bytes, self.select_title)

            if not rows:
                print("No data found for:", self.select_title)
                return False


            row = rows[0]


            (
                self.select_group,
                _title,
                self.select_email,
                self.select_password,
                self.created_at,
                self.updated_at
            ) = row


            self.formated_record_get = row

            return True

        except Exception as e:
            print("extract_data error:", e)
            return False

        

        return True
    
    def edit_record(self):

        ScutumEditPasswordWindow(self,self.loaded_image,self.formated_record_get,self.password_list_widget,self.clipboard_manager)

               


                    