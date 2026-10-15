import datetime
import tkinter as tk
from Functions import database, otherfunctions
from Classes.baseGUI import FONT_DEFAULT,BaseWindow, WINDOW_SIZE_LANDSCAPE
from scutumPassMainFunctionalities.passwordGeneratorWin import PasswordGeneratorWindow
from Classes.Accounts import ContainerRowContainer


class ScutumEditPasswordWindow(BaseWindow):

    def __init__(self, master, loaded_image,extracted_data,password_list_widget):
        super().__init__(master)
        self.title("Scutum Pass")
        self.geometry(WINDOW_SIZE_LANDSCAPE)
        self.resizable(False, False)
        self.loaded_image = loaded_image
        self.master_window = master

        self.extracted_data = extracted_data
        self.password_list = password_list_widget


        session = ContainerRowContainer.get_session()


        if session is None:
            self.destroy()
            return

        
        self.db_location = session.db_location
        self.key_bytes = session.key_bytes

        self.extracted_data = [x.strip() for x in extracted_data]

        self.group_var = tk.StringVar(value=self.extracted_data[0])
        self.title_var = tk.StringVar(value=self.extracted_data[1])
        self.email_var = tk.StringVar(value=self.extracted_data[2])
        self.pass_var = tk.StringVar(value=self.extracted_data[3])

        self.created_at = self.extracted_data[4]
        self.updated_at = self.extracted_data[5]

        self.old_name = self.extracted_data[1]

        self.updated_at = extracted_data[5]

        
        self.master_window.withdraw()
        self.create_widgets()

    def password_generator_program(self):
        password_generator_win = PasswordGeneratorWindow(self,self.loaded_image)
        password_generator_win.grab_set()


    def edit_password(self):
        edited_at = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:

            group = self.group_var.get().strip() or self.extracted_data[0]
            title = self.title_var.get().strip() or self.extracted_data[1]
            email = self.email_var.get().strip() or self.extracted_data[2]
            password = self.pass_var.get().strip() or self.extracted_data[3]

            if (group, title, email, password) == tuple(self.extracted_data[:4]):
                tk.messagebox.showerror("Error", "No changes were made.")
                return


            database.edit_db_data(
                group,
                title,
                email,
                password,
                self.created_at,
                edited_at,
                self.db_location,
                self.key_bytes,
                self.old_name
            )

            # refresh listbox
            self.password_list.delete(0, tk.END)

            records = database.select_db_data(
                self.db_location,
                self.key_bytes
            )

            for record in records:
                clean = [str(x).strip() for x in record]
                self.password_list.insert(tk.END, ", ".join(clean))

            tk.messagebox.showinfo("Success",f'"{self.old_name}" was updated successfully.')

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
   

    def create_widgets(self):
        

        tk.Label(self,image=self.loaded_image["orange_landscape_gui"]).pack()


        tk.Label(self,font=(FONT_DEFAULT,8,"bold"),text="Edit password row",fg="#818181",bg="white").place(x=45,y=70)


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

        tk.Button(self.frame_add_password,font=(FONT_DEFAULT,8),text="Add password",command=self.edit_password,width=12).grid(row=4,column=1,pady=10)

        self.button_logo = tk.Button(self,image=self.loaded_image["scutum_pass_img"],highlightbackground="#de3800",borderwidth=0,activebackground="#de3800",command=self.go_back,bg="#de3800")
        self.button_logo.place(x=otherfunctions.x_center_widget(self.button_logo,400),y=5)

        self.generate_password_button = tk.Button(self.frame_add_password,image=self.loaded_image["random_button"],highlightbackground="white",borderwidth=0,command=self.password_generator_program)
        self.generate_password_button.grid(row=3,column=2,padx=8)