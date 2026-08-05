#!/bin/bash
# takavar Gym System - Startup Script (Linux/Mac)
# Usage: ./start_system.sh

echo "══════════════════════════════════════════════════════════════════"
echo "  🏋️  takavar Gym System - راه‌اندازی سیستم"
echo "  سیستم مدیریت باشگاه بدنسازی تکاور"
echo "══════════════════════════════════════════════════════════════════"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/3] راه‌اندازی بک‌اند API...${NC}"
echo ""
cd "$SCRIPT_DIR/backend"

if command -v python3 &> /dev/null; then
    PYTHON="python3"
else
    PYTHON="python"
fi

nohup $PYTHON main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "  ✓ بک‌اند راه‌اندازی شد (PID: $BACKEND_PID)"
echo -e "  لاگ‌ها: $SCRIPT_DIR/logs/backend.log"
sleep 2

echo ""
echo -e "${BLUE}[2/3] راه‌اندازی وب اپلیکیشن...${NC}"
echo ""
cd "$SCRIPT_DIR/web-app"

if command -v npm &> /dev/null; then
    nohup npm run dev > ../logs/web.log 2>&1 &
    WEB_PID=$!
    echo -e "  ✓ وب اپلیکیشن راه‌اندازی شد (PID: $WEB_PID)"
    echo -e "  لاگ‌ها: $SCRIPT_DIR/logs/web.log"
    echo -e "  آدرس: ${GREEN}http://localhost:5173${NC}"
else
    echo -e "  ⚠ npm پیدا نشد. لطفاً Node.js نصب کنید."
    echo -e "  دستگاهriere: ${YELLOW}cd web-app && npm run dev${NC}"
fi
sleep 2

echo ""
echo -e "${BLUE}[3/3] راه‌اندازی دسکتاپ اپلیکیشن...${NC}"
echo ""
cd "$SCRIPT_DIR/desktop-app"

nohup $PYTHON main.py > ../logs/desktop.log 2>&1 &
DESKTOP_PID=$!
echo -e "  ✓ دسکتاپ اپلیکیشن راه‌اندازی شد (PID: $DESKTOP_PID)"
echo -e "  لاگ‌ها: $SCRIPT_DIR/logs/desktop.log"

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo -e "  ${GREEN}✅ تمام سرویس‌ها راه‌اندازی شدند${NC}"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "وب‌اپلیکیشن: ${GREEN}http://localhost:5173${NC}"
echo "بک‌اند API:  ${GREEN}http://localhost:8000${NC}"
echo "API Docs:    ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "اطلاعات ورود پیش‌فرض:"
echo "  • نام کاربری: admin"
echo "  • رمز عبور: admin123"
echo ""
echo "برای توقف تمام سرویس‌ها:"
echo "  kill $BACKEND_PID $WEB_PID $DESKTOP_PID"
echo ""
