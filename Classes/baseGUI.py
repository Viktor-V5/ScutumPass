import tkinter as tk
import os
import sys

from image_loader import load_loaded_image
from Classes.Accounts import ContainerRow, ContainerRowContainer


WINDOW_X = 300
WINDOW_Y = 400

WINDOW_X_LANDSCAPE = 400
WINDOW_Y_LANDSCAPE = 300

WINDOW_SIZE = f"{WINDOW_X}x{WINDOW_Y}"
WINDOW_SIZE_LANDSCAPE = f"{WINDOW_X_LANDSCAPE}x{WINDOW_Y_LANDSCAPE}"


# ---------------------------------------------------------
# Platform-specific GUI settings
# ---------------------------------------------------------

if sys.platform.startswith("linux"):
    FONT_DEFAULT = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    COLOR_GRABBER_PROGRAM_WIN_SIZE = "240x70"
    LIST_BOX_WIDTH = 28
    LIST_BOX_HEIGHT = 10
    SEARCH_PASSWORD_ENTRY_WIDTH = 20
    PASS_GEN_BUTTONS_FONT_SIZE = 6

else:
    FONT_DEFAULT = "Arial"
    COLOR_GRABBER_PROGRAM_WIN_SIZE = ""
    LIST_BOX_WIDTH = 38
    LIST_BOX_HEIGHT = 10
    SEARCH_PASSWORD_ENTRY_WIDTH = 34
    PASS_GEN_BUTTONS_FONT_SIZE = 10


# ---------------------------------------------------------
# Base Window
# ---------------------------------------------------------

class BaseWindow(tk.Toplevel):

    def __init__(self, master=None, loaded_image=None, title="Window"):
        super().__init__(master)

        self.master = master
        self.title(title)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)

        if loaded_image is not None:
            self.loaded_image = loaded_image
        else:
            self.loaded_image = load_loaded_image()


        # -------------------------------------------------
        # Cross-platform window close button
        # -------------------------------------------------

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_poped_window
        )

    # -----------------------------------------------------
    # Clear all widgets from this window
    # -----------------------------------------------------

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # -----------------------------------------------------
    # Default widget creation
    # -----------------------------------------------------

    def create_widgets(self):
        tk.Label(
            self,
            text="Base Window"
        ).pack(pady=20)

    # -----------------------------------------------------
    # Close only this popup window
    # -----------------------------------------------------

    def close_poped_window(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass

        self.destroy()

    # -----------------------------------------------------
    # Go back to the parent window
    # -----------------------------------------------------

    def go_back(self):
        self.destroy()

        if self.master is not None:
            try:
                if self.master.winfo_exists():
                    self.master.deiconify()
            except tk.TclError:
                pass

    # -----------------------------------------------------
    # Hide the parent window
    # -----------------------------------------------------

    def hide(self):
        if self.master is not None:
            try:
                if self.master.winfo_exists():
                    self.master.withdraw()
            except tk.TclError:
                pass

    # -----------------------------------------------------
    # Close the entire application
    # -----------------------------------------------------

    def close_application(self):
        try:
            ContainerRow.clear_session()
        except Exception:
            pass

        try:
            ContainerRowContainer.clear_session()
        except Exception:
            pass

        # Get the actual Tk root window.
        try:
            root = self.nametowidget(".")
        except tk.TclError:
            root = self

        # Stop the Tkinter event loop.
        try:
            root.quit()
        except tk.TclError:
            pass

        # Destroy the root window and all child windows.
        try:
            root.destroy()
        except tk.TclError:
            pass

    # -----------------------------------------------------
    # Close this window and the entire application
    # -----------------------------------------------------

    def on_close(self):
        self.close_application()

