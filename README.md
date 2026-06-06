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

초기에는 Flask와 Jinja2 기반의 서버사이드 렌더링(SSR) 방식으로 개발했지만, 페이지 이동 시마다 전체 HTML을 다시 받아오는 구조의 한계를 경험했습니다.

이를 개선하기 위해 Vue.js 기반 SPA(Single Page Application) 구조로 리팩토링하고, Flask는 REST API 서버로 분리했습니다. 이 과정에서 클라이언트 라우팅, 전역 상태 관리(Pinia), 세션 기반 인증, Google OAuth2 인증 흐름을 직접 설계하고 구현했습니다.

또한 Google Calendar API를 연동하여 Todo 생성 시 일정이 자동 등록되도록 구현함으로써 반복적인 일정 입력 작업을 줄이고 생산성 관리 과정을 하나의 흐름으로 통합했습니다.

이 프로젝트를 통해 단순 CRUD 구현을 넘어 REST API 설계, 인증 처리, 외부 API 연동, 사용자 데이터 분리, SPA 아키텍처 전환 경험을 쌓을 수 있었습니다.
---

## 2. 기술 스택
| 분류 | 기술 | 선택 이유 |
|------|------|-----------|
| Backend | Python 3, Flask | REST API 설계, 사용자 인증, 외부 API 연동 등 웹 백엔드의 핵심 기능을 직접 구현하기 위해 선택 |
| Frontend | Vue.js 3, Vue Router, Pinia, Axios, Vite | SPA 구조를 구축하여 페이지 새로고침 없이 동작하는 사용자 경험을 구현하기 위해 선택. Pinia를 활용해 로그인 상태를 전역으로 관리 |
| Database | SQLite, SQLAlchemy ORM | 개인 프로젝트 규모에 적합한 경량 데이터베이스. SQLAlchemy ORM을 활용하여 Python 객체 중심으로 데이터 모델링 및 CRUD 기능 구현 |
| 인증 | Flask-Login, Werkzeug | 세션 기반 로그인 관리와 비밀번호 해시화를 통해 기본적인 인증 및 보안 기능 구현 |
| 외부 연동 | Google Calendar API (OAuth2 PKCE) | Todo와 일정 관리를 하나의 흐름으로 통합하기 위해 연동. 일정 이중 입력을 줄이고 자동 등록 기능 구현 |
| 배포 | PythonAnywhere | Flask 백엔드와 Vue 빌드 결과물을 하나의 서버에서 운영하며 실제 서비스 배포 경험 확보 |

본 프로젝트에서는 단순 CRUD 기능 구현에 그치지 않고, REST API 설계, 인증 처리, 사용자 데이터 관리, 외부 API 연동, SPA 아키텍처 전환 과정에서 발생한 문제를 해결하는 데 중점을 두었습니다.

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
- Google Calendar 연동을 통한 일정 자동 등록

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

사용자가 여러 서비스에 분산하여 관리하던 할 일, 일정, 목표, 기념일 정보를 하나의 화면에서 확인할 수 있도록 구성했습니다.

### 3-4. Google Calendar 자동 연동

- Google OAuth2 PKCE 인증 지원
- Todo 생성 시 Google Calendar 이벤트 자동 등록
- 일정 이중 입력 작업 제거
- Todo 관리와 일정 관리를 하나의 흐름으로 통합

기존에는 사용자가 할 일을 등록한 후 캘린더에 동일한 내용을 다시 입력해야 했습니다. 이를 개선하기 위해 Google Calendar API를 연동하여 Todo 생성 시 일정이 자동 등록되도록 구현했습니다.
---

## 4. 시스템 구조
Flask를 REST API 서버로 구성하고, Vue.js를 독립적인 SPA 프론트엔드로 분리하여 역할을 명확하게 구분했습니다.

사용자의 요청은 Vue 컴포넌트에서 Axios를 통해 API로 전달되며, Flask는 인증 처리 및 데이터 조회 후 JSON 응답을 반환합니다. 데이터는 SQLAlchemy ORM을 통해 SQLite에 저장되며, 모든 주요 데이터는 사용자별로 분리 관리됩니다.

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

이를 위해 Pinia Store를 도입하여 사용자 정보와 인증 상태를 전역으로 관리했습니다. 애플리케이션 시작 시 /api/me API를 호출하여 세션 유효성을 확인하고, 인증 상태를 모든 컴포넌트에서 공유할 수 있도록 구현했습니다.

이를 통해 컴포넌트 간 인증 상태를 일관되게 유지하고, 로그인 여부에 따른 화면 제어를 효율적으로 처리할 수 있었습니다.

---

### 5-3. 사용자 데이터 분리 설계

Todo, Goal, Diary, Anniversary 데이터는 모두 사용자 계정과 연결되어 관리됩니다.

모든 API 요청에서 Flask-Login의 current_user 정보를 활용하여 로그인한 사용자의 데이터만 조회하도록 구현했습니다.

이를 통해 하나의 서비스 내에서도 사용자별 데이터가 서로 노출되지 않도록 설계했습니다.

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

사용자는 일반적으로 할 일을 등록한 뒤 다시 캘린더에 일정을 입력해야 합니다.

이 프로젝트에서는 Google OAuth2 PKCE 인증을 통해 사용자의 캘린더 접근 권한을 획득하고, Todo 생성 시 Google Calendar API를 호출하여 이벤트를 자동 등록하도록 구현했습니다.

이를 통해 동일한 일정을 반복 입력하는 작업을 줄이고, Todo 관리와 일정 관리를 하나의 흐름으로 통합했습니다.

Todo 생성
    ↓
Google OAuth2 인증 확인
    ↓
Calendar API 호출
    ↓
Google Calendar 일정 자동 생성

---

## 6. AI 활용 내역
본 프로젝트는 AI(Claude, ChatGPT)를 개발 보조 도구로 활용했으며, 최종 설계와 구현은 직접 수행했습니다.

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

### AI 활용 원칙

AI가 제안한 코드와 설계를 그대로 적용하지 않고, 공식 문서와 직접 테스트를 통해 검증한 후 프로젝트에 반영했습니다.

문제 원인 분석, 코드 리뷰, 학습 보조 용도로 AI를 활용했으며 최종 구현과 디버깅은 직접 수행했습니다.

---