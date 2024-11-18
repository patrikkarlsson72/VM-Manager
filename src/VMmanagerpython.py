import tkinter as tk
from tkinter import font as tkfont  # Add this import
from tkinter import simpledialog, messagebox, filedialog, ttk, colorchooser
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
    """Handles all file operations and paths"""
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

    def _get_data_directory(self):
        default_data_dir = os.path.join(os.getenv("LOCALAPPDATA"), "VmManager")
        settings_file_path = os.path.join(default_data_dir, "settings.txt")
        
        # Ensure the default directory exists
        os.makedirs(default_data_dir, exist_ok=True)

        # Use default if no settings file
        if not os.path.exists(settings_file_path):
            # Write default data directory path to settings.txt
            with open(settings_file_path, "w") as f:
                f.write(f"data_dir={default_data_dir}\n")
            return default_data_dir
        else:
            # Read data directory path from settings.txt
            with open(settings_file_path, "r") as f:
                data_dir = f.readline().split("=")[1].strip()
            
            # If path in settings.txt is invalid, default to LOCALAPPDATA
            if not os.path.exists(data_dir):
                data_dir = default_data_dir
                with open(settings_file_path, "w") as f:
                    f.write(f"data_dir={default_data_dir}\n")
            
            return data_dir

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
        """Load categories from file and remove duplicates"""
        categories = ["Default"]  # Always start with Default
        if os.path.exists(self.categories_file_path):
            with open(self.categories_file_path, "r") as file:
                # Add non-duplicate categories that aren't "Default"
                for category in file.read().splitlines():
                    if category not in categories and category != "Default":
                        categories.append(category)
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

    # ... other file operations ...

class SettingsManager:
    """Manages application settings"""
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
    """Main application logic"""
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

    def connect_to_pc(self, pc_name):
        """Connect to a PC and track the connection"""
        rdp_file = self.machine_rdp_paths.get(pc_name, self.settings_manager.settings["rdp_path"])
        try:
            subprocess.Popen(["mstsc", rdp_file, "/v:" + pc_name])
            self.connected_machines.add(pc_name)  # Add to connected machines
            self.last_used_times[pc_name] = datetime.now().strftime("%d/%m %H:%M")
            self.file_manager.save_last_used_times(self.last_used_times)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to {pc_name}: {str(e)}")
            return False

    def check_machine_status(self, pc_name, port=3389, timeout=3):
        """Check if machine is running by testing RDP port"""
        try:
            with socket.create_connection((pc_name, port), timeout=timeout):
                return True
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
        """Delete a PC from the list"""
        if pc_name in self.pc_names:
            self.pc_names.remove(pc_name)
            self.machine_status.pop(pc_name, None)
            self.last_used_times.pop(pc_name, None)
            self.descriptions.pop(pc_name, None)
            self.machine_rdp_paths.pop(pc_name, None)
            
            # Save all changes
            self.file_manager.save_pcs(self.pc_names)
            self.file_manager.save_last_used_times(self.last_used_times)
            self.file_manager.save_descriptions(self.descriptions)
            self.file_manager.save_machine_rdp_paths(self.machine_rdp_paths)
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

    def add_category(self, category_name):
        """Add a new category"""
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            self.file_manager.save_categories(self.categories)
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

class VMManagerUI:
    """Main application UI"""
    def __init__(self, vm_manager):
        self.vm_manager = vm_manager
        self.root = tk.Tk()
        self.root.title("VM Manager")
        
        # Initialize active_tag_filters as a set
        self.active_tag_filters = set()
        
        # Set window size
        window_width = 1000
        window_height = 700
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position coordinates
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Initialize theme-related attributes
        self.current_theme = "dark"  # default theme
        self.current_filter = None
        self.current_tag_filter = None
        
        # Get theme colors
        theme = THEMES[self.current_theme]
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.border_color = theme["borders"]
        
        # Rest of your initialization code...
        
        # Set the root reference in VMManager
        self.vm_manager.root = self.root  # Add this line
        
        self.root.geometry("1000x700")
        
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

        self.setup_ui()
        self.running_indicators = {}
        self.connection_indicators = {}
        self.drag_data = {"x": 0, "y": 0, "item": None, "original_pos": None}
        self.dragging = False  # Add this flag to track drag state

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
            font=("Montserrat", 22, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=20)

        # Theme switch
        self.theme_switch = ThemeSwitch(self.header_container, command=self.toggle_theme)
        self.theme_switch.pack(side=tk.RIGHT, padx=20)

        # Underline
        self.underline_frame = tk.Frame(self.header_frame, height=2, bg=self.borders_and_dividers_color)
        self.underline_frame.pack(fill=tk.X)

    def create_sidebar(self):
        self.left_frame = tk.Frame(self.root, width=200, bg=self.secondary_bg_color)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.border_frame = tk.Frame(self.root, width=2, bg=self.borders_and_dividers_color)
        self.border_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Settings button
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

        # Add PC Buttons Frame
        add_pc_frame = tk.Frame(
            self.left_frame, 
            bg=self.secondary_bg_color,  # Use theme color
            highlightthickness=0  # Remove border
        )
        add_pc_frame.pack(fill="x", padx=10, pady=10)

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
        self.single_pc_input_frame = tk.Frame(  # Make it an instance variable
            self.left_frame,
            bg=self.secondary_bg_color  # This controls the background
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
        self.add_pc_btn = tk.Button(  # Make it an instance variable so we can update it
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

        # Add Tag Section after Categories
        self.create_tag_section()

    def create_tag_section(self):
        """Create the tag filter section in sidebar"""
        # Tag Frame
        tag_frame = tk.Frame(
            self.left_frame,
            bg=self.secondary_bg_color
        )
        tag_frame.pack(pady=10, padx=10, fill="x")

        # Header Frame with blue background
        header_frame = tk.Frame(
            tag_frame,
            bg='#1a73e8'  # Blue color similar to Manage Tags button
        )
        header_frame.pack(fill="x", pady=(0, 5))

        # Header Label
        self.tags_label = tk.Label(
            header_frame,
            text="Filter by Tag",
            bg='#1a73e8',  # Match frame background
            fg='white',    # White text for better contrast
            font=('Helvetica', 14, 'bold'))
        self.tags_label.pack(anchor="w", pady=5, padx=5)

        # Container for tag filters 
        self.tag_filters_container = tk.Frame(
            tag_frame,
            bg=self.secondary_bg_color
        )
        self.tag_filters_container.pack(fill="x", pady=5)

        # Update tag filters
        self.update_tag_filters()

        # Button container for Manage Tags and Reset Filter - moved to bottom
        button_container = tk.Frame(
            tag_frame,
            bg=self.secondary_bg_color
            
        )
        button_container.pack(fill="x", pady=(10, 0))

        # Manage Tags Button
        manage_tags_btn = tk.Button(
            button_container,
            text="Manage Tags",
            command=lambda: self.show_tag_manager(),
            bg='#1a73e8',  # Blue color similar to your website
            fg='white',
            font=('Helvetica', 11),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        manage_tags_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

        # Reset Filter Button
        reset_filter_btn = tk.Button(
            button_container,
            text="Reset Filter",
            command=self.reset_tag_filter,
            bg='#dc3545',  # Red color for reset
            fg='white',
            font=('Helvetica', 11),
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        reset_filter_btn.pack(side="right", fill="x", expand=True, padx=(2, 0))

    def update_tag_filters(self):
        """Update the tag filter buttons display"""
        # Clear existing tag filters
        for widget in self.tag_filters_container.winfo_children():
            widget.destroy()

        # Create a frame that will allow tags to wrap
        wrap_frame = tk.Frame(
            self.tag_filters_container,
            #bg=self.primary_bg_color
        )
        wrap_frame.pack(fill="x", expand=True)
        wrap_frame.grid_columnconfigure(0, weight=1)

        row = 0
        col = 0
        max_cols = 3  # Number of tags per row

        # Fixed colors for tags - matching your website design
        tag_bg_color = "#ffffff"  # White background for inactive tags
        tag_border_color = "#dee2e6"  # Light gray border
        tag_active_color = "#0d6efd"  # Bootstrap blue for active state
        tag_text_color = "#000000"  # Black text for inactive
        tag_active_text_color = "#ffffff"  # White text for active state

        # Create a button for each tag
        for tag in self.vm_manager.tags:
            tag_btn = tk.Button(
                wrap_frame,
                text=f"🏷️ {tag}",
                command=lambda t=tag: self.filter_by_tag(t),
                bg=tag_bg_color if tag not in self.active_tag_filters else tag_active_color,
                fg=tag_text_color if tag not in self.active_tag_filters else tag_active_text_color,
                font=('Helvetica', 9),
                bd=1,
                relief="solid",
                padx=5,
                pady=2,
                cursor="hand2"
            )
            tag_btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

            # Bind hover effects
            tag_btn.bind('<Enter>', 
                lambda e, btn=tag_btn: btn.configure(bg=tag_active_color, fg=tag_active_text_color))
            tag_btn.bind('<Leave>', 
                lambda e, btn=tag_btn, t=tag: btn.configure(
                    bg=tag_active_color if t in self.active_tag_filters else tag_bg_color,
                    fg=tag_active_text_color if t in self.active_tag_filters else tag_text_color))

            # Update row and column
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

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

    def create_category_section(self):
        """Create the category management section in sidebar"""
        # Category Frame
        category_frame = tk.Frame(
            self.left_frame,
            bg=self.secondary_bg_color
        )
        category_frame.pack(pady=10, padx=10, fill="x")

        # Categories Label
        self.categories_label = tk.Label(  # Make it an instance variable to update later
            category_frame,
            text="Categories",
            bg=self.secondary_bg_color,
            fg=self.text_color,  # Use theme text color
            font=('Helvetica', 14, 'bold')
        )
        self.categories_label.pack(anchor="w", pady=(0, 5))

        # Container for category buttons
        self.category_buttons_container = tk.Frame(
            category_frame,
            bg=self.secondary_bg_color
        )
        self.category_buttons_container.pack(fill="x", padx=5, pady=5)

        # Add Category Button
        self.add_category_btn = tk.Button(
            category_frame,
            text="Add Category+",
            command=self.add_category_dialog,
            bg=self.button_bg_color,
            fg=self.text_color,
            font=('Helvetica', 10),
            relief="solid",
            bd=1,
            cursor="hand2"
        )
        self.add_category_btn.pack(pady=(5, 10), padx=10, fill="x")

        # Create initial category buttons
        self.update_category_buttons()

    def update_category_buttons(self):
        """Update the category buttons display"""
        # Clear existing buttons
        for widget in self.category_buttons_container.winfo_children():
            widget.destroy()

        # Create button for each category
        for category in self.vm_manager.categories:
            # Set initial background color based on whether this is the current filter
            initial_bg = self.hover_active_color if (hasattr(self, 'current_filter') and self.current_filter == category) else self.secondary_bg_color
            
            btn = tk.Button(
                self.category_buttons_container,
                text=category,
                command=lambda c=category: self.filter_by_category(c),
                bg=initial_bg,
                fg=self.text_color,
                font=('Helvetica', 11),
                bd=0,
                anchor="w",
                padx=10,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=2)

            # Store category name as an attribute
            btn.category = category

            # Bind hover effects
            btn.bind('<Enter>', lambda e, b=btn: self.on_category_button_hover(b))
            btn.bind('<Leave>', lambda e, b=btn: self.on_category_button_leave(b))
            
            # Add right-click menu for non-Default categories
            if category != "Default":
                btn.bind('<Button-3>', lambda e, c=category: self.show_category_context_menu(e, c))

    def on_category_button_hover(self, button):
        """Handle category button hover"""
        if not hasattr(self, 'current_filter') or button.category != self.current_filter:
            button.configure(bg=self.hover_active_color)

    def on_category_button_leave(self, button):
        """Handle category button mouse leave"""
        if not hasattr(self, 'current_filter') or button.category != self.current_filter:
            button.configure(bg=self.secondary_bg_color)
        else:
            button.configure(bg=self.hover_active_color)

    def filter_by_category(self, category_name):
        """Filter machines by category"""
        self.current_filter = category_name
        filtered_pcs = self.vm_manager.get_machines_by_category(category_name)
        self.position_buttons(filtered_pcs)
        
        # Update all category button colors
        for btn in self.category_buttons_container.winfo_children():
            if hasattr(btn, 'category'):
                if btn.category == category_name:
                    btn.configure(bg=self.hover_active_color)
                else:
                    btn.configure(bg=self.secondary_bg_color)

    def add_category_dialog(self):
        """Show dialog to add a new category"""
        category_name = simpledialog.askstring("Add Category", "Enter category name:")
        if category_name:
            if self.vm_manager.add_category(category_name):
                self.update_category_buttons()  # Update the category buttons instead of listbox

    def create_main_area(self):
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
        """Create a rounded button with responsive text sizes"""
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
            tags=(button_tag, "button", "button_bg")  # Add background-specific tag
        )
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

        # Calculate vertical positions
        center_x = x + (width / 2)
        title_y = y + (height * 0.25)  # Title at 25% from top
        last_used_y = y + (height * 0.45)  # Last used at 45% from top
        description_y = y + (height * 0.65)  # Description at 65% from top
        
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
            
            self.canvas.create_text(
                center_x, y + (height * 0.85),
                text=tags_text,
                fill=self.text_color,
                font=('Helvetica', status_font_size),
                anchor="center",
                width=max_tag_width,  # Set maximum width
                tags=(button_tag, "button"))

        # Bind events to the button background
        self.canvas.tag_bind(button_tag, '<Button-1>', lambda e, name=text: self.handle_button_press(e, name))
        self.canvas.tag_bind(button_tag, '<B1-Motion>', self.drag)
        self.canvas.tag_bind(button_tag, '<ButtonRelease-1>', lambda e, name=text: self.handle_button_release(e, name, command))
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
        if self.active_tag_filters:
            # If tag filters are active, show only machines with those tags
            filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
            self.position_buttons(filtered_pcs)
        elif hasattr(self, 'current_filter') and self.current_filter:
            # If category filter is active, maintain it
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

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        theme = THEMES[self.current_theme]
        
        # Update all theme colors
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.border_color = theme["borders"]
        self.header_bg_color = theme["header_bg"]  # Make sure to update header bg color
        
        # Update all UI elements with new colors
        self.update_theme_colors()

    def update_theme_colors(self):
        """Update all UI elements with current theme colors"""
        # Update header
        self.header_frame.configure(bg=self.header_bg_color)
        self.header_container.configure(bg=self.header_bg_color)
        self.title_label.configure(bg=self.header_bg_color, fg=self.text_color)
        
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
            self.tag_header_frame.configure(bg=self.header_bg_color)
            self.tags_label.configure(
                bg=self.header_bg_color,
                fg=self.text_color
            )

        # Update tag buttons
        if hasattr(self, 'tag_filters_container'):
            self.tag_filters_container.configure(bg=self.secondary_bg_color)
            for btn in self.tag_filters_container.winfo_children():
                if isinstance(btn, tk.Button):
                    if hasattr(self, 'current_tag_filter') and hasattr(btn, 'tag') and btn.tag == self.current_tag_filter:
                        btn.configure(
                            bg=self.hover_active_color,
                            fg=self.text_color
                        )
                    else:
                        btn.configure(
                            bg=self.secondary_bg_color,
                            fg=self.text_color
                        )

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
        """Show context menu for PC button"""
        menu_style = MenuStyle.get_themed_menu_style(self.current_theme)
        
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.configure(**menu_style)
        
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
                    background=menu_style['bg']
                )
        
        context_menu.add_cascade(
            label="  📂  Set Category",
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
            if self.current_filter:
                filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
                self.position_buttons(filtered_pcs)
            else:
                self.position_buttons()

    def update_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x600")
        settings_window.configure(bg=self.primary_bg_color)
        settings_window.transient(self.root)
        settings_window.grab_set()

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
        """Change the application's data directory and move existing files"""
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
                        shutil.move(old_path, new_path)
                
                # Update settings with new directory
                self.vm_manager.settings_manager.settings["data_dir"] = new_dir
                self.vm_manager.settings_manager.save_settings()
                
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
            command()  # Execute the command (connect to VM)
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
        
        # Redraw all buttons in their new positions
        self.position_buttons()

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
        """Position machine buttons in the grid"""
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
        
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(
            label=f"Delete '{category}'",
            command=lambda: self.delete_category(category)
        )
        context_menu.tk_popup(event.x_root, event.y_root)

    def delete_category(self, category):
        """Delete a category after confirmation"""
        if category == "Default":
            messagebox.showerror("Error", "Cannot delete the Default category")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete the category '{category}'?\n"
                              "All machines in this category will be unassigned."):
            if self.vm_manager.delete_category(category):
                self.update_category_buttons()
                # If current filter is the deleted category, switch to Default
                if self.current_filter == category:
                    self.filter_by_category("Default")

    def show_tag_manager(self):
        """Show dialog for managing tags"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Tags")
        
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
                
            # Add each tag with a delete button
            for tag in self.vm_manager.tags:
                tag_frame = tk.Frame(tag_list_frame, bg=self.primary_bg_color)
                tag_frame.pack(fill="x", pady=2)
                
                tk.Label(
                    tag_frame,
                    text=tag,
                    bg=self.primary_bg_color,
                    fg=self.text_color,
                    font=('Helvetica', 12)
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Button(
                    tag_frame,
                    text="×",
                    command=lambda t=tag: self.delete_tag(t, tag_frame),
                    bg='#dc3545',
                    fg='white',
                    font=('Helvetica', 10, 'bold'),
                    bd=0,
                    padx=5,
                    cursor="hand2"
                ).pack(side=tk.RIGHT)
        
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

    def reset_tag_filter(self):
        """Reset all tag filters"""
        self.active_tag_filters.clear()  # Clear all active filters
        self.position_buttons()  # Refresh the display
        self.update_tag_filters()  # Update tag button appearances

    def filter_by_tag(self, tag):
        """Filter machines by tag"""
        if tag in self.active_tag_filters:
            self.active_tag_filters.remove(tag)
        else:
            self.active_tag_filters.add(tag)
        
        # Update the display
        if self.active_tag_filters:
            filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
            self.position_buttons(filtered_pcs)
        else:
            self.position_buttons()
        
        # Update tag button appearances
        self.update_tag_filters()

    def delete_tag(self, tag, tag_frame=None):
        """Delete a tag and update UI"""
        if self.vm_manager.delete_tag(tag):
                # Remove tag from active filters if it's there
                if tag in self.active_tag_filters:
                    self.active_tag_filters.remove(tag)
                
                # Update main window tag display
                self.update_tag_filters()
                
                # Update machine display if needed
                if self.active_tag_filters:
                    filtered_pcs = self.vm_manager.get_machines_by_multiple_tags(self.active_tag_filters)
                    self.position_buttons(filtered_pcs)
                else:
                    self.position_buttons()
                
                # Instead of just removing the tag frame, refresh the entire tag list
        if tag_frame:
            # Get the parent frame (tag_list_frame) and update all tags
            tag_list_frame = tag_frame.master
            for widget in tag_list_frame.winfo_children():
                widget.destroy()

            # Recreate all tag entries
            for existing_tag in self.vm_manager.tags:
                new_tag_frame = tk.Frame(tag_list_frame, bg=self.primary_bg_color)
                new_tag_frame.pack(fill="x", pady=2)
                
                tk.Label(
                    new_tag_frame,
                    text=existing_tag,
                    bg=self.primary_bg_color,
                    fg=self.text_color,
                    font=('Helvetica', 12)
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Button(
                    new_tag_frame,
                    text="×",
                    command=lambda t=existing_tag: self.delete_tag(t, new_tag_frame),
                    bg='#dc3545',
                    fg='white',
                    font=('Helvetica', 10, 'bold'),
                    bd=0,
                    padx=5,
                    cursor="hand2"
                ).pack(side=tk.RIGHT)

    def toggle_machine_tag(self, machine_name, tag):
        """Toggle a tag on/off for a machine"""
        current_tags = self.vm_manager.get_machine_tags(machine_name)
        
        if tag in current_tags:
            # Remove tag
            if self.vm_manager.remove_machine_tag(machine_name, tag):
                self.position_buttons()  # Refresh display
        else:
            # Add tag
            if self.vm_manager.add_machine_tag(machine_name, tag):
                self.position_buttons()  # Refresh display

class ThemeSwitch(tk.Canvas):
    def __init__(self, parent, current_theme="dark", command=None):
        # Initialize with the correct theme's header color
        super().__init__(parent, width=60, height=30, 
                        bg=THEMES[current_theme]["header_bg"], 
                        highlightthickness=0)
        self.command = command
        
        # Initialize switch state based on provided theme
        self.switch_on = current_theme == "light"
        
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
    vm_manager = VMManager()
    app = VMManagerUI(vm_manager)
    app.root.mainloop()

if __name__ == "__main__":
    main()