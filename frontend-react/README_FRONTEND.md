# Frontend (React + Vite)

This is a minimal React frontend that connects to the Django backend.

Prereqs
- Node 18+ and npm/yarn

Install & run
```powershell
cd frontend-react
npm install
npm run dev
```

Features
- JWT login using `/api/auth/login/` (access + refresh)
- Automatic refresh of access token via `/api/auth/refresh/`
- CSV upload to `/api/datasets/upload/`
- Dashboard shows last 5 datasets, charts, and a table for rows

Notes
- The app assumes the backend runs at `http://127.0.0.1:8000`. To change, set `REACT_APP_API_URL` env var before starting.
- Tokens are stored in `localStorage` for demo.
- This implementation focuses on connectivity; you can enhance styling and UX as needed.
