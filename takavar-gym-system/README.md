# takavar-gym-system
시스템이 체육관 관리 통합 시스템 — 데스크톱 (GTK4/리눅스) + 웹 (Vue.js) + 백엔드 (FastAPI) + 로컬 SQLite

## 기술 스택
- **데스크톱**: Python 3.11 + PyGObject + GTK4 + libadwaita (Ubuntu GNOME 동일 UI)
- **웹**: Vue.js 3 + Vuetify 3 + Vite
- **백엔드**: Python FastAPI + SQLAlchemy + SQLite
- **데이터베이스**: SQLite (로컬)

## 설치 및 실행

### 필수 의존성 설치
```bash
pip install -r desktop-app/requirements.txt
pip install -r backend/requirements.txt
cd web-app && npm install
```

### 백엔드 서버 실행
```bash
python backend/main.py
```

### 데스크톱 앱 실행
```bash
python desktop-app/main.py
```

### 웹 앱 실행
```bash
cd web-app && npm run dev
```

## 프로젝트 구조
- desktop-app/ — GTK4 데스크톱 애플리케이션
- web-app/ — Vue.js 웹 대시보드
- backend/ — FastAPI 백엔드 서버
- database/ — SQLite 데이터베이스 및 마이그레이션
- docs/ — 문서
- config/ — 설정 파일
- scripts/ — 유틸리티 스크립트
- installers/ — 설치 관리자
