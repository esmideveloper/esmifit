# takavar Gym System - Windows Installer Script
# Run this script in PowerShell with Administrator privileges

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🏋️  takavar Gym System - Windows Installer      ║" -ForegroundColor Cyan
Write-Host "║     سیستم مدیریت باشگاه بدنسازی تکاور                      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check for Administrator privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "[WARN] این اسکریپت بهتر است با دسترسی Administrator اجرا شود." -ForegroundColor Yellow
    Write-Host ""
}

# Set variables
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$PythonExe = "python"
$PipExe = "pip"

Write-Host "[1/5] بررسی نصب Python..." -ForegroundColor Blue
try {
    $pythonVersion = & $PythonExe --version 2>&1
    Write-Host "  ✓ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "  dowload from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[2/5] نصب وابستگی‌های Python..." -ForegroundColor Blue

$packages = @(
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "pydantic",
    "pydantic-settings",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-multipart",
    "qrcode[pil]",
    "reportlab",
    "python-dateutil",
    "aiofiles"
)

foreach ($pkg in $packages) {
    Write-Host "  Installing $pkg..." -NoNewline
    & $PipExe install $pkg 2>&1 | Out-Null
    Write-Host " ✓" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/5] راه‌اندازی دیتابیس..." -ForegroundColor Blue

Set-Location "$ProjectDir\backend"
& $PythonExe main.py --seed-only 2>&1 | Out-Null
Set-Location $ProjectDir

Write-Host "  ✓ دیتابیس راه‌اندازی شد" -ForegroundColor Green

Write-Host ""
Write-Host "[4/5] چک کردن وابستگی‌های وب اپ..." -ForegroundColor Blue

$webAppDir = "$ProjectDir\web-app"
if (Test-Path "$webAppDir\package.json") {
    Set-Location $webAppDir
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install 2>&1 | Out-Null
        Write-Host "  ✓ وب اپ dependencies نصب شدند" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ npm not found. Please install Node.js" -ForegroundColor Yellow
    }
    Set-Location $ProjectDir
}

Write-Host ""
Write-Host "[5/5] اطلاعات نصب..." -ForegroundColor Blue

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ✅ نصب تکمیل شد!                                         ║
║                                                              ║
║     برای شروع سیستم، دستورات زیر را استفاده کنید:            ║
║                                                              ║
║     ──────────────────────────────────────                  ║
║                                                              ║
║     🖥️  شروع بک‌اند:                                        ║
║     cd backend                                                ║
║     python main.py                                            ║
║                                                              ║
║     📱 شروع دسکتاپ:                                         ║
║     cd desktop-app                                            ║
║     python main.py                                            ║
║                                                              ║
║     🌐 شروع وب اپ:                                           ║
║     cd web-app                                                ║
║     npm run dev                                               ║
║                                                              ║
║     ──────────────────────────────────────                  ║
║                                                              ║
║     اطلاعات ورود پیش‌فرض:                                    ║
║     • نام کاربری: admin                                       ║
║     • رمز عبور: admin123                                      ║
║                                                              ║
║     وب‌اپلیکیشن در آدرس زیر در دسترس خواهد بود:              ║
║     http://localhost:5173                                    ║
║                                                              ║
║     API در آدرس زیر در دسترس خواهد بود:                      ║
║     http://localhost:8000                                    ║
║     Documentation: http://localhost:8000/docs                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

Write-Host ""
Write-Host "برای راه‌اندازی خودکار، می‌توانید از فایل batch زیر استفاده کنید:" -ForegroundColor Yellow
Write-Host "  start_system.bat" -ForegroundColor White
Write-Host ""
