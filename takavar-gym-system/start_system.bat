@echo off
echo ════════════════════════════════════════════════════════════════════
echo   takavar Gym System - راه‌اندازی سیستم
echo   سیستم مدیریت باشگاه بدنسازی تکاور
echo ════════════════════════════════════════════════════════════════════
echo.

echo [1/3] راه‌اندازی بک‌اند API...
echo.

cd /d "%~dp0backend"
start "Takavar Backend API" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [2/3] راه‌اندازی وب اپلیکیشن...
echo.

cd /d "%~dp0web-app"
start "Takavar Web App" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul

echo [3/3] راه‌اندازی دسکتاپ اپلیکیشن ( GTK4 / PyQt6 / Tkinter )...
echo.

cd /d "%~dp0desktop-app"
start "Takavar Desktop App" cmd /k "python main.py"

echo.
echo ════════════════════════════════════════════════════════════════════
echo   ✅ تمام سرویس‌ها راه‌اندازی شدند
echo ════════════════════════════════════════════════════════════════════
echo.
echo وب‌اپلیکیشن: http://localhost:5173
echo بک‌اند API:  http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo.
echo اطلاعات ورود پیش‌فرض:
echo   • نام کاربری: admin
echo   • رمز عبور: admin123
echo.
pause
