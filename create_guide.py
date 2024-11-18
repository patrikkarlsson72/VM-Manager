import os

def create_guide():
    try:
        # Get file paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        md_path = os.path.join(current_dir, 'docs', 'how-to-guide.md')
        
        # Ensure docs directory exists
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        
        # Split content into chunks
        chunks = [
            # Chunk 1: Header and TOC
            """# VM Manager - How To Guide

## Table of Contents
- [Initial Setup](#initial-setup)
- [Adding Virtual Machines](#adding-virtual-machines)
- [Managing Categories](#managing-categories)
- [Managing Tags](#managing-tags)
- [Connecting to Machines](#connecting-to-machines)
- [Managing Machines](#managing-machines)
- [Customizing Settings](#customizing-settings)
- [Sharing Machines](#sharing-machines)
- [Tips and Tricks](#tips-and-tricks)
""",
            # Chunk 2: Initial Setup
            """## Initial Setup

### First Launch
When you first launch VM Manager, you'll be prompted to select a default RDP file:

![Initial Setup](images/initial-setup.png)

1. Click "OK" on the prompt
2. Browse to select your default RDP file
3. The application will create necessary folders automatically

### Theme Selection
VM Manager supports both light and dark themes:

![Theme Selection](images/theme-selection.png)

1. Click the theme toggle (☀️/🌙) in the header
2. Theme changes apply immediately
3. Selection persists between sessions
""",
            # Chunk 3: Adding VMs
            """## Adding Virtual Machines

### Adding a Single Machine
You can add machines one at a time using the sidebar:

![Add Single Machine](images/add-single.png)

1. Enter the machine name in the "Add Single PC" field
2. Click "Add PC"
3. The machine will appear in the main view

### Adding Multiple Machines
For batch additions:

![Add Multiple Machines](images/add-multiple.png)

1. Enter machine names in the text area (one per line)
2. Click "Add PCs"
3. All machines will be added to the main view
""",
            # Chunk 4: Categories
            """## Managing Categories

### Creating and Managing Categories
To organize your machines into categories:

![Categories](images/categories.png)

1. Click "Manage Categories" in the sidebar
2. Add a new category:
   - Click "Add Category"
   - Enter category name
   - Choose category color (optional)
   - Click Save

![Categories](images/set-categories.png)

3. Assign machines to categories:
   - Right-click any machine
   - Select "Set Category"
   - Choose from available categories
4. Filter by category:
   - Click category name in sidebar
   - View only machines in that category
   - Click "All Machines" to clear filter

### Category Organization
Tips for effective category management:

1. Use clear, descriptive category names
2. Assign colors for visual organization
3. Categories can be nested (subcategories)
4. Machines can belong to multiple categories
5. Categories can be edited or deleted through the management panel
""",        
            # Chunk 5: Tags
            """## Managing Tags

### Creating and Managing Tags
To use the tagging system:

![Tags](images/tags.png)

1. Add tags:
- Click "Manage Tags" in the sidebar
- Enter new tag name in the input field
- Click "Add Tag" or press Enter
- Tags will appear in the list above

2. Assign tags to machines:
- Right-click any machine
- Select "Tags"
- Check the tag from the list to assign it. To remove a tag, click on it again.
- Changes are saved automatically

3. Filter by tags:
- Click tags in the sidebar to filter
- Select multiple tags to see machines with any of those tags
- Click "Reset Filter" to clear all tag filters or click on the tag name in the sidebar

### Tag Organization Tips
1. Use consistent naming conventions
2. Keep tags simple and descriptive
3. Regular cleanup of unused tags
4. Use tags alongside categories for better organization

### Managing Existing Tags
- View all tags in the tag manager
- Delete tags using the × button next to each tag
- Deleting a tag removes it from all machines
""",

            # Chunk 6: Connecting
            """## Connecting to Machines

### Basic Connection
To connect to a machine:

![Connect to Machine](images/connect.png)

1. Click on any machine tile
2. The RDP connection will launch automatically
3. Status indicator shows if machine is available (green) or unavailable (red)

### Custom RDP Connections
To use a specific RDP configuration:

![Custom RDP](images/custom-rdp.png)

1. Right-click the machine
2. Select "Set RDP Path"
3. Choose your custom RDP file
4. Future connections will use this configuration
""",
            # Chunk 7: Managing
            """## Managing Machines

### Context Menu Options
Right-click any machine to access management options:

![Context Menu](images/context-menu.png)

1. Add/Edit Description
2. Set Custom RDP Path
3. Share Machine Configuration
4. Delete Machine

### Adding Descriptions
To add a description:

![Add Description](images/add-description.png)

1. Right-click the machine
2. Select "Add or Edit Description"
3. Enter your description
4. Click OK
""",
            # Chunk 8: Settings
            """## Customizing Settings

### Settings Panel
![Settings Panel](images/settings-panel.png)

Access application settings:

![Settings Panel Button](images/settings-panel-button.png)

1. Click the Settings button in the sidebar
2. Settings are organized into categories:
   - **Machine Settings**:
     - Default RDP File: Choose a different RDP template file
     - Machine sharing options
     - Custom RDP configurations
   - **Application Settings**:
     - Status Refresh Interval: Control check frequency
     - Data Directory: Change storage location
     - Theme preferences
   - **User Preferences**:
     - Display options
     - Behavior settings
   - **Import/Export**:
     - Settings backup/restore
     - Machine list management
     - Shared configurations

### Changing Default RDP File
To change the default RDP configuration:

1. Open Settings
2. Navigate to Machine Settings
3. Click "Change Default RDP File"
4. Browse to select your new RDP template file
5. Click OK to save

*Note: This affects new connections only. Existing machine-specific RDP settings are preserved.*

### Adjusting Status Refresh
To modify how often machine status is checked:

1. Open Settings
2. Go to Application Settings
3. Find the "Status Refresh Interval" setting
4. Enter your preferred interval in seconds
5. Click Save

*Tip: A longer interval reduces network traffic but makes status updates less frequent.*
""",
            # Chunk 9: Sharing
            """## Sharing Machines

### Exporting Machine Configurations
To share machine settings with others:

![Share Machine](images/share-machine.png)

1. Right-click the machine you want to share
2. Select "Share Machine Configuration"
3. Choose which settings to include:
   - RDP configuration
   - Machine description
   - Custom paths
4. Click "Export" and choose save location

### Importing Shared Machines
To import shared machine configurations:

![Import Machine](images/import-machine.png)

1. Open Settings
2. Go to Import/Export section
3. Click "Import Shared Configuration"
4. Browse to the shared configuration file
5. Review and confirm the import

*Note: Imported settings will not override existing machines unless specified.*

### Managing Shared Configurations
To manage your shared machines:

1. Open Settings
2. Navigate to Import/Export
3. View shared configuration history
4. Remove old shared configurations
5. Update sharing preferences
""",
            # Chunk 10: Tips and Troubleshooting
            """## Tips and Tricks

### Status Monitoring
- Green indicator: Machine is available
- Red indicator: Machine is unavailable
- Last used time updates automatically

### Keyboard Shortcuts
- `Enter` in single machine field to quickly add
- Right-click for context menu
- Mouse wheel to scroll through machines
- `Ctrl+S` to quickly share selected machine
- `Ctrl+I` to import configurations
- `Ctrl+E` to export settings

### Best Practices
1. Use descriptive names for machines
2. Add descriptions for better organization
3. Regular exports for backup
4. Customize RDP settings for specific needs
5. Share configurations with team members
6. Keep shared configurations organized
7. Review and update machine settings periodically

### Troubleshooting Common Issues
1. **Connection Problems**
   - Verify machine name
   - Check network connectivity
   - Confirm RDP port access

2. **Sharing Issues**
   - Verify file permissions
   - Check configuration completeness
   - Ensure compatible settings

3. **Settings Issues**
   - Clear application cache
   - Verify write permissions
   - Check available disk space

*For additional support, consult the full documentation or contact support.*
"""
        ]
        
        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(chunk)
                f.flush()
                print(f"Chunk {i} written")
        
        print("\nGuide created successfully!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    create_guide()