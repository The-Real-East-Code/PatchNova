from patch_modules.log_viewer import show_log
from patch_modules.check_software import check_software, is_admin
from patch_modules.custom_dialog import custom_dialog, get_user_consent
from patch_modules.set_bg_image import set_background_with_label
import tkinter as tk
from tkinter import ttk, messagebox, font
import platform
import subprocess
import distro
import logging
from logging.handlers import RotatingFileHandler
import ctypes
import sys
import os

class UpdateCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Checker")
        # INCREASE THE INITIAL SIZE OF THE MAIN WINDOW
        self.root.geometry('1000x500')
        self.root.configure(bg='#fb8200')
        # root.attributes('-alpha',"0.5")
        # ENHANCED FONT AND COLOR CONFIGURATION FOR LARGER UI ELEMENTS
        self.font_style = ("Consolas", 16)
        self.button_color = "#15065c"
        self.text_color = "#FFFFFF"
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#2c99b4"
        # HARDWARE INFO LABEL
        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # INCREASE VERTICAL PADDING
        # DISPLAY HARDWARE INFORMATION
        self.hardware_info_label = tk.Label(root, text="")
        self.hardware_info_label.pack()
        self.get_hardware_info()
        # LOADING INDICATOR
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        # STATUS LABEL
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        # LARGER BUTTONS WITH INCREASED PADDING
        self.check_updates_button = tk.Button(root, text="Install System Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)  # INCREASE VERTICAL PADDING
        self.check_software_updates_button = tk.Button(root, text="Check Installed Software", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)  # INCREASE VERTICAL PADDING
        self.logger = logging.getLogger("UpdateCheckerApp")
        self.show_logs_button = tk.Button(root, text="Show Logs", command=self.show_logs, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        # self.show_logs_button = tk.Button(root, text="Show Logs", command=lambda: show_logs(self, self.root), bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.show_logs_button.pack(pady=10)
        self.show_about_patchnova = tk.Button(root, text="About PatchNova", command=self.show_about, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        # self.show_logs_button = tk.Button(root, text="Show Logs", command=lambda: show_logs(self, self.root), bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.show_about_patchnova.pack(pady=10)
        # SETUP LOGGING
        self.setup_logging()

    def get_user_consent(self):
        return messagebox.askyesno("User Consent", "Do you want to proceed?")

    def show_logs(self):
        return show_log(self, self.root)

    def check_software_updates(self):
        return check_software(self, self.root)

    def create_custom_dialog(self, title, message, width, height):
        return custom_dialog(self, title, message, width, height)
    
    def show_about(self):
            title = "About PatchNova"
            text = f"PatchNova is a streamlined, local update management application designed for efficient software and system updates.\n\nThis desktop tool offers a user-friendly interface to monitor and manage updates for your operating system, ensuring optimal performance, security, and efficiency.\n\nWith features like automated update checks, verbose log files, and user consent control, PatchNova empowers users to stay ahead of the curve in maintaining a secure and up-to-date computing environment."
            return self.create_custom_dialog(title, text, 500,400)


    def setup_logging(self):
        # CREATE A LOGGER
        self.logger.setLevel(logging.DEBUG)
        # CREATE A FORMATTER AND ADD IT TO THE HANDLER
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # CREATE A ROTATING FILE HANDLER FOR UPDATE HISTORY
        self.history_handler = RotatingFileHandler("update_history.log", maxBytes=1024 * 1024, backupCount=5)
        self.history_handler.setLevel(logging.INFO)
        self.history_handler.setFormatter(formatter)
        self.logger.addHandler(self.history_handler)
        # CREATE A ROTATING FILE HANDLER FOR ERRORS
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
        # self.get_hardware_info()
        get_update_consent = get_user_consent("Do you want to install your system updates?")
        if get_update_consent:
            doublecheck_update_consent = get_user_consent("Are you sure?")
            # DOUBLE-CHECK USER CONSENT
            if doublecheck_update_consent:
                # CHECK IF PLATFORM IS WINDOWS
                if platform.system() == 'Windows':
                    # TRIGGER WINDOWS UPDATES
                    subprocess.run(["powershell", "Install-Module PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser"])
                    # CHECK IF ADMIN OR ELEVATE PRIVS
                    if is_admin():
                        self.logger.info("Windows update is running as admin user")
                        command = "Get-WindowsUpdate -Install -AcceptAll"
                        os.system(f'powershell -Command "{command}"')
                    else:
                        # RE-RUN THE SCRIPT WITH ADMIN RIGHTS
                        self.logger.info("Windows update is elevating privileges as admin user")
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                        self.logger.info("Windows update is running as admin user")
                    self.logger.info("Windows Update completed")
                # CHECK IF PLATFORM IS MAC
                elif platform.system() == 'Darwin':
                    # TRIGGER MACOS UPDATE
                    subprocess.run(["softwareupdate", "-i", "-a"])
                    self.logger.info("macOS Update completed")
                # CHECK IF PLATFORM IS LINUX
                elif platform.system() == 'Linux':
                    # USE DISTRO.ID() TO GET THE DISTRIBUTION ID AS A STRING
                    dist_id = distro.id()
                    update_command = ""
                    if "ubuntu" in dist_id or "debian" in dist_id:
                        subprocess.run(["sudo", "apt-get", "update"])
                        update_command = "sudo apt-get upgrade -y"
                    elif "fedora" in dist_id or "centos" in dist_id:
                        update_command = "sudo dnf update"
                    else:
                        self.create_custom_dialog("Linux Update Information",
                                                "Your Linux distribution is not supported for automatic updates through this script.",
                                                500,200)
                        self.logger.error("The Linux distribution is not supported for automatic updates through this script")
                        return
                    self.create_custom_dialog("Update Information", "System update complete.",
                                              500,100)
                    self.logger.info(f"Linux update completed for: {dist_id}")
                    # RUN THE UPDATE COMMAND IN THE TERMINAL
                    subprocess.run(update_command.split())
                else:
                    self.create_custom_dialog("Unsupported System",
                                            "Updates are not supported for the current operating system.",
                                            500,200)
                    self.logger.error("Updates are not supported for the current operating system")
                self.logger.info("Update process completed.")
            
            else:
                self.create_custom_dialog("User Does Not Consent",
                                                "Understood. PatchNova will not install any updates on your system.",
                                                500,200)
                self.logger.info("User cancelled update installation process")


if __name__ == "__main__":
    image_path = "assets/PatchNovaLogo2.png"
    root = tk.Tk()
    set_background_with_label(root, image_path)
    app = UpdateCheckerApp(root)
    root.mainloop()
