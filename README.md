# VM Manager

<p align="center">
  <img src="docs/images/vm_logo.png" alt="VM Manager Logo" width="200"/>
</p>

A desktop application for managing and connecting to virtual machines, built with Python and Tkinter.

## Features

- Easy connection to virtual machines via RDP
- Enhanced category system with:
  - Visual category indicators on machine tiles
  - Color-coded categories with customizable colors
  - Category selection with checkmark indicators
  - Hover effects for better interaction
  - Category renaming capability
  - Drag-and-drop category reordering
- Machine categorization and tagging system
- Dark and light theme support
- Drag-and-drop tag functionality
- Machine status monitoring
- Custom RDP file configuration
- Import/Export settings
- Machine descriptions and last-used tracking

## Core Components

- **Machine Management**: Add, remove, and organize virtual machines
- **Enhanced Category System**: 
  - Color-coded grouping with visual indicators
  - Interactive category buttons with hover effects
  - Category renaming and color customization
  - Toggle selection with checkmarks
  - Intuitive drag-and-drop reordering
- **Tag System**: Flexible tagging system for better organization
- **Theme Support**: Multiple theme options including dark and light modes
- **Settings Management**: Configurable RDP settings and data directory
- **Status Monitoring**: Real-time machine status checks

## Technical Details

- Built with Python 3.11+
- Uses Tkinter for the GUI
- Supports Windows OS (RDP functionality)
- Data stored locally in user's AppData directory

## Installation

1. Ensure Python 3.11 or higher is installed
2. Clone the repository
3. Install required dependencies
4. Run `VMmanagerpython.py`

## Usage

- Add machines using the "Add PC" button
- Organize machines using categories and tags
- Right-click machines for additional options
- Use the sidebar for filtering and organization
- Access settings via the gear icon

## Configuration

- Default RDP file location can be set in Settings
- Data directory can be changed via Settings
- Multiple theme options available
- Customizable refresh intervals

## Development

- Written in Python
- Modular architecture for easy maintenance
- Follows DRY principles
- Includes comprehensive error handling

## License

[Your License Information Here]