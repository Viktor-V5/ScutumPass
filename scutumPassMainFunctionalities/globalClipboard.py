import tkinter as tk


class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.timer_id = None

    def copy_clip(self, text, timeout=10):
        if self.timer_id is not None:
            try:
                self.root.after_cancel(self.timer_id)
            except tk.TclError:
                pass

        self.timer_id = None

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(text))
            self.root.update_idletasks()

            self.timer_id = self.root.after(
                timeout * 1000,
                self.clear_clip
            )

        except tk.TclError as error:
            print("Copy error:", error)

    def clear_clip(self):
        self.timer_id = None

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append("")
            self.root.update()

            print("Clipboard cleared. Test with Ctrl+V.")

        except tk.TclError as error:
            print("Clipboard error:", error)
