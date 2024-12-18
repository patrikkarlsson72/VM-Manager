import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class TagSidebarPrototype(ttk.Frame):
    def __init__(self, parent, theme="light"):
        super().__init__(parent)
        self.theme = theme
        self.setup_styles()
        self.create_widgets()
        
        # Bind mouse wheel scrolling when mouse enters/leaves the widget
        self.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel))
        self.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        # Update scrollregion after initial display
        self.tags_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def setup_styles(self):
        # Update dark theme colors for better contrast
        self.colors = {
            "light": {
                "bg": "#f8f9fa",
                "tag_bg": "#e9ecef",
                "tag_bg_hover": "#dee2e6",
                "tag_bg_selected": "#228be6",
                "text": "#495057",
                "text_selected": "white",
                "border": "#dee2e6"
            },
            "dark": {
                "bg": "#1a1a1a",            # Darker background
                "tag_bg": "#2d2d2d",        # Darker tag background
                "tag_bg_hover": "#3d3d3d",  # Darker hover state
                "tag_bg_selected": "#0d6efd",# Brighter selection color
                "text": "#ffffff",          # White text
                "text_selected": "white",
                "border": "#404040"         # Darker border
            }
        }
        
        # Create custom styles
        style = ttk.Style()
        
        # Configure frame styles
        style.layout("TagItem.TFrame", [
            ("Frame.border", {"sticky": "nswe"})
        ])
        style.layout("TagItem.TFrame.Hover", [
            ("Frame.border", {"sticky": "nswe"})
        ])
        style.layout("TagItem.TFrame.Selected", [
            ("Frame.border", {"sticky": "nswe"})
        ])
        
        # Configure frame colors and properties
        style.configure(
            "Tag.TFrame",
            background=self.colors[self.theme]["bg"]
        )
        style.configure(
            "TagItem.TFrame",
            background=self.colors[self.theme]["tag_bg"],
            relief="flat"
        )
        style.configure(
            "TagItem.TFrame.Hover",
            background=self.colors[self.theme]["tag_bg_hover"],
            relief="flat"
        )
        style.configure(
            "TagItem.TFrame.Selected",
            background=self.colors[self.theme]["tag_bg_selected"],
            relief="flat"
        )
        
        # Configure label styles
        style.layout("TagItem.TLabel", [
            ("Label.border", {"sticky": "nswe"}),
            ("Label.padding", {"sticky": "nswe", "children":
                [("Label.label", {"sticky": "nswe"})]
            })
        ])
        style.layout("TagItem.TLabel.Hover", [
            ("Label.border", {"sticky": "nswe"}),
            ("Label.padding", {"sticky": "nswe", "children":
                [("Label.label", {"sticky": "nswe"})]
            })
        ])
        style.layout("TagItem.TLabel.Selected", [
            ("Label.border", {"sticky": "nswe"}),
            ("Label.padding", {"sticky": "nswe", "children":
                [("Label.label", {"sticky": "nswe"})]
            })
        ])
        
        style.configure(
            "Tag.TLabel",
            background=self.colors[self.theme]["bg"],
            foreground=self.colors[self.theme]["text"],
            font=("Segoe UI", 11)
        )
        style.configure(
            "TagItem.TLabel",
            background=self.colors[self.theme]["tag_bg"],
            foreground=self.colors[self.theme]["text"],
            font=("Segoe UI", 11)
        )
        style.configure(
            "TagItem.TLabel.Hover",
            background=self.colors[self.theme]["tag_bg_hover"],
            foreground=self.colors[self.theme]["text"]
        )
        style.configure(
            "TagItem.TLabel.Selected",
            background=self.colors[self.theme]["tag_bg_selected"],
            foreground=self.colors[self.theme]["text_selected"]
        )
        
        # Configure Scrollbar style
        style.layout("Vertical.TScrollbar", [
            ('Vertical.Scrollbar.trough', {
                'sticky': 'ns',
                'children': [('Vertical.Scrollbar.thumb', {
                    'sticky': 'nswe'
                })]
            })
        ])
        
        style.configure("Vertical.TScrollbar",
            background=self.colors[self.theme]["tag_bg"],
            troughcolor=self.colors[self.theme]["bg"],
            width=8,
            arrowsize=0
        )
        
        # Add scrollbar thumb color
        style.map("Vertical.TScrollbar",
            background=[
                ("pressed", self.colors[self.theme]["tag_bg_hover"]),
                ("active", self.colors[self.theme]["tag_bg_hover"]),
                ("!active", self.colors[self.theme]["tag_bg"])
            ]
        )
        
        # Update button style with explicit background control
        style.layout("Tag.TButton", [
            ('Button.padding', {'children': [
                ('Button.label', {'sticky': 'nswe'})
            ], 'sticky': 'nswe'})
        ])
        
        style.configure(
            "Tag.TButton",
            background=self.colors[self.theme]["tag_bg"],
            foreground=self.colors[self.theme]["text"],
            padding=0,
            font=("Segoe UI", 11),
            relief="flat",
            borderwidth=0,
            focuscolor=self.colors[self.theme]["tag_bg"],  # Remove focus highlight
            lightcolor=self.colors[self.theme]["tag_bg"],  # Remove 3D effect
            darkcolor=self.colors[self.theme]["tag_bg"]    # Remove 3D effect
        )
        
        style.map("Tag.TButton",
            background=[
                ("pressed", self.colors[self.theme]["tag_bg_selected"]),
                ("active", self.colors[self.theme]["tag_bg_hover"]),
                ("!active", self.colors[self.theme]["tag_bg"])  # Default state
            ],
            foreground=[
                ("pressed", self.colors[self.theme]["text_selected"]),
                ("active", self.colors[self.theme]["text"])
            ],
            relief=[("pressed", "flat"), ("!pressed", "flat")],  # Always flat
            borderwidth=[("pressed", 0), ("!pressed", 0)]        # Always no border
        )
    
    def create_widgets(self):
        # Header
        self.header_frame = ttk.Frame(self, style="Tag.TFrame")
        self.header_frame.pack(fill="x", padx=4, pady=(4, 0))
        
        # Left side: Tags count
        self.header_label = ttk.Label(
            self.header_frame,
            text="Tags (0)",
            style="Tag.TLabel"
        )
        self.header_label.pack(side="left", padx=4)
        
        # Right side: Theme toggle and Add button in a container
        button_container = ttk.Frame(self.header_frame, style="Tag.TFrame")
        button_container.pack(side="right", padx=4)
        
        self.theme_button = ttk.Button(
            button_container,
            text="◐" if self.theme == "light" else "◑",
            width=3,  # Back to original width
            style="Tag.TButton",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=(0, 2))
        
        self.add_button = ttk.Button(
            button_container,
            text="+",
            width=3,  # Back to original width
            style="Tag.TButton",
            command=self.show_add_tag_dialog
        )
        self.add_button.pack(side="right", padx=(2, 0))
        
        # Main container for both scrollable area and create tag button
        self.main_container = ttk.Frame(self, style="Tag.TFrame")
        self.main_container.pack(fill="both", expand=True, padx=4)
        
        # Container for scrollable content
        self.scroll_container = ttk.Frame(self.main_container, style="Tag.TFrame")
        self.scroll_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar inside scroll_container
        self.canvas = tk.Canvas(
            self.scroll_container,
            bg=self.colors[self.theme]["bg"],
            highlightthickness=0,
        )
        
        self.scrollbar = ttk.Scrollbar(
            self.scroll_container,
            orient="vertical",
            command=self.canvas.yview,
            style="Vertical.TScrollbar"
        )
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")  # Always show scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Tags container inside canvas
        self.tags_frame = ttk.Frame(self.canvas, style="Tag.TFrame")
        
        # Create window in canvas for tags
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.tags_frame,
            anchor="nw",
            width=self.canvas.winfo_width()
        )
        
        # Sample tags (adding more to test scrolling)
        sample_tags = [
            "Development",
            "Testing",
            "Production",
            "Long Running Tag That Should Truncate",
            "QA",
            "Frontend",
            "Backend",
            "Database",
            "API",
            "Security",
            "Performance",
            "UI/UX",
            "Mobile",
            "Desktop",
            "Cloud",
            "DevOps",
            "Analytics",
            "Machine Learning",
            "Infrastructure",
            "Monitoring"
        ]
        
        for tag in sample_tags:
            self.create_tag(tag)
        
        # Add "Create Tag" button at the bottom
        self.create_tag_button = ttk.Frame(self.main_container, style="TagItem.TFrame")
        self.create_tag_button.pack(fill="x", pady=1)
        
        create_label = ttk.Label(
            self.create_tag_button,
            text="➕ Create Tag",
            style="TagItem.TLabel"
        )
        create_label.pack(fill="x", padx=8, pady=4)
        
        # Bind hover and click events for create button
        for widget in (self.create_tag_button, create_label):
            widget.bind("<Enter>", lambda e: self.on_create_hover(True))
            widget.bind("<Leave>", lambda e: self.on_create_hover(False))
            widget.bind("<Button-1>", lambda e: self.show_add_tag_dialog())
        
        # Configure canvas scrolling
        self.tags_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Configure mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # After adding all sample tags, update the count
        self.update_tag_count()
    
    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Force an update to ensure proper measurements
        self.update_idletasks()
    
    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.tags_frame.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def create_tag(self, text, selected=False):
        tag_frame = ttk.Frame(self.tags_frame, style="TagItem.TFrame")
        tag_frame.pack(fill="x", pady=1)
        
        tag_label = ttk.Label(
            tag_frame,
            text=f"⚫ {text}",
            style="TagItem.TLabel"
        )
        tag_label.pack(fill="x", padx=8, pady=4)
        
        # Store the label reference and text
        tag_frame.label = tag_label
        tag_frame.selected = selected
        tag_frame.tag_text = text  # Store the tag text for reference
        
        # Create right-click menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(
            label="Remove",
            command=lambda: self.remove_tag(tag_frame)
        )
        
        # Bind hover and click events
        for widget in (tag_frame, tag_label):
            widget.bind("<Enter>", lambda e, tf=tag_frame: self.on_tag_hover(tf, True))
            widget.bind("<Leave>", lambda e, tf=tag_frame: self.on_tag_hover(tf, False))
            widget.bind("<Button-1>", lambda e, tf=tag_frame: self.on_tag_click(tf))
            widget.bind("<Button-3>", lambda e, tf=tag_frame: self.show_context_menu(e, tf))  # Right-click
        
        # After creating the tag, update the count
        self.update_tag_count()
    
    def on_tag_hover(self, tag_frame, entering):
        if not tag_frame.selected:
            style_suffix = ".Hover" if entering else ""
            tag_frame.configure(style=f"TagItem.TFrame{style_suffix}")
            tag_frame.label.configure(style=f"TagItem.TLabel{style_suffix}")
    
    def on_tag_click(self, tag_frame):
        # Toggle selection
        tag_frame.selected = not tag_frame.selected
        
        if tag_frame.selected:
            tag_frame.configure(style="TagItem.TFrame.Selected")
            tag_frame.label.configure(style="TagItem.TLabel.Selected")
        else:
            tag_frame.configure(style="TagItem.TFrame")
            tag_frame.label.configure(style="TagItem.TLabel")
    
    def update_tag_count(self):
        """Update the header label with the current number of tags"""
        tag_count = len(self.tags_frame.winfo_children())
        self.header_label.configure(text=f"Tags ({tag_count})")
    
    def show_add_tag_dialog(self):
        """Show dialog to add a new tag"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Tag")
        dialog.transient(self.winfo_toplevel())  # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("300x100")
        x = self.winfo_toplevel().winfo_x() + (self.winfo_toplevel().winfo_width() // 2) - 150
        y = self.winfo_toplevel().winfo_y() + (self.winfo_toplevel().winfo_height() // 2) - 50
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog contents
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Tag name:").pack(pady=(0, 5))
        
        entry = ttk.Entry(frame)
        entry.pack(fill="x", pady=(0, 10))
        entry.focus_set()
        
        def add_tag():
            tag_name = entry.get().strip()
            if tag_name:
                self.create_tag(tag_name)
                dialog.destroy()
        
        def handle_enter(event):
            add_tag()
        
        entry.bind("<Return>", handle_enter)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x")
        
        ttk.Button(
            button_frame,
            text="Add",
            command=add_tag
        ).pack(side="right", padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="right")

    def show_context_menu(self, event, tag_frame):
        """Show the context menu for a tag"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def remove_tag(self, tag_frame):
        """Remove a tag from the sidebar"""
        tag_frame.destroy()
        self.update_tag_count()
        # Ensure proper scroll region update
        self.on_frame_configure()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme = "dark" if self.theme == "light" else "light"
        # Use Unicode symbols that work well in both themes
        if self.theme == "dark":
            self.theme_button.configure(text="◑")  # Half moon for dark theme
        else:
            self.theme_button.configure(text="◐")  # Half moon for light theme
        self.setup_styles()
        self.update_all_widgets()

    def update_all_widgets(self):
        """Update all widgets with new theme colors"""
        # Update canvas and its background
        self.canvas.configure(
            bg=self.colors[self.theme]["bg"],
            highlightthickness=0
        )
        
        # Update frames - removed search_frame from the list
        for frame in [self.header_frame, self.scroll_container]:
            frame.configure(style="Tag.TFrame")
        
        # Update all tags
        for tag_frame in self.tags_frame.winfo_children():
            if hasattr(tag_frame, "selected") and tag_frame.selected:
                tag_frame.configure(style="TagItem.TFrame.Selected")
                tag_frame.label.configure(style="TagItem.TLabel.Selected")
            else:
                tag_frame.configure(style="TagItem.TFrame")
                tag_frame.label.configure(style="TagItem.TLabel")
        
        # Update labels and buttons
        self.header_label.configure(style="Tag.TLabel")
        self.theme_button.configure(style="Tag.TButton")
        self.add_button.configure(style="Tag.TButton")
        
        # Update scrollbar colors
        style = ttk.Style()
        style.configure("Vertical.TScrollbar",
            background=self.colors[self.theme]["tag_bg"],
            troughcolor=self.colors[self.theme]["bg"],
            arrowcolor=self.colors[self.theme]["text"],
            bordercolor=self.colors[self.theme]["border"],
            lightcolor=self.colors[self.theme]["tag_bg"],
            darkcolor=self.colors[self.theme]["tag_bg"]
        )
        
        # Update create tag button
        self.create_tag_button.configure(style="TagItem.TFrame")
        for child in self.create_tag_button.winfo_children():
            child.configure(style="TagItem.TLabel")
    
    def on_create_hover(self, entering):
        """Handle hover events for create tag button"""
        style_suffix = ".Hover" if entering else ""
        self.create_tag_button.configure(style=f"TagItem.TFrame{style_suffix}")
        for child in self.create_tag_button.winfo_children():
            child.configure(style=f"TagItem.TLabel{style_suffix}")

    def create_context_menu(self):
        """Create the context menu with proper theme colors"""
        self.context_menu = tk.Menu(
            self,
            tearoff=0,
            bg=self.colors[self.theme]["tag_bg"],
            fg=self.colors[self.theme]["text"],
            activebackground=self.colors[self.theme]["tag_bg_hover"],
            activeforeground=self.colors[self.theme]["text_selected"],
            relief="flat",
            borderwidth=1
        )
        self.context_menu.add_command(
            label="Remove",
            command=lambda: self.remove_tag(self.current_tag_frame)
        )

def main():
    root = tk.Tk()
    root.title("Tag Sidebar Prototype")
    
    # Create a frame with fixed width for sidebar
    sidebar = ttk.Frame(root, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    
    # Add some padding and height to better simulate the sidebar
    root.geometry("300x600")
    
    app = TagSidebarPrototype(sidebar)
    app.pack(fill="both", expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main() 