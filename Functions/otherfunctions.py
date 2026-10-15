import os
import tkinter as tk


def file_name(path : str):


    container_db = os.path.basename(path)


    container_name  = str(container_db.replace(".db",""))

    return container_name


def x_center_widget(widget_name, window_width):
    widget_width = widget_name.winfo_reqwidth()
    x_coordinate = (window_width - widget_width) // 2 

    return x_coordinate


def y_center_widget(widget_name, window_height):
    widget_height = widget_name.winfo_reqheight()
    y_coordinate = (window_height - widget_height) // 2 
    return y_coordinate

    return tkfont.Font(family="Liberation Sans", size=size, weight=weight)