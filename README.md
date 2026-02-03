# Chemical Equipment Parameter Visualizer

## FOSSEE Internship Screening Task – Hybrid Web & Desktop Application

### 📌 Project Description

- This project is a hybrid Web and Desktop application developed as part of the FOSSEE Internship Screening Task.

- The system allows users to upload CSV files containing chemical equipment parameters such as
     - Equipment Name,
     - Type,
     - Flowrate,
     - Pressure,
     - Temperature.
- The uploaded data is processed by a single Django backend, which performs analysis and exposes results through REST APIs.

- Both the React-based Web application and the PyQt5-based Desktop application consume the same backend APIs, ensuring consistent analytics and shared business logic across platforms.

### 🎯 Objectives

1. Upload and validate CSV datasets
2. Perform statistical analysis using Pandas
3. Visualize equipment parameters using charts and tables
4. Maintain history of the last 5 uploaded datasets
5. Provide both Web and Desktop interfaces
6. Generate downloadable PDF analytical reports
7. Implement basic user authentication

### 🛠️ Tech Stack Used

1. Backend: Django, Django REST Framework
2. Data Processing: Pandas
3. Database: SQLite
4. Web Frontend: React.js, Chart.js
5. Desktop Frontend: PyQt5, Matplotlib
6. Version Control: Git & GitHub

### 🗂️ Project Structure
```
fosee/
│
├── backend/                # Django backend (APIs + analytics)
├── frontend-react/         # React web application
├── desktop_app/            # PyQt5 desktop application
├── sample_equipment_data.csv
├── README.md
```


- A single Django backend is shared between both frontends.

### 🔐 Authentication

- Both the Web and Desktop applications require authentication before accessing datasets and analytics.

1. Web Login Interface
2. Desktop Login Interface
3. Authentication ensures controlled access and mirrors real-world system behavior.

### 🌐 Web Application
- Dashboard Overview
-  After logging in, users are redirected to the dashboard which provides:
   1. Total dataset count
   2. Storage usage
   3. List of recently uploaded datasets (limited to last 5)

- CSV Upload (Web)
  1. Users can upload CSV files using a simple upload interface.
  2. Files are validated and processed by the Django backend using Pandas.

- Analytics & Visualization (Web)
  1. Once processed, the application displays:
       1. Average Flowrate,
       2. Pressure, and
       3. Temperature
  2. Total number of records
  3. Interactive charts rendered using Chart.js
  4. Each dataset also provides quick actions to:
  5. View analytics
  6. Download CSV
  7. Download PDF report

### 🖥️ Desktop Application (PyQt5)
The desktop application provides the same core functionality as the web version, implemented using PyQt5 and Matplotlib.

1. Recent Datasets View
  1. The dashboard lists recently uploaded datasets retrieved from the same backend API.
  2. CSV Upload (Desktop)
  3. CSV files can be uploaded directly from the desktop interface and are processed by the shared backend.
  4. Detailed Analytics & PDF Export (Desktop)
  5. The analytics view displays:
    1. Summary statistics
    2. Parameter distributions
    3. Correlation matrix
    4. Analytical insights
  6. Users can also export a PDF report containing these analytics.

### 📊 Backend Functionality
The Django backend is responsible for:
1. CSV validation (required column checks)
2. Data parsing and analytics using Pandas
3. Computing averages and distributions
4. Maintaining dataset history (max 5 records)
5. Serving REST APIs for both Web & Desktop
6. Generating PDF reports
7. All analytics are computed dynamically — no hardcoded data is used.

### ▶️ Demo Video
- A short demo video (2–3 minutes) demonstrating:
  1. Web application workflow
  2. Desktop application workflow
  3. CSV upload and analytics
  4. PDF report generation

- 📽️ Demo Video Link: (Add your video link here)

### 🚀 Setup Instructions
1. Backend (Django)
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. Web Frontend (React)
```powershell
cd frontend-react
npm install
npm start
```

3. Desktop Application (PyQt5)
```powershell
cd desktop_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 📄 Sample CSV Format
Equipment | Name | Type | Flowrate | Pressure | Temperature
Pump A | Pump | 120 | 2.5 | 60
Valve B | Valve | 80 | 1.8 | 45

### ✅ Task Requirements Coverage

1. ✔ Hybrid Web + Desktop application
2. ✔ Django backend with REST APIs
3. ✔ CSV upload & analytics
4. ✔ Data visualization
5. ✔ Dataset history (last 5 uploads)
6. ✔ PDF report generation
7. ✔ Authentication
8. ✔ Clean and modular repository structure

### 👩‍💻 Author

Kritika Niranjan
B.Tech – Computer Science
GitHub: https://github.com/KRITIKA233CODER

### 🙏 Acknowledgement

This project was developed as part of the FOSSEE Internship Screening Task, focusing on backend-driven analytics, data visualization, and cross-platform application development.

### 🔍 Final Note

This submission reflects my ability to

Work with real datasets

Design and integrate backend APIs

Build consistent applications across Web and Desktop platforms

Thank you for reviewing my submission.
