# Flask Todo

Flask REST API + Vue.js SPA 기반 개인 생산성 관리 웹 앱

## 프로젝트 정보

- 개발 기간: 2026
- 개발 인원: 1인
- 주요 기술: Flask, Vue.js, SQLAlchemy, OAuth2, Google Calendar API

- GitHub
  - https://github.com/yunniku/flask-todo

- 배포
  - https://yuniku.pythonanywhere.com

---

## 1. 프로젝트 개요
업무와 개인 프로젝트를 병행하면서 할 일, 목표, 일정, 기념일을 여러 서비스에 나누어 관리하는 과정에서 반복적인 입력과 정보 분산 문제를 경험했습니다.

특히 할 일을 작성한 뒤 다시 캘린더에 일정을 등록해야 하는 이중 입력 작업이 반복되었고, 진행 상황을 한곳에서 확인하기 어려웠습니다.

이러한 불편함을 해결하기 위해 Todo, Goal, Diary, Anniversary 기능을 하나의 서비스로 통합한 개인 생산성 관리 웹 애플리케이션을 개발했습니다.
Google Calendar API를 연동하여 작업결과가 동기화되어 기록물들을 쉽게 확인할 수 있게 접근성을 강화 했습니다.

## 2. 기술 스택
| 분류 | 기술 | 선택 이유 |
|------|------|-----------|
| Backend | Flask | REST API 설계 및 핵심 백엔드 기능 구현 |
| Frontend | Vue.js 3 | SPA 구조 기반 UI 및 상태 관리 구현 |
| Database | SQLite, SQLAlchemy ORM | 경량 DB 기반 CRUD 및 객체 중심 데이터 모델링 |
| Auth | Flask-Login, Werkzeug | 세션 기반 인증 및 비밀번호 암호화 처리 |
| External API | Google Calendar API (OAuth2 PKCE) | 일정 관리 자동화 및 외부 캘린더 연동 |
| Deploy | PythonAnywhere | 통합 배포 및 서비스 운영 경험 |

---

## 3. 주요 기능

### 3-1. 회원 관리

- 이메일 기반 회원가입 및 로그인
- Flask-Login을 활용한 세션 기반 인증 처리
- Werkzeug를 활용한 비밀번호 해시화 저장
- 로그인 사용자별 데이터 분리 관리 (Todo, Goal, Diary, Anniversary)

### 3-2. 생산성 관리 기능

#### Todo 관리
- 카테고리 분류 및 마감일 설정
- 완료 상태 즉시 반영 (비동기 API 통신)
- 진행 중인 작업과 완료된 작업 구분 관리

#### Goal 관리
- 일간 / 주간 / 월간 목표 설정
- 목표 달성 여부 기록
- 달성률 자동 계산 및 시각화

#### Diary 관리
- 날짜별 다이어리 작성
- 기분 이모지 및 테마 색상 설정
- 월별 작성 내역 조회

#### Anniversary 관리
- D-Day 자동 계산
- 매년 반복되는 기념일 지원
- 다가오는 일정 자동 표시

### 3-3. 통합 대시보드 및 통계

- 오늘의 할 일 요약
- 다가오는 기념일 카운트다운
- 목표 달성 현황 확인
- 월별 Todo 완료 현황 통계
- 카테고리별 작업 분포 확인

분산 관리하던 할 일, 일정, 목표, 기념일 정보를 <하나의 화면> 또는 <Google Calendar>에서 관리.

### 3-4. Google Calendar 자동 연동

- Google OAuth2 PKCE 인증 지원
- 자동 연동처리를 통한 이중 입력 작업 제거
- 유저 접근성 향상

## 4. 시스템 구조
Flask를 REST API 서버로 구성하고, Vue.js를 독립적인 SPA 프론트엔드로 분리하여 역할을 명확하게 구분했습니다.

사용자의 요청은 Vue 컴포넌트에서 Axios를 통해 API로 전달되며, Flask는 인증 처리 및 데이터 조회 후 JSON 응답을 반환합니다. 데이터는 SQLAlchemy ORM을 통해 SQLite에 저장되며, 모든 주요 데이터는 사용자별로 분리 관리됩니다.




```
Client (Browser)
        │
        ▼
Vue.js SPA
        │ REST API
        ▼
Flask Backend
 ├── Schedule CRUD
 ├── Google API
 ├── Authenticate
        │
        ▼
SQLite (SQLAlchemy ORM)
```

```
Frontend (Vue.js)
├── Vue Router
├── Pinia
├── Axios
└── Views

Backend (Flask)
├── Auth API
├── Todo / Goal / Diary API
├── Google Calendar API
├── Flask-Login
└── SQLAlchemy ORM

Database (SQLite)
```

---
## 5. 핵심 구현 포인트

### 5-1. Jinja2 SSR → Vue.js SPA 전환

초기 버전은 Flask와 Jinja2를 활용한 서버사이드 렌더링(SSR) 구조였습니다. 하지만 페이지 이동 시마다 서버에서 전체 HTML을 다시 받아와야 했고, 사용자 경험 측면에서도 한계가 있었습니다.

이를 개선하기 위해 Vue.js 기반 SPA 구조로 리팩토링하고, Flask는 JSON만 반환하는 REST API 서버로 역할을 분리했습니다.

Vue Router를 활용해 브라우저에서 URL 기반 화면 전환을 처리하고, Flask는 데이터 제공과 인증 처리에 집중하도록 구조를 변경했습니다.

이를 통해 화면 전환 시 불필요한 페이지 새로고침을 제거하고, 프론트엔드와 백엔드의 역할을 명확하게 분리할 수 있었습니다.

---

### 5-2. Pinia 전역 인증 상태 관리

SPA 환경에서는 페이지를 이동하더라도 로그인 상태를 유지해야 합니다.

이를 위해 Pinia Store를 도입하여 사용자 정보와 인증 상태를 전역으로 관리했습니다. 애플리케이션 시작 시 /api/me API를 호출하여 세션 유효성을 검증하고, 인증 상태를 모든 컴포넌트에서 공유할 수 있도록 구현했습니다.

이를 통해 컴포넌트 간 인증 상태를 일관되게 유지하고, 로그인 여부에 따른 화면 제어를 정확하게 처리할 수 있었습니다.

---

### 5-3. 사용자 데이터 분리 설계

Todo, Goal, Diary, Anniversary 데이터는 모두 사용자 계정과 연결되어 관리됩니다.

모든 API 요청에서 Flask-Login의 current_user 정보를 활용하여 로그인한 사용자의 데이터만 조회하도록 구현했습니다.

```python
@login_required
def get_todos():
    todos = Todo.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify(...)
```

사용자 식별 정보를 기준으로 데이터를 조회하도록 구현하여, 멀티 유저 환경에서도 각 사용자의 데이터가 독립적으로 관리되도록 했습니다.

---

### 5-4. Google Calendar API 자동 연동

Todo 생성
    ↓
Google OAuth2 인증 확인
    ↓
Calendar API 호출
    ↓
Google Calendar 일정 자동 생성

반복 입력하는 등의 불편함을 없애고, 사용성이 높은 Google Calendar를 연동람으로서 꼭 사이트에 방문하지 않아도
관리된 기록물들을 쉽게 확인 할 수 있게 접근성을 높이고자 하였습니다.


---
## 6. 배포 구조
git push → PythonAnywhere 배포
├── Frontend: Vue.js build 결과 (정적 파일)
├── Backend: Flask REST API 실행
├── Database: SQLite
└── External API: Google Calendar API 연동 유지

로컬 환경(개발) - Flask와 Vue를 분리하여 실행
배포 환경 - 빌드된 Vue 파일을 Flask와 함께 서빙하도록 구성
SPA 구조를 유지&단일 서버 기반으로 배포 및 운영 가능하도록 설계

OAuth2 인증 및 Google Calendar API 연동은 배포 환경에서도 동일하게 동작하도록 환경 변수 기반으로 관리했습니다.

---

## 7. AI 활용 내역
본 프로젝트는 AI(Claude, ChatGPT)를 개발 보조 도구로 사용
문제 원인 분석, 코드 리뷰, 학습 보조 용도로 AI를 활용했으며 최종 설계, 구현, 디버깅은 직접 수행했습니다.

### 직접 설계 및 구현
- Vue.js SPA + Flask REST API 아키텍처 설계
- Pinia 기반 전역 인증 상태 관리 흐름 구현
- Vue Router 인증 가드 로직 구현
- Flask Blueprint 기반 기능별 모듈 분리
- SQLAlchemy ORM 데이터 모델 설계
- Google OAuth2 PKCE 인증 흐름 구현
- Google Calendar API 자동 등록 기능 구현
- PythonAnywhere 배포 및 운영 환경 설정

### AI 보조 활용

- Jinja2 ↔ Vue 템플릿 문법 충돌 원인 분석
- Flask 세션과 Vue SPA 연동 시 인증 처리 방식 검토
- OAuth2 토큰 갱신 로직 코드 리뷰
- 리팩토링 아이디어 검토
- README 초안 작성 및 문서 구조 개선

---
