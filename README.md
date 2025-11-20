# Eng-Drill API (FastAPI + JWT + Email Verify + QE Proxy)

A minimal FastAPI backend for **Eng-Drill**:
- Email-based sign-up with **verification via SMTP (MIMEText)**
- JWT login, `/me` protected route
- Proxies to external QE model service (Cloud Run) via `/qe/score` and `/qe/score_batch`
- Containerized for **Cloud Run**

## Endpoints (summary)
- `POST /auth/register` – create user, sends verification email
- `GET  /auth/verify?token=...` – verify email
- `POST /auth/login` – returns access token
- `GET  /me` – current user info (Authorization: Bearer <token>)
- `POST /qe/score` – forward to MODEL_API_BASE/score
- `POST /qe/score_batch` – forward to MODEL_API_BASE/score_batch
- `GET  /healthz` – health check
- `GET  /` – root ping

## Quickstart

```bash
# 1) local env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # fill values

# 2) run
uvicorn app.main:app --reload --port 8080

# 3) test
curl http://127.0.0.1:8080/check
```

## How to Deploy
- Uploaded to github and connected the link with Google Cloud Run.