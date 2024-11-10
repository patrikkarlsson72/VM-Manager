import PyInstaller.__main__
import os
import sys

# Get the absolute path to the source directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

PyInstaller.__main__.run([
    'src/VMmanagerpython.py',
    '--name=VMManager',
    '--onefile',
    '--windowed',
    f'--icon={os.path.join(resources_path, "icon.ico")}',
    '--add-data=resources/icon.ico;resources',
    '--clean',
    '--noconfirm',
    '--uac-admin',  # Request admin privileges
    '--version-file=version.txt',
])