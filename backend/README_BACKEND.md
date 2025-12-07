# Backend (Django + DRF)

This backend implements CSV upload and analytics for the Chemical Equipment Parameter Visualizer.

Requirements
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

Quickstart (local dev)
1. Create and activate a virtualenv

```powershell
python -m venv .venv; .\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run migrations and create superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

3. Run the dev server

```powershell
python manage.py runserver
```

4. Use the JWT auth endpoint to obtain access and refresh tokens:

POST `/api/auth/login/` with `username` and `password` -> returns `{ "access": "...", "refresh": "..." }`
Use the refresh token endpoint to refresh the access token:

POST `/api/auth/refresh/` with `refresh` -> returns `{ "access": "..." }`

5. Upload CSV (authenticated):

POST `/api/datasets/upload/` form-data `file` with header `Authorization: Bearer <access_token>` -> returns dataset id + summary

Useful endpoints
- `GET /api/datasets/` -> list last 5 datasets
- `GET /api/datasets/{id}/summary/` -> JSON summary
- `GET /api/datasets/{id}/table/?page=1&page_size=50` -> paginated rows
- `GET /api/datasets/{id}/report/` -> download PDF report

Notes
- Uploaded CSVs and generated PDFs are stored under `media/uploads/` and `media/reports/`.
- The backend trims older datasets to keep only the 5 most recent entries.
- Tests: `python manage.py test datasets`
