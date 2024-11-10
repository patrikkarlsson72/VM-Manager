import os

def create_guide():
    try:
        # Get file path
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
- [Connecting to Machines](#connecting-to-machines)
- [Managing Machines](#managing-machines)
- [Customizing Settings](#customizing-settings)
""",
            # Chunk 2: Initial Setup
            """## Initial Setup

### First Launch
When you first launch VM Manager, you'll be prompted to select a default RDP file:

![Initial Setup](images/initial-setup.png)

1. Click "OK" on the prompt
2. Browse to select your default RDP file
3. The application will create necessary folders automatically
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
            # Chunk 4: Connecting
            """## Connecting to Machines

### Basic Connection
To connect to a machine:

![Connect to Machine](images/connect.png)

1. Click on any machine tile
2. The RDP connection will launch automatically
3. Status indicator shows if machine is available (green) or unavailable (red)
""",
            # Chunk 5: Managing
            """## Managing Machines

### Context Menu Options
Right-click any machine to access management options:

![Context Menu](images/context-menu.png)

1. Add/Edit Description
2. Set Custom RDP Path
3. Delete Machine

### Adding Descriptions
To add a description:

![Add Description](images/add-description.png)

1. Right-click the machine
2. Select "Add or Edit Description"
3. Enter your description
4. Click OK
""",
            # Chunk 6: Settings
            """## Customizing Settings

### Settings Panel
![Settings Panel](images/settings-panel.png)

Access application settings:

![Settings Panel Button](images/settings-panel-button.png)

1. Click the Settings button in the sidebar
2. Adjust various options:
   - **Default RDP File**: Choose a different RDP template file for new connections
   - **Status Refresh Interval**: Control how frequently machine status is checked (in seconds)
   - **Data Directory**: Change where VM Manager stores its data
   - **Import/Export**: Backup or restore your settings and machine list

### Changing Default RDP File
To change the default RDP configuration:

1. Open Settings
2. Click "Change Default RDP File"
3. Browse to select your new RDP template file
4. Click OK to save

*Note: This affects new connections only. Existing machine-specific RDP settings are preserved.*

### Adjusting Status Refresh
To modify how often machine status is checked:

1. Open Settings
2. Find the "Status Refresh Interval" setting
3. Enter your preferred interval in seconds
4. Click Save

*Tip: A longer interval reduces network traffic but makes status updates less frequent.*
""",
            # Chunk 7: Tips
            """## Tips and Tricks

### Status Monitoring
- Green indicator: Machine is available
- Red indicator: Machine is unavailable
- Last used time updates automatically

### Keyboard Shortcuts
- `Enter` in single machine field to quickly add
- Right-click for context menu
- Mouse wheel to scroll through machines

### Best Practices
1. Use descriptive names for machines
2. Add descriptions for better organization
3. Regular exports for backup
4. Customize RDP settings for specific needs
"""
        ]
        
        # Write chunks to file
        with open(md_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(chunk)
                f.flush()  # Ensure content is written
                print(f"Chunk {i} written")
                
        # Verify each chunk
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("\nVerifying content:")
            print(f"Total characters: {len(content)}")
            print(f"Total lines: {len(content.splitlines())}")
            
        print("\nGuide created successfully!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    create_guide()