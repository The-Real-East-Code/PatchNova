import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar
import platform
import subprocess
import distro
import logging
from logging.handlers import RotatingFileHandler
import pkgutil
import platform
if platform.system() == 'Windows':
    import winreg
from bs4 import BeautifulSoup
import urllib.request



class UpdateCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Checker")
        
        # Increase the initial size of the main window
        self.root.geometry('800x400')  # Adjust width and height as needed
        self.root.configure(bg='#333333')  # Dark background for the main window
        
        # Enhanced font and color configuration for larger UI elements
        self.font_style = ("Consolas", 14)  # Increase font size
        self.button_color = "#15065c"
        self.text_color = "#FFFFFF" 
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#333333"

        self.setup_logging()

        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding

        # Loading indicator
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        
        # Status label
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)

        # Larger buttons with increased padding
        self.check_updates_button = tk.Button(root, text="Check for Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.check_software_updates_button = tk.Button(root, text="Check Software Updates", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.check_browser_updates_button = tk.Button(root, text="Check Browser Updates", command=self.check_browser_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_browser_updates_button.pack(pady=10)  # Increase vertical padding
        
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
    
    def show_loading_indicator(self):
        self.loading_indicator.pack(pady=10)
        self.loading_indicator.start()

    def hide_loading_indicator(self):
        self.loading_indicator.stop()
        self.loading_indicator.pack_forget()

    def update_status_label(self, text):
        self.status_label.config(text=text)
        self.status_label.pack(pady=10)

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
            update_info_div = soup.find('div', class_='release-info')

            if update_info_div:
                update_info = update_info_div.text
                self.create_custom_dialog("iOS Update Information", update_info)
                self.logger.info("iOS Update checked")
            else:
                self.create_custom_dialog("iOS Update Information", "Unable to find update information on the webpage.")
                self.logger.warning("iOS Update information not found on the webpage.")

    def check_browser_updates(self):
        # Check for updates on Firefox and Chrome
        self.perform_browser_update_check("firefox", "https://www.mozilla.org/en-US/firefox/releases/")
        self.perform_browser_update_check("chrome", "https://chromereleases.googleblog.com/")
        
    def perform_browser_update_check(self, browser_name, update_url):
        try:
            # Show loading indicator
            self.show_loading_indicator()
            
            # Update status label
            self.update_status_label(f"Checking updates for {browser_name}...")

            with urllib.request.urlopen(update_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')

                # Customize this part based on the structure of the webpage containing update information
                version_tag = soup.find('div', class_='version')  # Adjust based on the actual HTML structure

                if version_tag:
                    latest_version = version_tag.text.strip()
                    messagebox.showinfo(f"{browser_name.capitalize()} Update", f"Update available for {browser_name}: {latest_version}")
                    self.logger.info(f"{browser_name.capitalize()} Update checked")
                else:
                    messagebox.showinfo(f"{browser_name.capitalize()} Update", f"No update information found for {browser_name}")
                    self.logger.warning(f"No update information found for {browser_name}")
        except Exception as e:
            messagebox.showinfo(f"Error", f"Error occurred while checking updates for {browser_name}: {str(e)}")
            self.logger.error(f"Error occurred while checking updates for {browser_name}: {str(e)}")
        finally:
            # Hide loading indicator and clear status label
            self.hide_loading_indicator()
            self.update_status_label("")
            

    def check_updates(self):
        self.get_hardware_info()
        if self.get_user_consent():
            # Check for updates based on the user's operating system
            if platform.system() == 'Windows':
                # Trigger Windows Update
                subprocess.run(["powershell", "Install-Module PSWindowsUpdate -Force -AllowClobber"])
                subprocess.run(["powershell", "Get-WindowsUpdate -Install -AcceptAll"])
                self.logger.info("Windows Update checked")

                # Check for updates on Firefox and Chrome
                self.check_browser_updates("firefox", "https://www.mozilla.org/en-US/firefox/releases/")
                self.check_browser_updates("chrome", "https://chromereleases.googleblog.com/")

            elif platform.system() == 'Darwin':
                # Trigger macOS Update
                subprocess.run(["softwareupdate", "-i", "-a"])
                self.logger.info("macOS Update checked")

                # Check for updates on Firefox and Chrome
                self.check_browser_updates("firefox", "https://www.mozilla.org/en-US/firefox/releases/")
                self.check_browser_updates("chrome", "https://chromereleases.googleblog.com/")

                
            elif platform.system() == 'Linux':
                # Use distro.id() to get the distribution ID as a string
                dist_id = distro.id()
                update_command = ""
                if "ubuntu" in dist_id or "debian" in dist_id:
                    update_command = "sudo apt-get update && sudo apt-get upgrade -y"
                elif "fedora" in dist_id or "centos" in dist_id:
                    update_command = "sudo dnf update -y"
                elif "arch" in dist_id:
                    update_command = "sudo pacman -Syu"
                else:
                    self.create_custom_dialog("Linux Update Information", "Your Linux distribution is not supported for automatic updates through this script.")
                    return
                self.create_custom_dialog("Update Information", f"For your system ({dist_id}), use the following command to update:\n{update_command}")
                self.logger.info(f"Linux Update Information provided for {dist_id}")
                # Run the update command in the terminal
                subprocess.run(update_command.split())

                # Check for updates on Firefox and Chrome
                self.check_browser_updates("firefox", "https://www.mozilla.org/en-US/firefox/releases/")
                self.check_browser_updates("chrome", "https://chromereleases.googleblog.com/")

            else:
                self.create_custom_dialog("Unsupported System", "Updates are not supported for the current operating system.")
            self.logger.info("Update process completed.")


    def check_software_updates(self):
        # Get installed programs from registry
        installed_programs = {}
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                key = winreg.EnumKey(reg_key, i)
                val = winreg.OpenKey(reg_key, key)
                name = winreg.QueryValueEx(val, "DisplayName")[0]
                version = winreg.QueryValueEx(val, "DisplayVersion")[0]
                installed_programs[name] = version
            except OSError:
                pass

        # Create popup 
        popup = tk.Toplevel(self.root)
        listbox = Listbox(popup)
        listbox.pack()

        # Check updates
        for name, version in installed_programs.items():
            update = self.check_update(name)  # Use self.check_update
            if update:
                listbox.insert(tk.END, f"{name}: {version} -> {update}")

        # Add scrollbar
        scrollbar = Scrollbar(popup, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

    def check_update(self, name):  # Define check_update within the class
        # Check website, API, etc and return latest version
        return "2.0"

    def choose_log_location(self):
        log_location = filedialog.askdirectory()
        if log_location:
            # Update log file locations
            self.history_handler.baseFilename = f"{log_location}/update_history.log"
            self.error_handler.baseFilename = f"{log_location}/error_log.log"
            self.create_custom_dialog("Log Location Updated", f"Log files will be saved in: {log_location}")
            

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
