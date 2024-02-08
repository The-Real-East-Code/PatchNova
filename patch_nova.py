from patch_modules.log_viewer import show_log
from patch_modules.check_software import check_software
from patch_modules.custom_dialog import custom_dialog
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar, Text, font
import platform
import subprocess
import distro
import logging
from logging.handlers import RotatingFileHandler


class UpdateCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Checker")
        # INCREASE THE INITIAL SIZE OF THE MAIN WINDOW
        self.root.geometry('1000x500')  # Adjust width and height as needed
        self.root.configure(bg='#333333')  # Dark background for the main window
        # ENHANCED FONT AND COLOR CONFIGURATION FOR LARGER UI ELEMENTS
        self.font_style = ("Consolas", 16)  # Increase font size
        self.button_color = "#15065c"
        self.text_color = "#FFFFFF"
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#333333"
        # HARDWARE INFO LABEL
        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding
        # Display hardware information
        self.hardware_info_label = tk.Label(root, text="")
        self.hardware_info_label.pack()
        self.get_hardware_info()
        # Loading indicator
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        # Status label
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        # Larger buttons with increased padding
        self.check_updates_button = tk.Button(root, text="System Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)  # Increase vertical padding
        self.check_software_updates_button = tk.Button(root, text="Check Installed Software", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)  # Increase vertical padding
        self.show_logs_button = tk.Button(root, text="Show Logs", command=self.show_logs, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        # self.show_logs_button = tk.Button(root, text="Show Logs", command=lambda: show_logs(self, self.root), bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.show_logs_button.pack(pady=10)
        # SETUP LOGGING
        # self.setup_logging()

    def show_logs(self):
        return show_log(self, self.root)

    def check_software_updates(self):
        return check_software(self, self.root)

    def create_custom_dialog(self, title, message):
        return custom_dialog(self, title, message)

    def setup_logging(self):
        # Create a logger
        self.logger = logging.getLogger("UpdateCheckerApp")
        self.logger.setLevel(logging.DEBUG)
        # Create a formatter and add it to the handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # Create a rotating file handler for update history
        self.history_handler = RotatingFileHandler("update_history.log", maxBytes=1024 * 1024, backupCount=5)
        self.history_handler.setLevel(logging.INFO)
        self.history_handler.setFormatter(formatter)
        self.logger.addHandler(self.history_handler)
        # Create a rotating file handler for errors
        self.error_handler = RotatingFileHandler("error_log.log", maxBytes=1024 * 1024, backupCount=5)
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(formatter)
        self.logger.addHandler(self.error_handler)


    def get_hardware_info(self):
        system_info = platform.uname()
        info_text = f"System: {system_info.system}\nNode Name: {system_info.node}\n" \
                    f"Release: {system_info.release}\nVersion: {system_info.version}\n" \
                    f"Machine: {system_info.machine}\nProcessor: {system_info.processor}"
        self.hardware_info_label.config(text=info_text)


    def get_user_consent(self):
        return messagebox.askyesno("User Consent", "Do you want to install your system updates?")


    def show_loading_indicator(self):
        self.loading_indicator.pack(pady=10)
        self.loading_indicator.start()


    def hide_loading_indicator(self):
        self.loading_indicator.stop()
        self.loading_indicator.pack_forget()


    def update_status_label(self, text):
        self.status_label.config(text=text)
        self.status_label.pack(pady=10)


    def check_updates(self):
        self.get_hardware_info()

        if self.get_user_consent():
            
            ask_if_should_update = messagebox.askyesno("User Consent", "Are you sure?")

            if ask_if_should_update:
                # Check for updates based on the user's operating system
                if platform.system() == 'Windows':
                    # Trigger Windows Update
                    subprocess.run(["powershell", "Install-Module PSWindowsUpdate -Force -AllowClobber"])
                    subprocess.run(["powershell", "Get-WindowsUpdate -Install -AcceptAll"])
                    self.logger.info("Windows Update checked")

                elif platform.system() == 'Darwin':
                    # Trigger macOS Update
                    subprocess.run(["softwareupdate", "-i", "-a"])
                    self.logger.info("macOS Update checked")

                elif platform.system() == 'Linux':
                    # Use distro.id() to get the distribution ID as a string
                    dist_id = distro.id()
                    update_command = ""
                    if "ubuntu" in dist_id or "debian" in dist_id:
                        subprocess.run(["sudo", "apt-get", "update"])
                        update_command = "sudo apt-get upgrade -y"
                    elif "fedora" in dist_id or "centos" in dist_id:
                        update_command = "sudo dnf update"
                    elif "arch" in dist_id:
                        update_command = "sudo pacman -Syu"
                    else:
                        self.create_custom_dialog("Linux Update Information",
                                                "Your Linux distribution is not supported for automatic updates through this script.")
                        return
                    self.create_custom_dialog("Update Information", "System update complete.")
                    self.logger.info(f"Linux Update Information provided for {dist_id}")
                    # Run the update command in the terminal
                    subprocess.run(update_command.split())

                else:
                    self.create_custom_dialog("Unsupported System",
                                            "Updates are not supported for the current operating system.")
                self.logger.info("Update process completed.")
            
            else:
                self.create_custom_dialog("User Does Not Consent",
                                                "Understood. PatchNova will not install any updates on your system. Thank you.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateCheckerApp(root)
    root.mainloop()