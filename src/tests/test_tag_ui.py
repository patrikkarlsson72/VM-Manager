import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tag_manager import TagManager
from tag_sidebar import TagSidebar

class TestApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tag System Test")
        self.geometry("800x600")
        
        # Create a mock file manager (we'll implement this properly later)
        self.mock_file_manager = type('MockFileManager', (), {
            'load_tags': lambda self: [],
            'save_tags': lambda self, tags: None,
            'load_machine_tags': lambda self: {},
            'save_machine_tags': lambda self, machine_tags: None
        })()
        
        # Initialize tag manager
        self.tag_manager = TagManager(self.mock_file_manager)
        
        # Create main layout
        self.create_layout()
        
        # Add some test machines
        self.test_machines = ["TestVM1", "TestVM2", "TestVM3"]
        self.update_machine_list()

        # Add test tags
        test_tags = ["Development", "Production", "Testing"]
        for tag in test_tags:
            self.tag_manager.add_tag(tag)
            self.tag_sidebar.refresh_tags()  # Refresh the display after each tag

    def create_layout(self):
        # Create split view
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # Add tag sidebar with dark theme background color
        self.tag_sidebar = TagSidebar(self.paned, self.tag_manager)
        if hasattr(self.tag_sidebar, 'theme') and self.tag_sidebar.theme == 'dark':
            self.tag_sidebar.tag_canvas.configure(bg='#274156')
        self.paned.add(self.tag_sidebar, weight=1)
        
        # Add machine list (right side)
        self.machine_frame = ttk.Frame(self.paned)
        self.paned.add(self.machine_frame, weight=2)
        
        # Add machine listbox with right-click binding
        self.machine_list = tk.Listbox(self.machine_frame)
        self.machine_list.pack(fill=tk.BOTH, expand=True)
        self.machine_list.bind("<Button-3>", self.show_machine_menu)
        
        # Bind tag events
        self.tag_sidebar.bind("<<TagSelected>>", self.handle_tag_selection)
        self.tag_sidebar.bind("<<TagAdded>>", self.handle_tag_added)
        self.tag_sidebar.bind("<<TagRemoved>>", self.handle_tag_removed)

        # Add theme toggle to header (for testing only)
        self.theme_button = ttk.Button(
            self,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="top", pady=5)

    def update_machine_list(self, filtered_machines=None):
        self.machine_list.delete(0, tk.END)
        machines = filtered_machines if filtered_machines is not None else self.test_machines
        
        for machine in machines:
            # Get machine's tags
            tags = self.tag_manager.get_machine_tags(machine)
            # Create display string with tags
            display = f"{machine} [{', '.join(tags)}]" if tags else machine
            self.machine_list.insert(tk.END, display)

    def handle_tag_selection(self, event):
        selected_tags = self.tag_sidebar.get_selected_tags()
        if selected_tags:
            filtered_machines = self.tag_manager.get_machines_by_tags(selected_tags)
            self.update_machine_list(filtered_machines)
        else:
            self.update_machine_list()

    def handle_tag_added(self, event):
        print(f"Tag added: {self.tag_sidebar.last_added_tag}")

    def handle_tag_removed(self, event):
        print(f"Tag removed: {self.tag_sidebar.last_removed_tag}")
        self.update_machine_list()

    def create_machine_context_menu(self, machine_name):
        menu = tk.Menu(self, tearoff=0)
        
        # Create Tags submenu
        tags_menu = tk.Menu(menu, tearoff=0)
        
        # Get machine's current tags
        machine_tags = self.tag_manager.get_machine_tags(machine_name)
        
        # Add "Assign Tag" submenu
        assign_menu = tk.Menu(tags_menu, tearoff=0)
        for tag in sorted(self.tag_manager.get_all_tags()):
            if tag not in machine_tags:
                assign_menu.add_command(
                    label=tag,
                    command=lambda t=tag: self.toggle_machine_tag(machine_name, t)
                )
        
        # Add "Remove Tag" submenu
        remove_menu = tk.Menu(tags_menu, tearoff=0)
        for tag in sorted(machine_tags):
            remove_menu.add_command(
                label=tag,
                command=lambda t=tag: self.toggle_machine_tag(machine_name, t)
            )
        
        # Add submenus to Tags menu
        if len(self.tag_manager.get_all_tags()) > len(machine_tags):
            tags_menu.add_cascade(label="✚ Assign Tag", menu=assign_menu)
        if machine_tags:
            tags_menu.add_cascade(label="✖ Remove Tag", menu=remove_menu)
        
        # If no tags available, show appropriate message
        if not self.tag_manager.get_all_tags():
            tags_menu.add_command(label="No tags available", state="disabled")
        elif not assign_menu.index("end") and not remove_menu.index("end"):
            tags_menu.add_command(label="No actions available", state="disabled")
        
        menu.add_cascade(label="Tags", menu=tags_menu)
        return menu

    def toggle_machine_tag(self, machine_name, tag_name):
        """Toggle tag assignment for a machine"""
        if tag_name in self.tag_manager.get_machine_tags(machine_name):
            self.tag_manager.remove_machine_tag(machine_name, tag_name)
        else:
            self.tag_manager.add_machine_tag(machine_name, tag_name)
        self.update_machine_list()  # Refresh display

    def show_machine_menu(self, event):
        # Get clicked item
        index = self.machine_list.nearest(event.y)
        if index >= 0:
            # Get full text and extract just the machine name
            full_text = self.machine_list.get(index)
            machine_name = full_text.split(" [")[0]  # Get text before any tags
            menu = self.create_machine_context_menu(machine_name)
            menu.post(event.x_root, event.y_root)

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = "light" if self.tag_sidebar.theme == "dark" else "dark"
        # Update tag sidebar theme
        self.tag_sidebar.update_theme(new_theme)

def main():
    app = TestApplication()
    app.mainloop()

if __name__ == "__main__":
    main() 