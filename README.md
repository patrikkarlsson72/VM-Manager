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

## Usage

### Adding Machines
- Single machine: Enter machine name in the left sidebar
- Multiple machines: Use the text area in the sidebar for batch input

### Connecting to Machines
- Click on a machine tile to connect via RDP
- Right-click for additional options:
  - Add/Edit Description
  - Set Custom RDP Path
  - Delete Machine

### Settings
Access settings through the gear icon to configure:
- Default RDP file path
- Data directory location
- Theme preferences
- Status refresh interval
- Import/Export settings

## Customization

### Themes
- Built-in themes: Dark, Light, Blue Dark, Blue Light
- Customizable colors for:
  - Primary Background
  - Secondary Background
  - Buttons
  - Text
  - Borders

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

- 1.0.0
  - Initial release
  - Basic VM management features
  - Theme support
  - Settings import/export