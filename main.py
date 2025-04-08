import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class OculusUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("upToQuest")
        
        # Variables
        self.firmware_path = tk.StringVar()
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for firmware path
        tk.Label(self.root, text="Firmware File (.zip):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.firmware_entry = tk.Entry(self.root, textvariable=self.firmware_path, width=50)
        self.firmware_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_firmware).grid(row=0, column=2, padx=10, pady=5)

        # Button to check device connection in sideload mode
        tk.Button(self.root, text="Check Sideload Connection", command=self.check_sideload_connection).grid(row=2, column=1, pady=10)

        # Button to start update process
        tk.Button(self.root, text="Start Update", command=self.start_update).grid(row=3, column=1, pady=20)

    def browse_firmware(self):
        """Open file dialog to select the firmware .zip file."""
        file_path = filedialog.askopenfilename(
            title="Select Firmware File",
            filetypes=[("ZIP files", "*.zip")]
        )
        if file_path:
            self.firmware_path.set(file_path)

    def check_sideload_connection(self):
        """Check if the device is connected in sideload mode."""
        if not self.check_adb_installed():
            return

        try:
            result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            devices = result.stdout.decode().strip().split("\n")[1:]
            sideload_device = any("sideload" in d for d in devices)
            if sideload_device:
                messagebox.showinfo("Success", "Device is connected in sideload mode.")
            else:
                messagebox.showwarning("Warning", "No device detected in sideload mode. Please ensure your Oculus is in sideload mode.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect devices: {e}")

    def start_update(self):
        """Initiate the firmware update process."""
        firmware_file = self.firmware_path.get()
        if not firmware_file or not firmware_file.endswith(".zip"):
            messagebox.showerror("Error", "Please select a valid .zip firmware file.")
            return

        # Check if ADB is installed
        if not self.check_adb_installed():
            return

        # Check if device is connected in sideload mode
        if not self.check_device_in_sideload_mode():
            return

        # Start the update process
        try:
            self.run_adb_command(f"sideload {firmware_file}")
            messagebox.showinfo("Success", "Firmware update completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the update: {e}")

    def check_adb_installed(self):
        """Check if ADB is installed on the system."""
        try:
            result = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if "Android Debug Bridge" in result.stdout.decode():
                return True
            else:
                messagebox.showerror("Error", "ADB is not installed or not in PATH. Please install ADB and try again.")
                return False
        except FileNotFoundError:
            messagebox.showerror("Error", "ADB is not installed or not in PATH. Please install ADB and try again.")
            return False

    def check_device_in_sideload_mode(self):
        """Check if the device is connected in sideload mode."""
        try:
            result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            devices = result.stdout.decode().strip().split("\n")[1:]
            if any("sideload" in d for d in devices):
                return True
            else:
                messagebox.showwarning("Warning", "No device detected in sideload mode. Please ensure your Oculus is in sideload mode.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect devices: {e}")
            return False

    def run_adb_command(self, command):
        """Run an ADB command."""
        full_command = ["adb"] + command.split()
        try:
            subprocess.run(full_command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ADB command failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OculusUpdaterApp(root)
    root.mainloop()