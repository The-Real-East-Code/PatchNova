import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar, Text, font

def custom_dialog(self, title, message, width, height):
    # STYLING
    font_style = "Consolas", 12
    background = '#2c99b4'
    text_background = 'white'
    text_color = '#222222'
    # DIALOG BOX
    dialog = tk.Toplevel(self.root)
    dialog.title(title)
    dialog.configure(bg=background)
    dialog.geometry(f"{width}x{height}")
    # MESSAGE LABEL
    message_label = tk.Label(dialog, text=message, wraplength=450, bg=text_background, fg=text_color,
                                font=font_style)
    message_label.pack(padx=10, pady=10)
    # CLOSE BUTTON
    close_button = tk.Button(dialog, text="Close", command=dialog.destroy, bg=self.button_color,
                                fg=self.button_text_color, font=self.font_style)
    close_button.pack(pady=10)


def get_user_consent(message):
    return messagebox.askyesno("User Consent", message)