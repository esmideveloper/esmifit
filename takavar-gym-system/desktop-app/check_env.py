import sys
import os

# Tkinter 대신 GTK4 임포트 확인
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, Gio, GLib, Pango, GObject
    GTK4_AVAILABLE = True
except (ImportError, ValueError) as e:
    GTK4_AVAILABLE = False
    print(f"GTK4 not available: {e}")

# PySide6 폴백
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
    from PySide6.QtCore import Qt
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

# Tkinter 폴백
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

print(f"GTK4: {GTK4_AVAILABLE}")
print(f"PySide6: {PYSIDE6_AVAILABLE}")
print(f"Tkinter: {TKINTER_AVAILABLE}")
