import sys
import os
import time
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QListWidget, QMessageBox, QStackedWidget,
    QTableWidget, QTableWidgetItem, QDialog, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt

# Matplotlib Qt5 backend
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import numpy as np
import seaborn as sns
from api_client import ApiClient

# Logging
_log_path = os.path.join(os.path.dirname(__file__), 'desktop_app_run.log')
def _log(msg: str):
    try:
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except:
        pass

_log("main.py imported")


# =============================
# Login Widget
# =============================
class LoginWidget(QWidget):
    def __init__(self, client: ApiClient, on_logged):
        super().__init__()
        self.client = client
        self.on_logged = on_logged

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username"))

        self.username = QLineEdit()
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        from PyQt5.QtWidgets import QLineEdit as _QLE
        try:
            # PyQt5 echo mode
            self.password.setEchoMode(_QLE.Password)
        except Exception:
            try:
                self.password.setEchoMode(QLineEdit.EchoMode.Password)
            except Exception:
                pass
        layout.addWidget(self.password)

        btns = QHBoxLayout()

        login = QPushButton("Login")
        login.clicked.connect(self.login)
        btns.addWidget(login)

        signup = QPushButton("Sign Up")
        signup.clicked.connect(self.signup)
        btns.addWidget(signup)

        layout.addLayout(btns)
        self.msg = QLabel("")
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        if not u or not p:
            self.msg.setText("Enter username & password")
            return

        try:
            self.client.login(u, p)
            self.msg.setText("Logged in")
            self.on_logged()
        except Exception as e:
            self.msg.setText("Login failed: " + str(e))

    def signup(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        if not u or not p:
            self.msg.setText("Enter username & password")
            return

        try:
            self.client.signup(u, "", p)
            self.msg.setText("Signup successful")
            self.on_logged()
        except Exception as e:
            self.msg.setText("Signup failed: " + str(e))


# =============================
# Upload Widget
# =============================
class UploadWidget(QWidget):
    def __init__(self, client: ApiClient, on_uploaded):
        super().__init__()
        self.client = client
        self.on_uploaded = on_uploaded
        self.path = None

        layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        btns = QHBoxLayout()

        choose = QPushButton("Choose CSV")
        choose.clicked.connect(self.choose)
        btns.addWidget(choose)

        upload = QPushButton("Upload")
        upload.clicked.connect(self.upload)
        btns.addWidget(upload)

        layout.addLayout(btns)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def choose(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", os.path.expanduser("~"), "CSV Files (*.csv)"
        )
        if p:
            self.path = p
            self.file_label.setText(os.path.basename(p))

    def upload(self):
        if not self.path:
            QMessageBox.warning(self, "Upload", "Select a file first")
            return

        try:
            self.progress.setVisible(True)
            self.progress.setValue(30)
            resp = self.client.upload_csv(self.path)
            self.progress.setValue(100)

            QMessageBox.information(self, "Success", "File uploaded")

            if isinstance(resp, dict):
                self.on_uploaded(resp.get("id"))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.progress.setVisible(False)


# =============================
# Dataset Dialog
# =============================
class DatasetDialog(QDialog):
    def __init__(self, client: ApiClient, dataset):
        super().__init__()
        self.client = client
        self.dataset = dataset

        self.setWindowTitle(dataset.get("filename") or dataset.get("id"))
        self.resize(1000, 700)

        layout = QVBoxLayout()

        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btns = QHBoxLayout()

        dl = QPushButton("Download PDF")
        dl.clicked.connect(self.download_pdf)
        btns.addWidget(dl)

        close = QPushButton("Close")
        close.clicked.connect(self.accept)
        btns.addWidget(close)

        layout.addLayout(btns)
        self.setLayout(layout)

        self.refresh()

    def refresh(self):
        try:
            summary = self.client.get_summary(self.dataset["id"]) or {}
            hist = summary.get("histograms", {})
            corr = summary.get("correlation_matrix") or summary.get("correlation", {})
            insights = summary.get("insights") or []
            top_values = summary.get("top_values") or {}

            # prepare figure: 2 rows x 3 cols (3 histograms on top, heatmap + texts below)
            fig = self.canvas.figure
            fig.clear()
            axs = fig.subplots(2, 3, constrained_layout=True)

            numeric_keys = ["flowrate", "pressure", "temperature"]
            for i, key in enumerate(numeric_keys):
                ax = axs[0, i]
                ax.clear()
                # try server-provided histogram
                hk = hist.get(key, {})
                if isinstance(hk, dict) and hk.get("counts"):
                    bins = hk.get("bins", [])
                    counts = hk.get("counts", [])
                    if bins and counts:
                        lefts = bins[:-1]
                        widths = [bins[j+1] - bins[j] for j in range(len(bins) - 1)]
                        ax.bar(lefts, counts, width=widths, align="edge")
                        ax.set_title(key.title())
                else:
                    # fallback to reading table values
                    t = self.client.get_table(self.dataset["id"]) or {}
                    rows = t.get("rows", [])
                    vals = []
                    for r in rows:
                        try:
                            vals.append(float(r.get(key) or r.get(key.title()) or 0))
                        except Exception:
                            pass
                    if vals:
                        ax.hist(vals, bins=12)
                        ax.set_title(key.title())

            # correlation heatmap in bottom-left
            ax_heat = axs[1, 0]
            ax_heat.clear()
            if corr:
                # corr might be dict-of-dict
                try:
                    import pandas as _pd
                    df_corr = _pd.DataFrame(corr)
                    sns.heatmap(df_corr, ax=ax_heat, annot=True, fmt='.2f', cmap='coolwarm')
                    ax_heat.set_title('Correlation')
                except Exception:
                    ax_heat.text(0.5, 0.5, 'Correlation unavailable', ha='center')
            else:
                ax_heat.text(0.5, 0.5, 'No correlation data', ha='center')

            # insights text
            ax_ins = axs[1, 1]
            ax_ins.clear()
            ax_ins.axis('off')
            ins_text = ''
            if isinstance(insights, (list, tuple)):
                ins_text = '\n'.join(str(x) for x in insights[:12])
            elif isinstance(insights, str):
                ins_text = insights
            ax_ins.text(0, 1, 'Insights:\n' + ins_text, va='top', wrap=True, fontsize=9)

            # top values
            ax_top = axs[1, 2]
            ax_top.clear()
            ax_top.axis('off')
            tv_lines = []
            if isinstance(top_values, dict):
                for k, v in top_values.items():
                    line = f"{k.title()}: "
                    try:
                        if isinstance(v, dict):
                            top = v.get('top') or v.get('max') or []
                            low = v.get('low') or v.get('min') or []
                            s = f"top={top[:3]}, low={low[:3]}"
                        elif isinstance(v, list):
                            s = str(v[:3])
                        else:
                            s = str(v)
                    except Exception:
                        s = str(v)
                    tv_lines.append(line + s)
            ax_top.text(0, 1, 'Top Values:\n' + '\n'.join(tv_lines[:12]), va='top', fontsize=9)

            self.canvas.draw()

            # Fill table (keep below plots)
            tb = self.client.get_table(self.dataset["id"]) or {}
            rows = tb.get("rows", [])
            cols = list(rows[0].keys()) if rows else []

            self.table.clear()
            self.table.setColumnCount(len(cols))
            self.table.setRowCount(len(rows))
            if cols:
                self.table.setHorizontalHeaderLabels(cols)

            for i, r in enumerate(rows):
                for j, c in enumerate(cols):
                    self.table.setItem(i, j, QTableWidgetItem(str(r.get(c, ""))))

        except Exception as e:
            QMessageBox.warning(self, "Load Error", str(e))

    def download_pdf(self):
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            f"{self.dataset.get('filename')}.pdf",
            "PDF Files (*.pdf)"
        )
        if dest:
            try:
                self.client.download_report(self.dataset["id"], dest)
                QMessageBox.information(self, "Saved", "PDF saved")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))


# =============================
# Dashboard
# =============================
class DashboardWidget(QWidget):
    def __init__(self, client, open_fn):
        super().__init__()
        self.client = client
        self.open_fn = open_fn

        layout = QVBoxLayout()

        btn = QPushButton("Refresh")
        btn.clicked.connect(self.load)
        layout.addWidget(btn)

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.open_selected)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.load()

    def load(self):
        try:
            resp = self.client.list_datasets()
            data = resp.get("results") if isinstance(resp, dict) else resp
            data = data or []
            self._items = data

            self.list.clear()
            for d in data:
                disp = f"{d.get('filename')} — rows: {d.get('total_rows', '?')}"
                self.list.addItem(disp)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_selected(self):
        idx = self.list.currentRow()
        if idx >= 0:
            self.open_fn(self._items[idx])


# =============================
# Main Window
# =============================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        _log("MainWindow created")

        self.client = ApiClient()

        self.setWindowTitle("Chemical Equipment Visualizer — Desktop")
        self.resize(900, 700)

        layout = QVBoxLayout()

        # Top bar
        top = QHBoxLayout()

        login = QPushButton("Login")
        login.clicked.connect(self.show_login)
        top.addWidget(login)

        logout = QPushButton("Logout")
        logout.clicked.connect(self.logout)
        top.addWidget(logout)

        upload = QPushButton("Upload CSV")
        upload.clicked.connect(self.show_upload)
        top.addWidget(upload)

        layout.addLayout(top)

        # Stacked pages
        self.stack = QStackedWidget()
        self.login_widget = LoginWidget(self.client, self.on_logged)
        self.upload_widget = UploadWidget(self.client, self.on_uploaded)
        self.dashboard_widget = DashboardWidget(self.client, self.open_dataset)

        self.stack.addWidget(self.dashboard_widget)
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.upload_widget)

        layout.addWidget(self.stack)
        self.setLayout(layout)

        if self.client.access:
            self.stack.setCurrentWidget(self.dashboard_widget)
        else:
            self.stack.setCurrentWidget(self.login_widget)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_widget)

    def show_upload(self):
        self.stack.setCurrentWidget(self.upload_widget)

    def on_logged(self):
        self.dashboard_widget.load()
        self.stack.setCurrentWidget(self.dashboard_widget)

    def on_uploaded(self, ds_id):
        self.dashboard_widget.load()
        if ds_id:
            for d in self.dashboard_widget._items:
                if str(d.get("id")) == str(ds_id):
                    self.open_dataset(d)
                    break

    def open_dataset(self, d):
        dlg = DatasetDialog(self.client, d)
        dlg.exec()

    def logout(self):
        self.client.clear_tokens()
        QMessageBox.information(self, "Logout", "Logged out")
        self.stack.setCurrentWidget(self.login_widget)


# =============================
# Entry Point
# =============================
if __name__ == "__main__":
    try:
        print("Starting QApplication...", flush=True)
        _log("Starting QApplication")

        app = QApplication(sys.argv)

        w = MainWindow()
        w.show()
        _log("MainWindow shown")

        ret = app.exec_()
        sys.exit(ret)

    except Exception as e:
        import traceback
        traceback.print_exc()
        _log("ERROR: " + str(e))
        print("ERROR:", e)
        sys.exit(1)
