#!/usr/bin/env python3
"""
takavar Gym System - Installation and Setup Script
این اسکریپت برای راه‌اندازی اولیه سیستم استفاده می‌شود
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🏋️  takavar Gym System - را養子系統                    ║
║     سیستم مدیریت باشگاه بدنسازی تکاور                      ║
║                                                              ║
║     نسخه: 1.0.0                                              ║
║     توسعه‌دهنده: تیم تکاور                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
""")

def check_python():
    """Check Python version"""
    print(f"{Colors.BLUE}[1/6] بررسی نسخه Python...{Colors.RESET}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{Colors.RED}  ✗ Python 3.8 یا بالاتر требуется.{Colors.RESET}")
        return False
    print(f"{Colors.GREEN}  ✓ Python {version.major}.{version.minor}.{version.micro}检测到{Colors.RESET}")
    return True

def check_dependencies():
    """Check and install Python dependencies"""
    print(f"{Colors.BLUE}[2/6] بررسی зависимостей Python...{Colors.RESET}")

    base_dir = Path(__file__).parent.parent
    backend_req = base_dir / "backend" / "requirements.txt"

    packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose",
        "passlib",
        "bcrypt",
        "python-multipart",
        "qrcode",
        "reportlab",
        "python-dateutil",
        "aiofiles",
    ]

    for package in packages:
        try:
            __import__(package if package != "python-jose" else "jose")
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"  ✓ {package} 설치해撒")

    print(f"{Colors.GREEN}  ✓ تمام وابستگی‌ها نصب شدند{Colors.RESET}")

def setup_database():
    """Initialize database"""
    print(f"{Colors.BLUE}[3/6] راه‌اندازی دیتابیس...{Colors.RESET}")

    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
        from models import init_db, seed_default_data
    except ImportError:
        print(f"{Colors.YELLOW}  ! importing from backend/main.py{Colors.RESET}")
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from backend.models import init_db, seed_default_data

    db_path = Path(__file__).parent.parent / "gym_system.db"
    engine, Session = init_db(str(db_path))
    seed_default_data()
    print(f"{Colors.GREEN}  ✓ دیتابیس راه‌اندازی شد: {db_path}{Colors.RESET}")

def create_directories():
    """Create necessary directories"""
    print(f"{Colors.BLUE}[4/6] ایجاد پوشه‌های لازم...{Colors.RESET}")

    base_dir = Path(__file__).parent.parent

    dirs = [
        base_dir / "qr_codes",
        base_dir / "database" / "migrations",
        base_dir / "database" / "seed_data",
        base_dir / "web-app" / "src" / "views" / "Members",
        base_dir / "web-app" / "src" / "views" / "Subscriptions",
        base_dir / "web-app" / "src" / "views" / "Payments",
        base_dir / "web-app" / "src" / "views" / "Workouts",
        base_dir / "web-app" / "src" / "views" / "Equipment",
        base_dir / "web-app" / "src" / "views" / "Schedule",
        base_dir / "web-app" / "src" / "views" / "Trainers",
        base_dir / "web-app" / "src" / "views" / "Attendance",
        base_dir / "web-app" / "src" / "views" / "Nutrition",
        base_dir / "web-app" / "src" / "views" / "Billing",
        base_dir / "web-app" / "src" / "views" / "Reports",
        base_dir / "web-app" / "src" / "views" / "Settings",
        base_dir / "web-app" / "src" / "views" / "Products",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d.relative_to(base_dir)}")

    print(f"{Colors.GREEN}  ✓ پوشه‌ها ایجاد شدند{Colors.RESET}")

def create_default_config():
    """Create default configuration"""
    print(f"{Colors.BLUE}[5/6] ایجاد فایل پیکربندی پیش‌فرض...{Colors.RESET}")

    base_dir = Path(__file__).parent.parent
    config_dir = base_dir / "config"
    config_dir.mkdir(exist_ok=True)

    config = {
        "app": {
            "name": "takavar Gym System",
            "version": "1.0.0",
            "debug": False
        },
        "database": {
            "path": str(base_dir / "gym_system.db"),
            "type": "sqlite"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        },
        "ui": {
            "theme": "dark",
            "language": "fa",
            "direction": "rtl",
            "timezone": "Asia/Tehran"
        }
    }

    config_file = config_dir / "settings.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"{Colors.GREEN}  ✓ فایل پیکربندی ایجاد شد: {config_file.relative_to(base_dir)}{Colors.RESET}")

def print_summary():
    """Print installation summary"""
    print(f"""
{Colors.GREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ✅ نصب تکمیل شد!                                         ║
║                                                              ║
║     برای راه‌اندازی سیستم دستورات زیر را اجرا کنید:         ║
║                                                              ║
║     {Colors.YELLOW}🍎 شروع بک‌اند ({Colors.BLUE}cd backend && python main.py{Colors.YELLOW}){Colors.GREEN}       ║
║     {Colors.YELLOW}📱 شروع دسکتاپ ({Colors.BLUE}cd desktop-app && python main.py{Colors.YELLOW}){Colors.GREEN}     ║
║     {Colors.YELLOW}🌐 شروع وب ({Colors.BLUE}cd web-app && npm run dev{Colors.YELLOW}){Colors.GREEN}           ║
║                                                              ║
║     اطلاعات ورود پیش‌فرض:                                    ║
║     • نام کاربری: admin                                       ║
║     • رمز عبور: admin123                                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
""")

def main():
    print_header()

    if not check_python():
        sys.exit(1)

    create_directories()
    create_default_config()
    setup_database()
    check_dependencies()
    print_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}بر فراخوانده 중도 종료.{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}خطا: {e}{Colors.RESET}")
        sys.exit(1)
