import tkinter as tk

class MenuStyle:
    MENU_STYLE = {
        'font': ('Segoe UI', 10),
        'bg': '#FFFFFF',
        'fg': '#2c3e50',
        'activebackground': '#f1f3f5',
        'activeforeground': '#2c3e50',
        'relief': tk.SOLID,
        'borderwidth': 1,
        'selectcolor': '#0366d6'
    }
    
    MENU_ITEM_STYLE = {
        'font': ('Segoe UI', 10),
        'compound': tk.LEFT,
        'padx': 15,
        'pady': 8,
        'activeforeground': '#0366d6'
    }
    
    DELETE_ITEM_STYLE = {
        'font': ('Segoe UI', 10, 'bold'),
        'foreground': '#dc3545',
        'compound': tk.LEFT,
        'padx': 15,
        'pady': 8
    }

    @staticmethod
    def get_themed_menu_style(theme):
        """Get menu style based on current theme"""
        if theme in ["dark", "blue_dark"]:
            return {
                'font': ('Segoe UI', 11),
                'bg': '#133951',
                'fg': '#FFFFFF',
                'activebackground': '#274156',
                'activeforeground': '#D1B278',
                'relief': tk.SOLID,
                'borderwidth': 1,
                'selectcolor': '#D1B278'
            }
        else:
            return {
                'font': ('Segoe UI', 11),
                'bg': '#F0F7FF',
                'fg': '#2B4B6F',
                'activebackground': '#CCE8FF',
                'activeforeground': '#1a365d',
                'relief': tk.SOLID,
                'borderwidth': 1,
                'selectcolor': '#7AB8E0'
            }