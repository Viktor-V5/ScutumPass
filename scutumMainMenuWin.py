import os
import sys
from Functions import cryptographicfunctions, database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow,WINDOW_SIZE, WINDOW_SIZE_LANDSCAPE,LIST_BOX_WIDTH,LIST_BOX_HEIGHT,SEARCH_PASSWORD_ENTRY_WIDTH
import tkinter as tk
from scutumAddPasswordWin import ScutumAddPasswordWindow
from scutumViewRecordWin import ScutumViewRecordWindow
from scutumContainerInfoWin import ScutumContainerInfoWindow
from Classes.Accounts import (
    ContainerRow,
    ContainerRowContainer
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


class ScutumMainMenuWindow(BaseWindow):

    def __init__(self, master, loaded_image):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        self.loaded_image = loaded_image

        session = ContainerRowContainer.get_session()


        if session is None:
            self.destroy()
            return

        self.db_location = session.db_location
        self.key_bytes = session.key_bytes

        self.extracted_data = database.select_db_data(self.db_location, self.key_bytes)

        self.search_variable = tk.StringVar()
        self.container_name = os.path.basename(self.db_location)

        self.password_list = None

        self.create_widgets()


    def clear_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append("")
        self.update()

    def create_widgets(self):

        tk.Label(self,image=self.loaded_image["orange_gui"]).pack()
        tk.Label(self,font=(FONT_DEFAULT,11,"bold"),text=f"Container {self.container_name}",fg="grey",bg="white").place(x=45,y=70)

        # Search box

        self.search_frame = tk.Frame(self,bg="white",width=235)
        self.search_frame.place(x=otherfunctions.x_center_widget(self.search_frame,300),y=100)

        tk.Label(self.search_frame,image=self.loaded_image["search_icon"],bg="white").grid(row=0,column=0,padx=2)

        self.search_password = tk.Entry(self.search_frame,textvariable=self.search_variable,borderwidth=1,width=SEARCH_PASSWORD_ENTRY_WIDTH)
        self.search_password.grid(row=0,column=1)

        self.search_password.bind("<KeyRelease>", self.search_listbox)

        # List box
        self.password_list = tk.Listbox(self,width=LIST_BOX_WIDTH,height=LIST_BOX_HEIGHT,borderwidth=0)   
        self.password_list.place(x=otherfunctions.x_center_widget(self.password_list,300),y=130)

    
        # Open files

        for record_list in self.extracted_data:
            formated_record = ', '.join(map(str, record_list))
            formated_record = formated_record.replace("(", "").replace(")", "")      
            
            self.password_list.insert(tk.END,f"{formated_record}")



        frame_buttons = tk.Frame(self,bg="#de3800")
        frame_buttons.place(x=28,y=5)

        tk.Button(frame_buttons,image=self.loaded_image["scutumpass_password_gui"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",command=self.add_password_window,bg="#de3800").grid(row=0,column=0,padx=10)
        tk.Label(frame_buttons,image=self.loaded_image["scutum_pass_img"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",bg="#de3800").grid(row=0,column=1,padx=40)
        tk.Button(frame_buttons,image=self.loaded_image["scutumpass_container_gui"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",command=self.information_container,bg="#de3800").grid(row=0,column=2,padx=10)

        frame_buttons_functions = tk.Frame(self,bg="white")
        frame_buttons_functions.place(x=35,y=310)  

        tk.Button(frame_buttons_functions,image=self.loaded_image["delete_icon"],highlightbackground="white",bg="white",borderwidth=0,command=self.remove_record).grid(row=0,column=0,padx=5) 
        tk.Button(frame_buttons_functions,image=self.loaded_image["view_icon"],highlightbackground="white",bg="white",borderwidth=0,command=self.reveal_record_details).grid(row=0,column=1,padx=5)
        tk.Button(frame_buttons_functions,image=self.loaded_image["copy_name_icon"],highlightbackground="white",bg="white",borderwidth=0,command=self.copy_name).grid(row=0,column=2,padx=5)
        tk.Button(frame_buttons_functions,image=self.loaded_image["copy_email_icon"],highlightbackground="white",bg="white",borderwidth=0,command=self.copy_email).grid(row=0,column=3,padx=5)
        tk.Button(frame_buttons_functions,image=self.loaded_image["copy_password_icon"],highlightbackground="white",bg="white",borderwidth=0,command=self.copy_password).grid(row=0,column=4,padx=5)

    def remove_record(self):

        selected = self.password_list.curselection()

        if not selected:
            tk.messagebox.showerror("Error", "Please select a record.")
            return

        selected_index = selected[0]
        record_get = self.password_list.get(selected_index)

        if not tk.messagebox.askyesno(
            "Warning",
            "Are you sure you want to delete this record?"
        ):
            return

        record = [item.strip() for item in record_get.split(",")]

        database.delete_record_db(
            self.db_location,
            self.key_bytes,
            record[1]
        )

        self.password_list.delete(selected_index)

        tk.messagebox.showinfo(
            "Success",
            f'"{record[1]}" was removed successfully.'
        )

    def add_password_window(self):   

        ScutumAddPasswordWindow(self,self.loaded_image,self.password_list)

    def information_container(self):
        
        ScutumContainerInfoWindow(self,self.loaded_image,self.password_list)

    def copy_password(self):
        if not self.password_list.curselection():
            tk.messagebox.showerror("Error", "Please select a record.")
            return

        string_get = str(self.password_list.get(self.password_list.curselection()))
        record = string_get.split(",")

        if len(record) < 2:
            messagebox.showerror("Error", "Invalid record format")
            return


        name_field = record[1].strip()

   
        record_password = database.get_db_password(self.db_location,self.key_bytes,name_field)

        self.clipboard_clear()
        self.clipboard_append(record_password)
        self.update()
        tk.messagebox.showinfo("Success","Password has been coppied. After 10 seconds the clipboard will be cleared")   
        self.after(10000, self.clear_clipboard)

    def copy_name(self):
        if not self.password_list.curselection():
            tk.messagebox.showerror("Error", "Please select a record.")
            return

        string_get = str(self.password_list.get(self.password_list.curselection()))
        record = string_get.split(",")

        if len(record) < 2:
            tk.messagebox.showerror("Error", "Invalid record format")
            return


        name_field = record[1].strip()


        self.clipboard_clear()
        self.clipboard_append(name_field)
        self.update()  
        tk.messagebox.showinfo("Success","Name has been coppied")  
        self.after(10000, self.clear_clipboard)

    def copy_email(self):
        if not self.password_list.curselection():
            tk.messagebox.showerror("Error", "Please select a record. After 10 seconds the clipboard will be cleared")
            return

        string_get = str(self.password_list.get(self.password_list.curselection()))
        record =  string_get.split(",")

        if len(record) < 2:
            tk.messagebox.showerror("Error", "Invalid record format")
            return

        record_email = record[2].strip()

        self.clipboard_clear()
        self.clipboard_append(record_email)
        self.update() 
        tk.messagebox.showinfo("Success","Email has been coppied. After 10 seconds the clipboard will be cleared") 
        self.after(10000, self.clear_clipboard)

    def reveal_record_details(self):

        if not self.password_list.curselection():
            tk.messagebox.showerror("Error", "Please select a record.")
            return

        record_get = self.password_list.get(self.password_list.curselection())

        question = tk.messagebox.askquestion(
            "Warning",
            "Are you sure you want to see this record?"
        )

        if question == "no":
            return

        ScutumViewRecordWindow(self, self.loaded_image, record_get,self.password_list)
       
    def search_listbox(self,event=None):

        search_term = self.search_variable.get().lower()
        self.password_list.delete(0, tk.END)
    
        try:

    
            selected_records = database.select_db_data(self.db_location,self.key_bytes)

    
            for record_list in selected_records:
                formatted_record = ', '.join(map(str, record_list))
                formatted_record = formatted_record.replace("(", "").replace(")", "")
    
                
                if search_term == "" or search_term in formatted_record.lower():
                    self.password_list.insert(tk.END, formatted_record)
    
        except ValueError as e:
            messagebox.showerror("Error", e)

