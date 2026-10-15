import os
from tkinter import Tk
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Data", "Images")


def image_path(*parts):
    return os.path.join(IMAGE_DIR, *parts)

def load_image(file_path):
    image = Image.open(file_path)
    return ImageTk.PhotoImage(image)
    
def load_loaded_image():
    loaded_image = {}

    # 17 x 17
    loaded_image["random_button"] = load_image(
        image_path("17 x 17", "Random_button.png")
    )
    loaded_image["copy_button"] = load_image(
        image_path("17 x 17", "Copy_button.png")
    )


    # 28 x 30
    loaded_image["history_icon"] = load_image(
        image_path("28 x 30", "History_icon.png")
    )

    # 31 x 24
    loaded_image["copy_password_icon"] = load_image(
        image_path("31 x 24", "Copy_password_icon.png")
    )
    loaded_image["copy_name_icon"] = load_image(
        image_path("31 x 24", "Copy_name_icon.png")
    )
    loaded_image["copy_email_icon"] = load_image(
        image_path("31 x 24", "Copy_email_icon.png")
    )
    loaded_image["view_icon"] = load_image(
        image_path("31 x 24", "View_password_icon.png")
    )

    # 31 x 31
    loaded_image["delete_icon"] = load_image(
        image_path("31 x 31", "Delete_icon.png")
    )
    loaded_image["open_folder_icon"] = load_image(
        image_path("31 x 31", "Open_folder_icon.png")
    )
    loaded_image["search_location"] = load_image(
        image_path("31 x 31", "Search_location_icon.png")
    )
    loaded_image["import_csv"] = load_image(
        image_path("31 x 31", "Import_csv_icon.png")
    )
    loaded_image["export_csv"] = load_image(
        image_path("31 x 31", "Export_csv_icon.png")
    )
    loaded_image["change_key"] = load_image(
        image_path("31 x 31", "Change_key_icon.png")
    )


    # 36 x 36
  
    loaded_image["scutumpass_password_gui"] = load_image(
        image_path("36 x 36", "Password_icon.png")
    )
    loaded_image["scutumpass_container_gui"] = load_image(
        image_path("36 x 36", "Container_icon.png")
    )
    

    # 43 x 43
   
    loaded_image["scutum_pass_img"] = load_image(
        image_path("43 x 43", "Scutum_pass_logo.png")
    )
    


    # 84 x 84
    loaded_image["scutum_pass_open_button"] = load_image(
        image_path("84 x 84", "Scutum_pass_open_container.png")
    )
    loaded_image["scutum_pass_create_button"] = load_image(
        image_path("84 x 84", "Scutum_pass_create_container.png")
    )
  
    # Other dimensions

    loaded_image["database_icon"] = load_image(
        image_path("Other dimensions", "Database_logo.png")
    )
    loaded_image["search_icon"] = load_image(
        image_path("Other dimensions", "Search_icon.png")
    )


    # GUI backgrounds
    guis = {
        
        "orange_gui": "Orange_GUI.png",
        "orange_landscape_gui": "Orange_landscape_GUI.png",
    }

    for key, file in guis.items():
        loaded_image[key] = load_image(
            image_path("Background objects", file)
        )


    return loaded_image