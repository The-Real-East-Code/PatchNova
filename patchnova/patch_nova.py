import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # For improved styling capabilities
import platform
import urllib.request
import webbrowser
import pkg_resources
import logging
import subprocess
import distro
from bs4 import BeautifulSoup
from logging.handlers import RotatingFileHandler

class UpdateCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Checker")
        
        # Increase the initial size of the main window
        self.root.geometry('800x400')  # Adjust width and height as needed
        self.root.configure(bg='#333333')  # Dark background for the main window
        
        # Enhanced font and color configuration for larger UI elements
        self.font_style = ("Arial", 14)  # Increase font size
        self.button_color = "#4609d4"
        self.text_color = "#FFFFFF"
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#333333"
        
        # Initialize logging
        self.setup_logging()
        
        # Display hardware information with increased padding
        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding
        
        # Larger buttons with increased padding
        self.check_updates_button = tk.Button(root, text="Check for Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.check_software_updates_button = tk.Button(root, text="Check Software Updates", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.choose_log_location_button = tk.Button(root, text="Choose Log Location", command=self.choose_log_location, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.choose_log_location_button.pack(pady=10)  # Increase vertical padding


    def create_custom_dialog(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='#333333')  # Dark background for dialog
        dialog.geometry("600x400")  # Adjust size as needed
        
        # Message label
        message_label = tk.Label(dialog, text=message, wraplength=350, bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        message_label.pack(padx=10, pady=10)
        
        # Close button
        close_button = tk.Button(dialog, text="Close", command=dialog.destroy, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        close_button.pack(pady=10)
    
    
    def create_custom_dialog(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x400")  # Adjust size as needed

        # Message label
        message_label = tk.Label(dialog, text=message, wraplength=350)  # Wrap text to fit the dialog
        message_label.pack(padx=10, pady=10)

        # Close button
        close_button = tk.Button(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=10)


    def setup_logging(self):
        # Create a logger
        self.logger = logging.getLogger("UpdateCheckerApp")
        self.logger.setLevel(logging.DEBUG)
        # Create a formatter and add it to the handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # Create a rotating file handler for update history
        self.history_handler = RotatingFileHandler("update_history.log", maxBytes=1024*1024, backupCount=5)
        self.history_handler.setLevel(logging.INFO)
        self.history_handler.setFormatter(formatter)
        self.logger.addHandler(self.history_handler)
        # Create a rotating file handler for errors
        self.error_handler = RotatingFileHandler("error_log.log", maxBytes=1024*1024, backupCount=5)
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
        return messagebox.askyesno("User Consent", "Do you want to check for updates?")
    
    
    def web_scrape_for_windows_updates(self):
        # Web scraping logic for Windows updates
        windows_update_url = "https://support.microsoft.com/en-us/windows/release-information"
        with urllib.request.urlopen(windows_update_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            update_info = soup.find('div', class_='release-info').text
            self.create_custom_dialog("Windows Update Information", update_info)
            self.logger.info("Windows Update checked")
    
    
    def web_scrape_for_ios_updates(self):
        # Web scraping logic for iOS updates
        ios_update_url = "https://support.apple.com/en-us/HT201222"
        with urllib.request.urlopen(ios_update_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            update_info = soup.find('div', class_='release-info').text
            self.create_custom_dialog("iOS Update Information", update_info)
            self.logger.info("iOS Update checked")
    
    
    def check_updates(self):
        self.get_hardware_info()
        if self.get_user_consent():
            # Check for updates based on the user's operating system
            if platform.system() == 'Windows':
                self.web_scrape_for_windows_updates()
            elif platform.system() == 'Darwin':  # 'Darwin' is the system name for macOS
                self.web_scrape_for_ios_updates()
            elif platform.system() == 'Linux':
                # Use distro.id() to get the distribution ID as a string
                dist_id = distro.id()
                update_command = ""
                if "ubuntu" in dist_id or "debian" in dist_id:
                    update_command = "sudo apt-get update && sudo apt-get upgrade -y"
                elif "fedora" in dist_id or "centos" in dist_id:
                    update_command = "sudo dnf update -y"  # Note: CentOS has shifted to using dnf in its latest versions
                elif "arch" in dist_id:
                    update_command = "sudo pacman -Syu"
                else:
                    self.create_custom_dialog("Linux Update Information", "Your Linux distribution is not supported for automatic updates through this script.")
                    return

                self.create_custom_dialog("Linux Update Command", f"For your system ({dist_id}), use the following command to update:\n{update_command}")
                self.logger.info(f"Linux Update Command provided for {dist_id}")
            else:
                self.create_custom_dialog("Unsupported System", "Updates are not supported for the current operating system.")

            # Optionally open the default web browser with the update page for Windows and macOS
            if platform.system() == 'Windows' or platform.system() == 'Darwin':
                open_browser = messagebox.askyesno("Open Browser", "Do you want to open the update page in your browser?")
                if open_browser:
                    webbrowser.open("https://support.microsoft.com/en-us/windows/release-information"
                                    if platform.system() == 'Windows'
                                    else "https://support.apple.com/en-us/HT201222")

    
    
    def check_software_updates(self):
        # Get a list of installed Python packages
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        # You would need to customize this part based on the structure of the update information for your software
        # Here, we are assuming that the update information is available on PyPI
        for package_name, installed_version in installed_packages.items():
            # Check PyPI for updates
            pypi_url = f"https://pypi.org/project/{package_name}/"
            with urllib.request.urlopen(pypi_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                latest_version_tag = soup.find('span', class_='css-1rzqfyi')
                if latest_version_tag:
                    latest_version = latest_version_tag.text.strip()
                    if installed_version < latest_version:
                        self.create_custom_dialog("Software Update", f"Update available for {package_name}: {installed_version} -> {latest_version}")
                        self.logger.info(f"Software Update checked for {package_name}")
                    else:
                        self.create_custom_dialog("Software Update", f"{package_name} is up to date.")
                        self.logger.info(f"{package_name} is up to date")
    
    
    def choose_log_location(self):
        log_location = filedialog.askdirectory()
        if log_location:
            # Update log file locations
            self.history_handler.baseFilename = f"{log_location}/update_history.log"
            self.error_handler.baseFilename = f"{log_location}/error_log.log"
            self.create_custom_dialog("Log Location Updated", f"Log files will be saved in: {log_location}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateCheckerApp(root)
    root.mainloop()