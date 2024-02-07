import subprocess
import platform
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar, Text, font

if platform.system() == 'Windows':
    import winreg

def check_software(self, root):
    if platform.system() == "Windows":
        installed_programs = get_installed_programs_windows(self)
    elif platform.system() == "Darwin":
        installed_programs = get_installed_programs_mac(self)
    elif platform.system() == "Linux":
        installed_programs = get_installed_programs_linux(self)
    else:
        print("Unsupported operating system")
        return

    # CREATE POPUP
    popup = tk.Toplevel(root)
    popup.geometry("500x600")  # Set the size of the popup window
    popup.title("Installed Software")  # Set title
    popup.configure(bg="dark gray")  # Set background color
    # CUSTOMIZE FONT STYLE FOR LISTBOX
    listbox_font = font.Font(family="Helvetica", size=12, weight="bold")
    listbox = Listbox(popup, font=listbox_font, bg="gray", fg="blue")  # Set font, background color, and foreground color
    listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Expand to fill the popup window, add padding

    # CHECK UPDATES
    for name, version in installed_programs.items():
        listbox.insert(tk.END, f"{name}: {version}")

    # ADD SCROLLBAR
    scrollbar = Scrollbar(popup, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)


def get_installed_programs_windows(self):
    installed_programs = {}
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg_key:
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    key = winreg.EnumKey(reg_key, i)
                    with winreg.OpenKey(reg_key, key) as val:
                        name = winreg.QueryValueEx(val, "DisplayName")[0]
                        version = winreg.QueryValueEx(val, "DisplayVersion")[0]
                        installed_programs[name] = version
                except OSError:
                    pass
    except FileNotFoundError:
        pass
    return installed_programs


def get_installed_programs_mac(self):
    installed_programs = {}
    try:
        output = subprocess.check_output(["/usr/sbin/system_profiler", "SPApplicationsDataType", "-xml"])
        soup = BeautifulSoup(output, features='xml')

        for item in soup.find_all('dict'):
            name_tag = item.find('key', string='_name')
            version_tag = item.find('key', string='version')

            if name_tag and version_tag:
                name = name_tag.find_next('string').text
                version = version_tag.find_next('string').text
                installed_programs[name] = version
    except subprocess.CalledProcessError:
        pass
    return installed_programs


def get_installed_programs_linux(self):
    installed_programs = {}
    try:
        list_packages_command = "apt list --upgradable"
        output = subprocess.check_output(list_packages_command.split())
        output = output.decode("utf-8").split("\n")
        i = 1
        for item in output:
            if item != "Listing..." and item != '':
                index = i
                name = item
                installed_programs[index] = name
                i += 1
    except subprocess.CalledProcessError:
        pass
    return installed_programs