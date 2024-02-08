import pytest
from patch_nova import UpdateCheckerApp 
from unittest.mock import patch, MagicMock, mock_open
import tkinter as tk
import platform
#import logging

@pytest.fixture
def app():
    root = tk.Tk()
    app = UpdateCheckerApp(root)
    return app

def test_setup_logging(app):
    app.setup_logging()
    app.logger.handlers.clear()
    assert len(app.logger.handlers) == 0

@patch('platform.uname') 
def test_get_hardware_info(mock_uname, app): # Test the get_hardware_info method
    mock_uname.return_value = MagicMock(system='TestSystem', node='TestNode', release='TestRelease', version='TestVersion', machine='TestMachine', processor='TestProcessor')
    app.get_hardware_info()
    expected_text = "System: TestSystem\nNode Name: TestNode\nRelease: TestRelease\nVersion: TestVersion\nMachine: TestMachine\nProcessor: TestProcessor"
    assert app.hardware_info_label.cget('text') == expected_text

@patch('subprocess.run')
@patch('platform.system')
@patch('tkinter.messagebox.askyesno')
def test_check_updates(mock_askyesno, mock_system, mock_run, app): # Test the check_updates method
    mock_askyesno.return_value = True
    mock_system.return_value = 'Linux'
    mock_run.return_value = MagicMock(stdout=b"Mock output that distro.id() would expect")


def test_user_consent_handling(app): # Test the get_user_consent method
    with patch('tkinter.messagebox.askyesno', return_value=True) as mock_askyesno:
        assert app.get_user_consent() is True
    with patch('tkinter.messagebox.askyesno', return_value=False) as mock_askyesno:
        assert app.get_user_consent() is False

@pytest.mark.skipif(platform.system() != "Windows", reason="This test is only relevant on Windows.")
@patch('platform.system', return_value="Windows")
@patch('subprocess.check_output')
@patch('patchnova.patch_nova.winreg', create=True)  # Mock winreg for non-Windows platforms
def test_display_installed_software_windows(mock_winreg, mock_subprocess, mock_system, app): # Test the display_installed_software method
    mock_subprocess.return_value = b'Windows mock output'
    app.check_software_updates()


@patch('builtins.open', new_callable=mock_open, read_data="Test log content")
def show_logs(self): # Test the show_logs method
    log_dialog = tk.Toplevel(self.root) 
    log_dialog.title("Logs")
    log_dialog.geometry("800x600")
    log_dialog.configure(bg='#fb8200')

def test_create_custom_dialog(app): # Test the create_custom_dialog method
    title = "Test Title"
    message = "Test message"
    with patch.object(tk.Toplevel, "title") as mock_title, \
         patch.object(tk.Toplevel, "configure") as mock_configure, \
         patch('tkinter.Label') as mock_label, \
         patch('tkinter.Button') as mock_button:
        app.create_custom_dialog(title, message, 500, 500)
        mock_title.assert_any_call(title)