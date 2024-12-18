import tkinter as tk
from tkinter import ttk

class TagCanvas(tk.Canvas):
    def __init__(self, parent, tag_sidebar, **kwargs):
        super().__init__(parent, **kwargs)
        self.tag_sidebar = tag_sidebar
        self.tags = []
        self.selected_tags = set()
        
        # Adjust dimensions for better spacing
        self.tag_height = 45  # Increased for more vertical space
        self.tag_padding = 8  # Reduced gap between tags
        self.corner_radius = 12
        self.horizontal_padding = 12  # Side padding
        self.content_padding = 15  # Padding between elements inside tag
        self.left_margin = 15  # Left margin for all content
        self.theme = "dark"
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind events
        self.bind("<Configure>", self._on_resize)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<MouseWheel>", self._on_mousewheel)
        
        # Track hover state
        self.hover_tag = None
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)

    def _on_resize(self, event):
        """Handle window resize"""
        self.redraw_tags()

    def _on_click(self, event):
        """Handle mouse click"""
        # Get clicked tag
        tag_index = self._get_tag_at_position(event.y)
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
        tag_index = self._get_tag_at_position(event.y)
        if tag_index is not None:
            if self.hover_tag != tag_index:
                self.hover_tag = tag_index
                self.redraw_tags()
        elif self.hover_tag is not None:
            self.hover_tag = None
            self.redraw_tags()

    def _on_leave(self, event):
        """Handle mouse leaving the canvas"""
        if self.hover_tag is not None:
            self.hover_tag = None
            self.redraw_tags()

    def _on_right_click(self, event):
        """Handle right-click for context menu"""
        tag_index = self._get_tag_at_position(event.y)
        if tag_index is not None:
            tag = self.tags[tag_index]
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label=f"Remove '{tag}'",
                command=lambda t=tag: self.tag_sidebar.remove_tag(t)
            )
            menu.tk_popup(event.x_root, event.y_root)

    def _get_tag_at_position(self, y):
        """Get tag index at given y position"""
        # Adjust y for scrolling
        y = y + self.yview()[0] * self.winfo_height()
        
        # Account for the Add Tag button and padding at top
        button_height = 40  # Match the height used in redraw_tags
        top_padding = self.tag_padding * 2
        start_y = button_height + (top_padding * 2)
        
        # Adjust y to account for the button space
        adjusted_y = y - start_y
        
        # Calculate tag index based on adjusted position
        tag_index = int(adjusted_y / (self.tag_height + self.tag_padding))
        if 0 <= tag_index < len(self.tags):
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

    def draw_tag(self, tag, index, start_y=0):
        """Draw a single tag as a rounded rectangle"""
        y_offset = 8
        y = start_y + (index * (self.tag_height + self.tag_padding)) + y_offset
        width = 250
        
        # Calculate maximum width for text
        max_text_width = width - (
            self.horizontal_padding * 2 +  # Left and right padding
            self.left_margin +             # Left margin
            self.content_padding * 2 +     # Content padding
            25                             # Space for checkmark/emoji
        )
        
        # Get theme-specific colors
        if self.theme == "dark":
            if tag in self.selected_tags:
                bg_color = '#2B4D6F'
                outline_color = '#5B9BD5'
                glow_color = '#4B7BBA'
            else:
                bg_color = '#274156'
                outline_color = '#385167'
            text_color = 'white'
        else:
            if tag in self.selected_tags:
                bg_color = '#E3F2FD'
                outline_color = '#2196F3'
                glow_color = '#64B5F6'
            else:
                bg_color = '#FFFFFF'
                outline_color = '#D0D7DE'
            text_color = '#0078D7' if tag in self.selected_tags else '#2B4B6F'

        # Draw base tag with shadow first
        if tag in self.selected_tags:
            # Selection glow
            for i in range(3):
                glow_offset = i * 1.2
                opacity = "gray75" if i == 0 else "gray50" if i == 1 else "gray25"
                self.create_rounded_rectangle(
                    self.horizontal_padding - glow_offset,
                    y - glow_offset,
                    width - self.horizontal_padding + glow_offset,
                    y + self.tag_height - 4 + glow_offset,
                    self.corner_radius,
                    fill='',
                    outline=glow_color,
                    width=1,
                    stipple=opacity
                )

        # Draw main tag background
        self.create_rounded_rectangle(
            self.horizontal_padding,
            y,
            width - self.horizontal_padding,
            y + self.tag_height - 4,
            self.corner_radius,
            fill=bg_color,
            outline=outline_color,
            width=2 if index == self.hover_tag or tag in self.selected_tags else 1
        )

        # Calculate text positions
        content_x = self.left_margin
        content_y = y + (self.tag_height // 2)

        # Draw checkmark for selected tags
        if tag in self.selected_tags:
            self.create_text(
                content_x, content_y,
                text="✓",
                anchor='w',
                fill=text_color,
                font=('Segoe UI', 12, 'bold')
            )
            content_x += self.content_padding + 10

        # Draw emoji
        self.create_text(
            content_x, content_y,
            text="🏷️",
            anchor='w',
            fill=text_color
        )
        content_x += self.content_padding + 15

        # Get tag count and create display text
        tag_count = len([m for m in self.tag_sidebar.tag_manager.get_machines_by_tags([tag])])
        tag_text = f"{tag} ({tag_count})" if tag_count > 0 else tag

        # Measure text width
        font = ('Segoe UI', 11, 'bold' if tag in self.selected_tags else '')
        temp = tk.Label(self, text=tag_text, font=font)
        text_width = temp.winfo_reqwidth()
        temp.destroy()

        # Truncate text if too long
        if text_width > max_text_width:
            while text_width > max_text_width and len(tag_text) > 3:
                tag_text = tag_text[:-4] + "..."  # Remove one character and add ellipsis
                temp = tk.Label(self, text=tag_text, font=font)
                text_width = temp.winfo_reqwidth()
                temp.destroy()

        # Draw tag text
        self.create_text(
            content_x, content_y,
            text=tag_text,
            anchor='w',
            fill=text_color,
            font=font
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
        button_height = 40  # Increased height for better visibility
        top_padding = self.tag_padding * 2  # Padding above and below button
        
        # Position the Add Tag button at the top with improved styling
        if hasattr(self.tag_sidebar, 'add_button'):
            self.tag_sidebar.add_button.place(
                x=self.horizontal_padding,
                y=top_padding,
                width=self.winfo_width() - (2 * self.horizontal_padding),
                height=button_height  # Set explicit height
            )
        
        # Calculate total height for scrolling, starting after the button
        start_y = button_height + (top_padding * 2)  # Space for button plus padding
        total_height = start_y + (len(self.tags) * (self.tag_height + self.tag_padding))
        
        # Configure scrollable area
        self.configure(scrollregion=(0, 0, self.winfo_width(), total_height))
        
        # Draw each tag, starting below the button
        for i, tag in enumerate(self.tags):
            # Adjust tag position to start after the button
            self.draw_tag(tag, i, start_y)

    def set_tags(self, tags):
        """Update the list of tags"""
        self.tags = tags
        self.redraw_tags()

    def get_selected_tags(self):
        """Get currently selected tags"""
        return list(self.selected_tags)

class TagSidebar(tk.Frame):
    def __init__(self, parent, tag_manager):
        super().__init__(parent)
        self.tag_manager = tag_manager
        self.theme = "dark"
        
        # Create custom button style
        style = ttk.Style()
        style.configure(
            'AddTag.TButton',
            font=('Segoe UI', 11),  # Larger font
            padding=(10, 8)  # Internal padding
        )
        
        # Create main container
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create container for canvas and scrollbar
        self.canvas_container = tk.Frame(self.main_container)
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # Create tag canvas with self reference
        self.tag_canvas = TagCanvas(
            self.canvas_container,
            tag_sidebar=self,
            bg='#274156',
            highlightthickness=0,
            width=250
        )
        self.tag_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Pack scrollbar directly next to canvas
        self.tag_canvas.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind tag selection event
        self.tag_canvas.bind("<<TagSelected>>", lambda e: self.event_generate("<<TagSelected>>"))
        
        # Add button with custom style
        self.add_button = ttk.Button(
            self.tag_canvas,
            text="+ Add Tag",  # Added plus sign for better visibility
            command=self._show_add_tag_dialog,
            style='AddTag.TButton'  # Apply custom style
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
        
        entry = ttk.Entry(dialog)
        entry.pack(pady=10, padx=10, fill=tk.X)
        
        def add():
            tag_name = entry.get().strip()
            if tag_name:
                self.add_tag(tag_name)
                dialog.destroy()
        
        # Bind Enter key to add function
        entry.bind('<Return>', lambda e: add())
        
        ttk.Button(dialog, text="Add", command=add).pack(pady=5)
        
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