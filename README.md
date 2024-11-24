# VM Manager

VM Manager is a desktop application that helps manage and connect to virtual machines through RDP (Remote Desktop Protocol). It provides an intuitive interface for organizing, monitoring, and accessing your virtual machines.

## Features

- **Easy VM Management**: Quick access to all your virtual machines in one place
- **Status Monitoring**: Real-time status checking of VM availability
- **Custom RDP Configurations**: Support for machine-specific RDP settings
- **Machine Descriptions**: Add descriptions to keep track of VM purposes
- **Last Used Tracking**: Automatically tracks when VMs were last accessed
- **Theme Support**: Light and dark themes with customizable colors
- **Data Export/Import**: Export and import settings and machine lists
- **Customizable Settings**: Flexible configuration options for various preferences
- **Machine Sharing**: Share machine configurations with other users
- **Organized Settings**: Categorized settings for better organization and access
- **Category Management**: Organize machines into customizable categories
- **Category Filtering**: Quick filtering by category
- **Visual Organization**: Color-coding for categories
- **Machine Tagging**: Add custom tags to machines for flexible organization
- **Tag Search**: Quick search through tagged machines

## Installation

### Using the Installer (Recommended)
1. Download the latest VMManager.msi from the releases page
2. Run the installer and follow the installation wizard
3. Launch VM Manager from the Start Menu or Desktop shortcut

### Manual Installation
1. Clone the repository: 
git clone https://github.com/patrikkarlsson72/VM-Manager.git

2. Install required dependencies:

pip install -r requirements.txt

3. Run the application:

python src/VMmanagerpython.py


## System Requirements

- Windows 11 23H2 or later
- Python 3.11+ (for manual installation)
- Administrative privileges (for installation)
- RDP client (mstsc.exe) installed

## Configuration

### First-Time Setup
1. On first launch, you'll be prompted to select a default RDP file
2. The application will create necessary folders in your AppData directory
3. You can start adding virtual machines through the interface

### Data Directory
- Default location: `%LOCALAPPDATA%\VmManager`
- Contains all configuration files and machine data
- Can be changed through Settings

### Categories
- Create custom categories to organize machines
- Assign colors for visual distinction
- Support for nested categories
- Multiple category assignments per machine
- Category-based filtering and sorting

### Tags
- Add multiple tags to each machine
- Flexible tag-based filtering
- Tag combinations for advanced filtering


## Usage

### Adding Machines
- Single machine: Enter machine name in the left sidebar
- Multiple machines: Use the text area in the sidebar for batch input

### Managing Categories
To organize your machines into categories:

![Categories](images/categories.png)

1. Click "Manage Categories" in the sidebar
2. Add a new category:
   - Click "Add Category"
   - Enter category name
   - Choose category color (optional)
   - Click Save
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

### Managing Tags
To use the tagging system:

![Tags](images/tags.png)

1. Add tags to machines:
   - Right-click any machine
   - Select "Manage Tags"
   - Add new tags or select existing ones
   - Click Save or hit enter

2. Filter by tags:
   - Use the tag filter in the sidebar
   - Select multiple tags for combined filtering
   - Use tag search to find specific tags
   - Clear filters to show all machines

### Tag Organization Tips
1. Use consistent naming conventions
2. Combine with categories for advanced organization
3. Regular tag cleanup and management

### Tag Search and Filtering
- Quick search through tagged machines
- Filter by single or multiple tags
- Combine tag and category filters

### Connecting to Machines
- Click on a machine tile to connect via RDP
- Right-click for additional options:
  - Add/Edit Description
  - Set Custom RDP Path
  - Delete Machine

### Settings
Access settings through the gear icon to configure:
- Machine Settings:
  - Default RDP file path
  - Machine sharing options
  - Custom RDP configurations
- Application Settings:
  - Data directory location
  - Theme preferences
  - Status refresh interval
- User Preferences:
  - Display options
  - Behavior settings
- Import/Export:
  - Settings backup/restore
  - Machine list management
  - Shared configurations

### Machine Sharing
- Share machine configurations with team members
- Export specific machine settings
- Import shared machine configurations
- Control which settings are shared:
  - RDP configurations
  - Machine descriptions
  - Custom paths

## Customization

### Application Settings
- **Default RDP File**: Change the default RDP configuration file used for connections
- **Refresh Interval**: Adjust how often machine status checks are performed
- **Data Directory**: Manage where application data is stored
- **Import/Export**: Backup and restore your settings and machine list

### Themes
- Two built-in themes:
  - Light: Optimized for daytime use
  - Dark: Easier on the eyes in low-light conditions
- Theme selection persists between sessions
- Switch easily using the theme toggle (☀️/🌙) in the header

### Machine-Specific Settings
- Custom RDP configurations per machine
- Individual descriptions
- Status tracking

## Troubleshooting

### Common Issues
1. **Connection Failed**
   - Verify machine name is correct
   - Check network connectivity
   - Ensure RDP port (3389) is accessible

2. **Settings Not Saving**
   - Check write permissions in data directory
   - Verify disk space availability

3. **UI Issues**
   - Try resetting to default theme
   - Restart application

### Error Logs
- Check Windows Event Viewer for application errors
- Data directory contains operation logs

## Building from Source

### Prerequisites
- Python 3.11+
- PyInstaller
- InstallShield (for MSI creation)

### Build Steps
1. Install build requirements:

pip install pyinstaller


2. Run build script:


python build_scripts/setup.py


3. Find executable in `dist` directory

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## Acknowledgments

- Thanks to all contributors
- Built with Python and Tkinter
- Packaged with InstallShield

## Version History

- 1.2.0
  - Added machine sharing functionality
  - Implemented categorized settings
  - Enhanced settings management
- 1.1.0
  - Added custom RDP path support per machine
  - Enhanced machine-specific settings
  - Bug fixes and performance improvements
- 1.0.0
  - Initial release
  - Basic VM management features
  - Theme support
  - Settings import/export