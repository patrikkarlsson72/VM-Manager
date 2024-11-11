import tkinter as tk
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
        """Load categories from file"""
        if os.path.exists(self.categories_file_path):
            with open(self.categories_file_path, "r") as file:
                return file.read().splitlines()
        return ["Default"]  # Always have a default category

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

    def set_machine_rdp_path(self, pc_name):
        """Set custom RDP path for specific machine"""
        rdp_path = filedialog.askopenfilename(
            title=f"Select RDP File for {pc_name}",
            filetypes=(("RDP Files", "*.rdp"), ("All Files", "*.*"))
        )
        
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

    def delete_category(self, category_name):
        """Delete a category and reassign its machines to Default"""
        if category_name == "Default":
            return False
        
        if category_name in self.categories:
            self.categories.remove(category_name)
            
            # Reassign machines to Default category
            for machine, category in self.machine_categories.items():
                if category == category_name:
                    self.machine_categories[machine] = "Default"
            
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

class VMManagerUI:
    """Main application UI"""
    def __init__(self, vm_manager):
        self.vm_manager = vm_manager
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("1000x600")
        
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
        self.current_filter = None  # Add this to track current category filter

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
            else:
                messagebox.showwarning("Note", "No new PCs were added. They might already exist.")

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
            btn = tk.Button(
                self.category_buttons_container,
                text=category,
                command=lambda c=category: self.filter_by_category(c),
                bg=self.secondary_bg_color,  # Set initial background
                fg=self.text_color,
                font=('Helvetica', 11),
                bd=0,
                anchor="w",
                padx=10,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=2)

            # Force initial state
            btn.update_idletasks()

            # Bind hover effects
            btn.bind('<Enter>', lambda e, b=btn: self.on_category_button_hover(b))
            btn.bind('<Leave>', lambda e, b=btn: self.on_category_button_leave(b))
            
            # Force correct initial state
            self.on_category_button_leave(btn)

    def on_category_button_hover(self, button):
        """Handle category button hover"""
        button.configure(bg=self.hover_active_color)

    def on_category_button_leave(self, button):
        """Handle category button mouse leave"""
        button.configure(bg=self.secondary_bg_color)

    def filter_by_category(self, category_name):
        """Filter machines by category"""
        self.current_filter = category_name
        filtered_pcs = self.vm_manager.get_machines_by_category(category_name)
        self.position_buttons(filtered_pcs)

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
            tags=(button_tag, "button")
        )

        # Calculate text positions
        text_y = y + (height * 0.25)
        last_used_y = y + (height * 0.6)
        description_y = y + (height * 0.8)
        center_x = x + (width / 2)

        # Create text elements with the same button tag
        title_text = self.canvas.create_text(
            center_x, text_y,
            text=text,
            fill=self.text_color,
            font=('Helvetica', title_font_size, 'bold'),
            anchor="center",
            tags=(button_tag, "button")
        )

        last_used_text = self.canvas.create_text(
            center_x, last_used_y,
            text=f"Last Used: {last_used}",
            fill=self.text_color,
            font=('Helvetica', info_font_size),
            anchor="center",
            tags=(button_tag, "button")
        )

        description_text = None
        if description:
            description_text = self.canvas.create_text(
                center_x, description_y,
                text=description,
                fill=self.text_color,
                font=('Helvetica', status_font_size),
                anchor="center",
                tags=(button_tag, "button")
            )

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
        
        # Update UI with current filter
        if self.current_filter:
            filtered_pcs = self.vm_manager.get_machines_by_category(self.current_filter)
            self.position_buttons(filtered_pcs)
        else:
            self.position_buttons()
            
        # Schedule next update
        self.root.after(5000, self.update_machine_status)

    def _check_single_machine_status(self, pc_name):
        """Check status of a single machine"""
        is_running = self.vm_manager.check_machine_status(pc_name)
        self.vm_manager.machine_status[pc_name] = is_running

    def toggle_theme(self):
        current_theme = "light" if self.primary_bg_color == THEMES["dark"]["primary_bg"] else "dark"
        theme = THEMES[current_theme]
        
        # Update colors
        self.primary_bg_color = theme["primary_bg"]
        self.secondary_bg_color = theme["secondary_bg"]
        self.button_bg_color = theme["button_bg"]
        self.header_bg_color = theme["header_bg"]
        self.text_color = theme["text"]
        self.hover_active_color = theme["hover_active"]
        self.borders_and_dividers_color = theme["borders"]
        
        # Update UI elements
        self.root.configure(bg=self.primary_bg_color)
        self.update_theme_colors()
        self.position_buttons()

    def update_theme_colors(self):
        """Update all UI elements with current theme colors"""
        # Update header
        self.header_frame.configure(bg=self.header_bg_color)
        self.header_container.configure(bg=self.header_bg_color)
        self.title_label.configure(bg=self.header_bg_color, fg=self.text_color)
        self.theme_switch.configure(bg=self.header_bg_color)
        self.underline_frame.configure(bg=self.borders_and_dividers_color)
        
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
            self.border_frame.configure(bg=self.borders_and_dividers_color)  # This will use #B4D8F0 in light theme

    def update_rdp_path(self):
        result = messagebox.askyesno(
            "Update RDP Path",
            "Do you want to change the default RDP file path?",
            icon='question'
        )
        
        if result:
            rdp_path = filedialog.askopenfilename(
                title="Select RDP File",
                filetypes=(("RDP Files", "*.rdp"), ("All Files", "*.*"))
            )
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
        context_menu = tk.Menu(self.root, tearoff=0)
        
        # Add category submenu
        category_menu = tk.Menu(context_menu, tearoff=0)
        
        # Add option to remove category
        current_category = self.vm_manager.get_machine_category(pc_name)
        if current_category and current_category != "Default":
            context_menu.add_command(
                label=f"Remove from '{current_category}'",
                command=lambda: self.remove_machine_category(pc_name)
            )
        
        # Add categories submenu
        for category in self.vm_manager.categories:
            if category != "Default":  # Skip Default as it's not an assignable category
                category_menu.add_command(
                    label=category,
                    command=lambda c=category: self.set_machine_category(pc_name, c)
                )
        
        context_menu.add_cascade(label="Set Category", menu=category_menu)
        
        # Add other menu items
        context_menu.add_separator()
        context_menu.add_command(label="Set RDP Path", command=lambda: self.set_rdp_path(pc_name))
        context_menu.add_command(label="Edit Description", command=lambda: self.edit_description(pc_name))
        context_menu.add_command(label="Delete", command=lambda: self.delete_pc(pc_name))
        
        context_menu.tk_popup(event.x_root, event.y_root)

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
        current_description = self.vm_manager.get_description(pc_name)
        new_description = simpledialog.askstring("Edit Description", "Enter new description:", initialvalue=current_description)
        if new_description:
            self.vm_manager.descriptions[pc_name] = new_description
            self.file_manager.save_descriptions(self.vm_manager.descriptions)
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
                        ])
                
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

    def position_buttons(self, pc_list=None):
        """Position buttons on canvas, optionally using a filtered list of PCs"""
        self.canvas.delete("all")

        # Use filtered list if provided, otherwise use all PCs
        pcs_to_display = pc_list if pc_list is not None else self.vm_manager.pc_names

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

        for idx, pc_name in enumerate(pcs_to_display):
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
        total_height = MARGIN_TOP + ((len(pcs_to_display) - 1) // BUTTONS_PER_ROW + 1) * (button_height + BUTTON_SPACING)
        self.canvas.config(scrollregion=(0, 0, canvas_width, total_height))

class ThemeSwitch(tk.Canvas):
    def __init__(self, parent, current_theme="dark", command=None):
        super().__init__(parent, width=60, height=30, bg=THEMES["dark"]["header_bg"], highlightthickness=0)
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
        self.dark_icon = self.create_text(15, 15, text="🌙", font=("Arial", 10), fill="white")
        
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        self.switch_on = not self.switch_on
        current_theme = "light" if self.switch_on else "dark"
        
        # Set background and switch button color based on the theme
        new_bg_color = self.active_bg_color if self.switch_on else self.inactive_bg_color
        new_button_color = self.switch_color_on if self.switch_on else self.switch_color_off
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