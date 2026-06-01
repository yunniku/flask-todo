# ✅ Flask Todo — 개인 생산성 관리 웹 앱

> Flask REST API + Vue.js SPA 기반의 개인 생산성 관리 웹 서비스

🔗 **배포 링크**: [https://yuniku.pythonanywhere.com](https://yuniku.pythonanywhere.com)

---

## 📌 프로젝트 소개

**Flask Todo**는 할 일 관리, 목표 설정, 다이어리, 기념일 D-day 관리 기능을 제공하는 개인 생산성 관리 웹 앱입니다.

처음에는 Flask Jinja2 템플릿으로 서버사이드 렌더링 방식으로 개발했습니다.
이후 페이지 새로고침 없이 빠른 화면 전환과 프론트/백엔드 분리를 위해
**Vue.js SPA + Flask REST API** 구조로 리팩토링했습니다.

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| **Backend** | Python 3, Flask, Flask-Login, Flask-CORS |
| **Frontend** | Vue.js 3, Vue Router, Pinia, Axios, Vite |
| **Database** | SQLite, SQLAlchemy ORM |
| **스타일** | Bootstrap 5, Bootstrap Icons |
| **배포** | PythonAnywhere |
| **외부 API** | Google Calendar API (OAuth2) |
| **인증** | Flask-Login (세션 기반), Werkzeug |

---

## ✨ 주요 기능

### 회원 관리
- 이메일 기반 회원가입 / 로그인
- 세션 기반 로그인 상태 유지
- 비밀번호 암호화 (Werkzeug)

### 할 일 관리 (Todos)
- 할 일 추가 / 완료 체크 / 수정 / 삭제
- 카테고리 분류 및 필터링
- 마감일 설정
- 삭제 확인 모달
- 페이지 새로고침 없이 즉시 반영 (fetch API)

### 목표 관리 (Goals)
- 일간 / 주간 / 월간 목표 설정
- 목표 달성 토글
- 달성률 퍼센트 표시

### 다이어리 (Diary)
- 날짜별 다이어리 작성 / 수정 / 삭제
- 기분 이모지 선택
- 테마 색상 선택 (보라 / 핑크 / 초록 / 파랑 / 노랑)
- 스티커 선택
- 월별 기록 목록 조회

### 기념일 관리 (Anniversary)
- 기념일 추가 / 삭제
- D-day 자동 계산
- 매년 반복 설정

### 대시보드 (Dashboard)
- 오늘 할 일 체크 (페이지 이동 없이)
- D-day 카운트다운
- 목표 달성률 (일간 / 주간 / 월간)
- 오늘 한 줄 다이어리 요약

### 통계 (Stats)
- 월별 완료 통계
- 카테고리별 통계
- 전체 달성률

### 구글 캘린더 연동
- Google OAuth2 인증
- 할 일을 구글 캘린더에 추가

---

## 🏗 기술 활용 포인트

### 1. Vue.js SPA + Flask REST API 분리 구조
```
기존: Flask Jinja2 → 서버가 HTML 렌더링 → 페이지 새로고침
변경: Vue Router → 클라이언트 라우팅 → 새로고침 없이 화면 전환
```

### 2. Vue Router (클라이언트 라우팅)
```javascript
const routes = [
  { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/todos', component: TodosView, meta: { requiresAuth: true } },
  { path: '/login', component: LoginView, meta: { guest: true } },
]

// 인증 가드 — 로그인 안 한 사용자 접근 차단
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth && !auth.isAuthenticated) next('/login')
  else next()
})
```

### 3. Pinia (전역 상태 관리)
```javascript
// 로그인 유저 정보를 모든 페이지에서 공유
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)

  async function fetchUser() {
    const res = await axios.get('/api/me')
    user.value = res.data.user
    isAuthenticated.value = true
  }
  return { user, isAuthenticated, fetchUser }
})
```

### 4. Flask Blueprint (기능별 라우트 분리)
```python
# 기능별로 파일을 분리해서 유지보수 용이
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp)
```

### 5. SQLAlchemy ORM
```python
# SQL 없이 Python 코드로 DB 조회
todos = Todo.query.filter_by(user_id=current_user.id).all()
todo = Todo.query.get_or_404(id)
```

### 6. Flask REST API
```python
# GET /api/todos → 할 일 목록 반환
@api_bp.route('/todos', methods=['GET'])
@login_required
def get_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify({'success': True, 'todos': [...]})
```

---

## 📁 프로젝트 구조

```
flask-todo/
├── routes/                 # Flask Blueprint 라우트
│   ├── api.py              # REST API (/api/todos, /api/goals 등)
│   ├── auth.py             # 로그인 · 회원가입
│   ├── todos.py            # 할 일 라우트
│   ├── goals.py            # 목표 라우트
│   ├── diary.py            # 다이어리 라우트
│   ├── anniversary.py      # 기념일 라우트
│   ├── dashboard.py        # 대시보드 라우트
│   └── calendar.py         # 구글 캘린더 연동
├── vue-app/                # Vue.js 프론트엔드
│   ├── src/
│   │   ├── views/          # 페이지 컴포넌트
│   │   │   ├── DashboardView.vue
│   │   │   ├── TodosView.vue
│   │   │   ├── GoalsView.vue
│   │   │   ├── DiaryView.vue
│   │   │   ├── AnniversaryView.vue
│   │   │   ├── StatsView.vue
│   │   │   ├── LoginView.vue
│   │   │   └── RegisterView.vue
│   │   ├── components/
│   │   │   └── NavBar.vue  # 네비게이션 컴포넌트
│   │   ├── stores/
│   │   │   └── auth.js     # Pinia 인증 스토어
│   │   ├── router/
│   │   │   └── index.js    # Vue Router 설정
│   │   └── main.js
│   └── vite.config.js
├── static/                 # 정적 파일
│   ├── style.css
│   └── dist/               # Vue 빌드 결과물 (npm run build 후 생성)
├── templates/              # Jinja2 템플릿 (기존)
├── models.py               # DB 모델 (User, Todo, Goal, Diary, Anniversary)
├── app.py                  # Flask 앱 팩토리
├── config.py               # 설정
├── requirements.txt
└── todo.db                 # SQLite DB (자동 생성)
```

---

## 🗄 데이터베이스 모델

| 모델 | 주요 필드 |
|------|----------|
| **User** | id, username, email, password |
| **Todo** | id, title, content, done, category, due_date, user_id |
| **Goal** | id, title, goal_type, achieved, target_date, user_id |
| **Diary** | id, date, content, mood, stickers, theme_color, user_id |
| **Anniversary** | id, title, date, emoji, repeat_yearly, user_id |

---

## 📊 API 엔드포인트

| 메서드 | URL | 설명 |
|--------|-----|------|
| GET | /api/me | 현재 로그인 유저 정보 |
| POST | /api/login | 로그인 |
| POST | /api/logout | 로그아웃 |
| GET | /api/todos | 할 일 목록 조회 |
| POST | /api/todos | 할 일 추가 |
| PUT | /api/todos/:id | 할 일 수정 / 완료 토글 |
| DELETE | /api/todos/:id | 할 일 삭제 |
| GET | /api/goals | 목표 목록 조회 |
| POST | /api/goals | 목표 추가 |
| PUT | /api/goals/:id/toggle | 목표 달성 토글 |
| DELETE | /api/goals/:id | 목표 삭제 |
| GET | /api/diary | 다이어리 목록 조회 |
| POST | /api/diary | 다이어리 저장 |
| DELETE | /api/diary/:id | 다이어리 삭제 |
| GET | /api/anniversary | 기념일 목록 조회 |
| POST | /api/anniversary | 기념일 추가 |
| DELETE | /api/anniversary/:id | 기념일 삭제 |
| GET | /api/dashboard | 대시보드 데이터 |
| GET | /api/stats | 통계 데이터 |

---

## 🚀 설치 방법

### 사전 요구사항

- Python 3.8 이상
- Node.js 18 이상
- pip3, npm

### 1. 레포지토리 클론

```bash
git clone https://github.com/yunniku/flask-todo.git
cd flask-todo
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Python 패키지 설치

```bash
pip3 install -r requirements.txt
```

### 4. Vue 프론트엔드 빌드

```bash
cd vue-app
npm install
npm run build   # → static/dist/ 폴더 생성
cd ..
```

### 5. Flask 서버 실행

```bash
python3 -c "from app import create_app; create_app().run(port=5001, debug=True)"
```

브라우저에서 `http://localhost:5001` 접속

> **참고** — Vue 개발 서버를 따로 띄우고 싶다면 (Hot Reload 지원):
> ```bash
> # 터미널 1: Flask 서버
> python3 -c "from app import create_app; create_app().run(port=5001, debug=True)"
>
> # 터미널 2: Vue 개발 서버
> cd vue-app && npm run dev
> # → http://localhost:5173 에서 접속
> ```

### 6. (선택) Google Calendar 연동

Google Cloud Console에서 OAuth2 자격 증명을 생성한 뒤,
`credentials.json` 파일을 프로젝트 루트에 배치하면 구글 캘린더 연동 기능을 사용할 수 있습니다.

---

## 📖 사용법

1. **회원가입 → 로그인**
2. **대시보드**: 오늘의 할 일 요약, D-day, 목표 달성률 한눈에 확인
3. **할 일**: 카테고리·마감일 설정 후 할 일 추가, 완료 체크
4. **목표**: 일간 / 주간 / 월간 목표를 설정하고 달성률 확인
5. **다이어리**: 날짜별로 기분 이모지·스티커·테마 색상을 선택해 작성
6. **기념일**: 기념일 추가 시 D-day 자동 계산, 매년 반복 설정 가능
7. **통계**: 월별·카테고리별 완료 현황 그래프 확인

---

## 📝 구현 흐름

```
회원가입 → 로그인 → 대시보드
                      ├── 할 일 추가 / 완료 체크
                      ├── 목표 설정 및 달성 체크
                      ├── 다이어리 작성
                      ├── 기념일 D-day 확인
                      └── 통계 확인
```

---

## 🤝 기여 방법

1. 이 레포를 **Fork** 하세요
2. 새 브랜치를 생성하세요
   ```bash
   git checkout -b feature/새기능
   ```
3. 변경사항을 커밋하세요
   ```bash
   git commit -m "feat: 새 기능 추가"
   ```
4. 브랜치에 Push 하세요
   ```bash
   git push origin feature/새기능
   ```
5. **Pull Request**를 열어주세요

---

## 👨‍💻 개발자

| 항목 | 내용 |
|------|------|
| **개발 기간** | 2026 |
| **개발 인원** | 1인 개발 |
| **GitHub** | [yunniku](https://github.com/yunniku) |
