# Lingtrain — Implementation Guide

Technical documentation for the authentication and authorization system.

## Architecture Overview

```
fe/                         Vue 3 + TypeScript frontend
  src/
    api/                    HTTP client and endpoint functions
    assets/                 CSS variables and shared styles
    components/             Reusable UI components
    composables/            Vue composables (shared logic)
    i18n/                   Internationalization (EN/RU)
    pages/                  Route-level page components
    router/                 Vue Router configuration + guards
    stores/                 Pinia state management

be/                         Python + FastAPI backend
  app/
    models/                 SQLAlchemy ORM models
    schemas/                Pydantic request/response schemas
    routers/                API route handlers
    services/               Business logic layer
```

### Technology Stack

| Layer     | Technology                                  |
| --------- | ------------------------------------------- |
| Frontend  | Vue 3.5, TypeScript 5.9, Vite 7.3, Pinia 3 |
| Backend   | Python, FastAPI, SQLAlchemy 2, SQLite        |
| Auth      | JWT (HS256), bcrypt password hashing         |
| i18n      | vue-i18n 11 (English + Russian)              |

---

## Authentication

### Token Strategy

- **Format:** JWT (HS256), issued by the backend
- **Payload:** `{ sub: "<user_id>", exp: <timestamp> }`
- **Expiry:** 30 days
- **Storage:** `localStorage` under the key `token`
- **Transport:** `Authorization: Bearer <token>` header on every API request

### Login Flow

1. User enters email/username + password in `SignInForm`
2. Frontend calls `POST /api/auth/login` with `{ login, password }`
3. Backend looks up user by email (lowercased) or username
4. Backend verifies password with bcrypt, checks `is_active` and `is_email_verified`
5. On success: returns `{ access_token, token_type, user }`
6. Frontend stores token in `localStorage`, sets `user` in the auth Pinia store
7. Router navigates to `/main`

### Error Responses

| Status | Detail                 | Cause                          |
| ------ | ---------------------- | ------------------------------ |
| 401    | Invalid credentials    | Wrong email/username/password  |
| 403    | Account is deactivated | `is_active` is false           |
| 403    | Email not verified     | `is_email_verified` is false   |

### Token Validation (Frontend)

On page refresh with an existing token in `localStorage`:

1. Router `beforeEach` guard detects token exists but `user` is null
2. Calls `fetchUser()` which hits `GET /api/users/me`
3. If valid: user object is restored into the store — navigation proceeds
4. If invalid/expired: token is cleared, user is logged out

### Logout

Clears `user` and `token` from the Pinia store and removes `token` from `localStorage`. No backend call is needed (JWT is stateless).

---

## Registration

### Flow

1. User fills `RegisterForm`: username, email, password, confirm password
2. **Client-side validation:**
   - All fields required (submit button disabled until filled)
   - Password minimum 6 characters
   - Password and confirm must match (checked on submit)
3. Frontend calls `POST /api/auth/register` with `{ username, email, password }`
4. Backend checks uniqueness of username and email (409 if taken)
5. Backend creates user with `is_email_verified = false`, generates 6-digit code
6. Code is printed to backend console and returned in the API response (dev mode)
7. Frontend transitions to `VerifyEmailForm`, pre-filling the code

### Duplicate Detection

| Status | Detail                  | Cause                     |
| ------ | ----------------------- | ------------------------- |
| 409    | Username already taken  | Username exists in DB     |
| 409    | Email already registered | Email exists in DB        |

### Password Hashing

Uses `bcrypt` with auto-generated salt. Passwords are never stored in plaintext. The `hash_password()` and `verify_password()` functions in `auth_service.py` handle all hashing operations.

---

## Email Verification

### Flow

1. After registration, a 6-digit numeric code is generated
2. Code is stored in the `email_verifications` table with a 15-minute expiry
3. Code is printed to backend stdout (development) and returned in the register response
4. `VerifyEmailForm` displays the target email and a code input field
5. User submits code via `POST /api/auth/verify-email` with `{ email, code }`
6. Backend validates: correct code, not expired, not already used
7. On success: sets `is_email_verified = true`, marks code as used
8. Frontend shows success toast and transitions back to sign-in form

### Verification Model

```
EmailVerification:
  id          — Primary key
  user_id     — FK to users table
  code        — 6-digit string
  created_at  — Timestamp
  expires_at  — created_at + 15 minutes
  is_used     — Boolean, prevents code reuse
```

### Error Responses

| Status | Detail                   | Cause                              |
| ------ | ------------------------ | ---------------------------------- |
| 400    | Invalid or expired code  | Wrong code, expired, or already used |

---

## Route Guards

Defined in `fe/src/router/index.ts` using Vue Router's `beforeEach` hook.

### Route Configuration

| Path     | Name    | Auth Required | Role Required | Redirect on Fail |
| -------- | ------- | ------------- | ------------- | ---------------- |
| `/`      | landing | No            | —             | —                |
| `/main`  | main    | No            | —             | —                |
| `/admin` | admin   | Yes           | `admin`       | See below        |

### Guard Logic

```
1. If token exists but user not loaded → fetchUser() (one-time on refresh)
2. If route requires auth and user not authenticated → redirect to /
3. If route requires role and user role doesn't match → redirect to /main
```

### Route Meta

Routes use `meta` fields to declare requirements:

```typescript
meta: { requiresAuth: true, requiresRole: 'admin' }
```

---

## Admin Panel

**Route:** `/admin` (requires `admin` role)

### Features

- Displays a table of all registered users
- Columns: ID, Username, Email, Role, Verified, Active
- Loading state while fetching data
- Error toast on API failure

### API

`GET /api/users` — returns all users. Requires admin role (403 for non-admins).

---

## API Layer

### HTTP Client (`fe/src/api/client.ts`)

A generic `apiFetch<T>()` wrapper around the native `fetch` API:

- Automatically injects `Authorization: Bearer <token>` from `localStorage`
- Sets `Content-Type: application/json` on all requests
- Parses error responses into `ApiError(status, detail)`
- Returns typed responses via generics

### Endpoint Functions (`fe/src/api/auth.ts`)

| Function          | Method | Path                    | Auth |
| ----------------- | ------ | ----------------------- | ---- |
| `apiRegister()`   | POST   | `/api/auth/register`    | No   |
| `apiLogin()`      | POST   | `/api/auth/login`       | No   |
| `apiVerifyEmail()` | POST  | `/api/auth/verify-email` | No  |
| `apiGetMe()`      | GET    | `/api/users/me`         | Yes  |
| `apiGetUsers()`   | GET    | `/api/users`            | Admin |

### Dev Proxy

Vite dev server proxies `/api` requests to `http://localhost:8000` so frontend and backend can run on different ports during development without CORS issues.

---

## State Management

### Auth Store (`fe/src/stores/auth.ts`)

Pinia store using the Composition API style.

**State:**
- `user: UserOut | null` — current authenticated user
- `token: string | null` — JWT token (initialized from `localStorage`)

**Computed:**
- `isAuthenticated` — `true` if `user` is not null
- `isAdmin` — `true` if user role is `admin`

**Actions:**
- `login(login, password)` — authenticates and stores token + user
- `register(username, email, password)` — registers new user
- `verifyEmail(email, code)` — verifies email with code
- `fetchUser()` — rehydrates user from token (calls `/users/me`)
- `logout()` — clears user, token, and localStorage

---

## Toast Notifications

### Composable (`fe/src/composables/useToast.ts`)

Module-level singleton pattern — all components share the same toast queue.

**Methods:**
- `success(message)` — green toast, 3s duration
- `error(message)` — red toast, 5s duration
- `info(message)` — blue toast, 3s duration

### Component (`fe/src/components/ToastNotification.vue`)

- Mounted globally in `App.vue`
- Rendered via `Teleport` to `<body>` (positioned top-right, z-index 10000)
- Uses Vue's `TransitionGroup` for slide-in/slide-out animations

---

## Internationalization (i18n)

All user-facing strings are localized using `vue-i18n`. Supported locales: **English** (`en`) and **Russian** (`ru`).

### Key Namespaces

| Namespace  | Usage                                        |
| ---------- | -------------------------------------------- |
| `landing`  | Landing page: title, subtitle, sign-in, logout |
| `sidebar`  | Main page sidebar labels                      |
| `auth`     | All auth forms: sign-in, register, verify     |
| `admin`    | Admin panel: table headers, status labels     |

### Locale Persistence

The selected locale is stored in `localStorage` under the key `locale` and restored on page load. The `LanguageSwitcher` component cycles between available languages.

---

## UI Components

### AuthDialog

Modal overlay with a card container. Uses `Teleport` to render outside the component tree. Closes on overlay click or close button. Animated with scale + fade transitions.

### SignInForm

- Google sign-in button (placeholder — shows "Coming soon" toast)
- "or" divider
- Email/username + password fields
- Submit button disabled until both fields are filled
- Link to switch to register form

### RegisterForm

- Username, email, password, confirm password fields
- Submit button disabled until all fields valid (password >= 6 chars)
- Client-side password match validation on submit
- On success, transitions to verify form

### VerifyEmailForm

- Shows target email address
- 6-digit code input (numeric, monospace, centered)
- Auto-filled with code from registration response (dev mode)
- Submit button disabled until code is 6 digits

---

## Shared Form Styles

Common form CSS is extracted into `fe/src/assets/forms.css` and imported globally in `App.vue`. This includes styles for:

- `.form-title` — centered heading
- `.form-hint` — subtitle/description text
- `.field-label` — form field labels
- `.field-input` — text inputs with focus state
- `.submit-btn` — primary action button with disabled state
- `.switch-text` — "Already have an account?" links

Component-specific styles (Google button, divider, code input) remain scoped to their respective components.

---

## Database

### Models

**User** (`users` table):

| Column             | Type         | Notes                        |
| ------------------ | ------------ | ---------------------------- |
| id                 | Integer (PK) | Auto-increment               |
| username           | String(50)   | Unique, indexed              |
| email              | String(255)  | Unique, indexed, lowercased  |
| password_hash      | String(255)  | bcrypt hash                  |
| role               | String(20)   | `user` or `admin`            |
| is_active          | Boolean      | Default `true`               |
| is_email_verified  | Boolean      | Default `false`              |
| created_at         | DateTime     | UTC timestamp                |
| updated_at         | DateTime     | UTC, auto-updated            |

**EmailVerification** (`email_verifications` table):

| Column      | Type         | Notes                     |
| ----------- | ------------ | ------------------------- |
| id          | Integer (PK) | Auto-increment            |
| user_id     | Integer (FK) | References `users.id`     |
| code        | String(6)    | 6-digit numeric string    |
| created_at  | DateTime     | UTC timestamp             |
| expires_at  | DateTime     | created_at + 15 minutes   |
| is_used     | Boolean      | Default `false`           |

### Seed Data

On startup, the backend seeds two test users (skipped if already present):

| Username | Email                    | Password        | Role  |
| -------- | ------------------------ | --------------- | ----- |
| admin    | admin@lingtrain.local    | adminadmin777   | admin |
| test     | test@lingtrain.local     | testtest777     | user  |

Both are created with `is_active = true` and `is_email_verified = true`.

---

## Configuration

### Backend (`be/app/config.py`)

| Variable                        | Default                            | Env Variable             |
| ------------------------------- | ---------------------------------- | ------------------------ |
| SECRET_KEY                      | `dev-secret-key-change-in-production` | `LINGTRAIN_SECRET_KEY`  |
| DATABASE_URL                    | `sqlite:///./lingtrain.db`         | `LINGTRAIN_DATABASE_URL` |
| ALGORITHM                       | `HS256`                            | —                        |
| ACCESS_TOKEN_EXPIRE_DAYS        | `30`                               | —                        |
| VERIFICATION_CODE_EXPIRE_MINUTES | `15`                              | —                        |

### Frontend Dev Proxy (`fe/vite.config.ts`)

All `/api` requests are proxied to `http://localhost:8000` during development.

---

## Running the Application

```bash
# Terminal 1 — Backend
cd be
pip install -r requirements.txt
python run.py
# Server starts on http://localhost:8000

# Terminal 2 — Frontend
cd fe
npm install
npm run dev
# Dev server starts on http://localhost:5173
```

### Quick Test

1. Open `http://localhost:5173`
2. Click "Sign in" → enter `admin` / `adminadmin777` → redirected to `/main`
3. Navigate to `/admin` → see the users table
4. Test registration: click "Register", fill form, code auto-fills, verify, then sign in
