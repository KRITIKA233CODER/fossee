Chemical Equipment Parameter Visualizer

FOSSEE Internship Screening Task – Hybrid Web & Desktop Application

📌 Project Description

This project is a hybrid Web and Desktop application developed as part of the FOSSEE Internship Screening Task.

The system allows users to upload CSV files containing chemical equipment parameters such as
Equipment Name, Type, Flowrate, Pressure, and Temperature.
The uploaded data is processed by a single Django backend, which performs analysis and exposes results through REST APIs.

Both the React-based Web application and the PyQt5-based Desktop application consume the same backend APIs, ensuring consistent analytics and shared business logic across platforms.

🎯 Objectives

Upload and validate CSV datasets

Perform statistical analysis using Pandas

Visualize equipment parameters using charts and tables

Maintain history of the last 5 uploaded datasets

Provide both Web and Desktop interfaces

Generate downloadable PDF analytical reports

Implement basic user authentication

🛠️ Tech Stack Used

Backend: Django, Django REST Framework

Data Processing: Pandas

Database: SQLite

Web Frontend: React.js, Chart.js

Desktop Frontend: PyQt5, Matplotlib

Version Control: Git & GitHub

🗂️ Project Structure
fosee/
│
├── backend/                # Django backend (APIs + analytics)
├── frontend-react/         # React web application
├── desktop_app/            # PyQt5 desktop application
├── sample_equipment_data.csv
├── README.md


A single Django backend is shared between both frontends.

🔐 Authentication

Both the Web and Desktop applications require authentication before accessing datasets and analytics.

Web Login Interface

Desktop Login Interface

Authentication ensures controlled access and mirrors real-world system behavior.

🌐 Web Application
Dashboard Overview

After logging in, users are redirected to the dashboard which provides:

Total dataset count

Storage usage

List of recently uploaded datasets (limited to last 5)

CSV Upload (Web)

Users can upload CSV files using a simple upload interface.
Files are validated and processed by the Django backend using Pandas.

Analytics & Visualization (Web)

Once processed, the application displays:

Average Flowrate, Pressure, and Temperature

Total number of records

Interactive charts rendered using Chart.js

Each dataset also provides quick actions to:

View analytics

Download CSV

Download PDF report

🖥️ Desktop Application (PyQt5)

The desktop application provides the same core functionality as the web version, implemented using PyQt5 and Matplotlib.

Recent Datasets View

The dashboard lists recently uploaded datasets retrieved from the same backend API.

CSV Upload (Desktop)

CSV files can be uploaded directly from the desktop interface and are processed by the shared backend.

Detailed Analytics & PDF Export (Desktop)

The analytics view displays:

Summary statistics

Parameter distributions

Correlation matrix

Analytical insights

Users can also export a PDF report containing these analytics.

📊 Backend Functionality

The Django backend is responsible for:

CSV validation (required column checks)

Data parsing and analytics using Pandas

Computing averages and distributions

Maintaining dataset history (max 5 records)

Serving REST APIs for both Web & Desktop

Generating PDF reports

All analytics are computed dynamically — no hardcoded data is used.

▶️ Demo Video

A short demo video (2–3 minutes) demonstrating:

Web application workflow

Desktop application workflow

CSV upload and analytics

PDF report generation

📽️ Demo Video Link: (Add your video link here)

🚀 Setup Instructions
Backend (Django)
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Web Frontend (React)
cd frontend-react
npm install
npm start

Desktop Application (PyQt5)
cd desktop_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

📄 Sample CSV Format
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120,2.5,60
Valve B,Valve,80,1.8,45

✅ Task Requirements Coverage

✔ Hybrid Web + Desktop application
✔ Django backend with REST APIs
✔ CSV upload & analytics
✔ Data visualization
✔ Dataset history (last 5 uploads)
✔ PDF report generation
✔ Authentication
✔ Clean and modular repository structure

👩‍💻 Author

Kritika Niranjan
B.Tech – Computer Science
GitHub: https://github.com/KRITIKA233CODER

🙏 Acknowledgement

This project was developed as part of the FOSSEE Internship Screening Task, focusing on backend-driven analytics, data visualization, and cross-platform application development.

🔍 Final Note

This submission reflects my ability to:

Work with real datasets

Design and integrate backend APIs

Build consistent applications across Web and Desktop platforms

Thank you for reviewing my submission.