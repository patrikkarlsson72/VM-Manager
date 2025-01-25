# VM Manager

<p align="center">
  <img src="docs/images/vm_logo.png" alt="VM Manager Logo" width="200"/>
</p>

A desktop application for managing and connecting to virtual machines, built with Python and Tkinter.

## Features

- Easy connection to virtual machines via RDP
- Enhanced category system with:
  - Visual category indicators (colored diamonds)
  - Color-coded categories with customizable colors
  - Category selection with checkmark indicators
  - Hover effects for better interaction
  - Category renaming capability
  - Drag-and-drop category reordering
- Machine categorization and tagging system
- Dark and light theme support
- Drag-and-drop tag functionality
- Machine status monitoring (online/offline)
- Custom RDP file configuration
- Import/Export settings
- Machine descriptions and last-used tracking
- DNS cache management for connection issues

## Core Components

- **Machine Management**: Add, remove, and organize virtual machines
- **Enhanced Category System**: 
  - Color-coded grouping with diamond indicators
  - Interactive category buttons with hover effects
  - Category renaming and color customization
  - Toggle selection with checkmarks
  - Intuitive drag-and-drop reordering
- **Tag System**: Flexible tagging system with drag-and-drop support
- **Theme Support**: Dark and light mode options
- **Settings Management**: Configurable RDP settings and data directory
- **Status Monitoring**: Real-time machine status checks with visual indicators

## Technical Details

- Built with Python 3.11+
- Uses Tkinter for the GUI
- Supports Windows OS (RDP functionality)
- Data stored locally in user's AppData directory
- Modular architecture for easy maintenance

## Installation

1. Ensure Python 3.11 or higher is installed
2. Clone the repository
3. Install required dependencies
4. Run `VMmanagerpython.py`

## Usage

- Add machines using the "Add Single PC" or "Add Multiple PCs" options
- Organize machines using categories and tags
- Right-click machines for additional options
- Use the sidebar for filtering and organization
- Access settings via the gear icon
- Clear DNS cache when experiencing connection issues

## Configuration

- Default RDP file location can be set in Settings
- Data directory can be changed via Settings
- Dark/Light theme selection
- Customizable category colors
- Customizable refresh intervals
- Flexible tag management system

## Development

- Written in Python with Tkinter
- Modular architecture for easy maintenance
- Follows DRY principles
- Includes comprehensive error handling
- Regular updates and improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.