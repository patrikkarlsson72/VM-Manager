import tkinter as tk
from tkinter import ttk
import os
import sys

class TagCanvas(tk.Canvas):
    def __init__(self, parent, tag_sidebar, main_canvas=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.tag_sidebar = tag_sidebar
        self.main_canvas = main_canvas
        self.tags = []
        self.selected_tags = set()
        
        # Add font initialization
        self.font = ('Segoe UI', 11)
        
        # Adjust dimensions for grid layout
        self.tag_width = 120  # Width of each tag
        self.tag_height = 45  # Height of each tag
        self.tag_padding = 8  # Space between tags
        self.corner_radius = 12
        self.horizontal_padding = 12
        self.content_padding = 15
        self.left_margin = 15
        self.tags_per_row = 2  # Number of tags per row
        self.theme = "dark"
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind events
        self.bind("<Configure>", self._on_resize)
        self.bind("<Button-1>", self._on_tag_drag_start)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind('<B1-Motion>', self._on_tag_drag_motion)
        self.bind('<ButtonRelease-1>', self._on_tag_drag_end)
        
        # Track hover state
        self.hover_tag = None
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)
        
        # Add tooltip attributes
        self.tooltip = None
        self.tooltip_tag = None

    def _on_resize(self, event):
        """Handle window resize"""
        self.redraw_tags()

    def _on_click(self, event):
        """Handle mouse click"""
        # Get clicked tag
        tag_index = self._get_tag_at_position(event.x, event.y)
        if tag_index is not None:
            tag = self.tags[tag_index]
            if tag in self.selected_tags:
                self.selected_tags.remove(tag)
            else:
                self.selected_tags.add(tag)
            self.redraw_tags()
            self.event_generate("<<TagSelected>>")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"  # Stop event propagation

    def _on_motion(self, event):
        """Handle mouse motion for hover effect"""
        tag_index = self._get_tag_at_position(event.x, event.y)
        if tag_index is not None:
            if self.hover_tag != tag_index:
                self.hover_tag = tag_index
                self.redraw_tags()
                
                # Show tooltip
                if self.tooltip:
                    self.delete(self.tooltip)
                
                # Get tag text
                tag_text = self.tags[tag_index]
                
                # Calculate tooltip position
                x = event.x + 10  # Offset from cursor
                y = event.y + 10
                
                # Create tooltip background
                tooltip_bg = self.create_rectangle(
                    x, y, x + len(tag_text) * 7 + 10, y + 25,
                    fill='#2c3e50' if self.theme == "dark" else '#f8f9fa',
                    outline='#34495e' if self.theme == "dark" else '#dee2e6',
                    tags='tooltip'
                )
                
                # Create tooltip text
                tooltip_text = self.create_text(
                    x + 5, y + 12,
                    text=tag_text,
                    anchor='w',
                    fill='white' if self.theme == "dark" else '#2c3e50',
                    font=('Segoe UI', 10),
                    tags='tooltip'
                )
                
                self.tooltip = tooltip_bg
                self.tooltip_tag = tooltip_text
                
        elif self.hover_tag is not None:
            self.hover_tag = None
            self.redraw_tags()
            # Remove tooltip
            if self.tooltip:
                self.delete('tooltip')
                self.tooltip = None
                self.tooltip_tag = None

    def _on_leave(self, event):
        """Handle mouse leaving the canvas"""
        if self.hover_tag is not None:
            self.hover_tag = None
            self.redraw_tags()
        # Remove tooltip
        if self.tooltip:
            self.delete('tooltip')
            self.tooltip = None
            self.tooltip_tag = None

    def _on_right_click(self, event):
        """Handle right-click for context menu"""
        tag_index = self._get_tag_at_position(event.x, event.y)
        if tag_index is not None:
            tag = self.tags[tag_index]
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label=f"Remove '{tag}'",
                command=lambda t=tag: self.tag_sidebar.remove_tag(t)
            )
            menu.tk_popup(event.x_root, event.y_root)

    def _get_tag_at_position(self, x, y):
        """Get tag index at given x,y position"""
        # Adjust y for scrolling
        y = y + self.yview()[0] * self.winfo_height()
        
        # Account for the Add Tag button and padding at top
        button_height = 40
        top_padding = self.tag_padding * 2
        start_y = button_height + (top_padding * 2)
        
        # Adjust coordinates to account for the button space
        adjusted_y = y - start_y
        adjusted_x = x - self.horizontal_padding
        
        # Calculate row and column
        row = int(adjusted_y / (self.tag_height + self.tag_padding))
        col = int(adjusted_x / (self.tag_width + self.tag_padding))
        
        # Calculate tag index
        tag_index = row * self.tags_per_row + col
        
        if (0 <= col < self.tags_per_row and 
            0 <= tag_index < len(self.tags) and 
            adjusted_x >= 0 and adjusted_x <= (self.tag_width + self.tag_padding) * self.tags_per_row):
            return tag_index
        return None

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def draw_tag(self, tag, index, start_y):
        """Draw a single tag with count"""
        # Calculate position
        row = index // self.tags_per_row
        col = index % self.tags_per_row
        
        x = self.horizontal_padding + (col * (self.tag_width + self.tag_padding))
        y = start_y + (row * (self.tag_height + self.tag_padding))
        
        # Get count of machines with this tag
        count = len([m for m in self.tag_sidebar.tag_manager.machine_tags 
                    if tag in self.tag_sidebar.tag_manager.machine_tags[m]])
        
        # Create tag background
        bg_color = '#385167' if self.theme == "dark" else '#E3F2FD'
        if tag in self.selected_tags:
            bg_color = self._lighten_color(bg_color, 0.3)
        elif index == self.hover_tag:
            bg_color = self._lighten_color(bg_color, 0.1)
        
        # Create the rounded rectangle background
        self.create_rounded_rectangle(
            x, y, x + self.tag_width, y + self.tag_height,
            self.corner_radius,
            fill=bg_color,
            outline='',
            tags=("tag", f"tag_{index}")
        )
        
        # Create font object for measurement
        font_obj = tk.font.Font(family='Segoe UI', size=11)
        count_text = f" ({count})" if count > 0 else ""
        count_width = font_obj.measure(count_text)
        
        # Calculate available width for tag text
        available_width = self.tag_width - 20 - count_width  # 20 for padding
        
        # Truncate tag text if needed
        tag_text = tag
        if font_obj.measure(tag_text) > available_width:
            while font_obj.measure(tag_text + "...") > available_width and len(tag_text) > 0:
                tag_text = tag_text[:-1]
            tag_text += "..."
        
        # Draw tag text
        self.create_text(
            x + 10, y + (self.tag_height // 2),
            text=tag_text,
            fill='white' if self.theme == "dark" else '#2B4B6F',
            font=('Segoe UI', 11),
            anchor='w',
            tags=("tag", f"tag_{index}")
        )
        
        # Draw count at fixed position on the right
        if count > 0:
            self.create_text(
                x + self.tag_width - 10, y + (self.tag_height // 2),
                text=count_text,
                fill='white' if self.theme == "dark" else '#2B4B6F',
                font=('Segoe UI', 11),
                anchor='e',
                tags=("tag", f"tag_{index}")
            )

    def _lighten_color(self, color, factor):
        """Lighten a hex color by a factor"""
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        rgb = tuple(min(int(x + (255 - x) * factor), 255) for x in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def redraw_tags(self):
        """Redraw all tags"""
        self.delete("all")  # Clear canvas
        
        # Add space for the Add Tag button at the top
        button_height = 40
        top_padding = self.tag_padding * 2
        
        # Position the Add Tag button at the top
        if hasattr(self.tag_sidebar, 'add_button'):
            self.tag_sidebar.add_button.place(
                x=self.horizontal_padding,
                y=top_padding,
                width=self.winfo_width() - (2 * self.horizontal_padding),
                height=button_height
            )
        
        # Calculate total height for scrolling
        start_y = button_height + (top_padding * 2)
        num_rows = (len(self.tags) + self.tags_per_row - 1) // self.tags_per_row  # Ceiling division
        total_height = start_y + (num_rows * (self.tag_height + self.tag_padding))
        
        # Configure scrollable area
        self.configure(scrollregion=(0, 0, self.winfo_width(), total_height))
        
        # Draw each tag
        for i, tag in enumerate(self.tags):
            self.draw_tag(tag, i, start_y)

    def set_tags(self, tags):
        """Update the list of tags"""
        self.tags = tags
        self.redraw_tags()

    def get_selected_tags(self):
        """Get currently selected tags"""
        return list(self.selected_tags)

    def _on_tag_drag_start(self, event):
        """Start dragging a tag"""
        tag_index = self._get_tag_at_position(event.x, event.y)
        if tag_index is not None:
            # Store initial click position and tag
            self.drag_data = {
                'tag': self.tags[tag_index],
                'start_x': event.x,
                'start_y': event.y,
                'dragging': False  # Start as not dragging
            }

    def _on_tag_drag_motion(self, event):
        """Handle tag being dragged"""
        if hasattr(self, 'drag_data'):
            dx = abs(event.x - self.drag_data['start_x'])
            dy = abs(event.y - self.drag_data['start_y'])
            if dx > 5 or dy > 5:  # Threshold for considering it a drag
                self.drag_data['dragging'] = True
                self.configure(cursor='hand2')
                
                # Delete previous ghost tag if it exists
                if hasattr(self, 'ghost_tag'):
                    self.delete('ghost_tag')
                
                # Create ghost tag following cursor
                ghost_x = event.x
                ghost_y = event.y
                self.create_rounded_rectangle(
                    ghost_x - 60, ghost_y - 20,  # Center around cursor
                    ghost_x + 60, ghost_y + 20,
                    self.corner_radius,
                    fill='#385167' if self.theme == "dark" else '#E3F2FD',
                    stipple='gray50',  # Makes it semi-transparent
                    tags='ghost_tag'
                )
                # Add tag text
                self.create_text(
                    ghost_x, ghost_y,
                    text=self.drag_data['tag'],
                    fill='white' if self.theme == "dark" else '#2B4B6F',
                    font=('Segoe UI', 11),
                    tags='ghost_tag'
                )

    def _on_tag_drag_end(self, event):
        """End tag drag"""
        if hasattr(self, 'drag_data'):
            if not self.drag_data.get('dragging', False):
                # It was a click, not a drag - handle selection
                tag_index = self._get_tag_at_position(event.x, event.y)
                if tag_index is not None:
                    tag = self.tags[tag_index]
                    if tag in self.selected_tags:
                        self.selected_tags.remove(tag)
                    else:
                        self.selected_tags.add(tag)
                    self.redraw_tags()
                    self.event_generate("<<TagSelected>>")
            else:
                # Convert canvas coordinates to screen coordinates
                abs_x = self.winfo_rootx() + event.x
                abs_y = self.winfo_rooty() + event.y
                
                # Generate custom event with drop data
                self.event_generate("<<TagDropped>>", 
                    data={
                        'tag': self.drag_data['tag'],
                        'x': abs_x,
                        'y': abs_y
                    }
                )
            
            # Clean up
            self.configure(cursor='')
            del self.drag_data
        if hasattr(self, 'ghost_tag'):
            self.delete('ghost_tag')

        # Reset all button effects in main canvas
        if self.main_canvas:  # Check if we have a reference
            for item in self.main_canvas.find_withtag("button_bg"):
                self.main_canvas.itemconfig(item,
                    outline=self.tag_sidebar.master.master.master.borders_and_dividers_color,
                    width=2)

class TagSidebar(tk.Frame):
    def __init__(self, parent, tag_manager, main_canvas=None):
        super().__init__(parent)
        self.tag_manager = tag_manager
        self.main_canvas = main_canvas
        self.theme = "dark"
        
        # Create custom button style
        style = ttk.Style()
        style.configure(
            'AddTag.TButton',
            font=('Segoe UI', 11),
            padding=(10, 8),
            justify='center',  # Center text horizontally
            anchor='center'    # Center the whole content
        )
        
        # Create main container with increased width
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create container for canvas and scrollbar
        self.canvas_container = tk.Frame(self.main_container)
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # Create tag canvas with increased width
        self.tag_canvas = TagCanvas(
            self.canvas_container,
            tag_sidebar=self,
            main_canvas=self.main_canvas,
            bg='#274156',
            highlightthickness=0,
            width=300
        )
        self.tag_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Pack scrollbar directly next to canvas
        self.tag_canvas.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind tag selection event
        self.tag_canvas.bind("<<TagSelected>>", lambda e: self.event_generate("<<TagSelected>>"))
        
        # Add button with custom style
        self.add_button = ttk.Button(
            self.tag_canvas,
            text="+ Add Tag",  # Simplified text without emoji for better centering
            command=self._show_add_tag_dialog,
            style='AddTag.TButton',
            width=15  # Add fixed width to help with centering
        )
        
        # Initialize last added/removed tag tracking
        self.last_added_tag = None
        self.last_removed_tag = None
        
        # Populate initial tags
        self.refresh_tags()
        
        # After creating the scrollbar in TagSidebar.__init__
        self.tag_canvas.scrollbar.bind("<MouseWheel>", lambda e: self.tag_canvas._on_mousewheel(e))

    def get_selected_tags(self):
        """Get list of currently selected tags"""
        return self.tag_canvas.get_selected_tags()

    def update_theme(self, theme):
        """Update the sidebar theme"""
        self.theme = theme
        self.tag_canvas.theme = theme  # Set theme directly on canvas
        if theme == "dark":
            self.tag_canvas.configure(bg='#274156')
            self.configure(bg='#274156')
        else:
            self.tag_canvas.configure(bg='#F0F7FF')
            self.configure(bg='#F0F7FF')
        
        self.tag_canvas.redraw_tags()

    def refresh_tags(self):
        """Refresh the tag list display"""
        tags = sorted(self.tag_manager.get_all_tags(), key=str.lower)
        self.tag_canvas.set_tags(tags)

    def add_tag(self, tag_name):
        """Add a new tag and refresh display"""
        if self.tag_manager.add_tag(tag_name):
            self.last_added_tag = tag_name
            self.refresh_tags()
            self.event_generate("<<TagAdded>>")
            return True
        return False

    def remove_tag(self, tag_name):
        """Remove a tag and refresh display"""
        if self.tag_manager.remove_tag(tag_name):
            self.last_removed_tag = tag_name
            self.refresh_tags()
            self.event_generate("<<TagRemoved>>")
            return True
        return False

    def _show_add_tag_dialog(self):
        """Show dialog to add a new tag"""
        dialog = tk.Toplevel(self)
        dialog.title("Add Tag")
        dialog.geometry("300x100")
        dialog.transient(self)
        dialog.grab_set()
        
        # Add icon loading logic
        try:
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = os.path.dirname(sys.executable)
                assets_path = os.path.join(base_path, "assets")
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
                assets_path = os.path.join(base_path, "assets")
            
            # Load the same icon used for settings
            icon_path = os.path.join(assets_path, "tag_icon.ico")
            if os.path.exists(icon_path):
                dialog.iconbitmap(icon_path)
            else:
                print(f"Warning: Could not find icon at {icon_path}")
                
        except Exception as e:
            print(f"Warning: Could not load dialog icon: {e}")
        
        # Center the dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        entry = ttk.Entry(dialog)
        entry.pack(pady=10, padx=10, fill=tk.X)
        
        def add():
            tag_name = entry.get().strip()
            if tag_name:
                self.add_tag(tag_name)
                dialog.destroy()
        
        # Bind Enter key to add function
        entry.bind('<Return>', lambda e: add())
        
        # Updated button text with emoji
        ttk.Button(dialog, text="🏷️ Add", command=add).pack(pady=5)
        
        # Set focus to entry
        entry.focus_set()

    def _show_context_menu(self, event):
        """Show context menu for tag list"""
        # Get clicked item
        index = self.tag_canvas.nearest(event.y)
        if index >= 0:
            # Create menu
            menu = tk.Menu(self, tearoff=0)
            
            # Get the tag name
            tag_name = self.tag_canvas.get(index)
            
            # Add menu items
            menu.add_command(
                label=f"Remove '{tag_name}'",
                command=lambda: self.remove_tag(tag_name)
            )
            
            # Show menu at mouse position
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def set_tags(self, tags):
        """Update the list of tags"""
        self.tag_canvas.set_tags(tags)
        self.tag_canvas.redraw_tags()