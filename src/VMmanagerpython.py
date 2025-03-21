import tkinter as tk
from tkinter import font as tkfont  # Add this import
from tkinter import simpledialog, messagebox, filedialog, ttk, colorchooser
import tkinter.messagebox as messagebox
import subprocess
import os
from datetime import datetime
import threading
import socket
import time
import sys
import json
import csv
import shutil
from styles import MenuStyle  # Add this import at the top
from tag_sidebar import TagSidebar
from tag_manager import TagManager

THEMES = {
    "dark": {
        "primary_bg": "#133951",
        "secondary_bg": "#274156",
        "button_bg": "#557080",
        "header_bg": "#133951",  # Dark header color
        "text": "#FFFFFF",
        "hover_active": "#D1B278",
        "borders": "#BD9865"
    },
    "light": {
        "primary_bg": "#F0F7FF",    # Very light blue background
        "secondary_bg": "#E8F4F9",   # Soft sky blue for sidebar
        "button_bg": "#89CFF0",      # Bright baby blue for buttons
        "header_bg": "#CCE8FF",      # Light azure blue header
        "text": "#2B4B6F",           # Deep blue text for contrast
        "hover_active": "#7AB8E0",   # Slightly darker blue for hover
        "borders": "#B4D8F0"         # Medium blue for borders
    },
    "light_origina": {
        "primary_bg": "#F8FAFF",    # Very subtle blue-white for main background
        "secondary_bg": "#F0F4F8",   # Lighter blue-gray for sidebar
        "button_bg": "#7BA9D0",      # Lighter blue for buttons
        "header_bg": "#EDF5FC",      # Pale blue header
        "text": "#2C3E50",           # Dark blue-gray for text
        "hover_active": "#6798C0",   # Slightly darker blue for hover
        "borders": "#7BA9D0"         # Matching blue for borders
    },
    "blue_dark": {
        "primary_bg": "#1a2733",
        "secondary_bg": "#243442",
        "button_bg": "#2d4052",
        "header_bg": "#1a2733",
        "text": "#ffffff",
        "hover_active": "#385167",
        "borders": "#385167"
    },
    "blue_light": {
        "primary_bg": "#f0f4f8",
        "secondary_bg": "#e1e8f0",
        "button_bg": "#d1dde8",
        "header_bg": "#f0f4f8",
        "text": "#1a2733",
        "hover_active": "#b8c9d9",
        "borders": "#b8c9d9"
    },
    "light_colorful": {
        "primary_bg": "#F0F7FF",    # Very light blue background
        "secondary_bg": "#E8F4F9",   # Soft sky blue for sidebar
        "button_bg": "#89CFF0",      # Bright baby blue for buttons
        "header_bg": "#CCE8FF",      # Light azure blue header
        "text": "#2B4B6F",           # Deep blue text for contrast
        "hover_active": "#7AB8E0",   # Slightly darker blue for hover
        "borders": "#B4D8F0"         # Medium blue for borders
    },
    "light_nature": {
        "primary_bg": "#F8FFF5",    # Very light mint background
        "secondary_bg": "#EFF8E8",   # Soft sage for sidebar
        "button_bg": "#9ED5A5",      # Fresh mint green for buttons
        "header_bg": "#DDEEDD",      # Light sage header
        "text": "#2F5241",           # Forest green text for contrast
        "hover_active": "#8BC495",   # Slightly darker mint for hover
        "borders": "#BCE5C0"         # Medium mint for borders
    },
    "light_warm": {
        "primary_bg": "#FFF9F5",    # Very light peach background
        "secondary_bg": "#F9F0E8",   # Soft cream for sidebar
        "button_bg": "#FFB6A3",      # Coral pink for buttons
        "header_bg": "#FFE4D6",      # Light peach header
        "text": "#6B4F4F",           # Warm brown text for contrast
        "hover_active": "#FFA088",   # Darker coral for hover
        "borders": "#FFD0BE"         # Medium peach for borders
    }





}

class FileManager:
    """Manages all file operations and data storage for the application.
    Handles reading/writing of machine data, settings, categories, and tags."""
    def __init__(self):
        self.data_dir = self._get_data_directory()
        self.pc_file_path = os.path.join(self.data_dir, "pcs.txt")
        self.last_used_file_path = os.path.join(self.data_dir, "last_used.txt")
        self.descriptions_file_path = os.path.join(self.data_dir, "descriptions.txt")
        self.settings_file_path = os.path.join(self.data_dir, "settings.txt")
        self.machine_rdp_file_path = os.path.join(self.data_dir, "machine_rdp.txt")
        self.categories_file_path = os.path.join(self.data_dir, "categories.txt")
        self.machine_categories_file_path = os.path.join(self.data_dir, "machine_categories.txt")
        self.tags_file_path = os.path.join(self.data_dir, "tags.txt")
        self.machine_tags_file_path = os.path.join(self.data_dir, "machine_tags.txt")
        self.machine_ips_file = os.path.join(self.data_dir, "machine_ips.txt")

    def _get_data_directory(self):
        """Get the data directory path from settings or use default"""
        # First check if there's a settings.txt in the same directory as the executable
        exe_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        exe_settings_path = os.path.join(exe_dir, "settings.txt")
        
        # Then check the default location in LOCALAPPDATA
        default_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "VmManager")
        default_settings_path = os.path.join(default_data_dir, "settings.txt")
        
        # Try to read settings from executable directory first, then default location
        for settings_path in [exe_settings_path, default_settings_path]:
            if os.path.exists(settings_path):
                try:
                    with open(settings_path, "r") as f:
                        for line in f:
                            if line.startswith("data_dir="):
                                data_dir = line.split("=")[1].strip()
                                if os.path.exists(data_dir):
                                    return data_dir
                except Exception as e:
                    print(f"Error reading settings from {settings_path}: {str(e)}")
        
        # If no valid settings found, use and create default
        os.makedirs(default_data_dir, exist_ok=True)
        with open(default_settings_path, "w") as f:
                f.write(f"data_dir={default_data_dir}\n")
        
        return default_data_dir  # Fixed indentation here

    def load_pcs(self):
        if os.path.exists(self.pc_file_path):
            with open(self.pc_file_path, "r") as file:
                return file.read().splitlines()
        return []

    def save_pcs(self, pc_names):
        with open(self.pc_file_path, "w") as file:
            for pc in pc_names:
                file.write(pc + "\n")

    def load_last_used_times(self):
        if os.path.exists(self.last_used_file_path):
            with open(self.last_used_file_path, "r") as file:
                return dict(line.strip().split(":", 1) for line in file)
        return {}

    def save_last_used_times(self, last_used_times):
        with open(self.last_used_file_path, "w") as file:
            for pc, time in last_used_times.items():
                file.write(f"{pc}:{time}\n")

    def load_descriptions(self):
        if os.path.exists(self.descriptions_file_path):
            with open(self.descriptions_file_path, "r") as file:
                return dict(line.strip().split(":", 1) for line in file)
        return {}

    def save_descriptions(self, descriptions):
        with open(self.descriptions_file_path, "w") as file:
            for pc, description in descriptions.items():
                file.write(f"{pc}:{description}\n")

    def load_machine_rdp_paths(self):
        if os.path.exists(self.machine_rdp_file_path):
            with open(self.machine_rdp_file_path, "r") as file:
                return dict(line.strip().split(":", 1) for line in file)
        return {}

    def save_machine_rdp_paths(self, machine_rdp_paths):
        with open(self.machine_rdp_file_path, "w") as file:
            for pc, rdp_path in machine_rdp_paths.items():
                file.write(f"{pc}:{rdp_path}\n")

    def update_paths(self):
        """Update all file paths when data directory changes"""
        self.pc_file_path = os.path.join(self.data_dir, "pcs.txt")
        self.last_used_file_path = os.path.join(self.data_dir, "last_used.txt")
        self.descriptions_file_path = os.path.join(self.data_dir, "descriptions.txt")
        self.settings_file_path = os.path.join(self.data_dir, "settings.txt")
        self.machine_rdp_file_path = os.path.join(self.data_dir, "machine_rdp.txt")

    def load_categories(self):
        """Load categories from file"""
        categories = ["Default"]  # Always ensure Default exists
        
        if os.path.exists(self.categories_file_path):
            try:
                with open(self.categories_file_path, "r") as file:
                    file_categories = [line.strip() for line in file]
                    if file_categories:  # If we got categories from file
                        if "Default" not in file_categories:
                            file_categories.insert(0, "Default")
                        categories = file_categories
            except Exception as e:
                print(f"Error loading categories: {str(e)}")
                # Return default list if there's an error
                return ["Default"]
        
        # If the file didn't exist, create it with the default category
        else:
            try:
                os.makedirs(os.path.dirname(self.categories_file_path), exist_ok=True)
                with open(self.categories_file_path, "w") as file:
                    file.write("Default\n")
            except Exception as e:
                print(f"Error creating categories file: {str(e)}")
        
        return categories

    def save_categories(self, categories):
        """Save categories to file"""
        with open(self.categories_file_path, "w") as file:
            for category in categories:
                file.write(f"{category}\n")

    def load_machine_categories(self):
        """Load machine category assignments"""
        if os.path.exists(self.machine_categories_file_path):
            with open(self.machine_categories_file_path, "r") as file:
                return dict(line.strip().split(":", 1) for line in file)
        return {}

    def save_machine_categories(self, machine_categories):
        """Save machine category assignments"""
        with open(self.machine_categories_file_path, "w") as file:
            for machine, category in machine_categories.items():
                file.write(f"{machine}:{category}\n")

    def load_tags(self):
        """Load all existing tags"""
        if os.path.exists(self.tags_file_path):
            with open(self.tags_file_path, "r") as file:
                return [line.strip() for line in file.readlines()]
        return []

    def save_tags(self, tags):
        """Save all tags"""
        with open(self.tags_file_path, "w") as file:
            for tag in tags:
                file.write(f"{tag}\n")

    def load_machine_tags(self):
        """Load machine-tag assignments"""
        machine_tags = {}
        if os.path.exists(self.machine_tags_file_path):
            with open(self.machine_tags_file_path, "r") as file:
                for line in file:
                    machine, tags = line.strip().split(":", 1)
                    machine_tags[machine] = tags.split(",") if tags else []
        return machine_tags

    def save_machine_tags(self, machine_tags):
        """Save machine-tag assignments"""
        with open(self.machine_tags_file_path, "w") as file:
            for machine, tags in machine_tags.items():
                file.write(f"{machine}:{','.join(tags)}\n")

    def save_category_colors(self, category_colors):
        """Save category colors to file"""
        with open(os.path.join(self.data_dir, 'category_colors.json'), 'w') as f:
            json.dump(category_colors, f)

    def load_category_colors(self):
        """Load category colors from file"""
        try:
            with open(os.path.join(self.data_dir, 'category_colors.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  # Return empty dict if file doesn't exist

    def load_machine_ips(self):
        """Load stored machine IPs"""
        if os.path.exists(self.machine_ips_file):
            try:
                with open(self.machine_ips_file, "r") as f:
                    return {line.split('=')[0]: line.split('=')[1].strip() 
                           for line in f if '=' in line}
            except Exception:
                return {}
        return {}

    def save_machine_ips(self, machine_ips):
        """Save machine IPs"""
        try:
            with open(self.machine_ips_file, "w") as f:
                for pc_name, ip in machine_ips.items():
                    f.write(f"{pc_name}={ip}\n")
        except Exception as e:
            print(f"Error saving machine IPs: {str(e)}")

    # ... other file operations ...

class SettingsManager:
    """Manages application settings and RDP configuration.
    Ensures required settings exist and handles default configurations."""
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.settings = self.load_settings()
        self.ensure_rdp_path()

    def load_settings(self):
        if os.path.exists(self.file_manager.settings_file_path):
            with open(self.file_manager.settings_file_path, "r") as file:
                settings = dict(line.strip().split("=", 1) for line in file)
        else:
            settings = {}

        # Ensure default for rdp_path if not set
        if "rdp_path" not in settings:
            settings["rdp_path"] = ""
        
        return settings

    def save_settings(self):
        with open(self.file_manager.settings_file_path, "w") as file:
            for key, value in self.settings.items():
                file.write(f"{key}={value}\n")

    def ensure_rdp_path(self):
        if not self.settings["rdp_path"]:
            messagebox.showinfo("RDP File Path Required", "Please select the path to the RDP file.")
            rdp_path = filedialog.askopenfilename(
                title="Select RDP File", 
                filetypes=(("RDP Files", "*.rdp"), ("All Files", "*.*"))
            )
            if rdp_path:
                self.settings["rdp_path"] = rdp_path
                self.save_settings()
            else:
                messagebox.showerror("Error", "RDP file path not set. The application cannot proceed.")
                # Since we're in the initialization phase, we need to exit the application
                sys.exit(1)

    # ... other settings methods ...

class VMManager:
    """Core application logic for managing virtual machines.
    Handles machine status, connections, categories, and tags."""
    def __init__(self):
        self.file_manager = FileManager()
        self.settings_manager = SettingsManager(self.file_manager)
        self.pc_names = self.file_manager.load_pcs()
        self.machine_status = {pc_name: False for pc_name in self.pc_names}
        self.last_used_times = self.file_manager.load_last_used_times()
        self.descriptions = self.file_manager.load_descriptions()
        self.machine_rdp_paths = self.file_manager.load_machine_rdp_paths()
        self.connected_machines = set()  # Track connected machines
        self.categories = self.file_manager.load_categories()
        self.machine_categories = self.file_manager.load_machine_categories()
        self.cleanup_temp_rdp_files()  # Clean up old temporary RDP files
        self.tags = self.file_manager.load_tags()
        self.machine_tags = self.file_manager.load_machine_tags()
        self.active_tag_filters = set()  # Add this to track multiple selected tags
        self.category_colors = self.file_manager.load_category_colors()  # Add this line
        self.machine_ips = self.file_manager.load_machine_ips()  # Add this line

    def connect_to_pc(self, pc_name):
        """Connect to a PC with IP verification"""
        try:
            # Verify IP before connecting
            try:
                current_ip = socket.gethostbyname(pc_name)
                stored_ip = self.machine_ips.get(pc_name)
                
                if stored_ip and stored_ip != current_ip:
                    # IP has changed
                    if not messagebox.askyesno(
                        "IP Changed",
                        f"Warning: {pc_name}'s IP has changed!\n"
                        f"Old IP: {stored_ip}\n"
                        f"New IP: {current_ip}\n\n"
                        "Do you want to connect anyway?"
                    ):
                        return False
                    
                    # Always store the current IP (whether it's new or changed)
                    self.machine_ips[pc_name] = current_ip
                    self.file_manager.save_machine_ips(self.machine_ips)
                
            except socket.gaierror:
                # Replace the old message boxes with our new DNS cache dialog
                if messagebox.askyesno(
                    "DNS Error",
                    f"Could not resolve hostname: {pc_name}\n\n"
                    "Would you like to see instructions for clearing the DNS cache?"
                ):
                    # Call the new DNS cache instructions dialog
                    self.ui.clear_dns_cache(pc_name)
                return False
                    
            rdp_file = self.machine_rdp_paths.get(pc_name, self.settings_manager.settings["rdp_path"])
            subprocess.Popen(["mstsc", rdp_file, "/v:" + pc_name])
            self.connected_machines.add(pc_name)
            self.last_used_times[pc_name] = datetime.now().strftime("%d/%m %H:%M")
            self.file_manager.save_last_used_times(self.last_used_times)
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to {pc_name}: {str(e)}")
            return False

    def check_machine_status(self, pc_name, port=3389, timeout=3):
        """Check if machine is running and verify its IP address"""
        try:
            # Get the current IP address
            current_ip = socket.gethostbyname(pc_name)
            
            # If we have a stored IP, compare it
            stored_ip = self.machine_ips.get(pc_name)
            if stored_ip and stored_ip != current_ip:
                # Just update the stored IP silently during status check
                self.machine_ips[pc_name] = current_ip
                self.file_manager.save_machine_ips(self.machine_ips)
            
            # Test connection
            with socket.create_connection((pc_name, port), timeout=timeout):
                return True
        except socket.gaierror:
            # Don't show error message during status check
            return False
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def add_pc(self, pc_name):
        """Add a new PC to the list"""
        if pc_name and pc_name not in self.pc_names:
            self.pc_names.append(pc_name)
            self.machine_status[pc_name] = False
            self.file_manager.save_pcs(self.pc_names)
            return True
        return False

    def delete_pc(self, pc_name):
        """Delete a PC from the list and remove all associated data"""
        if pc_name in self.pc_names:
            # Remove from main lists and dictionaries
            self.pc_names.remove(pc_name)
            self.machine_status.pop(pc_name, None)
            self.last_used_times.pop(pc_name, None)
            self.descriptions.pop(pc_name, None)
            self.machine_rdp_paths.pop(pc_name, None)
            
            # Remove from categories
            self.machine_categories.pop(pc_name, None)
            
            # Remove from tags
            self.machine_tags.pop(pc_name, None)
            
            # Remove from IPs
            self.machine_ips.pop(pc_name, None)
            
            # Save all changes
            self.file_manager.save_pcs(self.pc_names)
            self.file_manager.save_last_used_times(self.last_used_times)
            self.file_manager.save_descriptions(self.descriptions)
            self.file_manager.save_machine_rdp_paths(self.machine_rdp_paths)
            self.file_manager.save_machine_categories(self.machine_categories)
            self.file_manager.save_machine_tags(self.machine_tags)
            self.file_manager.save_machine_ips(self.machine_ips)
            return True
        return False

    def add_or_edit_description(self, pc_name):
        """Add or edit description for a PC"""
        current_description = self.descriptions.get(pc_name, "")
        description = simpledialog.askstring(
            "Add or Edit Description",
            f"Enter or edit description for {pc_name}:",
            initialvalue=current_description
        )
        
        if description is not None:  # None means user cancelled
            self.descriptions[pc_name] = description
            self.file_manager.save_descriptions(self.descriptions)
            return True
        return False

    def set_machine_rdp_path(self, pc_name, rdp_path):
        """Set custom RDP path for specific machine"""
        if rdp_path:
            self.machine_rdp_paths[pc_name] = rdp_path
            self.file_manager.save_machine_rdp_paths(self.machine_rdp_paths)
            messagebox.showinfo("Success", f"RDP path for {pc_name} has been updated.")
            return True
        return False

    def get_machine_status(self, pc_name):
        """Get current status of a machine"""
        return self.machine_status.get(pc_name, False)

    def get_last_used_time(self, pc_name):
        """Get last used time for a machine"""
        return self.last_used_times.get(pc_name, "Never")

    def get_description(self, pc_name):
        """Get description for a machine"""
        return self.descriptions.get(pc_name, "")

    def get_rdp_path(self, pc_name):
        """Get RDP path for a machine"""
        return self.machine_rdp_paths.get(pc_name, self.settings_manager.settings["rdp_path"])

    def add_category(self, category_name, category_color=None):
        """Add a new category"""
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            # Use gray as default if no color specified
            default_color = "#808080"
            self.category_colors[category_name] = category_color if category_color else default_color
            self.file_manager.save_categories(self.categories)
            self.file_manager.save_category_colors(self.category_colors)
            return True
        return False

    def delete_category(self, category):
        """Delete a category and its assignments"""
        if category == "Default":
            return False
            
        if category in self.categories:
            # Remove category from list
            self.categories.remove(category)
            
            # Remove all assignments of this category from machines
            for machine in list(self.machine_categories.keys()):
                if self.machine_categories[machine] == category:
                    del self.machine_categories[machine]
            
            # Save changes
            self.file_manager.save_categories(self.categories)
            self.file_manager.save_machine_categories(self.machine_categories)
            return True
        return False

    def set_machine_category(self, machine_name, category_name):
        """Assign a machine to a category"""
        if category_name in self.categories:
            self.machine_categories[machine_name] = category_name
            self.file_manager.save_machine_categories(self.machine_categories)
            return True
        return False

    def get_machines_by_category(self, category):
        """Get all machines in a category"""
        if category == "Default":
            # Return all machines for Default category
            return self.pc_names
        else:
            # For other categories, return only machines assigned to that category
            return [machine for machine, cat in self.machine_categories.items() 
                    if cat == category and machine in self.pc_names]

    def get_machine_category(self, pc_name):
        """Get the category for a machine"""
        return self.machine_categories.get(pc_name, "Default")

    def remove_machine_category(self, pc_name):
        """Remove the category assignment from a machine"""
        if self.machine_categories.get(pc_name, "Default") != "Default":
            category = self.machine_categories.get(pc_name)
            self.machine_categories[pc_name] = "Default"
            self.file_manager.save_machine_categories(self.machine_categories)
            return True
        return False

    def share_via_teams(self, pc_name):
        """Share machine via Microsoft Teams with RDP file"""
        try:
            # Get the RDP file path for this machine
            rdp_path = self.get_rdp_path(pc_name)
            
            # Create a temporary copy of the RDP file with machine-specific settings
            temp_rdp_path = self.prepare_shareable_rdp(pc_name, rdp_path)
            
            # Create the Teams deep link with URL-encoded message
            message = f"Connect to {pc_name} using Remote Desktop"
            encoded_message = message.replace(" ", "%20")
            teams_url = f"msteams:/l/chat/0/0?users=&message={encoded_message}"
            
            # Open Teams using the protocol handler
            os.startfile(teams_url)
            
            # Also open the file location so user can easily attach it in Teams
            if temp_rdp_path:
                subprocess.run(['explorer', '/select,', temp_rdp_path])
                
                messagebox.showinfo("Share via Teams", 
                    "Teams has been opened.\n"
                    "1. Select your recipient(s)\n"
                    "2. Attach the highlighted RDP file from the opened folder\n"
                    "3. Send your message")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error sharing via Teams: {str(e)}")

    def prepare_shareable_rdp(self, pc_name, source_rdp_path):
        """Prepare a shareable RDP file with machine-specific settings"""
        try:
            # Verify source RDP path exists
            if not source_rdp_path or not os.path.exists(source_rdp_path):
                messagebox.showerror("Error", 
                    "No RDP template file found.\n"
                    "Please set the RDP path in Settings first.")
                return None
            
            # Create a directory for temporary RDP files if it doesn't exist
            temp_dir = os.path.join(self.file_manager.data_dir, "temp_share")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create a new RDP file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_rdp_path = os.path.join(temp_dir, f"{pc_name}_{timestamp}.rdp")
            
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'ascii', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(source_rdp_path, 'r', encoding=encoding) as f:
                        content = f.readlines()
                    break  # If successful, break the loop
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                messagebox.showerror("Error", "Could not read the RDP file with any supported encoding.")
                return None
            
            # Write the new RDP file with UTF-8 encoding
            try:
                with open(temp_rdp_path, 'w', encoding='utf-8') as f:
                    has_full_address = False
                    for line in content:
                        # Skip any BOM or invalid characters
                        line = line.strip().replace('\ufeff', '')
                        if not line:
                            continue
                        
                        if line.startswith('full address:'):
                            f.write(f'full address:s:{pc_name}\n')
                            has_full_address = True
                        else:
                            f.write(f'{line}\n')
                    
                    if not has_full_address:
                        f.write(f'full address:s:{pc_name}\n')
                
                return temp_rdp_path
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not write RDP file: {str(e)}")
                # Clean up the temp file if we couldn't modify it
                if os.path.exists(temp_rdp_path):
                    try:
                        os.remove(temp_rdp_path)
                    except:
                        pass
                return None
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not prepare RDP file: {str(e)}")
            return None

    def share_via_email(self, pc_name):
        """Share machine via default email client with RDP file attachment"""
        try:
            # Get and prepare the RDP file
            rdp_path = self.get_rdp_path(pc_name)
            temp_rdp_path = self.prepare_shareable_rdp(pc_name, rdp_path)
            
            if temp_rdp_path:
                # Create mailto URL with machine details
                subject = f"Remote Desktop Connection - {pc_name}"
                body = (f"Connect to {pc_name} using the attached RDP file.\n\n"
                       f"Alternatively, you can connect using:\nmstsc /v:{pc_name}")
                mailto_url = f"mailto:?subject={subject}&body={body}"
                
                # First open the containing folder
                folder_path = os.path.dirname(temp_rdp_path)
                try:
                    # Try to open the folder first
                    os.startfile(folder_path)
                    
                    # Then open the email client
                    os.startfile(mailto_url)
                    
                    messagebox.showinfo("Share via Email", 
                        "1. The folder containing the RDP file has been opened\n"
                        "2. Your email client has been opened\n"
                        "3. Find the RDP file named: " + os.path.basename(temp_rdp_path) + "\n"
                        "4. Drag and drop it into your email\n"
                        "5. Send your email")
                    
                except Exception as folder_error:
                    # Fallback to explorer if os.startfile fails
                    try:
                        subprocess.run(['explorer', folder_path], check=True)
                    except:
                        messagebox.showerror("Error", 
                            f"Could not open folder. RDP file is located at:\n{temp_rdp_path}")
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error preparing share: {str(e)}")

    def copy_share_link(self, pc_name):
        """Copy RDP connection details and prepare RDP file for sharing"""
        try:
            # Get and prepare the RDP file
            rdp_path = self.get_rdp_path(pc_name)
            temp_rdp_path = self.prepare_shareable_rdp(pc_name, rdp_path)
            
            if temp_rdp_path:
                share_text = (
                    f"Remote Desktop Connection for {pc_name}\n"
                    f"1. Use the RDP file located at: {temp_rdp_path}\n"
                    f"2. Or connect using: mstsc /v:{pc_name}"
                )
                
                # Return the share text and path for the UI to handle
                return {
                    'text': share_text,
                    'path': temp_rdp_path
                }
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error preparing share: {str(e)}")
            return None

    def cleanup_temp_rdp_files(self):
        """Clean up old temporary RDP files"""
        temp_dir = os.path.join(self.file_manager.data_dir, "temp_share")
        if os.path.exists(temp_dir):
            try:
                # Remove files older than 24 hours
                current_time = datetime.now()
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            except Exception as e:
                print(f"Error cleaning up temporary RDP files: {str(e)}")

    def get_machine_tags(self, pc_name):
        """Get all tags for a machine"""
        return self.machine_tags.get(pc_name, [])

    def add_tag(self, tag_name):
        """Add a new tag"""
        if tag_name and tag_name not in self.tags:
            self.tags.append(tag_name)
            self.file_manager.save_tags(self.tags)
            return True
        return False

    def delete_tag(self, tag_name):
        """Delete a tag and remove it from all machines"""
        if tag_name in self.tags:
            self.tags.remove(tag_name)
            # Remove tag from all machines
            for machine in self.machine_tags:
                if tag_name in self.machine_tags[machine]:
                    self.machine_tags[machine].remove(tag_name)
            self.file_manager.save_tags(self.tags)
            self.file_manager.save_machine_tags(self.machine_tags)
            return True
        return False

    def add_machine_tag(self, machine_name, tag_name):
        """Add a tag to a machine"""
        if tag_name not in self.tags:
            return False
        
        if machine_name not in self.machine_tags:
            self.machine_tags[machine_name] = []
            
        if tag_name not in self.machine_tags[machine_name]:
            self.machine_tags[machine_name].append(tag_name)
            self.file_manager.save_machine_tags(self.machine_tags)
            return True
        return False

    def remove_machine_tag(self, machine_name, tag_name):
        """Remove a tag from a machine"""
        if (machine_name in self.machine_tags and 
            tag_name in self.machine_tags[machine_name]):
            self.machine_tags[machine_name].remove(tag_name)
            self.file_manager.save_machine_tags(self.machine_tags)
            return True
        return False

    def get_machines_by_tag(self, tag_name):
        """Get all machines with a specific tag"""
        return [machine for machine, tags in self.machine_tags.items() 
                if tag_name in tags and machine in self.pc_names]

    def get_machines_by_multiple_tags(self, tags):
        """Get machines that have ALL the specified tags"""
        filtered_machines = []
        for pc_name in self.pc_names:
            machine_tags = self.get_machine_tags(pc_name)
            if all(tag in machine_tags for tag in tags):
                filtered_machines.append(pc_name)
        return filtered_machines

    def remove_category(self, category):
        """Remove a category and update machine categories"""
        if category in self.categories and category != "Default":
            # Move machines from this category to Default
            for machine in list(self.machine_categories.keys()):
                if self.machine_categories[machine] == category:
                    self.machine_categories[machine] = "Default"
            
            # Remove the category
            self.categories.remove(category)
            
            # Save changes
            self.file_manager.save_categories(self.categories)
            self.file_manager.save_machine_categories(self.machine_categories)
            return True
        return False

    def filter_by_category(self, category_name):
        """Filter machines by category"""
        # If clicking the same category again (including Default), deselect it
        if self.current_filter == category_name:
            self.current_filter = None  # Clear the filter
            filtered_pcs = self.vm_manager.pc_names  # Show all PCs
        else:
            # Set new filter (even for Default category)
            self.current_filter = category_name
            # Get machines for the selected category
            filtered_pcs = self.vm_manager.get_machines_by_category(category_name)
        
        # If there are active tag filters, apply them as well
        if hasattr(self, 'active_tag_filters') and self.active_tag_filters:
            tag_filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
            # Show only machines that match both category and tag filters
            filtered_pcs = [pc for pc in filtered_pcs if pc in tag_filtered_pcs]
        
        # Update the category buttons to show the selected state
        self.update_category_buttons()
        
        self.position_buttons(filtered_pcs)

    def toggle_machine_tag(self, machine_name, tag):
        """Toggle a tag on/off for a machine"""
        current_tags = self.get_machine_tags(machine_name)
        
        if tag in current_tags:
            # Remove tag
            if self.remove_machine_tag(machine_name, tag):
                # Refresh with current filters
                self.refresh_filtered_view()
        else:
            # Add tag
            if self.add_machine_tag(machine_name, tag):
                # Refresh with current filters
                self.refresh_filtered_view()

    def refresh_filtered_view(self):
        """Refresh the view maintaining current filters"""
        if hasattr(self, 'active_tag_filters') and self.active_tag_filters:
            if hasattr(self, 'current_filter') and self.current_filter:
                # Both tag and category filters active
                tag_filtered = self.get_machines_by_multiple_tags(list(self.active_tag_filters))
                category_filtered = self.get_machines_by_category(self.current_filter)
                filtered_pcs = [pc for pc in tag_filtered if pc in category_filtered]
            else:
                # Only tag filters active
                filtered_pcs = self.get_machines_by_multiple_tags(list(self.active_tag_filters))
        elif hasattr(self, 'current_filter') and self.current_filter:
            # Only category filter active
            filtered_pcs = self.get_machines_by_category(self.current_filter)
        else:
            # No filters active
            filtered_pcs = self.pc_names
        
        self.position_buttons(filtered_pcs)

    def reorder_categories(self, new_order):
        """Reorder categories according to the provided list"""
        # Ensure Default stays first
        if "Default" in new_order:
            new_order.remove("Default")
        
        # Reconstruct categories list with Default first
        self.categories = ["Default"] + new_order
        self.file_manager.save_categories(self.categories)
        return True

    def remove_tag_from_machine(self, machine_name, tag):
        """Remove a tag from a machine"""
        if machine_name in self.machine_tags:
            if tag in self.machine_tags[machine_name]:
                self.machine_tags[machine_name].remove(tag)
                # If no tags left, remove the machine from machine_tags
                if not self.machine_tags[machine_name]:
                    del self.machine_tags[machine_name]
                # Save changes
                self.file_manager.save_machine_tags(self.machine_tags)
                return True
        return False 

class VMManagerUI:
    # Update the CATEGORY_COLORS dictionary to have both light and dark theme variants
    CATEGORY_COLORS = {
        "dark": {
            "Blue": "#1E90FF",    # Brighter blue for dark theme
            "Green": "#32CD32",   # Brighter green for dark theme
            "Purple": "#9370DB",  # Brighter purple for dark theme
            "Orange": "#FF8C00",  # Brighter orange for dark theme
            "Pink": "#FF69B4",    # Brighter pink for dark theme
            "Teal": "#20B2AA",    # Brighter teal for dark theme
            "Yellow": "#FFD700",  # Brighter yellow for dark theme
            "Red": "#FF4500"      # Brighter red for dark theme
        },
        "light": {
            "Blue": "#89CFF0",    # Light blue
            "Green": "#90EE90",   # Light green
            "Purple": "#E6E6FA",  # Lavender
            "Orange": "#FFB347",  # Pastel orange
            "Pink": "#FFB6C1",    # Light pink
            "Teal": "#80CBC4",    # Light teal
            "Yellow": "#F0E68C",  # Khaki
            "Red": "#FF9999"      # Light red
        }
    }
    """Main application UI"""
    def __init__(self, vm_manager=None):
        # If no vm_manager provided, create one with reference to self
        if vm_manager is None:
            self.vm_manager = VMManager()
            self.vm_manager.ui = self  # Add reference to UI
        else:
            self.vm_manager = vm_manager  # Fixed indentation here
            self.vm_manager.ui = self  # Add reference to UI
        self.root = tk.Tk()
        self.root.title("VM Manager")
        
        # Remove the duplicate theme initialization and use only one
        self.current_theme = self.vm_manager.settings_manager.settings.get("theme", "dark")
        
        # Save the theme preference if it's not already saved
        if "theme" not in self.vm_manager.settings_manager.settings:
            self.vm_manager.settings_manager.settings["theme"] = self.current_theme
            self.vm_manager.settings_manager.save_settings()
        
        # Get theme colors
        theme = THEMES[self.current_theme]
        
        # Initialize colors from theme
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.border_color = theme["borders"]
        self.header_bg_color = theme["header_bg"]
        
        # Configure root window with theme
        self.root.configure(bg=self.primary_bg_color)
        
        # Remove the second theme initialization that was here before
        self.current_filter = None
        self.current_tag_filter = None
        
        # Update icon loading logic
        try:
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = os.path.dirname(sys.executable)
                assets_path = os.path.join(base_path, "assets")
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
                assets_path = os.path.join(base_path, "assets")
            
            # Main window icon
            icon_path = os.path.join(assets_path, "VmManagerlogo256.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"Warning: Could not find main icon at {icon_path}")
                
        except Exception as e:
            print(f"Warning: Could not load main window icon: {e}")

        # Initialize active_tag_filters as a set
        self.active_tag_filters = set()
        
        # Set window size
        window_width = 1300
        window_height = 900
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position coordinates
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Initialize theme-related attributes
        #self.current_theme = "dark"  # default theme
        
        # Load saved theme or use default
        saved_theme = self.vm_manager.settings_manager.settings.get("theme", "dark")
        theme = THEMES[saved_theme]
        
        # Initialize colors from theme
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.header_bg_color = theme["header_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.borders_and_dividers_color = theme["borders"]
        
        # Load any custom colors
        self.load_custom_colors()
        
        self.root.configure(bg=self.primary_bg_color)

        # Initialize tag manager before setup_ui
        self.tag_manager = TagManager(self.vm_manager.file_manager)
        
        self.setup_ui()  # This will create the sidebar with tag system
        self.update_category_buttons()  # Add this line to ensure proper initial colors
        
        # Move these after setup_ui
        self.running_indicators = {}
        self.connection_indicators = {}
        self.drag_data = {"x": 0, "y": 0, "item": None, "original_pos": None}
        self.dragging = False

        # Bind tag events after UI setup
        self.tag_sidebar.bind("<<TagSelected>>", self.handle_tag_selection)
        self.tag_sidebar.bind("<<TagAdded>>", self.handle_tag_added)
        self.tag_sidebar.bind("<<TagRemoved>>", self.handle_tag_removed)

        # Add tag drop binding
        self.tag_sidebar.tag_canvas.bind("<<TagDropped>>", 
            lambda e: self.handle_tag_drop(
                e.widget.drag_data['tag'],
                e.widget.winfo_pointerx() - self.canvas.winfo_rootx(),
                e.widget.winfo_pointery() - self.canvas.winfo_rooty()
            )
        )

    def setup_ui(self):
        # Create header
        self.create_header()
        
        # Create main layout
        self.create_sidebar()
        self.create_main_area()
        
        # Initialize buttons
        self.position_buttons()
        
        # Start updating machine status
        self.root.after(1000, self.update_machine_status)

    def create_header(self):
        self.header_frame = tk.Frame(self.root, height=60, bg=self.header_bg_color)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Header container
        self.header_container = tk.Frame(self.header_frame, bg=self.header_bg_color)
        self.header_container.pack(fill=tk.X, pady=5)

        # Title
        self.title_label = tk.Label(
            self.header_container, 
            text="VM Manager", 
            bg=self.header_bg_color, 
            fg=self.text_color, 
            font=("Calibri", 22, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=20)

        # Theme switch
        #self.theme_switch = ThemeSwitch(self.header_container, command=self.switch_theme)
        # Theme switch
        self.theme_switch = ThemeSwitch(self.header_container, 
                               current_theme=self.current_theme,  # Add this
                               command=self.switch_theme)
        self.theme_switch.pack(side=tk.RIGHT, padx=20)

        # Underline
        self.underline_frame = tk.Frame(self.header_frame, height=2, bg=self.border_color)
        self.underline_frame.pack(fill=tk.X)

    def create_sidebar(self):
        # Create left panel with theme colors
        self.left_frame = tk.Frame(self.root, width=200, bg=self.secondary_bg_color)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add vertical border/divider after left_frame
        self.sidebar_border = tk.Frame(self.root, width=2, bg=self.borders_and_dividers_color)
        self.sidebar_border.pack(side=tk.LEFT, fill=tk.Y)

        # Settings button first
        self.settings_button = tk.Button(
            self.left_frame, 
            text="Settings", 
            command=self.update_settings,
            font=('Helvetica', 12),
            bg=self.secondary_bg_color,
            fg=self.text_color,
            activebackground=self.hover_active_color
        )
        self.settings_button.pack(pady=10, padx=10)

        # Add Category Management section
        self.create_category_section()

        # Add separator
        ttk.Separator(self.left_frame, orient='horizontal').pack(fill='x', padx=5, pady=5)

        # Add Single PC section (moved up)
        self.create_add_pc_section()

        # Add separator
        ttk.Separator(self.left_frame, orient='horizontal').pack(fill='x', padx=5, pady=5)

        # Add tag sidebar at the bottom
        self.tag_sidebar = TagSidebar(self.left_frame, self.tag_manager)
        self.tag_sidebar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize the tag sidebar with the current theme
        self.tag_sidebar.update_theme(self.current_theme)  # Add this line

    def create_main_area(self):
        """Creates the scrollable canvas area where machine buttons are displayed."""
        self.main_frame = tk.Frame(self.root, bg=self.primary_bg_color)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.main_frame, 
            bg=self.primary_bg_color, 
            highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.main_frame, 
            orient=tk.VERTICAL, 
            command=self.canvas.yview
        )

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind events
        self.canvas.bind('<Configure>', lambda e: self.position_buttons())
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def create_rounded_button(self, text, last_used, description, command, x, y, width, height, corner_radius, 
                             title_font_size, info_font_size, status_font_size):
        """Creates a machine button with status indicators and information.
        
        Features:
        - Machine name and last used time
        - Status indicator (green/red circle)
        - Category indicator (colored diamond)
        - Hover tooltips for tags
        """
        # Get machine status
        is_running = self.vm_manager.get_machine_status(text)
        status_color = "#4CAF50" if is_running else "#FF5252"  # Green if running, red if not
        
        # Button background with tag for the specific button
        button_tag = f"button_{text}"  # Create unique tag for this button
        button_bg = self.create_rounded_rectangle(
            self.canvas,
            x, y, x + width, y + height, 
            corner_radius,
            fill=self.button_bg_color,
            outline=status_color,
            width=2,
            tags=(button_tag, "button_bg")
        )
        
        # Add hover bindings for tag popup
        def show_tag_popup(event):
            # First destroy any existing popup
            if hasattr(self.canvas, 'current_popup'):
                try:
                    self.canvas.current_popup.destroy()
                except:
                    pass
                delattr(self.canvas, 'current_popup')
            
            # Get machine tags
            machine_tags = self.vm_manager.get_machine_tags(text)
            if not machine_tags:
                return
            
            # Create popup
            popup = tk.Toplevel(self.root)
            popup.overrideredirect(True)
            popup.configure(bg=self.secondary_bg_color)
            
            # Create frame with border
            frame = tk.Frame(popup, bg=self.secondary_bg_color, 
                              highlightbackground=self.border_color,
                              highlightthickness=1)
            frame.pack(padx=1, pady=1)
            
            # Add tags with commas
            tag_text = ", ".join(machine_tags)
            tk.Label(frame, text=tag_text,
                    bg=self.secondary_bg_color,
                    fg=self.text_color,
                    font=('Segoe UI', 10)).pack(padx=8, pady=5)
            
            # Position popup near the button
            x = self.canvas.winfo_rootx() + event.x + 20
            y = self.canvas.winfo_rooty() + event.y + 10
            popup.geometry(f"+{x}+{y}")
            
            # Store popup reference
            self.canvas.current_popup = popup
            
            # Add a timer to automatically destroy popup after a short delay when mouse leaves
            popup.bind('<Leave>', lambda e: popup.after(100, hide_tag_popup))
        
        def hide_tag_popup(event=None):
            if hasattr(self.canvas, 'current_popup'):
                try:
                    self.canvas.current_popup.destroy()
                except:
                    pass
                delattr(self.canvas, 'current_popup')
        
        # Bind hover events
        self.canvas.tag_bind(button_tag, '<Enter>', show_tag_popup)
        self.canvas.tag_bind(button_tag, '<Leave>', hide_tag_popup)
        
        # Status indicator circle (top right corner)
        indicator_radius = min(width, height) * 0.05
        indicator_x = x + width - (indicator_radius * 2)
        indicator_y = y + (indicator_radius * 2)
        
        self.canvas.create_oval(
            indicator_x - indicator_radius,
            indicator_y - indicator_radius,
            indicator_x + indicator_radius,
            indicator_y + indicator_radius,
            fill=status_color,
            outline=status_color,
            tags=(button_tag, "button"))

        # Category indicator as a small diamond (bottom left)
        category = self.vm_manager.get_machine_category(text)
        if category != "Default":
            default_color = "#808080"
            category_color = self.vm_manager.category_colors.get(category, default_color)
            diamond_x = x + width * 0.1  # Position at 10% of button width
            diamond_y = y + height * 0.85  # Position at 85% of button height
            
            self.canvas.create_text(
                diamond_x, diamond_y,
                text="🔹",  # Small diamond icon
                fill=category_color,
                font=('Segoe UI', int(min(width, height) * 0.12)),  # Increased size
                tags=(button_tag, "button")
            )

        # Calculate vertical positions
        center_x = x + (width / 2)
        title_y = y + (height * 0.25)
        last_used_y = y + (height * 0.45)
        description_y = y + (height * 0.65)
        
        # Create text elements
        title_text = self.canvas.create_text(
            center_x, title_y,
            text=text,
            fill=self.text_color,
            font=('Helvetica', title_font_size, 'bold'),
            anchor="center",
            tags=(button_tag, "button"))
        
        last_used_text = self.canvas.create_text(
            center_x, last_used_y,
            text=f"Last Used: {last_used}",
            fill=self.text_color,
            font=('Helvetica', info_font_size),
            anchor="center",
            tags=(button_tag, "button"))

        # Truncate description if it's too long (around 50 characters)
        truncated_description = description[:50] + "..." if description and len(description) > 50 else description

        # Create the truncated description text on button
        if description:
            description_text = self.canvas.create_text(
                center_x, description_y,
                text=truncated_description,
                fill=self.text_color,
                font=('Helvetica', status_font_size),
                anchor="center",
                width=width * 0.9,  # Limit width to 90% of button width
                tags=(button_tag, "button"))

            def show_tooltip(event):
                # Safely destroy existing tooltip
                if hasattr(self, 'current_tooltip') and self.current_tooltip is not None:
                    try:
                        self.current_tooltip.destroy()
                    except:
                        pass
                    self.current_tooltip = None
                
                tooltip = tk.Toplevel(self.root)
                tooltip.wm_overrideredirect(True)
                tooltip.configure(bg=self.secondary_bg_color)
                tooltip.geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
                
                label = tk.Label(
                    tooltip,
                    text=description,
                    wraplength=300,
                    justify="left",
                    bg=self.secondary_bg_color,
                    fg=self.text_color,
                    padx=10,
                    pady=5
                )
                label.pack()
                
                self.current_tooltip = tooltip

            def hide_tooltip(event):
                # Safely destroy tooltip
                if hasattr(self, 'current_tooltip') and self.current_tooltip is not None:
                    try:
                        self.current_tooltip.destroy()
                    except:
                        pass
                    self.current_tooltip = None

            # Bind both the text and the button background for tooltip events
            for item in self.canvas.find_withtag(button_tag):
                self.canvas.tag_bind(item, '<Enter>', show_tooltip)
                self.canvas.tag_bind(item, '<Leave>', hide_tooltip)

        # Add tags display
        tags = self.vm_manager.get_machine_tags(text)
        if tags:
            # Calculate maximum width for tags (slightly less than button width)
            max_tag_width = width * 0.9  # 90% of button width
            
            # Create font object for measuring
            tag_font = tkfont.Font(family='Helvetica', size=status_font_size)
            
            # Create the full tags text
            tags_text = "🏷️ " + ", ".join(tags)
            
            # Truncate tags text if it's too long
            while tag_font.measure(tags_text) > max_tag_width:
                # Remove the last tag and add ellipsis
                tags = tags[:-1]
                if not tags:
                    tags_text = "🏷️ ..."
                    break
                tags_text = "🏷️ " + ", ".join(tags) + "..."
            
            # Create the tags text with its own tag for binding
            tags_tag = f"tags_{text}"  # Create unique tag for the tags text
            self.canvas.create_text(
                center_x, y + (height * 0.85),
                text=tags_text,
                fill=self.text_color,
                font=('Helvetica', status_font_size),
                anchor="center",
                width=max_tag_width,  # Set maximum width
                tags=(button_tag, "button", tags_tag)  # Add the tags_tag
            )
            
            # Bind hover events specifically to the tags text
            self.canvas.tag_bind(tags_tag, '<Enter>', show_tag_popup)
            self.canvas.tag_bind(tags_tag, '<Leave>', hide_tag_popup)

        # Bind events to the button background
        self.canvas.tag_bind(button_tag, '<Button-1>', lambda e, name=text: self.handle_button_press(e, name))
        self.canvas.tag_bind(button_tag, '<B1-Motion>', self.drag)
        self.canvas.tag_bind(button_tag, '<ButtonRelease-1>', 
            lambda e, name=text: self.handle_button_release(e, name, 
                lambda: self.handle_machine_click(name, command)))
        self.canvas.tag_bind(button_tag, '<Button-3>', lambda e: self.show_context_menu(e, text))

        # Add hover bindings
        self.canvas.tag_bind(button_tag, '<Enter>', lambda e: self.on_button_hover(e, button_tag))
        self.canvas.tag_bind(button_tag, '<Leave>', lambda e: self.on_button_leave(e, button_tag))

    # Helper method for creating rounded rectangles
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)



    def update_machine_status(self):
        """Update status of all machines"""
        for pc_name in self.vm_manager.pc_names:
            # Run status check in a separate thread to prevent UI freezing
            threading.Thread(
                target=self._check_single_machine_status,
                args=(pc_name,),
                daemon=True
            ).start()
        
        # Update display based on current filters
        if hasattr(self, 'tag_sidebar'):
            selected_tags = self.tag_sidebar.get_selected_tags()
            if selected_tags:
                # Get machines that match the tag filter
                filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(selected_tags)
                
                # If there's also a category filter active, intersect the results
                if hasattr(self, 'current_filter') and self.current_filter:
                    category_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                    # Only show machines that match both filters
                    filtered_pcs = [pc for pc in filtered_pcs if pc in category_pcs]
                
                self.position_buttons(filtered_pcs)
            elif hasattr(self, 'current_filter') and self.current_filter:
                # Only category filter is active
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_pcs)
            else:
                # No filters active, show all machines
                self.position_buttons()
            
        # Schedule next update
        self.root.after(5000, self.update_machine_status)

    def _check_single_machine_status(self, pc_name):
        """Check status of a single machine"""
        is_running = self.vm_manager.check_machine_status(pc_name)
        self.vm_manager.machine_status[pc_name] = is_running

    def switch_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        theme = THEMES[self.current_theme]
        
        # Save the theme preference
        self.vm_manager.settings_manager.settings["theme"] = self.current_theme
        self.vm_manager.settings_manager.save_settings()
        
        # Update all theme colors
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.border_color = theme["borders"]
        self.header_bg_color = theme["header_bg"]
        
        # Update all UI elements with new colors
        self.update_theme_colors()
        
        # Update category buttons with new theme colors
        self.update_category_buttons()
        
        # Update tag sidebar theme explicitly
        if hasattr(self, 'tag_sidebar'):
            self.tag_sidebar.update_theme(self.current_theme)

    def update_theme_colors(self):
        """Update all UI elements with current theme colors"""
        # Update header
        self.header_frame.configure(bg=self.header_bg_color)
        self.header_container.configure(bg=self.header_bg_color)
        self.title_label.configure(bg=self.header_bg_color, fg=self.text_color)
        
        # Add this line to update the sidebar border color
        if hasattr(self, 'sidebar_border'):
            self.sidebar_border.configure(bg=self.border_color)
        
        # Update theme switch button if it exists
        if hasattr(self, 'theme_button'):  # Change 'theme_switch' to 'theme_button'
            self.theme_button.configure(bg=self.header_bg_color)
        
        self.underline_frame.configure(bg=self.border_color)
        
        # Update main sidebar frame
        self.left_frame.configure(bg=self.secondary_bg_color)
        
        # Update Categories section
        if hasattr(self, 'categories_label'):
            self.categories_label.configure(
                bg=self.secondary_bg_color,
                fg=self.text_color
            )
        
        if hasattr(self, 'category_buttons_container'):
            self.category_buttons_container.configure(bg=self.secondary_bg_color)
            # Update all category buttons
            for button in self.category_buttons_container.winfo_children():
                button.configure(
                    bg=self.secondary_bg_color,
                    fg=self.text_color
                )
        
        # Update Add Single PC section
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(
                    bg=self.secondary_bg_color,
                    fg=self.text_color
                )
            elif isinstance(widget, tk.Frame):  # For Add Single PC frame
                widget.configure(bg=self.secondary_bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Entry):
                        child.configure(
                            bg=self.primary_bg_color,
                            fg=self.text_color,
                            insertbackground=self.text_color
                        )
                    elif isinstance(child, tk.Button):
                        child.configure(
                            bg=self.button_bg_color,
                            fg=self.text_color,
                            activebackground=self.hover_active_color,
                            activeforeground=self.text_color
                        )
        
        # Update Add Category+ button specifically
        if hasattr(self, 'add_category_btn'):
            self.add_category_btn.configure(
                bg=self.button_bg_color,
                fg=self.text_color,
                activebackground=self.hover_active_color,
                activeforeground=self.text_color
            )

        # Update main area
        self.canvas.configure(bg=self.primary_bg_color)
        self.main_frame.configure(bg=self.primary_bg_color)
        
        # Update all widgets in sidebar
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.secondary_bg_color, fg=self.text_color)
            elif isinstance(widget, tk.Button) and widget not in self.category_buttons_container.winfo_children():
                widget.configure(
                    bg=self.button_bg_color,
                    fg=self.text_color,
                    activebackground=self.hover_active_color,
                    activeforeground=self.text_color
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=self.primary_bg_color, 
                    fg=self.text_color, 
                    insertbackground=self.text_color
                )
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=self.primary_bg_color, 
                    fg=self.text_color, 
                    insertbackground=self.text_color
                )

        # Update the border frame color to match the theme
        if hasattr(self, 'border_frame'):
            self.border_frame.configure(bg=self.border_color)  # This will use #B4D8F0 in light theme

        # Update tag section header
        if hasattr(self, 'tag_header_frame'):
            self.tag_header_frame.configure(bg=self.secondary_bg_color)
            self.tags_label.configure(
                bg=self.secondary_bg_color,
                fg=self.text_color
            )

        # Update tag buttons
        if hasattr(self, 'tag_filters_container'):
            self.tag_filters_container.configure(bg=self.secondary_bg_color)
            for widget in self.tag_filters_container.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=self.secondary_bg_color)

    def update_rdp_path(self):
        result = messagebox.askyesno(
            "Update RDP Path",
            "Do you want to change the default RDP file path?",
            icon='question'
        )
        if result:
            rdp_path = filedialog.askopenfilename(
                title="Select RDP File",
                filetypes=(("RDP Files", "*.rdp"), ("All Files", "*.*")))
            if rdp_path:
                self.vm_manager.settings_manager.settings["rdp_path"] = rdp_path
                self.vm_manager.settings_manager.save_settings()
                messagebox.showinfo("Success", "Default RDP path updated successfully!")

    def add_single_pc(self):
        new_pc = self.single_pc_entry.get().strip()
        if new_pc:
            self.vm_manager.add_pc(new_pc)
            self.single_pc_entry.delete(0, tk.END)
            self.position_buttons()

    def add_multiple_pcs(self):
        pcs = self.multi_pc_text.get("1.0", tk.END).strip().splitlines()
        if pcs:
            for pc in pcs:
                self.vm_manager.add_pc(pc.strip())
            self.multi_pc_text.delete("1.0", tk.END)
            self.position_buttons()
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_context_menu(self, event, pc_name):
        """Displays right-click menu for machine management options."""
        menu_style = MenuStyle.get_themed_menu_style(self.current_theme)
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.configure(**menu_style)
        
        # Replace Clear DNS Cache with Troubleshoot
        context_menu.add_command(
            label="  🔧  Troubleshoot",
            command=lambda: self.show_troubleshoot_window(pc_name),
            font=menu_style['font'],
            foreground=menu_style['fg']
        )
        
        context_menu.add_separator()
        
        # Category submenu
        category_menu = tk.Menu(context_menu, tearoff=0)
        category_menu.configure(**menu_style)
        
        # Add categories to submenu
        for category in self.vm_manager.categories:
            if category != "Default":
                category_menu.add_command(
                    label=f"  📁  {category}",
                    command=lambda c=category: self.set_machine_category(pc_name, c),
                    font=menu_style['font'],
                    foreground=menu_style['fg'],
                    background=menu_style['bg'])
        context_menu.add_cascade(
            label="    Set Category",
            menu=category_menu,
            font=menu_style['font'],
            foreground=menu_style['fg']
        )

        # Add option to remove category if machine has one
        current_category = self.vm_manager.get_machine_category(pc_name)
        if current_category and current_category != "Default":
            context_menu.add_command(
                label=f"  🗑️  Remove from '{current_category}'",
                command=lambda: self.remove_machine_category(pc_name),
                font=menu_style['font'],
                foreground=menu_style['fg']
            )

        # Tags submenu (moved up, right after categories)
        tags_menu = tk.Menu(context_menu, tearoff=0)
        tags_menu.configure(**menu_style)
        
        # Add "Manage Tags" option
        tags_menu.add_command(
            label="  ✨  Manage Tags",
            command=lambda: self.show_tag_manager(),
            font=menu_style['font'],
            foreground=menu_style['fg'],
            background=menu_style['bg']
        )
        
        tags_menu.add_separator()
        
        # Add existing tags
        machine_tags = self.vm_manager.get_machine_tags(pc_name)
        
        # Add remove options for existing machine tags
        if machine_tags:
            for tag in machine_tags:
                tags_menu.add_command(
                    label=f"  🗑️  Remove '{tag}'",
                    command=lambda t=tag: (
                        self.vm_manager.remove_tag_from_machine(pc_name, t),
                        self.position_buttons(self.vm_manager.pc_names)  # Changed from refresh_buttons to position_buttons
                    ),
                    font=menu_style['font'],
                    foreground='#dc3545',  # Red color for delete
                    background=menu_style['bg']
                )
            tags_menu.add_separator()
        
        # Add checkboxes for all available tags
        for tag in self.vm_manager.tags:
            tags_menu.add_checkbutton(
                label=f"  🏷️  {tag}",
                command=lambda t=tag: self.toggle_machine_tag(pc_name, t),
                onvalue=1,
                offvalue=0,
                variable=tk.BooleanVar(value=tag in machine_tags),
                font=menu_style['font'],
                foreground=menu_style['fg'],
                background=menu_style['bg']
            )
        
        context_menu.add_cascade(
            label="  🏷️  Tags",
            menu=tags_menu,
            font=menu_style['font'],
            foreground=menu_style['fg']
        )

        context_menu.add_separator()

        # Share submenu
        share_menu = tk.Menu(context_menu, tearoff=0)
        share_menu.configure(**menu_style)
        
        share_menu.add_command(
            label="  💬  Share via Teams",
            command=lambda: self.vm_manager.share_via_teams(pc_name),
            font=menu_style['font'],
            foreground=menu_style['fg'],
            background=menu_style['bg']
        )
        
        share_menu.add_command(
            label="  📋  Copy Share Link",
            command=lambda: self.handle_copy_share_link(pc_name),
            font=menu_style['font'],
            foreground=menu_style['fg'],
            background=menu_style['bg']
        )
        
        context_menu.add_cascade(
            label="  📤  Share",
            menu=share_menu,
            font=menu_style['font'],
            foreground=menu_style['fg']
        )

        # Add other menu items
        context_menu.add_separator()
        
        context_menu.add_command(
            label="  🔗  Set RDP Path",
            command=lambda: self.set_rdp_path(pc_name),
            font=menu_style['font'],
            foreground=menu_style['fg'],
            background=menu_style['bg']
        )
        
        context_menu.add_command(
            label="  ✏️  Edit Description",
            command=lambda: self.edit_description(pc_name),
            font=menu_style['font'],
            foreground=menu_style['fg'],
            background=menu_style['bg']
        )
        
        # Delete option with warning styling
        context_menu.add_command(
            label="  ⚠️  Delete",
            command=lambda: self.delete_pc(pc_name),
            font=('Segoe UI', 11, 'bold'),
            foreground='#dc3545',
            background=menu_style['bg']
        )
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def handle_copy_share_link(self, pc_name):
        """Handle copying share link to clipboard"""
        result = self.vm_manager.copy_share_link(pc_name)
        if result:
            try:
                # Copy to clipboard using tkinter
                self.root.clipboard_clear()
                self.root.clipboard_append(result['text'])
                
                # Open the file location
                folder_path = os.path.dirname(result['path'])
                try:
                    os.startfile(folder_path)
                except Exception:
                    subprocess.run(['explorer', folder_path], check=True)
                
                messagebox.showinfo("Copied", 
                    "Connection details copied to clipboard!\n"
                    "The RDP file location has been opened for you to share.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")

    def set_rdp_path(self, pc_name):
        """Set custom RDP path for a specific PC"""
        rdp_path = filedialog.askopenfilename(
            title=f"Select RDP File for {pc_name}",
            filetypes=(("RDP Files", "*.rdp"), ("All Files", "*.*"))
        )
        if rdp_path:
            self.vm_manager.set_machine_rdp_path(pc_name, rdp_path)

    def remove_machine_category(self, pc_name):
        """Remove the category assignment from a machine"""
        if self.vm_manager.remove_machine_category(pc_name):
            # Refresh display maintaining current filter
            if self.current_filter:
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_pcs)
            else:
                self.position_buttons()

    def edit_description(self, pc_name):
        """Edit the description for a machine"""
        if self.vm_manager.add_or_edit_description(pc_name):
            # Refresh the display
            if self.current_filter:
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_pcs)
            else:
                self.position_buttons()

    def delete_pc(self, pc_name):
        """Delete a machine and refresh the display"""
        if self.vm_manager.delete_pc(pc_name):
            # Refresh display maintaining current filter
            if self.current_filter:
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                if self.active_tag_filters:
                    tag_filtered = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
                    filtered_pcs = [pc for pc in filtered_pcs if pc in tag_filtered]
            elif self.active_tag_filters:
                filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
            else:
                filtered_pcs = self.vm_manager.pc_names
            
            self.position_buttons(filtered_pcs)

    def update_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        
        # Update settings window icon loading
        try:
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
                assets_path = os.path.join(base_path, "assets")
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
                assets_path = os.path.join(base_path, "assets")
            
            # Settings window icon
            settings_icon_path = os.path.join(assets_path, "settings_icon.ico")
            if os.path.exists(settings_icon_path):
                settings_window.iconbitmap(settings_icon_path)
            else:
                print(f"Warning: Could not find settings icon at {settings_icon_path}")
                
        except Exception as e:
            print(f"Warning: Could not load settings window icon: {e}")

        # Set initial size
        window_width = 400
        window_height = 600
        
        # Get screen dimensions
        screen_width = settings_window.winfo_screenwidth()
        screen_height = settings_window.winfo_screenheight()
        
        # Calculate position coordinates
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        settings_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        settings_window.configure(bg=self.primary_bg_color)
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Rest of your settings window code...
        # Main container frame
        main_frame = tk.Frame(settings_window, bg=self.primary_bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Style configuration
        section_padding = 20
        button_width = 30
        frame_width = 350  # Fixed width for all sections

        # RDP Settings Section
        rdp_frame = tk.LabelFrame(main_frame, text=" RDP Settings ", 
                                 bg=self.primary_bg_color, fg=self.text_color,
                                 font=('Helvetica', 12, 'bold'))
        rdp_frame.pack(fill='x', pady=(0, section_padding))

        tk.Button(rdp_frame, text="Change Default RDP File",
                  command=self.update_rdp_path,
                  bg=self.button_bg_color, fg=self.text_color,
                  width=button_width).pack(pady=15)

        # Appearance Settings Section
        appearance_frame = tk.LabelFrame(main_frame, text=" Appearance Settings ", 
                                       bg=self.primary_bg_color, fg=self.text_color,
                                       font=('Helvetica', 12, 'bold'))
        appearance_frame.pack(fill='x', pady=(0, section_padding))

        # Export/Import Section
        export_frame = tk.LabelFrame(main_frame, text=" Export/Import ", 
                                    bg=self.primary_bg_color, fg=self.text_color,
                                    font=('Helvetica', 12, 'bold'))
        export_frame.pack(fill='x', pady=(0, section_padding))

        for button_text, command in [
            ("Change Data Directory", self.change_data_directory),
            ("Export Settings", self.export_settings),
            ("Import Settings", self.import_settings),
            ("Export Machine List", self.export_machine_list)
        ]:
            tk.Button(export_frame, text=button_text,
                     command=command,
                     bg=self.button_bg_color, fg=self.text_color,
                     width=button_width).pack(pady=5)

        # Connection Settings Section
        conn_frame = tk.LabelFrame(main_frame, text=" Connection Settings ", 
                                  bg=self.primary_bg_color, fg=self.text_color,
                                  font=('Helvetica', 12, 'bold'))
        conn_frame.pack(fill='x', pady=(0, section_padding))

        tk.Label(conn_frame, text="Status Refresh Interval (seconds):",
                bg=self.primary_bg_color, fg=self.text_color).pack(pady=(15,5))
        
        refresh_entry = tk.Entry(conn_frame, bg=self.secondary_bg_color, 
                               fg=self.text_color, width=10, justify='center')
        refresh_entry.insert(0, str(self.vm_manager.settings_manager.settings.get("refresh_interval", 5)))
        refresh_entry.pack(pady=(0,15))

        # Save Button - moved outside of frames and adjusted padding
        tk.Button(main_frame, text="Save Settings",
                  command=lambda: self.save_settings(settings_window, refresh_entry),
                  bg=self.button_bg_color, fg=self.text_color,
                  width=button_width).pack(pady=(10, 0))

        # Add Reset Settings Section
        reset_frame = tk.LabelFrame(main_frame, text=" Reset Settings ", 
                                   bg=self.primary_bg_color, fg=self.text_color,
                                   font=('Helvetica', 12, 'bold'))
        reset_frame.pack(fill='x', pady=(0, section_padding))

        def reset_settings():
            """Reset all settings to default"""
            if messagebox.askyesno(
                "Confirm Reset",
                "This will reset all settings to default values.\n\n"
                "This includes:\n"
                "• Default RDP path\n"
                "• Theme preferences\n"
                "• Custom colors\n"
                "• Window positions\n"
                "• Refresh intervals\n"
                "• Data directory (will be reset to default location)\n\n"
                "Machine data will be moved to the default location:\n"
                "%LOCALAPPDATA%\\VmManager\n\n"
                "Are you sure you want to continue?",
                icon='warning'
            ):
                try:
                    # Get default data directory
                    default_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "VmManager")
                    current_data_dir = self.vm_manager.file_manager.data_dir

                    # Reset settings to defaults
                    default_settings = {
                        "theme": "dark",
                        "refresh_interval": 5,
                        "rdp_path": "",
                        "custom_colors": {},
                        "data_dir": default_data_dir  # Add default data directory
                    }
                    
                    # Create default directory if it doesn't exist
                    os.makedirs(default_data_dir, exist_ok=True)
                    
                    # Move all data files to default location if not already there
                    if current_data_dir != default_data_dir:
                        try:
                            for filename in os.listdir(current_data_dir):
                                if filename.endswith('.txt'):
                                    src = os.path.join(current_data_dir, filename)
                                    dst = os.path.join(default_data_dir, filename)
                                    shutil.copy2(src, dst)
                        except Exception as e:
                            messagebox.showerror(
                                "Error",
                                f"Failed to move data files: {str(e)}\n"
                                "Settings will still be reset, but you may need to move data files manually."
                            )
                    
                    # Update settings
                    self.vm_manager.settings_manager.settings = default_settings.copy()
                    self.vm_manager.settings_manager.save_settings()
                    
                    # Update file manager paths
                    self.vm_manager.file_manager.data_dir = default_data_dir
                    self.vm_manager.file_manager.update_paths()
                    
                    # Apply theme changes
                    self.current_theme = default_settings["theme"]
                    theme = THEMES[self.current_theme]
                    self.primary_bg_color = theme["primary_bg"]
                    self.secondary_bg_color = theme["secondary_bg"]
                    self.button_bg_color = theme["button_bg"]
                    self.text_color = theme["text"]
                    self.hover_active_color = theme["hover_active"]
                    self.border_color = theme["borders"]
                    self.header_bg_color = theme["header_bg"]
                    
                    # Update UI with new theme
                    self.update_theme_colors()
                    self.position_buttons()
                    
                    messagebox.showinfo(
                        "Settings Reset",
                        "All settings have been reset to default values.\n"
                        "Data directory has been reset to default location.\n"
                        "Please restart the application for all changes to take effect."
                    )
                    
                    # Close settings window
                    settings_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Failed to reset settings: {str(e)}\n"
                        "Please try again or reset manually by deleting settings.txt"
                    )

        tk.Button(
            reset_frame,
            text="Reset All Settings to Default",
            command=reset_settings,
            bg="#dc3545",  # Red background for warning
            fg="white",
            width=button_width
        ).pack(pady=15)

        # Add warning text
        tk.Label(
            reset_frame,
            text="Warning: This will reset all settings to their default values.\n"
                 "Machine data will not be affected.",
            bg=self.primary_bg_color,
            fg="#dc3545",  # Red text for warning
            font=('Helvetica', 9),
            wraplength=350
        ).pack(pady=(0, 15))

    def get_current_color(self, element):
        """Get the current color for a UI element"""
        element_map = {
            "Primary Background": self.primary_bg_color,
            "Secondary Background": self.secondary_bg_color,
            "Button Color": self.button_bg_color,
            "Text Color": self.text_color,
            "Border Color": self.borders_and_dividers_color
        }
        return element_map.get(element, "#000000")

    def pick_color(self, element, preview_frame=None):
        """Choose custom colors for UI elements"""
        initial_color = self.get_current_color(element)
        color = colorchooser.askcolor(color=initial_color, title=f"Choose {element} Color")[1]
        if color:
            # Update preview if provided
            if preview_frame:
                preview_frame.configure(bg=color)

            # Map element names to attribute names
            element_map = {
                "Primary Background": "primary_bg_color",
                "Secondary Background": "secondary_bg_color",
                "Button Color": "button_bg_color",
                "Text Color": "text_color",
                "Border Color": "borders_and_dividers_color"
            }
            
            attr_name = element_map.get(element)
            if attr_name:
                # Update the instance variable
                setattr(self, attr_name, color)
                
                # Save to custom colors settings
                custom_colors = self.vm_manager.settings_manager.settings.get("custom_colors", {})
                if not isinstance(custom_colors, dict):
                    custom_colors = {}
                custom_colors[attr_name] = color
                self.vm_manager.settings_manager.settings["custom_colors"] = custom_colors
                self.vm_manager.settings_manager.save_settings()
                
                # Apply the new colors
                self.update_theme_colors()
                self.position_buttons()

    def load_custom_colors(self):
        """Load custom colors if they exist"""
        custom_colors = self.vm_manager.settings_manager.settings.get("custom_colors", {})
        if isinstance(custom_colors, dict) and custom_colors:
            for attr_name, color in custom_colors.items():
                if hasattr(self, attr_name):
                    setattr(self, attr_name, color)

    def change_data_directory(self):
        """Changes application data storage location with file migration."""
        new_dir = filedialog.askdirectory(title="Select New Data Directory")
        if new_dir:
            try:
                # Confirm with user
                if not messagebox.askyesno("Confirm", 
                    "This will move all your data to the new location. Continue?"):
                    return

                old_dir = self.vm_manager.file_manager.data_dir
                
                # Create new directory if it doesn't exist
                os.makedirs(new_dir, exist_ok=True)
                
                # Move all files to new location
                for filename in os.listdir(old_dir):
                    if filename.endswith('.txt'):
                        old_path = os.path.join(old_dir, filename)
                        new_path = os.path.join(new_dir, filename)
                        shutil.copy2(old_path, new_path)  # Copy instead of move
                
                # Update ALL possible settings.txt locations
                settings_locations = [
                    # LocalAppData location
                    os.path.join(os.getenv("LOCALAPPDATA"), "VmManager", "settings.txt"),
                    # New directory location
                    os.path.join(new_dir, "settings.txt"),
                    # Current script directory location
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.txt"),
                    # Current working directory location
                    os.path.join(os.getcwd(), "settings.txt")
                ]
                
                # Print debug info
                print("Updating settings files in these locations:")
                for loc in settings_locations:
                    print(f"- {loc}")
                
                for settings_path in settings_locations:
                    try:
                        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
                        with open(settings_path, "w") as f:
                            f.write(f"data_dir={new_dir}\n")
                        print(f"Successfully updated: {settings_path}")
                    except Exception as e:
                        print(f"Failed to update {settings_path}: {str(e)}")
                
                # Update file manager paths
                self.vm_manager.file_manager.data_dir = new_dir
                self.vm_manager.file_manager.update_paths()
                
                messagebox.showinfo("Success", "Data directory changed successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change directory: {str(e)}")

    def export_settings(self):
        """Export all settings to a JSON file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="vm_manager_settings.json"
        )
        if file_path:
            try:
                export_data = {
                    "settings": self.vm_manager.settings_manager.settings,
                    "machine_rdp_paths": self.vm_manager.machine_rdp_paths,
                    "descriptions": self.vm_manager.descriptions,
                    "custom_theme": self.vm_manager.settings_manager.settings.get("custom_theme", {})
                }
                
                with open(file_path, 'w') as f:
                    json.dump(export_data, f, indent=4)
                
                messagebox.showinfo("Success", "Settings exported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export settings: {str(e)}")

    def import_settings(self):
        """Import settings from a JSON file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    import_data = json.load(f)
                
                # Confirm with user
                if not messagebox.askyesno("Confirm", 
                    "This will overwrite your current settings. Continue?"):
                    return
                
                # Update settings
                self.vm_manager.settings_manager.settings.update(import_data.get("settings", {}))
                self.vm_manager.machine_rdp_paths.update(import_data.get("machine_rdp_paths", {}))
                self.vm_manager.descriptions.update(import_data.get("descriptions", {}))
                
                # Save all updated settings
                self.vm_manager.settings_manager.save_settings()
                self.vm_manager.file_manager.save_machine_rdp_paths(self.vm_manager.machine_rdp_paths)
                self.vm_manager.file_manager.save_descriptions(self.vm_manager.descriptions)
                
                # Apply any custom theme settings
                if "custom_theme" in import_data:
                    self.vm_manager.settings_manager.settings["custom_theme"] = import_data["custom_theme"]
                    self.update_theme_colors()
                    self.position_buttons()
                
                messagebox.showinfo("Success", "Settings imported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import settings: {str(e)}")

    def export_machine_list(self):
        """Export machine list with descriptions and last used times to CSV"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="vm_machine_list.csv"
        )
        if file_path:
            try:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # Write header
                    writer.writerow(["Machine Name", "Description", "Last Used", "Custom RDP Path"])
                    
                    # Write data for each machine
                    for pc in self.vm_manager.pc_names:
                        writer.writerow([
                            pc,
                            self.vm_manager.descriptions.get(pc, ""),
                            self.vm_manager.last_used_times.get(pc, "Never"),
                            self.vm_manager.machine_rdp_paths.get(pc, "Default")
                        ])  # Added missing closing bracket here
            
                messagebox.showinfo("Success", "Machine list exported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export machine list: {str(e)}")

    def save_settings(self, settings_window, refresh_entry):
        """Save all settings and close the settings window"""
        try:
            # Save refresh interval
            refresh_interval = int(refresh_entry.get())
            self.vm_manager.settings_manager.settings["refresh_interval"] = refresh_interval
            
            # Save all settings
            self.vm_manager.settings_manager.save_settings()
            self.vm_manager.file_manager.save_machine_rdp_paths(self.vm_manager.machine_rdp_paths)
            self.vm_manager.file_manager.save_descriptions(self.vm_manager.descriptions)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Refresh interval must be a number!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def restore_default_colors(self, colors_frame):
        """Restore colors to theme defaults"""
        if messagebox.askyesno("Confirm Restore", 
                              "Are you sure you want to restore default colors? This will remove all custom colors."):
            # Get current theme
            current_theme = self.vm_manager.settings_manager.settings.get("theme", "dark")
            theme = THEMES[current_theme]
            
            # Reset colors to theme defaults
            self.primary_bg_color = theme["primary_bg"]
            self.secondary_bg_color = theme["secondary_bg"]
            self.button_bg_color = theme["button_bg"]
            self.header_bg_color = theme["header_bg"]
            self.text_color = theme["text"]
            self.hover_active_color = theme["hover_active"]
            self.borders_and_dividers_color = theme["borders"]
            
            # Remove custom colors from settings
            self.vm_manager.settings_manager.settings.pop("custom_colors", None)
            self.vm_manager.settings_manager.save_settings()
            
            # Update UI
            self.update_theme_colors()
            self.position_buttons()
            
            # Update color previews in settings
            for child in colors_frame.winfo_children():
                if isinstance(child, tk.Frame):
                    for widget in child.winfo_children():
                        if isinstance(widget, tk.Frame):  # This is the preview frame
                            color_label = child.winfo_children()[0]  # Get the label
                            color_name = color_label.cget("text").replace(":", "")
                            widget.configure(bg=self.get_current_color(color_name))
            
            messagebox.showinfo("Success", "Colors have been restored to default theme colors.")

    def handle_button_press(self, event, pc_name):
        """Handle initial button press - could be start of drag or click"""
        self.drag_data = {
            "x": event.x,
            "y": event.y,
            "item": pc_name,
            "original_pos": self.vm_manager.pc_names.index(pc_name),
            "moved": False  # Track if the button was actually dragged
        }
        # Raise the button being interacted with
        self.canvas.tag_raise(f"button_{pc_name}")

    def drag(self, event):
        """Handle dragging of a button"""
        if not self.drag_data.get("item"):
            return

        # Calculate the distance moved
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # If the movement is significant enough, mark as dragged
        if abs(dx) > 5 or abs(dy) > 5:  # 5 pixel threshold
            self.drag_data["moved"] = True

        # Move all elements with the button's specific tag
        button_tag = f"button_{self.drag_data['item']}"
        for item in self.canvas.find_withtag(button_tag):
            self.canvas.move(item, dx, dy)

        # Update the stored position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def handle_button_release(self, event, pc_name, command):
        """Handle button release - either complete drag or handle click"""
        if not self.drag_data.get("item"):
            return

        # If the button wasn't dragged, treat it as a click
        if not self.drag_data.get("moved"):
            # Instead of directly executing command(), use handle_machine_click
            self.handle_machine_click(pc_name, command)
        else:
            # Handle drag completion
            drop_pos = self._get_drop_position(event.x, event.y)
            if drop_pos != self.drag_data["original_pos"]:
                # Update the PC list order
                pc_list = self.vm_manager.pc_names
                pc_list.remove(pc_name)
                pc_list.insert(drop_pos, pc_name)
                # Save the new order
                self.vm_manager.file_manager.save_pcs(pc_list)

        # Reset drag data
        self.drag_data = {"x": 0, "y": 0, "item": None, "original_pos": None, "moved": False}
        
        # Redraw all buttons in their new positions with current filters
        if self.current_filter:
            filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
            if self.active_tag_filters:
                tag_filtered = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
                filtered_pcs = [pc for pc in filtered_pcs if pc in tag_filtered]
        elif self.active_tag_filters:
            filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
        else:
            filtered_pcs = self.vm_manager.pc_names
        
        self.position_buttons(filtered_pcs)

    def _get_drop_position(self, x, y):
        """Calculate the position where the button should be dropped"""
        # Get button dimensions from position_buttons
        canvas_width = self.canvas.winfo_width()
        BUTTONS_PER_ROW = 3
        MARGIN_LEFT = canvas_width * 0.02
        MARGIN_RIGHT = canvas_width * 0.02
        BUTTON_SPACING = canvas_width * 0.02
        
        available_width = canvas_width - (MARGIN_LEFT + MARGIN_RIGHT + (BUTTONS_PER_ROW - 1) * BUTTON_SPACING)
        button_width = available_width / BUTTONS_PER_ROW
        button_height = button_width * 0.6

        # Calculate row and column from drop coordinates
        col = int((x - MARGIN_LEFT) / (button_width + BUTTON_SPACING))
        row = int(y / (button_height + BUTTON_SPACING))
        
        # Ensure col is within bounds
        col = max(0, min(col, BUTTONS_PER_ROW - 1))
        
        # Calculate the position in the list
        position = row * BUTTONS_PER_ROW + col
        
        # Ensure the position is within bounds
        return max(0, min(position, len(self.vm_manager.pc_names) - 1))

    def on_button_hover(self, event, button_tag):
        """Handle mouse hover over button"""
        # Only change the background rectangle
        for item in self.canvas.find_withtag(button_tag):
            if "button_bg" in self.canvas.gettags(item):  # Check for background-specific tag
                self.canvas.itemconfig(item, fill=self.hover_active_color)

    def on_button_leave(self, event, button_tag):
        """Handle mouse leaving button"""
        # Only change the background rectangle
        for item in self.canvas.find_withtag(button_tag):
            if "button_bg" in self.canvas.gettags(item):  # Check for background-specific tag
                self.canvas.itemconfig(item, fill=self.button_bg_color)

    def set_machine_category(self, pc_name, category):
        """Set the category for a machine"""
        if self.vm_manager.set_machine_category(pc_name, category):
            # Refresh display maintaining current filter
            if self.current_filter:
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_pcs)
            else:
                self.position_buttons()

    def position_buttons(self, filtered_pcs=None):
        """Arranges machine buttons in a grid layout with responsive sizing."""
        # If no filtered PCs provided, use the active tag filters
        if filtered_pcs is None:
            if self.active_tag_filters:
                filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
            else:
                filtered_pcs = self.vm_manager.pc_names

        self.canvas.delete("all")

        # Get the actual visible area dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Fixed margins and spacing (as percentages of canvas width)
        MARGIN_LEFT = canvas_width * 0.02
        MARGIN_TOP = canvas_height * 0.02
        MARGIN_RIGHT = canvas_width * 0.02
        BUTTON_SPACING = canvas_width * 0.02
        CORNER_RADIUS = min(canvas_width, canvas_height) * 0.02
        
        # Calculate responsive button dimensions
        BUTTONS_PER_ROW = 3
        available_width = canvas_width - (MARGIN_LEFT + MARGIN_RIGHT + (BUTTONS_PER_ROW - 1) * BUTTON_SPACING)
        button_width = available_width / BUTTONS_PER_ROW
        button_height = button_width * 0.6
        
        # Calculate font sizes based on button dimensions
        title_font_size = int(min(button_width * 0.08, button_height * 0.15))
        info_font_size = int(min(button_width * 0.06, button_height * 0.12))
        status_font_size = int(min(button_width * 0.05, button_height * 0.1))
        
        # Ensure minimum font sizes
        title_font_size = max(title_font_size, 10)
        info_font_size = max(info_font_size, 8)
        status_font_size = max(status_font_size, 8)

        for idx, pc_name in enumerate(filtered_pcs):
            col = idx % BUTTONS_PER_ROW
            row = idx // BUTTONS_PER_ROW
            
            x = MARGIN_LEFT + col * (button_width + BUTTON_SPACING)
            y = MARGIN_TOP + row * (button_height + BUTTON_SPACING)
            
            last_used = self.vm_manager.get_last_used_time(pc_name)
            description = self.vm_manager.get_description(pc_name)

            # Create button with responsive dimensions and font sizes
            self.create_rounded_button(
                pc_name, 
                last_used, 
                description,
                lambda name=pc_name: self.vm_manager.connect_to_pc(name),
                x, y, 
                button_width, 
                button_height, 
                CORNER_RADIUS,
                title_font_size,
                info_font_size,
                status_font_size
            )

        # Update scroll region using filtered list length
        total_height = MARGIN_TOP + ((len(filtered_pcs) - 1) // BUTTONS_PER_ROW + 1) * (button_height + BUTTON_SPACING)
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))

    def show_category_context_menu(self, event, category):
        """Show context menu for category button"""
        if category == "Default":
            return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.configure(**MenuStyle.get_themed_menu_style(self.current_theme))
        
        # Add rename option
        menu.add_command(
            label=f"Rename '{category}'",
            command=lambda: self.show_rename_category_dialog(category)
        )
        
        # Add color submenu
        color_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Change Color", menu=color_menu)
        
        # Add color options from current theme
        theme_colors = self.CATEGORY_COLORS[self.current_theme]
        for color_name, color_hex in theme_colors.items():
            color_menu.add_command(
                label=color_name,
                command=lambda c=color_hex: self.change_category_color(category, c),
                background=color_hex
            )
        
        menu.add_separator()
        menu.add_command(
            label=f"Delete '{category}'",
            command=lambda: self.delete_category(category)
        )
        menu.tk_popup(event.x_root, event.y_root)

    def show_rename_category_dialog(self, category):
        """Show dialog for renaming a category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Rename Category")
        dialog.configure(bg=self.primary_bg_color)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set size and position
        dialog_width = 300
        dialog_height = 150
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create main frame
        main_frame = tk.Frame(dialog, bg=self.primary_bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label
        tk.Label(
            main_frame,
            text=f"Rename '{category}' to:",
            font=('Segoe UI', 11),
            bg=self.primary_bg_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        # Entry field
        entry = tk.Entry(
            main_frame,
            font=('Segoe UI', 11),
            bg=self.secondary_bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            width=30
        )
        entry.insert(0, category)  # Pre-fill with current name
        entry.select_range(0, tk.END)  # Select all text
        entry.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.primary_bg_color)
        button_frame.pack(fill=tk.X)
        
        def handle_rename():
            new_name = entry.get().strip()
            if new_name and new_name != category:
                if self.rename_category(category, new_name):
                    dialog.destroy()
        
        # OK button
        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=handle_rename,
            width=10,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10),
            relief="flat"
        )
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=10,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10),
            relief="flat"
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to OK button
        entry.bind('<Return>', lambda e: handle_rename())
        
        # Bind Escape key to Cancel
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
        # Set focus to entry
        entry.focus_set()

    def rename_category(self, old_name, new_name):
        """Rename a category"""
        if old_name == "Default" or new_name == "Default":
            messagebox.showerror("Error", "Cannot rename the Default category")
            return False
        
        if new_name in self.vm_manager.categories:
            messagebox.showerror("Error", f"Category '{new_name}' already exists")
            return False
        
        try:
            # Update the category name in the list
            index = self.vm_manager.categories.index(old_name)
            self.vm_manager.categories[index] = new_name
            
            # Update all machines that use this category
            for machine, category in self.vm_manager.machine_categories.items():
                if category == old_name:
                    self.vm_manager.machine_categories[machine] = new_name
            
            # Update the category color if it exists
            if old_name in self.vm_manager.category_colors:
                self.vm_manager.category_colors[new_name] = self.vm_manager.category_colors[old_name]
                del self.vm_manager.category_colors[old_name]
            
            # Update current filter if needed
            if self.current_filter == old_name:
                self.current_filter = new_name
            
            # Save all changes
            self.vm_manager.file_manager.save_categories(self.vm_manager.categories)
            self.vm_manager.file_manager.save_machine_categories(self.vm_manager.machine_categories)
            self.vm_manager.file_manager.save_category_colors(self.vm_manager.category_colors)
            
            # Update the UI
            self.update_category_buttons()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename category: {str(e)}")
            return False

    def delete_category(self, category):
        """Delete a category after confirmation"""
        if category == "Default":
            messagebox.showerror("Error", "Cannot delete the Default category")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete the category '{category}'?\n"
                              "All machines in this category will be unassigned."):
            if self.vm_manager.delete_category(category):
                # If we're deleting the currently selected category, reset to Default
                if self.current_filter == category:
                    self.current_filter = "Default"
                    filtered_pcs = self.vm_manager.get_machines_by_category("Default")
                    self.position_buttons(filtered_pcs)
                
                # Update the category buttons
                self.update_category_buttons()

    def show_tag_manager(self):
        """Show dialog for managing tags"""
        dialog = tk.Toplevel(self.root)
        self._current_tag_dialog = dialog
        dialog.title("Manage Tags")
        
        # Update icon loading logic
        try:
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = os.path.dirname(sys.executable)
                assets_path = os.path.join(base_path, "assets")
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
                assets_path = os.path.join(base_path, "assets")
            
            # Tag manager window icon
            icon_path = os.path.join(assets_path, "tag_icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
            else:
                print(f"Warning: Could not find tag manager icon at {icon_path}")
                
        except Exception as e:
            print(f"Warning: Could not load tag manager window icon: {e}")
        
        # Set dialog size
        dialog_width = 600
        dialog_height = 400
        
        # Get screen dimensions
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        # Calculate position coordinates
        center_x = int((screen_width - dialog_width) / 2)
        center_y = int((screen_height - dialog_height) / 2)
        
        # Set size and position
        dialog.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")
        dialog.configure(bg=self.primary_bg_color)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create a frame for the tag list (now at the top)
        tag_list_frame = tk.Frame(dialog, bg=self.primary_bg_color)
        tag_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        def update_tag_list():
            """Update the list of tags in the dialog"""
            # Clear existing tags
            for widget in tag_list_frame.winfo_children():
                widget.destroy()
                
            # Add header row
            header_frame = tk.Frame(tag_list_frame, bg=self.primary_bg_color)
            header_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(header_frame, text="Tag Name", 
                    bg=self.primary_bg_color, fg=self.text_color, 
                    font=('Helvetica', 10, 'bold')).pack(side="left", padx=10)
            
            tk.Label(header_frame, text="Assigned To", 
                    bg=self.primary_bg_color, fg=self.text_color,
                    font=('Helvetica', 10, 'bold')).pack(side="left", padx=10, expand=True)
                
            # Add each tag with assigned machines and delete options
            for tag in self.vm_manager.tags:
                tag_frame = tk.Frame(tag_list_frame, bg=self.primary_bg_color)
                tag_frame.pack(fill="x", pady=2)
                
                # Tag name
                tk.Label(tag_frame, text=tag, 
                        bg=self.primary_bg_color, fg=self.text_color).pack(side="left", padx=10)
                
                # Get machines with this tag
                assigned_machines = [m for m in self.vm_manager.pc_names 
                                   if tag in self.vm_manager.get_machine_tags(m)]
                
                # Assigned machines frame (scrollable if many machines)
                machines_frame = tk.Frame(tag_frame, bg=self.primary_bg_color)
                machines_frame.pack(side="left", expand=True, fill="x", padx=10)
                
                for machine in assigned_machines:
                    machine_frame = tk.Frame(machines_frame, bg=self.primary_bg_color)
                    machine_frame.pack(side="left", padx=(0, 5))
                    
                    # Machine name
                    tk.Label(machine_frame, text=machine,
                            bg=self.secondary_bg_color, fg=self.text_color,
                            padx=5).pack(side="left")
                    
                    # Delete tag from machine button - Remove 'self.' from the lambda
                    tk.Button(machine_frame, text="✕",
                             command=lambda m=machine, t=tag: handle_remove_tag(m, t),
                             bg=self.button_bg_color, fg="red",
                             width=2, padx=2).pack(side="left")
                
                # Delete entire tag button - Remove 'self.' from the lambda
                tk.Button(tag_frame, text="Delete Tag",
                         command=lambda t=tag: handle_delete_tag(t),
                         bg="#dc3545", fg="white",
                         padx=5).pack(side="right", padx=10)

        def handle_remove_tag(machine, tag):
            """Local handler for removing tag from machine"""
            if self.vm_manager.remove_machine_tag(machine, tag):
                update_tag_list()
                if self.active_tag_filters:
                    filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
                    self.position_buttons(filtered_pcs)

        def handle_delete_tag(tag):
            """Local handler for deleting entire tag"""
            if self.vm_manager.delete_tag(tag):
                update_tag_list()
                if self.active_tag_filters:
                    filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
                    self.position_buttons(filtered_pcs)
                # Add this line to update the sidebar
                self.update_tag_filters()

        # Add tag frame (now at the bottom)
        add_frame = tk.Frame(dialog, bg=self.primary_bg_color)
        add_frame.pack(pady=10, padx=10, fill="x", side=tk.BOTTOM)
        
        # Tag input with placeholder
        tag_entry = tk.Entry(
            add_frame,
            font=('Helvetica', 12),
            bg=self.secondary_bg_color,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        tag_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 5))

        # Add placeholder text
        tag_entry.insert(0, "Enter new tag...")
        tag_entry.config(fg='gray')

        def on_entry_click(event):
            """Handle entry field click"""
            if tag_entry.get() == "Enter new tag...":
                tag_entry.delete(0, tk.END)
                tag_entry.config(fg=self.text_color)

        def on_focus_out(event):
            """Handle focus leaving entry field"""
            if tag_entry.get().strip() == "":
                tag_entry.delete(0, tk.END)  # Clear any spaces
                tag_entry.insert(0, "Enter new tag...")
                tag_entry.config(fg='gray')

        tag_entry.bind('<FocusIn>', on_entry_click)
        tag_entry.bind('<FocusOut>', on_focus_out)
        
        # Function to handle adding a tag
        def add_tag():
            tag_name = tag_entry.get().strip()
            if tag_name and tag_name != "Enter new tag...":
                if self.vm_manager.add_tag(tag_name):
                    tag_entry.delete(0, tk.END)
                    tag_entry.insert(0, "Enter new tag...")  # Reset placeholder
                    tag_entry.config(fg='gray')  # Reset color
                    tag_entry.focus_set()  # Give focus back to entry
                    tag_entry.select_range(0, tk.END)  # Select all text
                    self.update_tag_filters()
                    update_tag_list()
        
        # Add button
        add_btn = tk.Button(
            add_frame,
            text="Add Tag",
            command=add_tag,
            font=('Helvetica', 12),
            bg=self.button_bg_color,
            fg=self.text_color
        )
        add_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to add_tag function
        tag_entry.bind('<Return>', lambda e: add_tag())
        
        # Initially populate the tag list
        update_tag_list()

    def toggle_machine_tag(self, machine_name, tag):
        """Toggle a tag on/off for a machine"""
        current_tags = self.vm_manager.get_machine_tags(machine_name)
        
        if tag in current_tags:
            # Remove tag
            if self.vm_manager.remove_machine_tag(machine_name, tag):
                # Refresh with current filters
                self.refresh_filtered_view()
        else:
            # Add tag
            if self.vm_manager.add_machine_tag(machine_name, tag):
                # Refresh with current filters
                self.refresh_filtered_view()

    def refresh_filtered_view(self):
        """Refresh the view maintaining current filters"""
        if hasattr(self, 'active_tag_filters') and self.active_tag_filters:
            if hasattr(self, 'current_filter') and self.current_filter:
                # Both tag and category filters active
                tag_filtered = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
                category_filtered = self.vm_manager.get_machines_by_category(self.current_filter)
                filtered_pcs = [pc for pc in tag_filtered if pc in category_filtered]
            else:
                # Only tag filters active
                filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
        elif hasattr(self, 'current_filter') and self.current_filter:
            # Only category filter active
            filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
        else:
            # No filters active
            filtered_pcs = self.vm_manager.pc_names
        
        self.position_buttons(filtered_pcs)

    def center_window(self, window, width, height):
        """Center a window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def handle_tag_selection(self, event):
        """Handle tag selection"""
        selected_tags = self.tag_sidebar.get_selected_tags()
        if selected_tags:
            # Get machines that match the tag filter
            filtered_machines = self.vm_manager.get_machines_by_multiple_tags(selected_tags)
            
            # If there's a category filter active, apply it as well
            if hasattr(self, 'current_filter') and self.current_filter:
                category_machines = self.vm_manager.get_machines_by_category(self.current_filter)
                # Only show machines that match both filters
                filtered_machines = [m for m in filtered_machines if m in category_machines]
            
            self.active_tag_filters = set(selected_tags)  # Store active filters
            self.position_buttons(filtered_machines)
        else:
            self.active_tag_filters = set()  # Clear active filters
            # If category filter is active, show only those machines
            if hasattr(self, 'current_filter') and self.current_filter:
                filtered_machines = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_machines)
            else:
                self.position_buttons()

    def handle_tag_added(self, event):
        """Handle new tag added"""
        print(f"Tag added: {self.tag_sidebar.last_added_tag}")
        self.vm_manager.tags = self.tag_manager.get_all_tags()
        if hasattr(self, '_current_tag_dialog'):
            self._current_tag_dialog.update_tag_list()
        self.position_buttons()

    def handle_tag_removed(self, event):
        """Handle tag removed"""
        print(f"Tag removed: {self.tag_sidebar.last_removed_tag}")
        self.position_buttons()

    def create_add_pc_section(self):
        """Create the Add PC section in sidebar"""
        # Add Single PC Label
        self.add_single_pc_label = tk.Label(
            self.left_frame,
            text="Add Single PC",
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Helvetica', 12)
        )
        self.add_single_pc_label.pack(anchor="w", pady=(10, 5), padx=(10, 0))

        # Add Single PC input frame
        self.single_pc_input_frame = tk.Frame(
            self.left_frame,
            bg=self.secondary_bg_color
        )
        self.single_pc_input_frame.pack(fill="x", padx=10)

        # Single PC input
        self.single_pc_entry = tk.Entry(
            self.single_pc_input_frame,
            font=('Helvetica', 12),
            bg=self.primary_bg_color,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        self.single_pc_entry.pack(side=tk.LEFT, expand=True, fill="x", padx=(0, 5))

        # Add PC Button
        self.add_pc_btn = tk.Button(
            self.single_pc_input_frame,
            text="+",
            command=self.add_single_pc,
            font=('Helvetica', 12),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=3
        )
        self.add_pc_btn.pack(side=tk.RIGHT)

        # Multiple PC Button
        multi_pc_btn = tk.Button(
            self.left_frame,
            text="Add Multiple PCs",
            command=self.show_multi_pc_dialog,
            font=('Helvetica', 12),
            bg=self.button_bg_color,
            fg=self.text_color
        )
        multi_pc_btn.pack(pady=5, padx=10, fill="x")

    def update_category_buttons(self):
        """Update category buttons in sidebar"""
        # Clear existing buttons
        for widget in self.category_buttons_container.winfo_children():
            widget.destroy()
        
        # Create button for each category
        for category in self.vm_manager.categories:
            # For Default category, use theme button color
            if category == "Default":
                button_color = self.button_bg_color
            else:
                # Get saved color or default to theme's blue
                default_color = "#808080"  # Neutral gray color
                saved_color = self.vm_manager.category_colors.get(category, default_color)
                button_color = saved_color

            def create_hover_handlers(btn, original_color):
                def on_enter(e):
                    btn.configure(bg=self.hover_active_color)
                
                def on_leave(e):
                    btn.configure(bg=original_color)
                
                return on_enter, on_leave

            # Add checkmark if category is selected
            button_text = f"✓ {category}" if self.current_filter == category else f"  {category}"

            button = tk.Button(
                self.category_buttons_container,
                text=button_text,
                font=('Segoe UI', 12, 'bold'),
                relief="solid",
                bd=1,
                cursor="hand2",
                bg=button_color,
                fg=self.text_color,
                anchor="w",
                padx=15,
                pady=5
            )
            button.pack(fill="x", pady=3)

            # Create and bind hover handlers
            on_enter, on_leave = create_hover_handlers(button, button_color)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
            
            # Bind click event
            button.bind('<Button-1>', lambda e, b=button, c=category: self.start_category_drag(e, b, c))
            button.bind('<B1-Motion>', lambda e, b=button: self.drag_category(e, b))
            button.bind('<ButtonRelease-1>', lambda e, c=category: self.end_category_drag(e, c))

            # Add back the right-click binding for context menu
            if category != "Default":  # Don't show context menu for Default category
                button.bind('<Button-3>', lambda e, c=category: self.show_category_context_menu(e, c))

    def change_category_color(self, category, color):
        """Change the color of a category"""
        self.vm_manager.category_colors[category] = color
        self.vm_manager.file_manager.save_category_colors(self.vm_manager.category_colors)
        self.update_category_buttons()

    def remove_category(self, category):
        """Remove a category"""
        if category != "Default":  # Prevent removing Default category
            if self.vm_manager.remove_category(category):
                # If we're deleting the currently selected category, reset to Default
                if self.current_filter == category:
                    self.current_filter = "Default"
                    filtered_pcs = self.vm_manager.get_machines_by_category("Default")
                    self.position_buttons(filtered_pcs)
                
                # Update the category buttons
                self.update_category_buttons()

    def filter_by_category(self, category_name):
        """Filter machines by category"""
        # If clicking the same category again (including Default), deselect it
        if self.current_filter == category_name:
            self.current_filter = None  # Clear the filter
            filtered_pcs = self.vm_manager.pc_names  # Show all PCs
        else:
            # Set new filter (even for Default category)
            self.current_filter = category_name
            # Get machines for the selected category
            filtered_pcs = self.vm_manager.get_machines_by_category(category_name)
        
        # If there are active tag filters, apply them as well
        if hasattr(self, 'active_tag_filters') and self.active_tag_filters:
            tag_filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
            # Show only machines that match both category and tag filters
            filtered_pcs = [pc for pc in filtered_pcs if pc in tag_filtered_pcs]
        
        # Update the category buttons to show the selected state
        self.update_category_buttons()
        
        self.position_buttons(filtered_pcs)

    def add_category_dialog(self):
        """Show dialog to add a new category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Category")
        dialog.configure(bg=self.primary_bg_color)

        # Add icon loading logic
        try:
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
        
            icon_path = os.path.join(base_path, "assets", "settings_icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not load dialog icon: {e}")
        
        # Set size and position
        dialog_width = 300
        dialog_height = 250
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(dialog, bg=self.primary_bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label
        tk.Label(
            main_frame,
            text="Enter category name:",
            font=('Segoe UI', 11),
            bg=self.primary_bg_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        # Entry field
        entry = tk.Entry(
            main_frame,
            font=('Segoe UI', 11),
            bg=self.secondary_bg_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            width=30
        )
        entry.pack(pady=(0, 20))
        
        # Color selection label
        tk.Label(
            main_frame,
            text="Select color:",
            font=('Segoe UI', 11),
            bg=self.primary_bg_color,
            fg=self.text_color
        ).pack(pady=(0, 10))
        
        # Color selection frame
        color_frame = tk.Frame(main_frame, bg=self.primary_bg_color)
        color_frame.pack(pady=(0, 20))
        
        # Get theme-appropriate colors
        theme_colors = self.CATEGORY_COLORS[self.current_theme]
        default_color = "#808080"  # Use gray as default
        selected_color = tk.StringVar(value=default_color)  # Set default to gray instead of blue
        
        # Create color buttons
        for color_name, color_hex in theme_colors.items():
            color_btn = tk.Button(
                color_frame,
                width=3,
                height=1,
                bg=color_hex,  # Use the actual color hex value
                relief="raised",
                cursor="hand2",
                command=lambda c=color_hex: selected_color.set(c)
            )
            color_btn.pack(side=tk.LEFT, padx=2)
            
            # Add tooltip
            self.create_tooltip(color_btn, color_name)
        
        entry.focus_set()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.primary_bg_color)
        button_frame.pack(fill=tk.X)
        
        def handle_ok():
            category_name = entry.get().strip()
            if category_name:
                if self.vm_manager.add_category(category_name, selected_color.get()):
                    self.update_category_buttons()
                dialog.destroy()
        
        # OK button
        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=handle_ok,
            width=10,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10),
            relief="flat"
        )
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=10,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10),
            relief="flat"
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to OK button
        entry.bind('<Return>', lambda e: handle_ok())
        
        # Bind Escape key to Cancel
        dialog.bind('<Escape>', lambda e: dialog.destroy())

    def create_category_section(self):
        """Create the category management section in sidebar"""
        # Category Frame
        category_frame = tk.Frame(
            self.left_frame,
            bg=self.secondary_bg_color
        )
        category_frame.pack(pady=10, padx=10, fill="x")

        # Categories Label
        self.categories_label = tk.Label(
            category_frame,
            text="Categories",
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Helvetica', 14, 'bold')
        )
        self.categories_label.pack(anchor="w", pady=(0, 5))

        # Container for category buttons
        self.category_buttons_container = tk.Frame(
            category_frame,
            bg=self.secondary_bg_color
        )
        self.category_buttons_container.pack(fill="x", padx=5, pady=5)

        # Add Category Button - Updated style
        self.add_category_btn = tk.Button(
            category_frame,
            text="Add Category+",
            command=self.add_category_dialog,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold'),  # Increased font size and made bold
            relief="solid",
            bd=1,
            cursor="hand2",
            pady=8,  # Added vertical padding
            padx=15  # Added horizontal padding
        )
        self.add_category_btn.pack(pady=(10, 5), padx=5, fill="x")

        # Create initial category buttons
        self.update_category_buttons()

    def show_multi_pc_dialog(self):
        """Show dialog for adding multiple PCs"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Multiple PCs")
        dialog.geometry("400x300")
        dialog.configure(bg=self.primary_bg_color)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Add explanation label
        tk.Label(
            dialog,
            text="Enter PC names (one per line):",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Helvetica', 12)
        ).pack(pady=10, padx=10)

        # Text area for PC names
        text_area = tk.Text(
            dialog,
            height=10,
            width=40,
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Helvetica', 12),
            insertbackground=self.text_color
        )
        text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Buttons frame
        btn_frame = tk.Frame(dialog, bg=self.primary_bg_color)
        btn_frame.pack(pady=10, padx=10, fill=tk.X)

        # Add button
        tk.Button(
            btn_frame,
            text="Add PCs",
            command=lambda: self.add_multiple_pcs_from_dialog(text_area, dialog),
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Helvetica', 12)
        ).pack(side=tk.LEFT, expand=True, padx=5)

        # Cancel button
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Helvetica', 12)
        ).pack(side=tk.LEFT, expand=True, padx=5)

    def add_multiple_pcs_from_dialog(self, text_area, dialog):
        """Add multiple PCs from dialog text area"""
        pc_text = text_area.get("1.0", tk.END).strip()
        if pc_text:
            pcs = pc_text.splitlines()
            added_count = 0
            for pc in pcs:
                if self.vm_manager.add_pc(pc.strip()):
                    added_count += 1
            self.position_buttons()
            dialog.destroy()
            if added_count > 0:
                messagebox.showinfo("Success", f"Added {added_count} PCs successfully!")

    def _create_tags_menu(self, menu, pc_name):
        """Create the improved tags submenu"""
        tags_menu = tk.Menu(menu, tearoff=0)
        tags_menu.configure(**MenuStyle.get_themed_menu_style(self.current_theme))
        
        # Add New Tag option
        tags_menu.add_command(
            label="+ Add New Tag",
            command=lambda: self.tag_sidebar._show_add_tag_dialog()
        )
        
        tags_menu.add_separator()
        tags_menu.add_label("Current Tags:")  # Header for existing tags
        
        # Add existing tags with checkboxes
        machine_tags = self.vm_manager.get_machine_tags(pc_name)
        for tag in sorted(self.vm_manager.tags):
            is_tagged = tag in machine_tags
            check_var = tk.BooleanVar(value=is_tagged)
            tags_menu.add_checkbutton(
                label=tag,
                onvalue=1,
                offvalue=0,
                variable=check_var,
                command=lambda t=tag: self.vm_manager.toggle_machine_tag(pc_name, t)
            )
        
        tags_menu.add_separator()
        tags_menu.add_command(
            label="🏷️ Manage All Tags",
            command=self.show_tag_manager
        )
        
        return tags_menu

    def _show_machine_context_menu(self, event, pc_name):
        """Show context menu for machine"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.configure(**MenuStyle.get_themed_menu_style(self.current_theme))
        
        # Category submenu (existing code remains the same)
        category_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Set Category", menu=category_menu)
        for category in self.vm_manager.categories:
            category_menu.add_command(
                label=category,
                command=lambda c=category: self.set_machine_category(pc_name, c)
            )
        
        # Add the improved tags menu
        menu.add_cascade(label="Manage Tags", menu=self._create_tags_menu(menu, pc_name))
        
        # Rest of the menu items remain the same
        menu.add_command(label=f"Remove from '{pc_name}'", command=lambda: self.delete_pc(pc_name))
        menu.add_cascade(label="Share", menu=self._create_share_menu(pc_name))
        menu.add_command(label="Set RDP Path", command=lambda: self.set_rdp_path(pc_name))
        menu.add_command(label="Edit Description", command=lambda: self.edit_description(pc_name))
        menu.add_command(label="Delete", command=lambda: self.delete_pc(pc_name))
        
        menu.tk_popup(event.x_root, event.y_root)

    def update_tag_filters(self):
        """Update tag filters after tag changes"""
        if hasattr(self, 'tag_sidebar'):
            self.tag_sidebar.set_tags(list(self.vm_manager.tags))

    def handle_tag_drop(self, tag_name, x, y):
        """Handles drag-and-drop of tags onto machine buttons."""
        # Find which machine button is under the drop position
        items = self.canvas.find_overlapping(x, y, x, y)
        for item in items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("button_"):
                    machine_name = tag.replace("button_", "")
                    # Add the tag to the machine
                    self.vm_manager.add_machine_tag(machine_name, tag_name)
                    self.position_buttons()
                    return True
        return False

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=2
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)

    def reorder_categories(self, new_order):
        """Reorder categories according to the provided list"""
        # Ensure Default stays first
        if "Default" in new_order:
            new_order.remove("Default")
        
        # Reconstruct categories list with Default first
        self.categories = ["Default"] + new_order
        self.file_manager.save_categories(self.categories)
        return True

    def start_category_drag(self, event, button, category):
        """Start dragging a category"""
        if category != "Default":  # Prevent dragging Default category
            # Store the original event for later comparison
            self._drag_start_x = event.x
            self._drag_start_y = event.y
            self.dragging_category = True
            self.drag_data = {
                "widget": button,
                "y": event.y,
                "start_y": button.winfo_y(),
                "category": category
            }
            button.lift()
            button.configure(bg=self.hover_active_color)
        else:
            # For Default category, just handle the click
            self.filter_by_category(category)

    def drag_category(self, event, button):
        """Handle category button drag"""
        if hasattr(self, 'dragging_category') and self.dragging_category:
            # Calculate new position
            delta_y = event.y_root - button.winfo_rooty() - self.drag_data["y"]
            new_y = button.winfo_y() + delta_y
            
            # Keep button within container bounds
            min_y = 0
            max_y = self.category_buttons_container.winfo_height() - button.winfo_height()
            new_y = max(min_y, min(new_y, max_y))
            
            # Move the button
            button.place(y=new_y, x=0, relwidth=1)

    def end_category_drag(self, event, category):
        """Handle category drag end"""
        if hasattr(self, 'dragging_category') and self.dragging_category:
            button = self.drag_data["widget"]
            
            # Check if this was a click rather than a drag
            if (abs(event.x - getattr(self, '_drag_start_x', 0)) < 5 and 
                abs(event.y - getattr(self, '_drag_start_y', 0)) < 5):
                # This was a click - call the filter function
                self.filter_by_category(category)
            else:
                # This was a drag - reorder categories
                buttons = sorted(
                    [w for w in self.category_buttons_container.winfo_children() if isinstance(w, tk.Button)],
                    key=lambda w: w.winfo_y()
                )
                
                new_order = []
                for btn in buttons:
                    cat_name = btn.cget("text").replace("✓ ", "").strip()
                    if cat_name != "Default":
                        new_order.append(cat_name)
                
                self.vm_manager.reorder_categories(new_order)
            
            # Reset drag state
            self.dragging_category = False
            self.drag_data = {"widget": None, "y": 0}
            
            # Refresh category buttons
            self.update_category_buttons()

    def show_add_single_dialog(self):
        """Show dialog to add a single PC"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Single PC")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create and pack widgets
        tk.Label(dialog, text="Enter PC Name:").pack(pady=10)
        entry = tk.Entry(dialog)
        entry.pack(pady=5, padx=20, fill=tk.X)
        
        def add_pc():
            pc_name = entry.get().strip()
            if pc_name:
                self.vm_manager.add_pc(pc_name)
                dialog.destroy()
                self.refresh_buttons()
        
        # Add button
        add_button = tk.Button(dialog, text="Add", command=add_pc)
        add_button.pack(pady=10)
        
        # Bind Enter key to add_pc function
        dialog.bind('<Return>', lambda e: add_pc())
        
        # Set focus to entry
        entry.focus_set()

    def handle_machine_click(self, pc_name, command):
        """Handle machine button click while maintaining filters"""
        command()  # Execute the connection command
        
        # Reapply current filters
        if self.current_filter:
            # Get machines for current category filter
            filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
            
            # If there are also tag filters, apply them
            if self.active_tag_filters:
                tag_filtered = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
                filtered_pcs = [pc for pc in filtered_pcs if pc in tag_filtered]
        elif self.active_tag_filters:
            # Only tag filters active
            filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(list(self.active_tag_filters))
        else:
            # No filters active
            filtered_pcs = self.vm_manager.pc_names
        
        self.position_buttons(filtered_pcs)

    def clear_dns_cache(self, pc_name=None):
        """Show instructions for clearing DNS cache with copy and execute options"""
        dns_dialog = tk.Toplevel(self.root)
        dns_dialog.title("Clear DNS Cache Instructions")
        dns_dialog.geometry("500x550")  # Increased height to show all content
        dns_dialog.configure(bg=self.primary_bg_color)
        dns_dialog.transient(self.root)
        dns_dialog.grab_set()
        dns_dialog.resizable(False, False)  # Make dialog non-resizable

        # Center the dialog on screen
        screen_width = dns_dialog.winfo_screenwidth()
        screen_height = dns_dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 550) // 2
        dns_dialog.geometry(f"500x550+{x}+{y}")

        # Main frame with padding
        main_frame = tk.Frame(dns_dialog, bg=self.primary_bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Instructions
        tk.Label(
            main_frame,
            text="To clear the DNS cache, you can use one of these methods:",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 11),
            wraplength=460
        ).pack(pady=(0, 15))

        # Command Prompt method
        cmd_frame = tk.LabelFrame(
            main_frame,
            text=" Command Prompt ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        )
        cmd_frame.pack(fill="x", pady=(0, 15))

        cmd_code = "ipconfig /flushdns"
        tk.Label(
            cmd_frame,
            text=cmd_code,
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Consolas', 11),
            padx=10,
            pady=5
        ).pack(pady=5)

        tk.Button(
            cmd_frame,
            text="📋 Copy CMD Command",
            command=lambda: self.root.clipboard_append(cmd_code),
            bg=self.button_bg_color,
            fg=self.text_color
        ).pack(pady=5)

        tk.Button(
            cmd_frame,
            text="🚀 Run as Administrator",
            command=lambda: self.run_elevated_command("cmd", cmd_code),
            bg=self.button_bg_color,
            fg=self.text_color
        ).pack(pady=5)

        # PowerShell method
        ps_frame = tk.LabelFrame(
            main_frame,
            text=" PowerShell ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        )
        ps_frame.pack(fill="x", pady=(0, 15))

        ps_code = "Clear-DnsClientCache"
        tk.Label(
            ps_frame,
            text=ps_code,
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Consolas', 11),
            padx=10,
            pady=5
        ).pack(pady=5)

        tk.Button(
            ps_frame,
            text="📋 Copy PowerShell Command",
            command=lambda: self.root.clipboard_append(ps_code),
            bg=self.button_bg_color,
            fg=self.text_color
        ).pack(pady=5)

        tk.Button(
            ps_frame,
            text="🚀 Run as Administrator",
            command=lambda: self.run_elevated_command("powershell", ps_code),
            bg=self.button_bg_color,
            fg=self.text_color
        ).pack(pady=5)

        # Bottom buttons frame - moved to bottom of dialog
        bottom_frame = tk.Frame(main_frame, bg=self.primary_bg_color)
        bottom_frame.pack(fill="x", pady=(20, 0), side="bottom")  # Added more padding and explicit side

        # Retry connection button if pc_name provided
        if pc_name:
            tk.Button(
                bottom_frame,
                text=f"↺ Retry Connection to {pc_name}",
                command=lambda: [dns_dialog.destroy(), self.vm_manager.connect_to_pc(pc_name)],
                bg=self.button_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 10, 'bold')
            ).pack(side="left", padx=5)

        # Close button
        tk.Button(
            bottom_frame,
            text="Close",
            command=dns_dialog.destroy,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(side="right", padx=5)

        # Bind Escape key to close dialog
        dns_dialog.bind('<Escape>', lambda e: dns_dialog.destroy())

    def run_elevated_command(self, shell_type, command):
        """Run a command with elevated privileges"""
        try:
            if shell_type == "cmd":
                # Create a temporary batch file
                with open("clear_dns.bat", "w") as f:
                    f.write(f"{command}\necho.\necho DNS cache has been cleared.\necho Press any key to exit...\npause >nul")
                
                # Run the batch file as administrator
                subprocess.run(["powershell", "Start-Process", "clear_dns.bat", "-Verb", "RunAs"])
                
                # Delete the batch file after a short delay
                self.root.after(2000, lambda: os.remove("clear_dns.bat") if os.path.exists("clear_dns.bat") else None)
                
            else:  # PowerShell
                # Create a temporary PowerShell script with proper command execution
                script_path = os.path.abspath('clear_dns.ps1')
                with open(script_path, "w") as f:
                    f.write(
                        f'Write-Host "Clearing DNS cache..." -ForegroundColor Yellow\n'
                        f'{command}\n'
                        f'Write-Host "DNS cache has been cleared." -ForegroundColor Green\n'
                        f'Write-Host "Press any key to exit..." -ForegroundColor Cyan\n'
                        f'$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")\n'
                        f'exit'  # Add explicit exit command
                    )
                
                # Run the PowerShell script as administrator without -NoExit flag
                powershell_command = f'Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File {script_path}" -Verb RunAs'
                subprocess.run(["powershell", "-Command", powershell_command])
                
                # Delete the script file after a short delay
                self.root.after(2000, lambda: os.remove(script_path) if os.path.exists(script_path) else None)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run command: {str(e)}")

    def show_troubleshoot_window(self, pc_name=None):
        """Show troubleshooting window for a machine"""
        troubleshoot_dialog = tk.Toplevel(self.root)
        troubleshoot_dialog.title(f"Troubleshoot - {pc_name}")
        troubleshoot_dialog.geometry("700x1000")  # Increased height from 900 to 1000
        troubleshoot_dialog.configure(bg=self.primary_bg_color)
        troubleshoot_dialog.transient(self.root)
        troubleshoot_dialog.grab_set()
        troubleshoot_dialog.resizable(False, False)

        # Update the centering calculation:
        screen_width = troubleshoot_dialog.winfo_screenwidth()
        screen_height = troubleshoot_dialog.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 1000) // 2  # Changed from 900 to 1000
        troubleshoot_dialog.geometry(f"700x1000+{x}+{y}")

        # Move the Automated Diagnostics section right after Network Diagnostics
        # and before Troubleshooting Tools (around line 350)
        # Cut the entire diagnostics_frame section from the bottom and paste it here

        # Define on_close function early
        def on_close():
            if hasattr(self, '_ping_running'):
                self._ping_running = False
            troubleshoot_dialog.destroy()

        # Main frame
        main_frame = tk.Frame(troubleshoot_dialog, bg=self.primary_bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 1. Machine Info Section
        info_frame = tk.LabelFrame(
            main_frame,
            text=" Machine Information ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold')
        )
        info_frame.pack(fill="x", pady=(0, 15))

        # Current IP
        current_ip = "Checking..."
        try:
            current_ip = socket.gethostbyname(pc_name)
        except socket.gaierror:
            current_ip = "Could not resolve hostname"

        # Stored IP
        stored_ip = self.vm_manager.machine_ips.get(pc_name, "No stored IP")

        # Add machine info
        tk.Label(
            info_frame,
            text=f"Machine Name: {pc_name}",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(anchor="w", pady=5, padx=10)

        tk.Label(
            info_frame,
            text=f"Current IP: {current_ip}",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(anchor="w", pady=5, padx=10)

        tk.Label(
            info_frame,
            text=f"Stored IP: {stored_ip}",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(anchor="w", pady=5, padx=10)

        # 2. Connection Status Section - Enhanced version
        status_frame = tk.LabelFrame(
            main_frame,
            text=" Connection Status ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold')
        )
        status_frame.pack(fill="x", pady=(0, 15))

        # Create a frame for status indicators
        status_indicators = tk.Frame(status_frame, bg=self.primary_bg_color)
        status_indicators.pack(fill="x", padx=10, pady=5)

        # Status indicators with icons and colors
        status_text = tk.StringVar(value="Checking connection status...")
        status_label = tk.Label(
            status_indicators,
            textvariable=status_text,
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        )
        status_label.pack(side="left", pady=5)

        # Add health indicator
        health_text = tk.StringVar(value="Health: Unknown")
        health_label = tk.Label(
            status_indicators,
            textvariable=health_text,
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        )
        health_label.pack(side="right", pady=5)

        # Add connection history
        history_frame = tk.Frame(status_frame, bg=self.primary_bg_color)
        history_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            history_frame,
            text="Connection History:",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor="w")

        # Create a frame for text and scrollbar
        history_container = tk.Frame(history_frame, bg=self.primary_bg_color)
        history_container.pack(fill="x", pady=(5, 0))

        history_text = tk.Text(
            history_container,
            height=4,
            bg=self.secondary_bg_color,
            fg=self.text_color,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        history_text.pack(side="left", fill="x", expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(history_container, command=history_text.yview)
        scrollbar.pack(side="right", fill="y")
        history_text.configure(yscrollcommand=scrollbar.set)

        def update_status():
            """Enhanced status update with health check"""
            is_running = self.vm_manager.check_machine_status(pc_name)
            
            # Basic status
            status = "Online" if is_running else "Offline"
            color = "green" if is_running else "red"
            status_text.set(f"Status: {status}")
            status_label.configure(fg=color)
            
            # Health check
            health_status = "Good"
            health_color = "green"
            
            try:
                # Check RDP port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                rdp_status = sock.connect_ex((pc_name, 3389)) == 0
                sock.close()
                
                # Quick ping test
                ping_result = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", pc_name],
                              capture_output=True, 
                    text=True
                )
                ping_success = "Reply from" in ping_result.stdout
                
                # Determine health based on checks
                if not is_running:
                    health_status = "Offline"
                    health_color = "red"
                elif not rdp_status:
                    health_status = "RDP Unavailable"
                    health_color = "orange"
                elif not ping_success:
                    health_status = "High Latency"
                    health_color = "orange"
                
                # Add to history - temporarily enable text widget
                history_text.configure(state="normal")
                current_time = datetime.now().strftime("%H:%M:%S")
                history_text.insert("1.0", f"[{current_time}] Status: {status}, Health: {health_status}\n")
                history_text.delete("5.0", tk.END)
                history_text.configure(state="disabled")
                history_text.see("1.0")  # Scroll to latest entry
                
            except Exception as e:
                health_status = "Check Failed"
                health_color = "red"
            
            health_text.set(f"Health: {health_status}")
            health_label.configure(fg=health_color)

        # Make history text read-only
        history_text.configure(state="disabled")

        # 3. Network Diagnostics Section
        network_frame = tk.LabelFrame(
            main_frame,
            text=" Network Diagnostics ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold')
        )
        network_frame.pack(fill="x", pady=(0, 15))

        # Define ping-related variables and functions first
        ping_status = tk.StringVar(value="Start continuous ping")
        ping_results = tk.StringVar(value="")

        def toggle_continuous_ping():
            if not hasattr(self, '_ping_running'):
                self._ping_running = False
            
            if self._ping_running:
                self._ping_running = False
                ping_button.configure(text="Start Continuous Ping")
            else:
                self._ping_running = True
                ping_button.configure(text="Stop Continuous Ping")
                continuous_ping()

        def continuous_ping():
            if not self._ping_running:
                return
            
            try:
                result = subprocess.run(
                    ["ping", "-n", "1", pc_name],
                    capture_output=True,
                    text=True
                )
                
                if "Reply from" in result.stdout:
                    ping_status.set("✅ Connected")
                    ping_results.set(result.stdout.split('\n')[2])  # Get the timing line
                else:
                    ping_status.set("❌ No Response")
                    ping_results.set("Request timed out")
                
            except Exception as e:
                ping_status.set(f"❌ Error: {str(e)}")
            
            if self._ping_running:
                troubleshoot_dialog.after(1000, continuous_ping)  # Run every second

        def check_rdp_port():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((pc_name, 3389))
                if result == 0:
                    messagebox.showinfo("Port Check", "RDP Port (3389) is open and accessible!")
                else:
                    messagebox.warning("Port Check", "RDP Port (3389) is not accessible.")
                sock.close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check RDP port: {str(e)}")

        def test_network_path():
            try:
                result = subprocess.run(["tracert", "-d", "-h", "15", pc_name], 
                                      capture_output=True, text=True)
                show_path_results(result.stdout)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to test network path: {str(e)}")

        def show_path_results(results):
            results_window = tk.Toplevel(troubleshoot_dialog)
            results_window.title("Network Path Results")
            results_window.geometry("600x400")
            results_window.configure(bg=self.primary_bg_color)
            
            text_widget = tk.Text(
                results_window,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                font=('Consolas', 10)
            )
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert('1.0', results)
            text_widget.configure(state='disabled')

        # Add network diagnostic buttons
        tk.Button(
            network_frame,
            text="Check RDP Port",
            command=check_rdp_port,
            bg=self.button_bg_color,
            fg=self.text_color,
            width=20
        ).pack(pady=5, padx=10)

        tk.Button(
            network_frame,
            text="Test Network Path",
            command=test_network_path,
            bg=self.button_bg_color,
            fg=self.text_color,
            width=20
        ).pack(pady=5, padx=10)

        # Add continuous ping button
        ping_button = tk.Button(
            network_frame,
            text="Start Continuous Ping",
            command=toggle_continuous_ping,
            bg=self.button_bg_color,
            fg=self.text_color,
            width=20
        )
        ping_button.pack(pady=5, padx=10)

        # Add ping status display
        ping_monitor_frame = tk.Frame(network_frame, bg=self.primary_bg_color)
        ping_monitor_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            ping_monitor_frame,
            textvariable=ping_status,
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(side="left", padx=5)

        tk.Label(
            ping_monitor_frame,
            textvariable=ping_results,
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Consolas', 10)
        ).pack(side="left", padx=5)

        # 4. Troubleshooting Tools Section
        tools_frame = tk.LabelFrame(
            main_frame,
            text=" Troubleshooting Tools ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold')
        )
        tools_frame.pack(fill="x", pady=(0, 15))

        # Create a frame for the grid layout
        button_grid = tk.Frame(tools_frame, bg=self.primary_bg_color)
        button_grid.pack(padx=10, pady=5)

        # First column
        tk.Button(
            button_grid,
            text="Clear DNS Cache",
            command=lambda: self.run_elevated_command("powershell", "Clear-DnsClientCache"),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Increased from 20 to 25
        ).grid(row=0, column=0, pady=5, padx=5)

        tk.Button(
            button_grid,
            text="Ping Machine",
            command=lambda: ping_machine(),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Increased from 20 to 25
        ).grid(row=1, column=0, pady=5, padx=5)

        tk.Button(
            button_grid,
            text="Refresh Status",
            command=update_status,
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Increased from 20 to 25
        ).grid(row=2, column=0, pady=5, padx=5)

        # Second column
        tk.Button(
            button_grid,
            text="Open Knowledge Base",
            command=lambda: show_knowledge_base(),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Increased from 20 to 25
        ).grid(row=0, column=1, pady=5, padx=5)

        tk.Button(
            button_grid,
            text="View Event Logs",
            command=lambda: show_event_logs(),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Increased from 20 to 25
        ).grid(row=1, column=1, pady=5, padx=5)

        # Second column buttons (add this after the View Event Logs button)
        tk.Button(
            button_grid,
            text="Start Troubleshooting Wizard",
            command=lambda: show_troubleshooting_wizard(),
            bg=self.button_bg_color,
            fg=self.text_color,
            width=25  # Same width as other buttons
        ).grid(row=2, column=1, pady=5, padx=5)

        def show_troubleshooting_wizard():
            """Show step-by-step troubleshooting wizard"""
            wizard_window = tk.Toplevel(troubleshoot_dialog)
            wizard_window.title(f"Troubleshooting Wizard - {pc_name}")
            wizard_window.geometry("700x500")
            wizard_window.configure(bg=self.primary_bg_color)
            wizard_window.transient(troubleshoot_dialog)
            wizard_window.grab_set()

            # Center the window
            x = troubleshoot_dialog.winfo_x() + 50
            y = troubleshoot_dialog.winfo_y() + 50
            wizard_window.geometry(f"700x500+{x}+{y}")

            # Main frame
            wizard_frame = tk.Frame(wizard_window, bg=self.primary_bg_color)
            wizard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Step indicator
            step_label = tk.Label(
                wizard_frame,
                text="Step 1 of 5",
                bg=self.primary_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 12, 'bold')
            )
            step_label.pack(pady=(0, 10))

            # Content frame
            content_frame = tk.Frame(wizard_frame, bg=self.primary_bg_color)
            content_frame.pack(fill=tk.BOTH, expand=True)

            # Result display
            result_text = tk.Text(
                content_frame,
                height=10,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 10),
                wrap=tk.WORD
            )
            result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            current_step = {"value": 1}

            def next_step():
                if current_step["value"] < 5:
                    current_step["value"] += 1
                    update_step_content()
                    if current_step["value"] == 5:
                        next_button.configure(state="disabled")
                prev_button.configure(state="normal")

            def prev_step():
                if current_step["value"] > 1:
                    current_step["value"] -= 1
                    update_step_content()
                    if current_step["value"] == 1:
                        prev_button.configure(state="disabled")
                next_button.configure(state="normal")

            # Navigation frame
            nav_frame = tk.Frame(wizard_frame, bg=self.primary_bg_color)
            nav_frame.pack(fill=tk.X, pady=(10, 0))

            prev_button = tk.Button(
                nav_frame,
                text="← Previous",
                command=prev_step,
                bg=self.button_bg_color,
                fg=self.text_color,
                state="disabled",
                width=15
            )
            prev_button.pack(side=tk.LEFT, padx=5)

            next_button = tk.Button(
                nav_frame,
                text="Next →",
                command=next_step,
                bg=self.button_bg_color,
                fg=self.text_color,
                width=15
            )
            next_button.pack(side=tk.RIGHT, padx=5)

            close_button = tk.Button(
                nav_frame,
                text="Close",
                command=wizard_window.destroy,
                bg=self.button_bg_color,
                fg=self.text_color,
                width=15
            )

            def update_step_content():
                """Update content based on current step"""
                step = current_step["value"]
                result_text.configure(state="normal")
                result_text.delete(1.0, tk.END)
                
                if step == 1:
                    step_label.configure(text="Step 1 of 5: Basic Connectivity")
                    result_text.insert(tk.END, "Checking basic network connectivity...\n\n")
                    try:
                        ping_result = subprocess.run(
                            ["ping", "-n", "2", pc_name],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if "Reply from" in ping_result.stdout:
                            result_text.insert(tk.END, "✅ Network connectivity: OK\n")
                            result_text.insert(tk.END, "\nNext step will check DNS resolution.")
                        else:
                            result_text.insert(tk.END, "❌ Network connectivity issue detected\n")
                            result_text.insert(tk.END, "\nRecommended actions:\n")
                            result_text.insert(tk.END, "1. Check network cable connection\n")
                            result_text.insert(tk.END, "2. Verify network adapter settings\n")
                            result_text.insert(tk.END, "3. Check if machine is powered on\n")
                    except Exception as e:
                        result_text.insert(tk.END, f"❌ Error checking connectivity: {str(e)}\n")

                elif step == 2:
                    step_label.configure(text="Step 2 of 5: DNS Resolution")
                    result_text.insert(tk.END, "Checking DNS resolution...\n\n")
                    try:
                        ip = socket.gethostbyname(pc_name)
                        result_text.insert(tk.END, f"✅ DNS Resolution successful\n")
                        result_text.insert(tk.END, f"Resolved IP: {ip}\n")
                        result_text.insert(tk.END, "\nNext step will check RDP port.")
                    except socket.gaierror:
                        result_text.insert(tk.END, "❌ DNS Resolution failed\n\n")
                        result_text.insert(tk.END, "Recommended actions:\n")
                        result_text.insert(tk.END, "1. Clear DNS cache\n")
                        result_text.insert(tk.END, "2. Check DNS server settings\n")
                        result_text.insert(tk.END, "3. Verify hostname is correct\n")

                elif step == 3:
                    step_label.configure(text="Step 3 of 5: RDP Port Check")
                    result_text.insert(tk.END, "Checking RDP port (3389)...\n\n")
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        result = sock.connect_ex((pc_name, 3389))
                        sock.close()
                        if result == 0:
                            result_text.insert(tk.END, "✅ RDP Port is accessible\n")
                            result_text.insert(tk.END, "\nNext step will check RDP service.")
                        else:
                            result_text.insert(tk.END, "❌ RDP Port is not accessible\n\n")
                            result_text.insert(tk.END, "Recommended actions:\n")
                            result_text.insert(tk.END, "1. Check firewall settings\n")
                            result_text.insert(tk.END, "2. Verify RDP is enabled on remote machine\n")
                            result_text.insert(tk.END, "3. Check network security policies\n")
                    except Exception as e:
                        result_text.insert(tk.END, f"❌ Error checking RDP port: {str(e)}\n")

                elif step == 4:
                    step_label.configure(text="Step 4 of 5: RDP Service Check")
                    result_text.insert(tk.END, "Checking RDP service status...\n\n")
                    try:
                        result = subprocess.run(
                            ["powershell", "-Command",
                             f"Get-Service -ComputerName {pc_name} -Name 'TermService' | Select-Object Status"],
                            capture_output=True,
                            text=True
                        )
                        if "Running" in result.stdout:
                            result_text.insert(tk.END, "✅ RDP Service is running\n")
                            result_text.insert(tk.END, "\nNext step will perform final checks.")
                        else:
                            result_text.insert(tk.END, "❌ RDP Service is not running\n\n")
                            result_text.insert(tk.END, "Recommended actions:\n")
                            result_text.insert(tk.END, "1. Start RDP service on remote machine\n")
                            result_text.insert(tk.END, "2. Check service dependencies\n")
                            result_text.insert(tk.END, "3. Verify service account permissions\n")
                    except Exception as e:
                        result_text.insert(tk.END, f"❌ Error checking RDP service: {str(e)}\n")

                elif step == 5:
                    step_label.configure(text="Step 5 of 5: Summary")
                    result_text.insert(tk.END, "Troubleshooting Summary\n\n")
                    result_text.insert(tk.END, "Completed Checks:\n")
                    result_text.insert(tk.END, "1. Network Connectivity\n")
                    result_text.insert(tk.END, "2. DNS Resolution\n")
                    result_text.insert(tk.END, "3. RDP Port\n")
                    result_text.insert(tk.END, "4. RDP Service\n\n")
                    result_text.insert(tk.END, "Next Steps:\n")
                    result_text.insert(tk.END, "• Try connecting to the machine\n")
                    result_text.insert(tk.END, "• If issues persist, check the Event Viewer\n")
                    result_text.insert(tk.END, "• Contact IT support if needed\n")
                    
                    # Hide the Next button and show Close button
                    next_button.pack_forget()
                    close_button.pack(side=tk.RIGHT, padx=5)

                result_text.configure(state="disabled")

            # Initialize first step
            update_step_content()

        # 5. Bottom buttons frame
        bottom_frame = tk.Frame(main_frame, bg=self.primary_bg_color)
        bottom_frame.pack(fill="x", pady=(20, 0), side="bottom")

        # Retry connection button
        tk.Button(
            bottom_frame,
            text=f"↺ Retry Connection",
            command=lambda: [troubleshoot_dialog.destroy(), self.vm_manager.connect_to_pc(pc_name)],
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        ).pack(side="left", padx=5)

        # Close button
        tk.Button(
            bottom_frame,
            text="Close",
            command=troubleshoot_dialog.destroy,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        ).pack(side="right", padx=5)

        # Initial status update
        update_status()

        # Add cleanup handlers
        troubleshoot_dialog.protocol("WM_DELETE_WINDOW", on_close)
        troubleshoot_dialog.bind('<Escape>', lambda e: on_close())

        # Add this function with the other diagnostic functions
        def ping_machine():
            """Ping the machine and show results"""
            try:
                result = subprocess.run(
                    ["ping", "-n", "4", pc_name],
                    capture_output=True,
                    text=True
                )
                show_ping_results(result.stdout)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to ping machine: {str(e)}")

        def show_ping_results(results):
            """Show ping results in a new window"""
            results_window = tk.Toplevel(troubleshoot_dialog)
            results_window.title("Ping Results")
            results_window.geometry("500x300")
            results_window.configure(bg=self.primary_bg_color)
            
            text_widget = tk.Text(
                results_window,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                font=('Consolas', 10)
            )
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert('1.0', results)
            text_widget.configure(state='disabled')

        # After Network Diagnostics section and before Troubleshooting Tools
        # Add Automated Diagnostics section
        diagnostics_frame = tk.LabelFrame(
            main_frame,
            text=" Automated Diagnostics ",
            bg=self.primary_bg_color,
            fg=self.text_color,
            font=('Segoe UI', 12, 'bold')
        )
        diagnostics_frame.pack(fill="x", pady=(0, 15))

        def run_diagnostics():
            """Run a series of automated diagnostic checks"""
            progress_var.set(0)
            progress_label.configure(text="Starting diagnostics...")
            
            # Create report header
            report = ["=== Diagnostic Report ==="]
            report.append(f"Machine: {pc_name}")
            report.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # List of diagnostic checks to run
            checks = [
                ("DNS Resolution", check_dns_resolution),
                ("RDP Port", check_rdp_availability),
                ("Network Path", check_network_path),
                ("Ping Response", check_ping_response),
                ("Machine Status", check_machine_status)
            ]
            
            progress_step = 100 / len(checks)
            
            for check_name, check_func in checks:
                progress_label.configure(text=f"Running {check_name}...")
                result = check_func()
                report.append(f"[{check_name}]\n{result}\n")
                progress_var.set(progress_var.get() + progress_step)
                diagnostics_frame.update()
            
            progress_label.configure(text="Diagnostics complete!")
            progress_var.set(100)
            
            # Show report
            show_diagnostic_report("\n".join(report))

        def check_dns_resolution():
            try:
                ip = socket.gethostbyname(pc_name)
                return f"✅ DNS Resolution successful\nResolved IP: {ip}"
            except socket.gaierror:
                return "❌ DNS Resolution failed"

        def check_rdp_availability():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((pc_name, 3389))
                sock.close()
                return "✅ RDP Port (3389) is accessible" if result == 0 else "❌ RDP Port is not accessible"
            except Exception as e:
                return f"❌ RDP check failed: {str(e)}"

        def check_network_path():
            try:
                result = subprocess.run(
                    ["tracert", "-d", "-h", "5", pc_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                return f"Network path trace:\n{result.stdout}"
            except Exception as e:
                return f"❌ Network path check failed: {str(e)}"

        def check_ping_response():
            try:
                result = subprocess.run(
                    ["ping", "-n", "3", pc_name],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return result.stdout
            except Exception as e:
                return f"❌ Ping check failed: {str(e)}"

        def check_machine_status():
            is_running = self.vm_manager.check_machine_status(pc_name)
            return "✅ Machine is running" if is_running else "❌ Machine is offline"

        def show_diagnostic_report(report_text):
            report_window = tk.Toplevel(troubleshoot_dialog)
            report_window.title("Diagnostic Report")
            report_window.geometry("700x500")
            report_window.configure(bg=self.primary_bg_color)
            report_window.transient(troubleshoot_dialog)
            report_window.grab_set()  # Make window modal

            # Add report content
            report_frame = tk.Frame(report_window, bg=self.primary_bg_color)
            report_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Add text widget with scrollbar
            text_frame = tk.Frame(report_frame, bg=self.primary_bg_color)
            text_frame.pack(fill="both", expand=True)

            text_widget = tk.Text(
                text_frame,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                font=('Consolas', 10),
                wrap=tk.WORD
            )
            text_widget.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.configure(yscrollcommand=scrollbar.set)

            # Insert report content
            text_widget.insert("1.0", report_text)
            text_widget.configure(state="disabled")

            # Button frame for Export and Close buttons
            button_frame = tk.Frame(report_frame, bg=self.primary_bg_color)
            button_frame.pack(fill="x", pady=(10, 0))

            # Export button
            tk.Button(
                button_frame,
                text="Export Report",
                command=lambda: export_report(),
                bg=self.button_bg_color,
                fg=self.text_color,
                width=15
            ).pack(side="left", padx=5)

            # Close button
            tk.Button(
                button_frame,
                text="Close",
                command=report_window.destroy,
                bg=self.button_bg_color,
                fg=self.text_color,
                width=15
            ).pack(side="right", padx=5)

            def export_report():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile=f"diagnostic_report_{pc_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(report_text)
                    messagebox.showinfo("Success", "Report exported successfully!")

            # Handle window close button (X)
            report_window.protocol("WM_DELETE_WINDOW", report_window.destroy)

        # Add progress bar and label
        progress_var = tk.DoubleVar()
        progress_label = tk.Label(
            diagnostics_frame,
            text="Ready to run diagnostics",
            bg=self.primary_bg_color,
            fg=self.text_color
        )
        progress_label.pack(pady=(5, 0))

        ttk.Progressbar(
            diagnostics_frame,
            variable=progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        ).pack(pady=5)

        # Add Run Diagnostics button
        tk.Button(
            diagnostics_frame,
            text="Run Full Diagnostics",
            command=run_diagnostics,
            bg=self.button_bg_color,
            fg=self.text_color,
            width=20
        ).pack(pady=5)

        def show_knowledge_base():
            """Show Knowledge Base in a separate window"""
            # Common issues and solutions
            common_issues = {
                "Cannot Connect to RDP": [
                    "1. Verify machine is powered on",
                    "2. Check if RDP service is running",
                    "3. Ensure firewall allows RDP (Port 3389)",
                    "4. Try clearing DNS cache",
                    "5. Check network connectivity"
                ],
                "DNS Resolution Failed": [
                    "1. Verify hostname is correct",
                    "2. Clear local DNS cache",
                    "3. Check DNS server settings",
                    "4. Try using IP address directly",
                    "5. Update DNS records if needed"
                ],
                "High Network Latency": [
                    "1. Check network load",
                    "2. Verify network path",
                    "3. Test connection stability",
                    "4. Check for network congestion",
                    "5. Monitor bandwidth usage"
                ],
                "Machine Not Responding": [
                    "1. Verify power status",
                    "2. Check network connectivity",
                    "3. Try ping test",
                    "4. Check for system updates",
                    "5. Verify resource usage"
                ]
            }

            # Define apply_quick_fix function
            def apply_quick_fix():
                """Apply quick fix based on selected issue"""
                selected_issue = issue_var.get()
                if selected_issue == "DNS Resolution Failed":
                    self.run_elevated_command("powershell", "Clear-DnsClientCache")
                elif selected_issue == "Cannot Connect to RDP":
                    check_rdp_port()
                elif selected_issue == "High Network Latency":
                    test_network_path()
                elif selected_issue == "Machine Not Responding":
                    update_status()

            kb_window = tk.Toplevel(troubleshoot_dialog)
            kb_window.title("Knowledge Base")
            kb_window.geometry("700x600")
            kb_window.configure(bg=self.primary_bg_color)
            kb_window.transient(troubleshoot_dialog)
            kb_window.grab_set()

            # Center the window
            x = troubleshoot_dialog.winfo_x() + 50
            y = troubleshoot_dialog.winfo_y() + 50
            kb_window.geometry(f"700x600+{x}+{y}")

            # Create main frame
            kb_frame = tk.Frame(kb_window, bg=self.primary_bg_color)
            kb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Add issue selector label with larger font
            tk.Label(
                kb_frame,
                text="Select Issue:",
                bg=self.primary_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 12, 'bold')
            ).pack(anchor="w")

            # Larger combobox
            issue_var = tk.StringVar()
            issue_selector = ttk.Combobox(
                kb_frame,
                textvariable=issue_var,
                values=list(common_issues.keys()),
                state="readonly",
                width=40,
                font=('Segoe UI', 11)
            )
            issue_selector.pack(pady=(5, 15))

            # Larger solution display
            solution_text = tk.Text(
                kb_frame,
                height=8,
                bg=self.secondary_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 11),
                wrap=tk.WORD
            )
            solution_text.pack(fill="x", pady=(0, 15))

            # Add back the show_solution function
            def show_solution(*args):
                """Display solution for selected issue"""
                selected_issue = issue_var.get()
                if selected_issue:
                    solution_text.configure(state="normal")
                    solution_text.delete("1.0", tk.END)
                    solution_text.insert("1.0", "\n".join(common_issues[selected_issue]))
                    solution_text.configure(state="disabled")

            # Bind selection change to show solution
            issue_selector.bind("<<ComboboxSelected>>", show_solution)

            # Add back the Quick Actions section
            tk.Label(
                kb_frame,
                text="Quick Actions:",
                bg=self.primary_bg_color,
                fg=self.text_color,
                font=('Segoe UI', 12, 'bold')
            ).pack(anchor="w", pady=(0, 10))

            # Action buttons frame
            button_frame = tk.Frame(kb_frame, bg=self.primary_bg_color)
            button_frame.pack(fill="x")

            tk.Button(
                button_frame,
                text="Apply Quick Fix",
                command=apply_quick_fix,
                bg=self.button_bg_color,
                fg=self.text_color,
                width=20,
                font=('Segoe UI', 10)
            ).pack(side="left", padx=5)

            tk.Button(
                button_frame,
                text="Run Diagnostics",
                command=run_diagnostics,
                bg=self.button_bg_color,
                fg=self.text_color,
                width=20,
                font=('Segoe UI', 10)
            ).pack(side="left", padx=5)

            # Keep the show_solution function and binding
            def show_solution(*args):
                """Display solution for selected issue"""
                selected_issue = issue_var.get()
                if selected_issue:
                    solution_text.configure(state="normal")
                    solution_text.delete("1.0", tk.END)
                    solution_text.insert("1.0", "\n".join(common_issues[selected_issue]))
                    solution_text.configure(state="disabled")

            # Bind selection change to show solution
            issue_selector.bind("<<ComboboxSelected>>", show_solution)

        # Rest of the code...

        

        def show_event_logs():
            """Show relevant Event Viewer logs"""
            try:
                # Get RDP and System logs for the machine
                result = subprocess.run(
                    ["powershell", "-Command",
                     f"Get-WinEvent -ComputerName {pc_name} " +
                     "-LogName 'Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational'," +
                     "'System' -MaxEvents 50 | Where-Object {$_.Message -like '*remote*' -or " +
                     "$_.Message -like '*RDP*' -or $_.Message -like '*network*'} | " +
                     "Select-Object TimeCreated, LevelDisplayName, Message | Format-List"],
                    capture_output=True,
                    text=True
                )

                # Create log window
                log_window = tk.Toplevel(troubleshoot_dialog)
                log_window.title(f"Event Logs - {pc_name}")
                log_window.geometry("800x600")
                log_window.configure(bg=self.primary_bg_color)
                log_window.transient(troubleshoot_dialog)
                log_window.grab_set()

                # Center the window
                x = troubleshoot_dialog.winfo_x() + 50
                y = troubleshoot_dialog.winfo_y() + 50
                log_window.geometry(f"800x600+{x}+{y}")

                # Create main frame
                log_frame = tk.Frame(log_window, bg=self.primary_bg_color)
                log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                # Add text widget with scrollbar
                text_frame = tk.Frame(log_frame, bg=self.primary_bg_color)
                text_frame.pack(fill=tk.BOTH, expand=True)

                text_widget = tk.Text(
                    text_frame,
                    bg=self.secondary_bg_color,
                    fg=self.text_color,
                    font=('Consolas', 10),
                    wrap=tk.WORD
                )
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                text_widget.configure(yscrollcommand=scrollbar.set)

                # Insert log content
                if result.returncode == 0 and result.stdout.strip():
                    text_widget.insert("1.0", result.stdout)
                else:
                    text_widget.insert("1.0", "No relevant logs found or unable to access Event Viewer.\n\n")
                    if result.stderr:
                        text_widget.insert(tk.END, f"Error: {result.stderr}")

                text_widget.configure(state="disabled")

                # Add close button
                tk.Button(
                    log_frame,
                    text="Close",
                    command=log_window.destroy,
                    bg=self.button_bg_color,
                    fg=self.text_color,
                    width=15
                ).pack(pady=(10, 0))

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to retrieve Event Viewer logs: {str(e)}\n\n"
                    "Make sure you have appropriate permissions and the remote machine is accessible."
                )

class ThemeSwitch(tk.Canvas):
    def __init__(self, parent, current_theme="dark", command=None):
        # Initialize with the correct theme's header color
        super().__init__(parent, width=60, height=30,
                        bg=THEMES[current_theme]["header_bg"],
                        highlightthickness=0)  # Fixed indentation here
        self.command = command
        
        # Initialize switch state based on provided theme
        self.switch_on = current_theme == "light"  # Will be False for dark theme
        
        # Define colors for active and inactive states
        self.active_bg_color = THEMES["light"]["button_bg"]
        self.inactive_bg_color = THEMES["dark"]["button_bg"]
        self.switch_color_on = "#FFD700"  # Yellow for light mode
        self.switch_color_off = "#1C3D5A"  # Dark blue for dark mode
        
        # Create switch background and toggle button
        self.switch_bg = self.create_rounded_rect(5, 5, 55, 25, 12, 
            fill=self.active_bg_color if self.switch_on else self.inactive_bg_color)
        
        # Position the toggle button based on current theme
        initial_x = 38 if self.switch_on else 8
        self.switch_button = self.create_oval(
            initial_x, 8, initial_x + 14, 22,
            fill=self.switch_color_on if self.switch_on else self.switch_color_off,
            width=0
        )
        
        # Add toggle text or icons
        self.light_icon = self.create_text(45, 15, text="☀️", font=("Arial", 10), fill="white")
        self.dark_icon = self.create_text(15, 15, text="", font=("Arial", 10), fill="white")
        
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        self.switch_on = not self.switch_on
        current_theme = "light" if self.switch_on else "dark"
        
        # Set background and switch button color based on the theme
        new_bg_color = self.active_bg_color if self.switch_on else self.inactive_bg_color
        new_button_color = self.switch_color_on if self.switch_on else self.switch_color_off
        
        # Update the header background color based on the current theme
        self.configure(bg=THEMES[current_theme]["header_bg"])
        
        # Animate the toggle switch
        self.animate_switch(new_bg_color, new_button_color)
        
        # Call command if provided
        if self.command:
            self.command()
    
    def animate_switch(self, new_bg_color, new_button_color):
        target_x = 38 if self.switch_on else 8
        current_x = self.coords(self.switch_button)[0]
        step = 2 if target_x > current_x else -2
        
        # Animate the movement of the toggle button
        while (step > 0 and current_x < target_x) or (step < 0 and current_x > target_x):
            self.coords(self.switch_button, current_x, 8, current_x + 14, 22)
            self.itemconfig(self.switch_button, fill=new_button_color)
            self.itemconfig(self.switch_bg, fill=new_bg_color)
            self.update()
            current_x += step
            time.sleep(0.01)  # Adjust animation speed

        # Ensure final position
        self.coords(self.switch_button, target_x, 8, target_x + 14, 22)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

def main():
    app = VMManagerUI()  # Create UI first, it will create VMManager with proper reference
    app.root.mainloop()

if __name__ == "__main__":
    main()