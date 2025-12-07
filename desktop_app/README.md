# Desktop App — Chemical Equipment Visualizer

This is a PyQt5 desktop client that connects to your existing Django + DRF backend for the Chemical Equipment Visualizer.

Features
- Sign up / Login (JWT)
- Upload CSV files
- List recent datasets
- View dataset details (charts + table)
- Download PDF report

Setup (Windows PowerShell)
1. Open PowerShell and create + activate a virtual environment inside `desktop_app`:

```powershell
cd C:\ReactProjects\fosee\desktop_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Edit `config.py` if your backend is not at `http://127.0.0.1:8000`.

3. Run the app:

```powershell
python main.py
```

Notes
- Tokens are stored in `tokens.json` inside this folder. Remove it to log out.
- The app expects the backend endpoints described in the project (`/api/auth/login/`, `/api/signup/`, `/api/datasets/*`).

If you want, I can also:
- Add a packaged executable build (PyInstaller spec).
- Add better UX polish, themes, or embed more chart types.

Enjoy — tell me if you want tweaks or to wire additional endpoints.