import tkinter as tk
from tkinter import ttk, Text

def show_logs(self, root):
        log_dialog = tk.Toplevel(root)
        log_dialog.title("Logs")
        log_dialog.geometry("800x600")  # Adjust size as needed
        log_dialog.configure(bg='#333333')
        tab_control = ttk.Notebook(log_dialog)  # Define tab_control variable
        # HISTORY LOGGING
        update_history_tab = ttk.Frame(tab_control)
        tab_control.add(update_history_tab, text='Update History')
        update_history_text = Text(update_history_tab, wrap='word', yscrollcommand=lambda *args: True)
        update_history_text.pack(expand=True, fill='both')
        # ERROR LOGGING
        error_log_tab = ttk.Frame(tab_control)
        tab_control.add(error_log_tab, text='Error Log')
        error_log_text = Text(error_log_tab, wrap='word', yscrollcommand=lambda *args: True)
        error_log_text.pack(expand=True, fill='both')
        # TAB CONTROL
        tab_control.pack(expand=True, fill='both')  

        with open("update_history.log", "r") as file:
            update_history_text.insert('1.0', file.read())
        
        with open("error_log.log", "r") as file:
            error_log_text.insert('1.0', file.read())

        close_button = tk.Button(log_dialog, text="Close", command=log_dialog.destroy, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        close_button.pack(pady=10)

        self.setup_logging()

        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color,
                                            font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding
        # LOADING INDICATOR
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        # STATUS LABEL
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
