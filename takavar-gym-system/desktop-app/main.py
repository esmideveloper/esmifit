#!/usr/bin/env python3
"""
takavar Gym System - 데스크톱 애플리케이션 (GTK4 + libadwaita)
Ubuntu GNOME과 동일한 UI/UX를 제공하는 Windows 데스크톱 애플리케이션
"""

import sys
import os
import json
import datetime
import urllib.request
import urllib.error
import threading
import time

# ── Try GTK4 (Ubuntu GNOME style) ──
GTK4_AVAILABLE = False
PYQT6_AVAILABLE = False
TKINTER_AVAILABLE = False

try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, Gio, GLib, Pango, GObject, GtkSource
    GTK4_AVAILABLE = True
    print("[OK] GTK4 + libadwaita loaded (Ubuntu GNOME style)")
except Exception as e:
    print(f"[WARN] GTK4 not available: {e}")

# ═══════════════════════════════════════════════════════════════════
# 폴백: PyQt6
# ═══════════════════════════════════════════════════════════════════
if not GTK4_AVAILABLE:
    try:
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
            QLineEdit, QComboBox, QTextEdit, QTabWidget, QTabBar, QMenuBar,
            QMenu, QAction, QStatusBar, QSplitter, QFrame, QMessageBox,
            QScrollArea, QGridLayout, QGroupBox, QFormLayout, QDateEdit,
            QDoubleSpinBox, QSpinBox, QCheckBox, QRadioButton, QButtonGroup,
            QFileDialog, QSystemTrayIcon, QMenu as QMenuTray, QToolBar,
            QStackedWidget, QListWidget, QListWidgetItem, QProgressBar,
            QMessageBox, QInputDialog, QColorDialog, QFontDialog,
            QStyle, QStyleOption, QPainter, QPen, QBrush, QColor,
            QLinearGradient, QDockWidget, QMainWindow, QShortcut,
            QKeySequence, QToolButton, QSizePolicy, QSpacerItem, QWidgetAction,
        )
        from PySide6.QtCore import (
            Qt, QThread, Signal, Slot, QTimer, QDate, QSize, QPoint,
            QMargins, QRect, QFile, QTextStream, QPropertyAnimation,
            QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup,
        )
        from PySide6.QtGui import (
            QIcon, QPixmap, QFont, QFontDatabase, QPalette, QColor,
            QLinearGradient, QBrush, QPen, QImage, QPainter, QAction,
            QKeySequence, QToolTip, QFontMetrics, QResizeEvent,
            QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent,
        )
        PYQT6_AVAILABLE = True
        print("[OK] PySide6 (Qt6) loaded as fallback")
    except Exception as e:
        print(f"[WARN] PySide6 not available: {e}")

# ═══════════════════════════════════════════════════════════════════
# 폴백: Tkinter
# ═══════════════════════════════════════════════════════════════════
if not GTK4_AVAILABLE and not PYQT6_AVAILABLE:
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, scrolledtext, simpledialog, filedialog
        from tkinter import font as tkfont
        TKINTER_AVAILABLE = True
        print("[OK] Tkinter loaded as fallback")
    except Exception as e:
        print(f"[ERROR] No GUI framework available: {e}")
        sys.exit(1)


BACKEND_URL = "http://localhost:8000"
APP_NAME = "Takavar Gym System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Takavar Gym"
TOKEN = None
CURRENT_USER = None


# ═══════════════════════════════════════════════════════════════════
# API Helpers
# ═══════════════════════════════════════════════════════════════════
def api_request(method, endpoint, data=None, token=None):
    url = f"{BACKEND_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token or TOKEN:
        headers["Authorization"] = f"Bearer {token or TOKEN}"
    if data and method in ("POST", "PUT"):
        data = json.dumps(data).encode()
    else:
        data = None

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read())
        except:
            return {"error": str(e), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def api_get(endpoint, token=None):
    return api_request("GET", endpoint, token=token)

def api_post(endpoint, data=None, token=None):
    return api_request("POST", endpoint, data=data, token=token)

def api_put(endpoint, data=None, token=None):
    return api_request("PUT", endpoint, data=data, token=token)

def api_delete(endpoint, token=None):
    return api_request("DELETE", endpoint, token=token)


# ═══════════════════════════════════════════════════════════════════
# THEME / COLORS (Ubuntu GNOME style)
# ═══════════════════════════════════════════════════════════════════
UBUNTU_ORANGE = "#E95420"
UBUNTU_DARK_BG = "#2C003E"
UBUNTU_BG = "#300A4F"
UBUNTU_SURFACE = "#3D1A5C"
UBUNTU_FOREGROUND = "#FFFFFF"
UBUNTU_FOREGROUND_DIM = "#CCCCCC"
UBUNTU_ACCENT_GREEN = "#33D17A"
UBUNTU_ACCENT_BLUE = "#15AABF"
UBUNTU_ACCENT_YELLOW = "#F5C211"
UBUNTU_ACCENT_RED = "#FF5733"
UBUNTU_INACTIVE = "#5C3674"
UBUNTU_BORDER = "#4A2866"
UBUNTU_SHADOW = "rgba(0,0,0,0.3)"


def apply_ubuntu_theme(widget):
    """Ubuntu GNOME 스타일 테마 적용 (GTK4, Qt6, Tkinter 공통)"""
    pass  # 각 프레임워크별 구현


# ═══════════════════════════════════════════════════════════════════
# GTK4 THEME
# ═══════════════════════════════════════════════════════════════════
if GTK4_AVAILABLE:
    @Gtk.StyleProvider
    class UbuntuThemeProvider(Gtk.CssProvider):
        def __init__(self):
            super().__init__()

        def load_from_string(self, css_text):
            # GTK4 CSS 업체는 resources 시스템 사용
            pass


# ═══════════════════════════════════════════════════════════════════
# QT6 THEME
# ═══════════════════════════════════════════════════════════════════
if PYQT6_AVAILABLE:
    class UbuntuStyle:
        """Ubuntu GNOME 스타일 Qt6 테마"""
        @staticmethod
        def apply(app):
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#300A4F"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#3D1A5C"))
            palette.setColor(Q 팔레트.ColorRole.AlternateBase, QColor("#2C003E"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#E95420"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#E95420"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.BrightText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Link, QColor("#15AABF"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#33D17A"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.DisabledText, QColor("#777777"))
            palette.setColor(QPalette.ColorRole.Shadow, QColor("#1A001A"))

            # 버튼 호버 색상
            app.setPalette(palette)
            app.setStyle("Fusion")

            # 스타일 시트
            app.setStyleSheet("""
                QMainWindow { background-color: #300A4F; }
                QWidget { background-color: #300A4F; color: #FFFFFF; font-family: 'Ubuntu', 'Noto Sans', sans-serif; }
                QTabWidget::pane { background-color: #3D1A5C; border: 1px solid #4A2866; border-radius: 8px; }
                QTabBar::tab { background-color: #300A4F; color: #CCCCCC; padding: 10px 20px; margin-right: 2px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
                QTabBar::tab:selected { background-color: #E95420; color: #FFFFFF; font-weight: bold; }
                QTabBar::tab:hover:!selected { background-color: #4A2866; color: #FFFFFF; }
                QPushButton { background-color: #E95420; color: #FFFFFF; border: none; border-radius: 6px; padding: 8px 16px; font-weight: bold; }
                QPushButton:hover { background-color: #F06A30; }
                QPushButton:pressed { background-color: #D04818; }
                QPushButton:disabled { background-color: #5C3674; color: #777777; }
                QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 6px; padding: 6px 10px; }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 2px solid #E95420; }
                QComboBox::drop-down { border: none; }
                QComboBox::down-arrow { image: none; }
                QComboBox QAbstractItemView { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; selection-background-color: #E95420; }
                QTableWidget { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; gridline-color: #4A2866; }
                QTableWidget::item:selected { background-color: #E95420; color: #FFFFFF; }
                QTableWidget::item:hover { background-color: #4A2866; }
                QHeaderView::section { background-color: #2C003E; color: #FFFFFF; padding: 8px; border: none; border-bottom: 2px solid #E95420; }
                QLabel { color: #FFFFFF; }
                QGroupBox { border: 1px solid #4A2866; border-radius: 8px; margin-top: 12px; }
                QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #E95420; font-weight: bold; }
                QScrollArea { background-color: #300A4F; }
                QScrollBar:vertical { background-color: #300A4F; width: 10px; }
                QScrollBar::handle:vertical { background-color: #4A2866; border-radius: 5px; min-height: 20px; }
                QScrollBar::handle:vertical:hover { background-color: #E95420; }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
                QMenuBar { background-color: #2C003E; color: #FFFFFF; }
                QMenuBar::item { padding: 6px 20px; }
                QMenuBar::item:selected { background-color: #4A2866; }
                QMenu { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 6px; }
                QMenu::item { padding: 6px 20px; }
                QMenu::item:selected { background-color: #E95420; }
                QDockWidget { background-color: #3D1A5C; color: #FFFFFF; }
                QTabBar::tab:!selected { background-color: #300A4F; margin-top: 2px; }
                QHeaderView::section::horizontal { background-color: #2C003E; }
                QStatusBar { background-color: #2C003E; color: #CCCCCC; }
                QToolBar { background-color: #2C003E; spacing: 4px; padding: 4px; }
                QToolButton { background-color: transparent; color: #FFFFFF; border: none; padding: 6px; border-radius: 4px; }
                QToolButton:hover { background-color: #4A2866; }
                QToolButton:pressed { background-color: #E95420; }
                QProgressBar { background-color: #2C003E; border: 1px solid #4A2866; border-radius: 4px; text-align: center; }
                QProgressBar::chunk { background-color: #E95420; border-radius: 4px; }
                QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #4A2866; border-radius: 4px; background-color: #3D1A5C; }
                QCheckBox::indicator:checked { background-color: #E95420; }
                QRadioButton::indicator { width: 18px; height: 18px; border: 2px solid #4A2866; border-radius: 9px; background-color: #3D1A5C; }
                QRadioButton::indicator:checked { background-color: #E95420; border-color: #E95420; }
                QSplitter::handle { background-color: #4A2866; }
                QSplitter::handle:horizontal { width: 2px; }
                QSplitter::handle:vertical { height: 2px; }
                QHeaderView::down-arrow { image: none; }
                QHeaderView::up-arrow { image: none; }
                QDateEdit { padding: 4px; }
                QSpinBox, QDoubleSpinBox { padding: 4px; }
                QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { background-color: #4A2866; border: none; width: 16px; border-radius: 3px; }
                QSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover { background-color: #E95420; }
                QTabWidget::tab-bar { alignment: left; }
                QTabWidget::tab { margin-left: 0px; }
                QFrame { border: none; }
                QFrame[frameShape="Panel"] { border: 1px solid #4A2866; border-radius: 8px; }
                QMessageBox { background-color: #300A4F; }
                QMessageBox QLabel { color: #FFFFFF; }
                QMessageBox QPushButton { min-width: 80px; }
                QSystemTrayIcon { }
                QToolTip { background-color: #2C003E; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 4px; padding: 4px 8px; }
            """)


# ═══════════════════════════════════════════════════════════════════
# TKINTER THEME
# ═══════════════════════════════════════════════════════════════════
if TKINTER_AVAILABLE:
    class UbuntuStyleTk:
        """Ubuntu GNOME 스타일 Tkinter 테마"""
        @staticmethod
        def apply(root):
            # Ubuntu 폰트 설정
            ubuntu_font = ("Ubuntu", 10) if "Ubuntu" in tkfont.families() else ("Noto Sans", 10) if "Noto Sans" in tkfont.families() else ("Segoe UI", 10)
            root.option_add("*Font", ubuntu_font)
            root.option_add("*Background", "#300A4F")
            root.option_add("*Foreground", "#FFFFFF")
            root.option_add("*HighlightBackground", "#300A4F")
            root.option_add("*HighlightColor", "#E95420")
            root.option_add("*ActiveBackground", "#E95420")
            root.option_add("*ActiveForeground", "#FFFFFF")
            root.option_add("*SelectBackground", "#E95420")
            root.option_add("*SelectForeground", "#FFFFFF")

            style = ttk.Style()
            style.theme_use("clam")
            style.configure(".", background="#300A4F", foreground="#FFFFFF", fieldbackground="#3D1A5C", borderwidth=0)
            style.configure("TFrame", background="#300A4F")
            style.configure("TLabel", background="#300A4F", foreground="#FFFFFF")
            style.configure("TButton", background="#E95420", foreground="#FFFFFF", borderwidth=0, focusthickness=0, focuscolor="none")
            style.map("TButton", background=[("active", "#F06A30"), ("pressed", "#D04818")])
            style.configure("TLabelframe", background="#300A4F", foreground="#FFFFFF")
            style.configure("TLabelframe.Label", background="#300A4F", foreground="#E95420", font=(ubuntu_font[0], 10, "bold"))
            style.configure("TEntry", background="#3D1A5C", foreground="#FFFFFF", fieldbackground="#3D1A5C", borderwidth=1, bordercolor="#4A2866")
            style.map("TEntry", fieldbackground=[("focus", "#4A2866")])
            style.configure("TCombobox", background="#3D1A5C", foreground="#FFFFFF", fieldbackground="#3D1A5C", borderwidth=1, bordercolor="#4A2866")
            style.configure("TText", background="#3D1A5C", foreground="#FFFFFF", borderwidth=1, bordercolor="#4A2866")
            style.configure("Treeview", background="#3D1A5C", foreground="#FFFFFF", fieldbackground="#3D1A5C", borderwidth=1, bordercolor="#4A2866")
            style.configure("Treeview.Heading", background="#2C003E", foreground="#FFFFFF", font=(ubuntu_font[0], 10, "bold"))
            style.map("Treeview.Heading", background=[("active", "#4A2866")])
            style.configure("Treeview", rowheight=28)
            style.configure("Treeview", indentwidth=20)
            style.configure("Treeview", highlightthickness=0)
            style.configure("Treeview", selectbackground="#E95420", selectforeground="#FFFFFF")
            style.configure("Treeview", insertcolor="#E95420")
            style.configure("Horizontal.TProgressbar", background="#E95420", troughcolor="#2C003E", bordercolor="#4A2866")
            style.configure("TNotebook", background="#300A4F")
            style.configure("TNotebook.Tab", background="#300A4F", foreground="#CCCCCC", padding=[10, 5])
            style.map("TNotebook.Tab", background=[("selected", "#E95420"), ("active", "#4A2866")], foreground=[("selected", "#FFFFFF")])
            style.configure("TCheckbutton", background="#300A4F", foreground="#FFFFFF")
            style.configure("TRadiobutton", background="#300A4F", foreground="#FFFFFF")
            style.configure("TScrollbar", background="#300A4F", troughcolor="#2C003E", bordercolor="#4A2866")
            style.configure("TProgressbar", background="#E95420", troughcolor="#2C003E")
            style.configure("TSizeGrip", background="#300A4F")


# ═══════════════════════════════════════════════════════════════════
# GTK4 데스크톱 앱
# ═══════════════════════════════════════════════════════════════════
if GTK4_AVAILABLE:
    class MainWindow(Gtk.ApplicationWindow):
        """메인 윈도우 (GTK4 + libadwaita - Ubuntu GNOME 스타일)"""

        def __init__(self, app):
            super().__init__(application=app, title=f"{APP_NAME} v{APP_VERSION}")
            self.set_default_size(1400, 900)
            self.set_size_request(1200, 700)

            # 헤더바
            self.header_bar = Adw.HeaderBar()
            self.header_bar.set_title_widget(Gtk.Label(label=APP_NAME, hexpand=True, justification=Gtk.Justification.CENTER))
            self.set_titlebar(self.header_bar)

            # 설정 버튼
            settings_btn = Gtk.Button(image=gio_theme_icon("settings"), valign=Gtk.Align.CENTER)
            settings_btn.set_tooltip_text("تنظیمات")
            settings_btn.connect("clicked", self.on_settings)
            self.header_bar.pack_end(settings_btn)

            # 로그인 상태 표시
            self.login_status = Gtk.Label(label="로그인이 필요합니다", halign=Gtk.Align.START)
            self.login_status.set_css_classes(["dim-label"])
            self.header_bar.pack_start(self.login_status)

            # 콘텐츠
            self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True)
            self.set_child(self.content)

            # 로그인 화면
            self.login_view = self.create_login_view()
            self.content.append(self.login_view)

            # 메인 화면 (초기 숨김)
            self.main_view = None
            self.login_view.set_visible(True)
            if self.main_view:
                self.main_view.set_visible(False)

            self.login_view.connect("login-success", self.on_login_success)
            self.login_view.connect("register-click", self.on_show_register)

        def create_login_view(self):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True, margin=40)
            box.set_css_classes(["login-box"])

            # 로고 영역
            logo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=False, margin_bottom=40)
            logo_label = Gtk.Label(label="🏋️ تکاور")
            logo_label.set_markup("<span size='xx-large' weight='bold'>تکاور</span>\n<span size='large' color='#E95420'>سیستم مدیریت باشگاه بدنسازی</span>")
            logo_label.set_halign(Gtk.Align.CENTER)
            logo_box.append(logo_label)

            # 로그인 폼
            form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=False)
            form_box.set_css_classes(["login-form"])
            form_box.set_margin_bottom(20)

            username_entry = Gtk.Entry(placeholder_text="نام کاربری", hexpand=True)
            username_entry.set_css_classes(["login-input"])
            username_entry.set_margin_bottom(12)

            password_entry = Gtk.Entry(placeholder_text="رمز عبور", hexpand=True, visibility=False)
            password_entry.set_css_classes(["login-input"])
            password_entry.set_margin_bottom(20)

            login_btn = Gtk.Button(label="ورود به سیستم", hexpand=True, valign=Gtk.Align.CENTER)
            login_btn.set_css_classes(["login-btn"])
            login_btn.set_margin_bottom(10)

            register_btn = Gtk.Button(label="ثبت‌نام / ورود به عنوان کاربر جدید", hexpand=True, valign=Gtk.Align.CENTER)
            register_btn.set_css_classes(["register-btn"])

            # 에러 메시지
            error_label = Gtk.Label(label="", hexpand=True, halign=Gtk.Align.CENTER)
            error_label.set_css_classes(["error-label"])
            error_label.set_markup = ""

            login_btn.connect("clicked", lambda w: self.do_login(username_entry, password_entry, error_label))
            register_btn.connect("clicked", lambda w: self.emit("register-click"))

            form_box.append(username_entry)
            form_box.append(password_entry)
            form_box.append(login_btn)
            form_box.append(register_btn)
            form_box.append(error_label)

            box.append(logo_box)
            box.append(form_box)

            box.username_entry = username_entry
            box.password_entry = password_entry
            box.error_label = error_label
            return box

        def do_login(self, username_entry, password_entry, error_label):
            username = username_entry.get_text().strip()
            password = password_entry.get_text()

            if not username or not password:
                error_label.set_text("لطفاً نام کاربری و رمز عبور را وارد کنید")
                return

            result = api_post("/api/auth/login", {"username": username, "password": password})

            if "access_token" in result:
                global TOKEN, CURRENT_USER
                TOKEN = result["access_token"]
                CURRENT_USER = result["user"]
                error_label.set_text("")
                self.emit("login-success")
            else:
                error_label.set_text(f"⚠ {result.get('detail', result.get('error', 'خطا در ورود'))}")

        def on_login_success(self, widget):
            self.login_view.set_visible(False)
            if not self.main_view:
                self.main_view = self.create_main_view()
            self.main_view.set_visible(True)
            self.content.append(self.main_view)
            self.login_status.set_text(f"خوش آمدید، {CURRENT_USER.get('first_name', 'کاربر')}")

        def create_main_view(self):
            # Adw.NavigationSplitView 사용 (사이드바 + 콘텐츠)
            split_view = Adw.NavigationSplitView()
            split_view.set_policy(Adw.NavigationSplitViewPolicy.ALWAYS)

            # 사이드바
            sidebar = Adw.NavigationPage()
            sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True)

            # 사이드바 헤더
            sidebar_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, vexpand=False, margin_bottom=10)
            sidebar_logo = Gtk.Label(label="تکاور", hexpand=True, halign=Gtk.Align.START)
            sidebar_logo.set_markup("<span font='24' weight='bold' color='#E95420'>تکاور</span>")
            sidebar_header.append(sidebar_logo)
            sidebar_box.append(sidebar_header)

            # 메뉴 항목들
            menu_items = [
                ("🏠", "Dashboard", "dashboard", "پنجره اصلی"),
                ("👥", "اعضا", "members", "مدیریت اعضا"),
                ("📋", "عضویت‌ها", "subscriptions", "مدیریت عضویت‌ها"),
                ("💰", "پرداخت‌ها", "payments", "مدیریت پرداخت‌ها"),
                ("📅", "تأدیه", "attendance", "ثبت حضور و غیبت"),
                ("🏋️", "تمرینات", "workouts", "مدیریت تمرینات"),
                ("⏰", "زمان‌بندی", "schedule", "زمان‌بندی کلاس‌ها"),
                ("👨‍🏫", "کارشناسان", "trainers", "مدیریت کارشناسان"),
                ("🏗️", "تجهیزات", "equipment", "مدیریت تجهیزات"),
                ("🍎", "تغذیه", "nutrition", "برنامه‌های تغذیه‌ای"),
                ("📦", "فروشگاه", "products", "مدیریت فروشگاه"),
                ("📊", "گزارشات", "reports", "گزارشات و تحلیل‌ها"),
            ]

            # 대시보드 button 먼저
            for icon, title, page_id, tooltip in menu_items:
                btn = Adw.ButtonRow(title=title, subtitle=tooltip)
                btn.set_icon_name(icon if icon else None)

                # SVG 아이콘 대신 텍스트 아이콘 사용
                icon_label = Gtk.Label(label=icon, hexpand=False, valign=Gtk.Align.CENTER)
                icon_label.set_size_request(32, 32)
                btn.prepend(icon_label)

                btn.connect("clicked", lambda w, pid=page_id: self.navigate_to_page(pid))
                sidebar_box.append(btn)

            # 로그아웃 section
            logout_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, vexpand=False, margin_top=20)
            logout_btn = Gtk.Button(label="خروج از سیستم", valign=Gtk.Align.CENTER)
            logout_btn.set_css_classes(["logout-btn"])
            logout_btn.connect("clicked", self.on_logout)
            logout_box.append(logout_btn)
            sidebar_box.append(logout_box)

            sidebar.append(sidebar_box)
            split_view.set_sidebar(sidebar)

            # 초기 콘텐츠 페이지
            self.detail_stack = Gtk.Stack()
            self.detail_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
            self.detail_stack.set_transition_duration(200)

            dashboard_page = self.create_dashboard_page()
            self.detail_stack.add_titled(dashboard_page, "dashboard", "Dashboard")

            split_view.set_content(self.detail_stack)

            return split_view

        def navigate_to_page(self, page_id):
            # TODO: 페이지 전환 구현
            pass

        def on_logout(self, widget):
            global TOKEN, CURRENT_USER
            TOKEN = None
            CURRENT_USER = None
            if self.main_view:
                self.main_view.set_visible(False)
            self.login_view.set_visible(True)
            self.login_status.set_text("로그인이 필요합니다")

        def on_settings(self, widget):
            pass


    class LoginView(Gtk.Box):
        __gsignals__ = {
            "login-success": (GObject.SignalFlags.RUN_FIRST, None, ()),
            "register-click": (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

        def __init__(self):
            super().__init__(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True)


    class TakavarApp(Gtk.Application):
        def __init__(self):
            super().__init__(application_id="com.takavar.gym",
                             flags=Gio.ApplicationFlags.FLAGS_NONE)
            self.connect("activate", self.on_activate)
            self.connect("shutdown", self.on_shutdown)

        def on_activate(self, app):
            win = MainWindow(app)
            win.present()
            self.win = win

            # 로그인 모달 실행
            if not TOKEN:
                self.show_login_dialog(win)

        def show_login_dialog(self, parent):
            dialog = Gtk.Dialog(title="ورود به систему", parent=parent, flags=0)
            dialog.set_default_size(400, 300)

            content = dialog.get_content_area()

            form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True)
            form.set_margin(20)

            title_label = Gtk.Label(label="🏋️ Takavar Gym System")
            title_label.set_markup("<span size='xx-large' weight='bold'>تکاور</span>\n<span size='large'>سامانه مدیریت باشگاه بدنسازی</span>")
            title_label.set_halign(Gtk.Align.CENTER)
            form.append(title_label)

            username_entry = Gtk.Entry(placeholder_text="نام کاربری (پیش‌فرض: admin)", hexpand=True)
            username_entry.set_text("admin")
            form.append(username_entry)

            password_entry = Gtk.Entry(placeholder_text="رمز عبور (پیش‌فرض: admin123)", hexpand=True, visibility=False)
            password_entry.set_text("admin123")
            form.append(password_entry)

            error_label = Gtk.Label(label="", hexpand=True, halign=Gtk.Align.CENTER)
            error_label.set_css_classes(["label"])

            btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, halign=Gtk.Align.CENTER)
            login_btn = Gtk.Button(label="ورود", hexpand=True)
            login_btn.connect("clicked", lambda w: self.attempt_login(
                dialog, username_entry, password_entry, error_label
            ))
            btn_box.append(login_btn)
            form.append(btn_box)
            form.append(error_label)

            dialog.set_content_area(form)
            dialog.present()

        def attempt_login(self, dialog, username_entry, password_entry, error_label):
            username = username_entry.get_text().strip()
            password = password_entry.get_text()

            if not username or not password:
                error_label.set_text("لطفاً نام کاربری و رمز عبور را وارد کنید")
                return

            result = api_post("/api/auth/login", {"username": username, "password": password})

            if "access_token" in result:
                global TOKEN, CURRENT_USER
                TOKEN = result["access_token"]
                CURRENT_USER = result["user"]
                dialog.destroy()
                if self.win:
                    self.win.login_view.set_visible(False)
                    if not self.win.main_view:
                        self.win.main_view = self.win.create_main_view()
                    self.win.main_view.set_visible(True)
                    self.win.login_status.set_text(f"خوش آمدید، {CURRENT_USER.get('first_name', 'کاربر')}")
            else:
                error_label.set_text(f"⚠ {result.get('detail', result.get('error', 'خطا در ورود'))}")

        def on_shutdown(self, app):
            print("App shutting down...")


# ═══════════════════════════════════════════════════════════════════
# PyQt6 데스크톱 앱
# ═══════════════════════════════════════════════════════════════════
if PYQT6_AVAILABLE and not GTK4_AVAILABLE:
    class DashboardWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setup_ui()

        def setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(16)

            # 타이틀
            title = QLabel("🏋️ پنجره اصلی سیستم مدیریت باشگاه بدنسازی تکاور")
            title.setStyleSheet("font-size: 22px; font-weight: bold; color: #E95420; margin-bottom: 20px;")
            layout.addWidget(title)

            # 진영 카드 그리드
            stats_layout = QGridLayout()
            stats_layout.setSpacing(12)
            stats_layout.setContentsMargins(0, 0, 0, 0)

            stats = [
                ("👥", "تعداد اعضا", "0", "#33D17A"),
                ("📋", "عضویت‌های فعال", "0", "#15AABF"),
                ("💰", "درآمدهای시그니스", "0", "#F5C211"),
                ("👨‍🏫", "کارشناسان", "0", "#FF5733"),
                ("📅", "کلاس‌های امروز", "0", "#33D17A"),
                ("🏗️", "تجهیزات", "0", "#15AABF"),
            ]

            for i, (icon, label, value, color) in enumerate(stats):
                card = self.create_stat_card(icon, label, value, color)
                row = i // 3
                col = i % 3
                stats_layout.addWidget(card, row, col)

            layout.addLayout(stats_layout)

            # جدول آخرین اعضا
            section_title = QLabel("🔵 اخیرین اعضای ثبت‌نشده")
            section_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #15AABF; margin-top: 20px;")
            layout.addWidget(section_title)

            self.members_table = QTableWidget()
            self.members_table.setColumnCount(5)
            self.members_table.setHorizontalHeaderLabels(["ID", "نام", "تلفن", "پلن", "وضعیت"])
            self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.members_table.setStyleSheet("""
                QTableWidget { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 8px; }
                QTableWidget::item { padding: 8px; }
                QTableWidget::item:selected { background-color: #E95420; color: #FFFFFF; }
                QHeaderView::section { background-color: #2C003E; color: #FFFFFF; padding: 8px; border: none; border-bottom: 2px solid #E95420; }
            """)
            layout.addWidget(self.members_table)

            # تازه‌ها
            section_title2 = QLabel("📢 اخبار و اطلاعیه‌ها")
            section_title2.setStyleSheet("font-size: 16px; font-weight: bold; color: #F5C211; margin-top: 20px;")
            layout.addWidget(section_title2)

            news_label = QLabel("""
            ✓ سیستم مدیریت باشگاه بدنسازی تکاور با موفقیت راه‌اندازی شد
            ✓ می‌توانید از پنجره اصلی سیستم استفاده کنید
            ✓ برای راهنما به بخش راهنما مراجعه کنید
            """)
            news_label.setStyleSheet("color: #CCCCCC; font-size: 13px; line-height: 1.6;")
            news_label.setWordWrap(True)
            layout.addWidget(news_label)

        def create_stat_card(self, icon, label, value, color):
            card = QFrame()
            card.setFixedSize(200, 120)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #3D1A5C;
                    border: 1px solid #4A2866;
                    border-radius: 12px;
                    padding: 16px;
                }}
            """)

            layout = QVBoxLayout(card)
            layout.setContentsMargins(12, 12, 12, 12)
            layout.setSpacing(4)

            icon_label = QLabel(icon)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet(f"font-size: 32px;")
            layout.addWidget(icon_label)

            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
            layout.addWidget(value_label)

            label_lbl = QLabel(label)
            label_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_lbl.setStyleSheet("font-size: 12px; color: #CCCCCC;")
            layout.addWidget(label_lbl)

            return card

    class MembersWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setup_ui()

        def setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(16)

            title = QLabel("👥 مدیریت اعضا - باشگاه بدنسازی تکاور")
            title.setStyleSheet("font-size: 20px; font-weight: bold; color: #E95420;")
            layout.addWidget(title)

            # ابزارها
            toolbar = QHBoxLayout()
            toolbar.addWidget(QLabel("جستجو:"))
            self.search_bar = QLineEdit()
            self.search_bar.setPlaceholderText("نام، تلفن، ایمیل جستجو...")
            self.search_bar.setFixedHeight(36)
            toolbar.addWidget(self.search_bar, stretch=1)

            toolbar.addWidget(QLabel("  پلن:"))
            self.plan_filter = QComboBox()
            self.plan_filter.addItems(["همه پلن‌ها", "برونزی", "نقره‌ای", "طلایی", "VIP ویژه"])
            self.plan_filter.setFixedHeight(36)
            toolbar.addWidget(self.plan_filter)

            self.add_btn = QPushButton("➕ عضو جدید")
            self.add_btn.setFixedHeight(36)
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #E95420; color: white; border: none;
                    border-radius: 6px; padding: 0 16px; font-weight: bold;
                }
                QPushButton:hover { background-color: #F06A30; }
            """)
            toolbar.addWidget(self.add_btn)

            self.refresh_btn = QPushButton("🔄癲新")
            self.refresh_btn.setFixedHeight(36)
            self.refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; color: #15AABF; border: 1px solid #4A2866;
                    border-radius: 6px; padding: 0 16px; font-weight: bold;
                }
                QPushButton:hover { background-color: #4A2866; color: white; }
            """)
            toolbar.addWidget(self.refresh_btn)

            layout.addLayout(toolbar)

            # جدول
            self.table = QTableWidget()
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels(["ID", "نام", "نام خانوادگی", "تلفن", "ایمیل", "جنسیت", "پلن", "وضعیت", "تاریخ شروع"])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866;
                    border-radius: 8px; gridline-color: #4A2866;
                }
                QTableWidget::item { padding: 6px 8px; }
                QTableWidget::item:selected { background-color: #E95420; color: #FFFFFF; }
                QTableWidget::item:hover { background-color: #4A2866; }
                QHeaderView::section {
                    background-color: #2C003E; color: #FFFFFF; padding: 8px;
                    border: none; border-bottom: 2px solid #E95420;
                }
            """)
            layout.addWidget(self.table, stretch=1)

            # περιγραφή
            desc = QLabel("برای افزودن عضو جدید روی دکمه 'عضو جدید' کلیک کنید. برای ویرایش روی ردیف مورد نظر دوبار کلیک کنید.")
            desc.setStyleSheet("color: #777777; font-size: 12px;")
            layout.addWidget(desc)

            self.load_members()
            self.add_btn.clicked.connect(self.add_member)
            self.refresh_btn.clicked.connect(self.load_members)

        def load_members(self):
            self.table.setRowCount(0)
            result = api_get("/api/members")
            if "error" not in result:
                for i, m in enumerate(result):
                    self.table.insertRow(i)
                    self.table.setItem(i, 0, QTableWidgetItem(str(m.get("id", ""))))
                    self.table.setItem(i, 1, QTableWidgetItem(m.get("first_name", "")))
                    self.table.setItem(i, 2, QTableWidgetItem(m.get("last_name", "")))
                    self.table.setItem(i, 3, QTableWidgetItem(m.get("phone", "")))
                    self.table.setItem(i, 4, QTableWidgetItem(m.get("email", "")))
                    self.table.setItem(i, 5, QTableWidgetItem(m.get("gender", "نامشخص")))
                    self.table.setItem(i, 6, QTableWidgetItem(m.get("membership_type", "")))
                    status = m.get("status", "")
                    status_color = "#33D17A" if status == "active" else "#FF5733" if status == "suspended" else "#F5C211"
                    self.table.setItem(i, 7, QTableWidgetItem(f'<span style="color:{status_color}">● {status}</span>'))
                    self.table.setItem(i, 8, QTableWidgetItem(str(m.get("membership_start", ""))))

        def add_member(self):
            dialog = QDialog(self)
            dialog.setWindowTitle("ثبت عضو جدید")
            dialog.setFixedSize(500, 600)
            dialog.setStyleSheet("""
                QDialog { background-color: #300A4F; }
                QLabel { color: #FFFFFF; }
                QLineEdit, QTextEdit, QComboBox, QDateEdit { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 6px; padding: 6px 10px; }
                QPushButton { background-color: #E95420; color: white; border: none; border-radius: 6px; padding: 8px 20px; font-weight: bold; }
                QPushButton:hover { background-color: #F06A30; }
            """)

            layout = QVBoxLayout(dialog)
            layout.setSpacing(12)

            form = QFormLayout()
            form.setSpacing(10)
            form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

            first_name = QLineEdit()
            first_name.setPlaceholderText("نام")
            last_name = QLineEdit()
            last_name.setPlaceholderText("نام خانوادگی")
            national_id = QLineEdit()
            national_id.setPlaceholderText("کد ملی (اختیاری)")
            phone = QLineEdit()
            phone.setPlaceholderText("شماره تلفن")
            email = QLineEdit()
            email.setPlaceholderText("ایمیل")
            birth_date = QDateEdit()
            birth_date.setDisplayFormat("yyyy-MM-dd")
            gender_combo = QComboBox()
            gender_combo.addItems(["مذکر", "مونث", "سایر"])
            address = QTextEdit()
            address.setPlaceholderText("آدرس")
            address.setFixedHeight(60)
            membership_type = QComboBox()
            membership_type.addItems(["برونزی", "نقره‌ای", "طلایی", "VIP ویژه"])
            weight = QLineEdit()
            weight.setPlaceholderText("وزن (kg)")
            height = QLineEdit()
            height.setPlaceholderText("قد (cm)")

            form.addRow("نام:", first_name)
            form.addRow("نام خانوادگی:", last_name)
            form.addRow("کد ملی:", national_id)
            form.addRow("تلفن:", phone)
            form.addRow("ایمیل:", email)
            form.addRow("تاریخ تولد:", birth_date)
            form.addRow("جنسیت:", gender_combo)
            form.addRow("آدرس:", address)
            form.addRow("نوع پلن:", membership_type)
            form.addRow("وزن (kg):", weight)
            form.addRow("قد (cm):", height)

            layout.addLayout(form)

            btn_box = QHBoxLayout()
            btn_box.addStretch()
            cancel_btn = QPushButton("انصراف")
            cancel_btn.setStyleSheet("background-color: transparent; color: #777777; border: 1px solid #4A2866; border-radius: 6px; padding: 8px 20px;")
            save_btn = QPushButton("ثبت عضو")
            btn_box.addWidget(cancel_btn)
            btn_box.addWidget(save_btn)
            layout.addLayout(btn_box)

            def save():
                gender_map = {"مذکر": "male", "مونث": "female", "سایر": "other"}
                plan_map = {"برونزی": "bronze", "نقره‌ای": "silver", "طلایی": "gold", "VIP ویژه": "vip"}
                data = {
                    "first_name": first_name.text(),
                    "last_name": last_name.text(),
                    "national_id": national_id.text() or None,
                    "phone": phone.text() or None,
                    "email": email.text() or None,
                    "gender": gender_map.get(gender_combo.currentText(), None),
                    "address": address.toPlainText() or None,
                    "membership_type": plan_map.get(membership_type.currentText(), "bronze"),
                    "weight": float(weight.text()) if weight.text() else None,
                    "height": float(height.text()) if height.text() else None,
                }
                result = api_post("/api/members", data)
                if "error" not in result:
                    QMessageBox.information(dialog, "تأیید", "عضو با موفقیت ثبت شد!")
                    dialog.accept()
                    self.load_members()
                else:
                    QMessageBox.warning(dialog, "خطا", str(result.get("detail", "خطا در ثبت")))

            save_btn.clicked.connect(save)
            cancel_btn.clicked.connect(dialog.reject)

            dialog.exec()


    class TakavarQtApp(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
            self.setMinimumSize(1200, 800)
            self.resize(1400, 900)
            self.setup_ui()
            self.check_auth()

        def setup_ui(self):
            # 스타일 적용
            UbuntuStyle.apply(QApplication.instance())

            # 메뉴바
            menubar = self.menuBar()
            menubar.setStyleSheet("""
                QMenuBar { background-color: #2C003E; color: #FFFFFF; border-bottom: 2px solid #E95420; }
                QMenuBar::item { padding: 8px 20px; color: #FFFFFF; }
                QMenuBar::item:selected { background-color: #4A2866; }
                QMenu { background-color: #3D1A5C; color: #FFFFFF; border: 1px solid #4A2866; border-radius: 6px; }
                QMenu::item { padding: 8px 20px; }
                QMenu::item:selected { background-color: #E95420; color: #FFFFFF; }
            """)

            file_menu = menubar.addMenu("فایل")
            file_menu.addAction("تغییر نقشهчень دیتابیس...")
            file_menu.addAction("خروج")

            tools_menu = menubar.addMenu("ابزارها")
            tools_menu.addAction("تولید گزارش PDF")
            tools_menu.addAction("تولید کارت اعضا")
            tools_menu.addAction("همگام‌سازی dữ liệu")

            help_menu = menubar.addMenu("راهنما")
            help_menu.addAction("درباره programa")
            help_menu.addAction("مستندات")

            # ابزار 바에
            toolbar = QToolBar("ابزارها")
            toolbar.setStyleSheet("""
                QToolBar { background-color: #2C003E; spacing: 4px; padding: 4px; border-bottom: 1px solid #4A2866; }
                QToolButton { background-color: transparent; color: #FFFFFF; border: none; padding: 6px; border-radius: 4px; }
                QToolButton:hover { background-color: #4A2866; }
            """)
            toolbar.setIconSize(QSize(24, 24))
            self.addToolBar(toolbar)

            # Status bar
            self.statusBar().setStyleSheet("""
                QStatusBar { background-color: #2C003E; color: #CCCCCC; border-top: 1px solid #4A2866; }
            """)
            self.statusBar().showMessage("برای شروع وارد شوید")

            # 편의 메뉴
            self.dashboard_btn = QToolButton()
            self.dashboard_btn.setText("🏠 Dashboard")
            self.dashboard_btn.clicked.connect(lambda: self.navigate("dashboard"))
            toolbar.addWidget(self.dashboard_btn)

            toolbar.addSeparator()

            self.members_btn = QToolButton()
            self.members_btn.setText("👥 اعضا")
            self.members_btn.clicked.connect(lambda: self.navigate("members"))
            toolbar.addWidget(self.members_btn)

            self.subscriptions_btn = QToolButton()
            self.subscriptions_btn.setText("📋 عضویت‌ها")
            self.subscriptions_btn.clicked.connect(lambda: self.navigate("subscriptions"))
            toolbar.addWidget(self.subscriptions_btn)

            self.payments_btn = QToolButton()
            self.payments_btn.setText("💰 پرداخت‌ها")
            self.payments_btn.clicked.connect(lambda: self.navigate("payments"))
            toolbar.addWidget(self.payments_btn)

            toolbar.addSeparator()

            self.attendance_btn = QToolButton()
            self.attendance_btn.setText("📅 حضور و غیبت")
            self.attendance_btn.clicked.connect(lambda: self.navigate("attendance"))
            toolbar.addWidget(self.attendance_btn)

            self.workouts_btn = QToolButton()
            self.workouts_btn.setText("🏋️ تمرینات")
            self.workouts_btn.clicked.connect(lambda: self.navigate("workouts"))
            toolbar.addWidget(self.workouts_btn)

            toolbar.addSeparator()

            self.schedule_btn = QToolButton()
            self.schedule_btn.setText("⏰ زمان‌بندی")
            self.schedule_btn.clicked.connect(lambda: self.navigate("schedule"))
            toolbar.addWidget(self.schedule_btn)

            self.trainers_btn = QToolButton()
            self.trainers_btn.setText("👨‍🏫 کارشناسان")
            self.trainers_btn.clicked.connect(lambda: self.navigate("trainers"))
            toolbar.addWidget(self.trainers_btn)

            self.equipment_btn = QToolButton()
            self.equipment_btn.setText("🏗️ تجهیزات")
            self.equipment_btn.clicked.connect(lambda: self.navigate("equipment"))
            toolbar.addWidget(self.equipment_btn)

            toolbar.addSeparator()

            self.reports_btn = QToolButton()
            self.reports_btn.setText("📊 گزارشات")
            self.reports_btn.clicked.connect(lambda: self.navigate("reports"))
            toolbar.addWidget(self.reports_btn)

            # محتوا (StackedWidget)
            self.stack = QStackedWidget()
            self.setCentralWidget(self.stack)

            # صفحات
            self.dashboard_page = DashboardWidget()
            self.stack.addWidget(self.dashboard_page)

            self.members_page = MembersWidget()
            self.stack.addWidget(self.members_page)

            # 기본 페이지
            self.stack.setCurrentIndex(0)

        def check_auth(self):
            result = api_get("/api/auth/me")
            if "error" in result:
                self.show_login_overlay()
            else:
                global CURRENT_USER
                CURRENT_USER = result
                self.title=f"{APP_NAME} - {result.get('first_name', 'کاربر')}"
                self.statusBar().showMessage(f"خوش آمدید، {result.get('first_name', 'کاربر')} | نقش: {result.get('role', '')}")

        def show_login_overlay(self):
            overlay = QWidget(self)
            overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            overlay.setStyleSheet("""
                QWidget { background-color: rgba(48, 10, 79, 0.97); }
            """)
            overlay.setFixedSize(self.width(), self.height())
            overlay.move(0, 0)

            layout = QVBoxLayout(overlay)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(40, 40, 40, 40)

            logo = QLabel("🏋️ تکاور")
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo.setStyleSheet("""
                QLabel {
                    font-size: 36px; font-weight: bold; color: #E95420;
                }
            """)
            layout.addWidget(logo)

            subtitle = QLabel("سیستم مدیریت باشگاه بدنسازی")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle.setStyleSheet("font-size: 16px; color: #CCCCCC; margin-bottom: 30px;")
            layout.addWidget(subtitle)

            form = QFormLayout()
            form.setSpacing(12)

            self.login_username = QLineEdit()
            self.login_username.setPlaceholderText("نام کاربری")
            self.login_username.setFixedHeight(40)
            self.login_username.setText("admin")

            self.login_password = QLineEdit()
            self.login_password.setPlaceholderText("رمز عبور")
            self.login_password.setFixedHeight(40)
            self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.login_password.setText("admin123")

            form.addRow("نام کاربری:", self.login_username)
            form.addRow("رمز عبور:", self.login_password)

            layout.addLayout(form)

            error_label = QLabel("")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: #FF5733; font-weight: bold; margin-top: 10px;")
            layout.addWidget(error_label)

            btn_box = QHBoxLayout()
            btn_box.addStretch()

            login_btn = QPushButton("ورود به سیستم")
            login_btn.setFixedSize(150, 40)
            login_btn.clicked.connect(lambda: self.attempt_login(overlay, error_label))
            btn_box.addWidget(login_btn)

            layout.addLayout(btn_box)
            layout.addStretch()

            overlay.show()

        def attempt_login(self, overlay, error_label):
            result = api_post("/api/auth/login", {
                "username": self.login_username.text(),
                "password": self.login_password.text(),
            })
            if "access_token" in result:
                global TOKEN, CURRENT_USER
                TOKEN = result["access_token"]
                CURRENT_USER = result["user"]
                self.setWindowTitle(f"{APP_NAME} - {result['user'].get('first_name', 'کاربر')}")
                self.statusBar().showMessage(f"خوش آمدید، {result['user'].get('first_name', 'کاربر')} | نقش: {result['user'].get('role', '')}")
                overlay.deleteLater()
            else:
                error_label.setText(f"⚠ {result.get('detail', result.get('error', 'خطا در ورود'))}")

        def navigate(self, page_id):
            if page_id == "dashboard":
                self.stack.setCurrentWidget(self.dashboard_page)
            elif page_id == "members":
                self.stack.setCurrentWidget(self.members_page)
            else:
                self.stack.setCurrentIndex(0)

            self.statusBar().showMessage(f"وروش به: {page_id}")


# ═══════════════════════════════════════════════════════════════════
# Tkinter 데스크톱 앱
# ═══════════════════════════════════════════════════════════════════
if TKINTER_AVAILABLE and not GTK4_AVAILABLE and not PYQT6_AVAILABLE:
    class TakavarTkApp:
        def __init__(self, root):
            self.root = root
            self.root.title(f"{APP_NAME} v{APP_VERSION}")
            self.root.geometry("1400x900")
            self.root.minsize(1100, 700)

            # Ubuntu 스타일 테마
            UbuntuStyleTk.apply(root)

            self.create_ui()
            self.check_auth()

        def create_ui(self):
            # Menu
            menubar = tk.Menu(self.root, tearoff=0)
            self.root.config(menu=menubar)

            # 파일
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="تغییر نقشه케이션 دیتابیس...")
            file_menu.add_separator()
            file_menu.add_command(label="خروج", command=self.root.quit)
            menubar.add_cascade(label="فایل", menu=file_menu)

            # ابزارها
            tools_menu = tk.Menu(menubar, tearoff=0)
            tools_menu.add_command(label="تولید گزارش PDF")
            tools_menu.add_command(label="تولید کارت اعضا")
            tools_menu.add_command(label="همگام‌سازی dữ liệu")
            menubar.add_cascade(label="ابزارها", menu=tools_menu)

            # راهنما
            help_menu = tk.Menu(menubar, tearoff=0)
            help_menu.add_command(label="درباره برنامه")
            help_menu.add_command(label="مستندات")
            menubar.add_cascade(label="راهنما", menu=help_menu)

            # تابلو ابزار
            toolbar = ttk.Frame(self.root, padding=5)
            toolbar.pack(fill=tk.X, side=tk.TOP)

            self.nav_buttons = {}
            nav_items = [
                ("🏠", "Dashboard", "dashboard"),
                ("👥", "اعضا", "members"),
                ("📋", "عضویت‌ها", "subscriptions"),
                ("💰", "پرداخت‌ها", "payments"),
                ("📅", "حضور و غیبت", "attendance"),
                ("🏋️", "تمرینات", "workouts"),
                ("⏰", "زمان‌بندی", "schedule"),
                ("👨‍🏫", "کارشناسان", "trainers"),
                ("🏗️", "تجهیزات", "equipment"),
                ("📊", "گزارشات", "reports"),
            ]

            for icon, text, page_id in nav_items:
                btn = ttk.Button(toolbar, text=f"{icon} {text}", command=lambda pid=page_id: self.navigate(pid))
                btn.pack(side=tk.LEFT, padx=3, pady=3)
                self.nav_buttons[page_id] = btn

            # 프레임 اصلی
            self.main_frame = ttk.Frame(self.root, padding=10)
            self.main_frame.pack(fill=tk.BOTH, expand=True)

            # محتوا (notebook)
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)

            # Dashboard صفحه
            self.dashboard_frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.dashboard_frame, text="🏠 Dashboard")

            # اعضا صفحه
            self.members_frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.members_frame, text="👥 اعضا")

            # 초기 صفحه
            self.notebook.select(self.dashboard_frame)

            # وضعیت بار
            self.status_var = tk.StringVar()
            self.status_var.set("برای شروع وارد شوید")
            status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
            status_bar.pack(fill=tk.X, side=tk.BOTTOM)

            # Dashboard محتوا
            self.setup_dashboard()
            self.setup_members()

        def setup_dashboard(self):
            # تیتر
            ttk.Label(self.dashboard_frame, text="🏋️ پنجره اصلی سیستم مدیریت باشگاه بدنسازی تکاور",
                       font=("Ubuntu", 18, "bold"), foreground="#E95420").pack(pady=(0, 15))

            # 진영 카드
            card_frame = ttk.Frame(self.dashboard_frame)
            card_frame.pack(fill=tk.X, pady=10)

            stats = [
                ("👥", "تعداد اعضا", "0", "#33D17A"),
                ("📋", "عضویت‌های فعال", "0", "#15AABF"),
                ("💰", "درآمد ماهانه", "0", "#F5C211"),
                ("👨‍🏫", "کارشناسان", "0", "#FF5733"),
                ("📅", "کلاس‌های امروز", "0", "#33D17A"),
                ("🏗️", "تجهیزات", "0", "#15AABF"),
            ]

            for i, (icon, label, value, color) in enumerate(stats):
                card = ttk.LabelFrame(card_frame, text=f"{icon}  {label.upper()}", padding=8)
                card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
                card.config(borderwidth=1)
                card.config(relief="solid")
                card.config(background="#3D1A5C")

                val_label = ttk.Label(card, text=value, font=("Ubuntu", 22, "bold"), foreground=color)
                val_label.pack(expand=True)

                # 카드 색상
                card.tk.call("ttk::style", "configure", f"Card{i}.Card", background="#3D1A5C")

            # 진영 프레임 설정
            for i in range(3):
                card_frame.columnconfigure(i, weight=1)

            # اخبار
            ttk.Separator(self.dashboard_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
            ttk.Label(self.dashboard_frame, text="📢 اخبار و اطلاعیه‌ها",
                       font=("Ubuntu", 14, "bold"), foreground="#15AABF").pack(anchor="w")
            news = ttk.Label(self.dashboard_frame,
                text="✓ سیستم مدیریت باشگاه بدنسازی تکاور با موفقیت راه‌اندازی شد\n✓ می‌توانید از پنجره اصلی سیستم استفاده کنید\n✓ برای راهنما به بخش راهنما مراجعه کنید",
                foreground="#CCCCCC", font=("Ubuntu", 11), justify="left")
            news.pack(anchor="w", fill=tk.X)

        def setup_members(self):
            ttk.Label(self.members_frame, text="👥 مدیریت اعضا - باشگاه بدنسازی تکاور",
                       font=("Ubuntu", 16, "bold"), foreground="#E95420").pack(anchor="w", pady=(0, 10))

            # ابزارها
            toolbar = ttk.Frame(self.members_frame)
            toolbar.pack(fill=tk.X, pady=(0, 10))

            search_var = tk.StringVar()
            search_entry = ttk.Entry(toolbar, textvariable=search_var, width=30)
            search_entry.pack(side=tk.LEFT, padx=(0, 10))
            search_entry.insert(0, "جستجو...")
            search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "جستجو..." else None)
            search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, "جستجو...") if not search_entry.get() else None)

            ttk.Button(toolbar, text="➕ عضو جدید", command=self.add_member).pack(side=tk.LEFT, padx=5)
            ttk.Button(toolbar, text="🔄癲新", command=self.load_members).pack(side=tk.LEFT, padx=5)

            # جدول
            tree_frame = ttk.Frame(self.members_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            columns = ("id", "first_name", "last_name", "phone", "email", "gender", "membership_type", "status", "start_date")
            self.members_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
            self.members_tree.heading("id", text="ID")
            self.members_tree.heading("first_name", text="نام")
            self.members_tree.heading("last_name", text="نام خانوادگی")
            self.members_tree.heading("phone", text="تلفن")
            self.members_tree.heading("email", text="ایمیل")
            self.members_tree.heading("gender", text="جنسیت")
            self.members_tree.heading("membership_type", text="پلن")
            self.members_tree.heading("status", text="وضعیت")
            self.members_tree.heading("start_date", text="تاریخ شروع")

            self.members_tree.column("id", width=50)
            self.members_tree.column("first_name", width=100)
            self.members_tree.column("last_name", width=100)
            self.members_tree.column("phone", width=100)
            self.members_tree.column("email", width=150)
            self.members_tree.column("gender", width=70)
            self.members_tree.column("membership_type", width=100)
            self.members_tree.column("status", width=90)
            self.members_tree.column("start_date", width=100)

            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.members_tree.yview)
            self.members_tree.configure(yscrollcommand=scrollbar.set)

            self.members_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # 스타일
            style = ttk.Style()
            style.configure("Treeview", background="#3D1A5C", foreground="#FFFFFF", fieldbackground="#3D1A5C", rowheight=28)
            style.configure("Treeview.Heading", background="#2C003E", foreground="#FFFFFF", font=("Ubuntu", 10, "bold"))

            ttk.Label(self.members_frame, text="برای افزودن عضو جدید روی دکمه 'عضو جدید' کلیک کنید.",
                       foreground="#777777", font=("Ubuntu", 10)).pack(anchor="w", pady=(5, 0))

        def load_members(self):
            for item in self.members_tree.get_children():
                self.members_tree.delete(item)

            result = api_get("/api/members")
            if "error" not in result:
                for m in result:
                    status = m.get("status", "")
                    status_color = "#33D17A" if status == "active" else "#FF5733" if status == "suspended" else "#F5C211"
                    self.members_tree.insert("", tk.END, values=(
                        m.get("id"),
                        m.get("first_name", ""),
                        m.get("last_name", ""),
                        m.get("phone", ""),
                        m.get("email", ""),
                        m.get("gender", ""),
                        m.get("membership_type", ""),
                        status,
                        str(m.get("membership_start", "")),
                    ))

        def add_member(self):
            dialog = tk.Toplevel(self.root)
            dialog.title("ثبت عضو جدید")
            dialog.geometry("500x600")
            dialog.transient(self.root)
            dialog.grab_set()

            form_frame = ttk.LabelFrame(dialog, text="اطلاعات عضو", padding=10)
            form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            fields = {}
            row = 0
            for label_text in ["نام", "نام خانوادگی", "کد ملی", "تلفن", "ایمیل"]:
                ttk.Label(form_frame, text=f"{label_text}:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
                fields[label_text] = entry
                row += 1

            ttk.Label(form_frame, text="تاریخ تولد:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            date_entry = ttk.Entry(form_frame, width=30)
            date_entry.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            fields["تاریخ تولد"] = date_entry
            row += 1

            ttk.Label(form_frame, text="جنسیت:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            gender_var = tk.StringVar(value="مذکر")
            gender_combo = ttk.Combobox(form_frame, textvariable=gender_var, values=["مذکر", "مونث", "سایر"], state="readonly", width=28)
            gender_combo.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            row += 1

            ttk.Label(form_frame, text="نوع پلن:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            plan_var = tk.StringVar(value="برونزی")
            plan_combo = ttk.Combobox(form_frame, textvariable=plan_var, values=["برونزی", "نقره‌ای", "طلایی", "VIP ویژه"], state="readonly", width=28)
            plan_combo.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            row += 1

            ttk.Label(form_frame, text="وزن (kg):").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            weight_entry = ttk.Entry(form_frame, width=30)
            weight_entry.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            fields["وزن"] = weight_entry
            row += 1

            ttk.Label(form_frame, text="قد (cm):").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            height_entry = ttk.Entry(form_frame, width=30)
            height_entry.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            fields["قد"] = height_entry
            row += 1

            ttk.Label(form_frame, text="آدرس:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            address_text = tk.Text(form_frame, width=30, height=4, font=("Ubuntu", 10))
            address_text.grid(row=row, column=1, padx=5, pady=3, sticky="ew")
            fields["آدرس"] = address_text
            row += 1

            # دکمه‌ها
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(fill=tk.X, padx=10, pady=10)

            ttk.Button(btn_frame, text="ثبت عضو", command=lambda: self.save_member(dialog, fields, gender_var, plan_var)).pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="انصراف", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

            form_frame.columnconfigure(1, weight=1)

        def save_member(self, dialog, fields, gender_var, plan_var):
            plan_map = {"برونزی": "bronze", "نقره‌ای": "silver", "طلایی": "gold", "VIP ویژه": "vip"}
            gender_map = {"مذکر": "male", "مونث": "female", "سایر": "other"}

            data = {
                "first_name": fields["نام"].get(),
                "last_name": fields["نام خانوادگی"].get(),
                "national_id": fields["کد ملی"].get() or None,
                "phone": fields["تلفن"].get() or None,
                "email": fields["ایمیل"].get() or None,
                "gender": gender_map.get(gender_var.get()),
                "address": fields["آدرس"].get("1.0", tk.END).strip() or None,
                "membership_type": plan_map.get(plan_var.get(), "bronze"),
                "weight": float(fields["وزن"].get()) if fields["وزن"].get() else None,
                "height": float(fields["قد"].get()) if fields["قد"].get() else None,
            }

            result = api_post("/api/members", data)
            if "error" not in result:
                messagebox.showinfo("تأیید", "عضو با موفقیت ثبت شد!")
                dialog.destroy()
                self.load_members()
            else:
                messagebox.showerror("خطا", str(result.get("detail", "خطا در ثبت")))

        def navigate(self, page_id):
            if page_id == "dashboard":
                self.notebook.select(self.dashboard_frame)
            elif page_id == "members":
                self.notebook.select(self.members_frame)
            self.status_var.set(f"وروش به: {page_id}")

        def check_auth(self):
            result = api_get("/api/auth/me")
            if "error" in result:
                self.show_login_dialog()
            else:
                global CURRENT_USER
                CURRENT_USER = result
                self.status_var.set(f"خوش آمدید، {result.get('first_name', 'کاربر')} | نقش: {result.get('role', '')}")

        def show_login_dialog(self):
            overlay = tk.Toplevel(self.root)
            overlay.title("ورود به سیستم")
            overlay.geometry("400x350")
            overlay.transient(self.root)
            overlay.grab_set()
            overlay.attributes("-topmost", True)

            overlay.config(background="#300A4F")

            logo_label = ttk.Label(overlay, text="🏋️ تکاور", font=("Ubuntu", 28, "bold"), foreground="#E95420")
            logo_label.pack(pady=(30, 5))

            sub_label = ttk.Label(overlay, text="سیستم مدیریت باشگاه بدنسازی",
                                  font=("Ubuntu", 12), foreground="#CCCCCC")
            sub_label.pack(pady=(0, 20))

            form_frame = ttk.Frame(overlay)
            form_frame.pack(pady=10)

            ttk.Label(form_frame, text="نام کاربری:", foreground="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            self.login_user = ttk.Entry(form_frame, width=25)
            self.login_user.grid(row=0, column=1, padx=5, pady=5)
            self.login_user.insert(0, "admin")

            ttk.Label(form_frame, text="رمز عبور:", foreground="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            self.login_pass = ttk.Entry(form_frame, width=25, show="*")
            self.login_pass.grid(row=1, column=1, padx=5, pady=5)
            self.login_pass.insert(0, "admin123")

            self.login_error = ttk.Label(overlay, text="", foreground="#FF5733", font=("Ubuntu", 10))
            self.login_error.pack(pady=5)

            ttk.Button(overlay, text="ورود به سیستم", command=lambda: self.attempt_login(overlay)).pack(pady=10)

        def attempt_login(self, overlay):
            result = api_post("/api/auth/login", {
                "username": self.login_user.get(),
                "password": self.login_pass.get(),
            })
            if "access_token" in result:
                global TOKEN, CURRENT_USER
                TOKEN = result["access_token"]
                CURRENT_USER = result["user"]
                overlay.destroy()
                self.status_var.set(f"خوش آمدید، {result['user'].get('first_name', 'کاربر')} | نقش: {result['user'].get('role', '')}")
            else:
                self.login_error.config(text=f"⚠ {result.get('detail', result.get('error', 'خطا در ورود'))}")


# ═══════════════════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════════════════
def main():
    print(f"\n{'='*60}")
    print(f"  {APP_NAME} v{APP_VERSION}")
    print(f"  Sistem مدیریت باشگاه بدنسازی")
    print(f"{'='*60}\n")

    if GTK4_AVAILABLE:
        print("راه‌اندازی با GTK4 + libadwaita (Ubuntu GNOME style)...")
        app = TakavarApp()
        sys.exit(app.run(sys.argv))

    elif PYQT6_AVAILABLE:
        print("راه‌اندازی با PySide6 (Qt6)...")
        app = QApplication(sys.argv)
        window = TakavarQtApp()
        window.show()
        sys.exit(app.exec())

    elif TKINTER_AVAILABLE:
        print("راه‌اندازی با Tkinter...")
        root = tk.Tk()
        app = TakavarTkApp(root)
        root.mainloop()

    else:
        print("❌ هیچ فریم‌ورک گرافیکی مورد پشتیبانی پیدا نشد.")
        print("لطفاً یکی از موارد زیر را نصب کنید:")
        print("  pip install PyGObject  (GTK4)")
        print("  pip install PySide6    (Qt6)")
        print("  pip install tkinter    (پیش‌فرض Python)")
        sys.exit(1)


if __name__ == "__main__":
    main()
