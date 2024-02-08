import tkinter as tk

def custom_dialog(self, title, message):
    dialog = tk.Toplevel(self.root)
    dialog.title(title)
    dialog.configure(bg='#333333')  # Dark background for dialog
    dialog.geometry("600x400")  # Adjust size as needed
    # MESSAGE LABEL
    message_label = tk.Label(dialog, text=message, wraplength=350, bg=self.label_bg_color, fg=self.text_color,
                                font=self.font_style)
    message_label.pack(padx=10, pady=10)
    # CLOSE BUTTON
    close_button = tk.Button(dialog, text="Close", command=dialog.destroy, bg=self.button_color,
                                fg=self.button_text_color, font=self.font_style)
    close_button.pack(pady=10)