import sys
import os
import time
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QStackedWidget,
    QTableWidget, QTableWidgetItem, QDialog, QProgressBar, QTextEdit,
    QTabWidget, QTabBar, QScrollArea, QFrame, QSplitter
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
# Modern Dark Theme Stylesheet
# =============================
STYLESHEET = """
QWidget {
    background-color: #0b0f1a;
    color: #f8fafc;
    font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
}

QMainWindow, QDialog, QStackedWidget {
    background-color: #0b0f1a;
}

QLabel {
    color: #94a3b8;
}

QLabel[heading="true"] {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

QLabel#subheading {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 20px;
}

QLineEdit {
    background-color: #161e2e;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 12px 16px;
    color: #ffffff;
    selection-background-color: #6366f1;
}

QLineEdit:focus {
    border: 2px solid #6366f1;
    background-color: #1e293b;
}

QPushButton {
    background-color: #1e293b;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    color: #cbd5e1;
}

QPushButton:hover {
    background-color: #2d3748;
    color: #ffffff;
    border-color: #4a5568;
}

QPushButton:pressed {
    background-color: #161e2e;
}

QPushButton#primary {
    background-color: #6366f1;
    border: none;
    color: #ffffff;
}

QPushButton#primary:hover {
    background-color: #4f46e5;
}

QPushButton#primary:pressed {
    background-color: #4338ca;
}

QPushButton#secondary {
    background-color: #1e293b;
    border: 1px solid #334155;
    color: #f8fafc;
}

QPushButton#secondary:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton#ghost {
    background-color: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
}

QPushButton#ghost:hover {
    color: #ffffff;
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
}

QPushButton#danger:hover {
    background-color: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
    border-color: #ef4444;
}

QListWidget {
    background-color: transparent;
    border: none;
}

QListWidget::item {
    background-color: #161e2e;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid #2d3748;
}

QListWidget::item:hover {
    background-color: #1e293b;
    border-color: #4a5568;
}

QListWidget::item:selected {
    background-color: #1e293b;
    border-color: #6366f1;
    color: #ffffff;
}

#Card {
    background-color: #161e2e;
    border: 1px solid #2d3748;
    border-radius: 20px;
}

#Navbar {
    background-color: #0b0f1a;
    border-bottom: 1px solid #2d3748;
}

#SearchBox {
    background-color: #161e2e;
    border-radius: 20px;
    padding: 5px 15px;
    border: 1px solid #2d3748;
}

QTableWidget {
    background-color: #161e2e;
    border: 1px solid #2d3748;
    gridline-color: #2d3748;
    border-radius: 12px;
}

QHeaderView::section {
    background-color: #1e293b;
    color: #f8fafc;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #2d3748;
    font-weight: bold;
}

QProgressBar {
    background-color: #161e2e;
    border: 1px solid #2d3748;
    border-radius: 12px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #6366f1;
    border-radius: 11px;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #2d3748;
    background-color: #0b0f1a;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #161e2e;
    color: #94a3b8;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
    font-weight: 600;
}

QTabBar::tab:hover {
    background-color: #1e293b;
    color: #ffffff;
}

QTabBar::tab:selected {
    background-color: #6366f1;
    color: #ffffff;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

#InsightPanel {
    background-color: #161e2e;
    border-radius: 12px;
    padding: 15px;
}

#InsightBadge {
    background-color: rgba(99, 102, 241, 0.1);
    color: #818cf8;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: bold;
}
"""


class DatasetItemWidget(QWidget):
    """Custom widget for dataset list items with a premium look."""
    def __init__(self, dataset):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # Icon
        icon = QLabel("📊")
        icon.setStyleSheet("font-size: 24px; background: #1e293b; border-radius: 12px; padding: 8px;")
        layout.addWidget(icon)

        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name = dataset.get('filename') or dataset.get('id') or 'Unnamed Dataset'
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; color: #f8fafc; font-size: 15px;")
        info_layout.addWidget(name_label)
        
        date_str = dataset.get('uploaded_at') or dataset.get('created_at') or 'Unknown'
        if date_str != 'Unknown' and 'T' in date_str:
            date_str = date_str.split('T')[0]

        meta = f"Rows: {dataset.get('total_rows', '0')}  •  Date: {date_str}"
        meta_label = QLabel(meta)
        meta_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info_layout.addWidget(meta_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()

        # Action hint
        chevron = QLabel("→")
        chevron.setStyleSheet("color: #4a5568; font-size: 18px; font-weight: bold;")
        layout.addWidget(chevron)


# =============================
# Login Widget
# =============================
class LoginWidget(QWidget):
    def __init__(self, client: ApiClient, on_logged):
        super().__init__()
        self.client = client
        self.on_logged = on_logged

        # Main centering layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)

        card = QWidget()
        card.setObjectName("Card")
        card.setFixedWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        title = QLabel("Welcome Back")
        title.setProperty("heading", "true")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        sub = QLabel("Sign in to your FOSSEE account")
        sub.setObjectName("subheading")
        sub.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(sub)

        card_layout.addWidget(QLabel("Username"))
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        card_layout.addWidget(self.username)

        card_layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        self.password.setPlaceholderText("••••••••")
        self.password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password)

        card_layout.addSpacing(10)
        
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("primary")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.login)
        card_layout.addWidget(login_btn)

        card_layout.addSpacing(5)

        signup_btn = QPushButton("Create New Account")
        signup_btn.setObjectName("ghost")
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.clicked.connect(self.signup)
        card_layout.addWidget(signup_btn)

        self.msg = QLabel("")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setStyleSheet("color: #fb7185; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(self.msg)

        outer_layout.addWidget(card)

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

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Upload "Card"
        card = QWidget()
        card.setObjectName("Card")
        card.setFixedWidth(500)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        icon = QLabel("☁️")
        icon.setStyleSheet("font-size: 64px; margin-bottom: 10px; color: #6366f1;")
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)

        title = QLabel("Upload Dataset")
        title.setProperty("heading", "true")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.file_label = QLabel("Select a CSV file to begin analysis")
        self.file_label.setStyleSheet("color: #64748b; font-size: 14px;")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setWordWrap(True)
        card_layout.addWidget(self.file_label)

        card_layout.addSpacing(10)

        choose_btn = QPushButton("Browse Computer")
        choose_btn.setFixedHeight(45)
        choose_btn.setCursor(Qt.PointingHandCursor)
        choose_btn.clicked.connect(self.choose)
        card_layout.addWidget(choose_btn)

        self.upload_btn = QPushButton("Start Processing")
        self.upload_btn.setObjectName("primary")
        self.upload_btn.setFixedHeight(45)
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload)
        card_layout.addWidget(self.upload_btn)

        self.back_btn_upload = QPushButton("← Back to Dashboard")
        self.back_btn_upload.setObjectName("ghost")
        self.back_btn_upload.setFixedHeight(40)
        self.back_btn_upload.setCursor(Qt.PointingHandCursor)
        # We'll connect this in MainWindow or pass a callback
        card_layout.addWidget(self.back_btn_upload)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(12)
        card_layout.addWidget(self.progress)

        outer_layout.addWidget(card)

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

        self.setWindowTitle(f"Analysis — {dataset.get('filename') or dataset.get('id')}")
        self.resize(1100, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header: Filename & Summary Metrics
        header_widget = QWidget()
        header = QHBoxLayout(header_widget)
        header.setContentsMargins(0, 0, 0, 0)
        
        title_v = QVBoxLayout()
        title = QLabel(dataset.get("filename") or dataset.get("id"))
        title.setProperty("heading", "true")
        title_v.addWidget(title)
        
        info = QLabel(f"Dataset ID: {dataset.get('id')}  •  Total Rows: {dataset.get('total_rows', 'Unknown')}")
        info.setStyleSheet("color: #64748b; font-size: 13px;")
        title_v.addWidget(info)
        header.addLayout(title_v)
        
        header.addStretch()
        
        self.download_btn = QPushButton("Export PDF")
        self.download_btn.setObjectName("primary")
        self.download_btn.clicked.connect(self.download_pdf)
        header.addWidget(self.download_btn)

        self.maximize_btn = QPushButton("⛶")
        self.maximize_btn.setFixedSize(35, 35)
        self.maximize_btn.setObjectName("ghost")
        self.maximize_btn.setToolTip("Toggle Fullscreen")
        self.maximize_btn.clicked.connect(self.toggle_fullscreen)
        header.addWidget(self.maximize_btn)
        
        main_layout.addWidget(header_widget)

        # Tabs
        self.tabs = QTabWidget()
        
        # TAB 1: Analytics Dashboard
        self.analytics_tab = QWidget()
        anal_main = QVBoxLayout(self.analytics_tab)
        anal_main.setContentsMargins(15, 15, 15, 15)
        anal_main.setSpacing(20)

        # Top Snapshot Bar
        self.metrics_bar = QFrame()
        self.metrics_bar.setObjectName("Card")
        self.metrics_bar.setFixedHeight(80)
        self.metrics_layout = QHBoxLayout(self.metrics_bar)
        self.metrics_layout.setContentsMargins(20, 0, 20, 0)
        anal_main.addWidget(self.metrics_bar)

        anal_content = QHBoxLayout()
        anal_content.setSpacing(20)
        
        # Left: Charts
        plot_card = QFrame()
        plot_card.setObjectName("Card")
        plot_v = QVBoxLayout(plot_card)
        self.canvas = FigureCanvas(Figure(figsize=(8, 6), facecolor='#0b0f1a'))
        plot_v.addWidget(self.canvas)
        anal_content.addWidget(plot_card, 3)
        
        # Right: Insights Panel
        right_panel = QWidget()
        right_v = QVBoxLayout(right_panel)
        right_v.setContentsMargins(0, 0, 0, 0)
        
        ins_title = QLabel("ANALYTICAL INSIGHTS")
        ins_title.setStyleSheet("font-weight: 800; color: #6366f1; font-size: 11px; letter-spacing: 1px;")
        right_v.addWidget(ins_title)
        
        self.ins_scroll = QScrollArea()
        self.ins_container = QWidget()
        self.ins_v = QVBoxLayout(self.ins_container)
        self.ins_v.setSpacing(15)
        self.ins_v.setAlignment(Qt.AlignTop)
        self.ins_scroll.setWidget(self.ins_container)
        self.ins_scroll.setWidgetResizable(True)
        right_v.addWidget(self.ins_scroll)
        anal_content.addWidget(right_panel, 1)
        
        anal_main.addLayout(anal_content)
        
        self.tabs.addTab(self.analytics_tab, "🚀 Analytics Dashboard")
        
        # TAB 2: Explore Data
        self.data_tab = QWidget()
        data_layout = QVBoxLayout(self.data_tab)
        data_layout.setContentsMargins(15, 15, 15, 15)
        data_layout.setSpacing(15)
        
        # Table Search
        table_top = QHBoxLayout()
        search_ico = QLabel("🔍")
        table_top.addWidget(search_ico)
        self.table_search = QLineEdit()
        self.table_search.setPlaceholderText("Filter rows...")
        self.table_search.setStyleSheet("max-width: 300px; height: 35px;")
        table_top.addWidget(self.table_search)
        table_top.addStretch()
        data_layout.addLayout(table_top)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget { background-color: #161e2e; }")
        self.table.horizontalHeader().setStretchLastSection(True)
        data_layout.addWidget(self.table)
        
        self.tabs.addTab(self.data_tab, "📋 Raw Data Explorer")
        
        main_layout.addWidget(self.tabs)

        # Footer Actions
        footer = QHBoxLayout()
        back_btn = QPushButton("← Return to Dashboard")
        back_btn.setObjectName("ghost")
        back_btn.setFixedWidth(200)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.accept)
        footer.addWidget(back_btn)
        footer.addStretch()
        main_layout.addLayout(footer)
        
        self.refresh()

    def toggle_fullscreen(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def refresh(self):
        try:
            summary = self.client.get_summary(self.dataset["id"]) or {}
            hist = summary.get("histograms", {})
            corr = summary.get("correlation_matrix") or summary.get("correlation", {})
            insights = summary.get("insights") or []
            top_values = summary.get("top_values") or {}

            # Theme colors
            bg_color = '#0b0f1a'
            text_color = '#f8fafc'
            accent_color = '#6366f1'
            muted_color = '#64748b'

            # Clear metrics bar
            for i in reversed(range(self.metrics_layout.count())):
                widget = self.metrics_layout.itemAt(i).widget()
                if widget: widget.setParent(None)
                else: 
                    # handle layout items
                    li = self.metrics_layout.itemAt(i)
                    if li.layout(): 
                        # skip layouts for now as we just add widgets
                        pass

            def add_metric(label, value, icon="⚡"):
                m_v = QVBoxLayout()
                m_v.setSpacing(2)
                l1 = QLabel(label.upper())
                l1.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 0.5px;")
                m_v.addWidget(l1)
                l2 = QLabel(f"{icon} {value}")
                l2.setStyleSheet("color: #f8fafc; font-size: 18px; font-weight: bold;")
                m_v.addWidget(l2)
                self.metrics_layout.addLayout(m_v)
                self.metrics_layout.addSpacing(40)

            add_metric("Total Rows", str(self.dataset.get('total_rows', 0)), icon="📊")
            add_metric("Avg Flow", f"{self.dataset.get('avg_flowrate', 0):.2f}", icon="💧")
            add_metric("Avg Pres", f"{self.dataset.get('avg_pressure', 0):.2f}", icon="💨")
            add_metric("Avg Temp", f"{self.dataset.get('avg_temperature', 0):.2f}", icon="🔥")
            self.metrics_layout.addStretch()

            # Update Charts
            fig = self.canvas.figure
            fig.clear()
            fig.set_facecolor(bg_color)
            
            # Use GridSpec for better control
            from matplotlib.gridspec import GridSpec
            gs = GridSpec(2, 3, figure=fig, height_ratios=[1, 1.2])
            
            # Histograms on top
            axs_top = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])]
            # Heatmap on bottom (centered)
            ax_heat = fig.add_subplot(gs[1, :])

            numeric_keys = ["flowrate", "pressure", "temperature"]
            for i, key in enumerate(numeric_keys):
                ax = axs_top[i]
                ax.clear()
                ax.set_facecolor('#161e2e')
                ax.tick_params(colors=muted_color, labelsize=8)
                for spine in ax.spines.values():
                    spine.set_color('#2d3748')

                hk = hist.get(key, {})
                if isinstance(hk, dict) and hk.get("counts"):
                    bins = hk.get("bins", [])
                    counts = hk.get("counts", [])
                    if bins and counts:
                        lefts = bins[:-1]
                        widths = [bins[j+1] - bins[j] for j in range(len(bins) - 1)]
                        ax.bar(lefts, counts, width=widths, align="edge", color=accent_color, alpha=0.8)
                        ax.set_title(key.title(), color=text_color, fontsize=10, fontweight='bold')
                else:
                    t = self.client.get_table(self.dataset["id"]) or {}
                    rows = t.get("rows", [])
                    vals = []
                    for r in rows:
                        try:
                            vals.append(float(r.get(key) or r.get(key.title()) or 0))
                        except Exception:
                            pass
                    if vals:
                        ax.hist(vals, bins=12, color=accent_color, alpha=0.8)
                        ax.set_title(key.title(), color=text_color, fontsize=10, fontweight='bold')

            # correlation heatmap
            ax_heat.clear()
            ax_heat.set_facecolor(bg_color)
            if corr:
                try:
                    import pandas as _pd
                    df_corr = _pd.DataFrame(corr)
                    sns.heatmap(df_corr, ax=ax_heat, annot=True, fmt='.2f', cmap='magma', 
                                cbar=True, annot_kws={"size": 9})
                    ax_heat.set_title('Feature Correlation Matrix', color=text_color, fontsize=12, fontweight='bold', pad=15)
                    ax_heat.tick_params(colors=muted_color, labelsize=9)
                except Exception:
                    ax_heat.text(0.5, 0.5, 'Error loading correlation map', ha='center', color=muted_color)
            else:
                ax_heat.text(0.5, 0.5, 'No correlation data available', ha='center', color=muted_color)

            self.canvas.draw()

            # Clear old insights
            for i in reversed(range(self.ins_v.count())): 
                widget = self.ins_v.itemAt(i).widget()
                if widget: widget.setParent(None)

            # Add Insights
            if insights:
                for ins in (insights if isinstance(insights, list) else [insights]):
                    card = QFrame()
                    card.setObjectName("InsightPanel")
                    card_v = QVBoxLayout(card)
                    
                    badge_h = QHBoxLayout()
                    badge = QLabel("INSIGHT")
                    badge.setObjectName("InsightBadge")
                    badge_h.addWidget(badge)
                    badge_h.addStretch()
                    card_v.addLayout(badge_h)
                    
                    text = QLabel(str(ins))
                    text.setWordWrap(True)
                    text.setStyleSheet("color: #f8fafc; font-size: 13px; line-height: 1.4;")
                    card_v.addWidget(text)
                    self.ins_v.addWidget(card)

            # Add Stats
            if top_values:
                card = QFrame()
                card.setObjectName("InsightPanel")
                card_v = QVBoxLayout(card)
                
                badge_h = QHBoxLayout()
                badge = QLabel("DATA HIGHLIGHTS")
                badge.setObjectName("InsightBadge")
                badge_h.addWidget(badge)
                badge_h.addStretch()
                card_v.addLayout(badge_h)
                
                for k, v in top_values.items():
                    val_str = str(v)[:40] + ("..." if len(str(v)) > 40 else "")
                    row = QLabel(f"<span style='color:#64748b;'>{k.title()}:</span> <span style='color:#cbd5e1;'>{val_str}</span>")
                    row.setStyleSheet("font-size: 12px; margin-top: 2px;")
                    card_v.addWidget(row)
                self.ins_v.addWidget(card)

            # Fill table
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
                    item = QTableWidgetItem(str(r.get(c, "")))
                    item.setForeground(Qt.white)
                    self.table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.warning(self, "Load Error", str(e))

    def download_pdf(self):
        base_name = self.dataset.get('filename') or str(self.dataset.get('id', 'report'))
        if base_name.lower().endswith('.csv'):
            base_name = base_name[:-4]
            
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            f"{base_name}.pdf",
            "PDF Files (*.pdf)"
        )
        if dest:
            try:
                self.client.download_report(self.dataset["id"], dest)
                QMessageBox.information(self, "Saved", "PDF saved")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def download_csv(self):
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Save Cleaned CSV",
            f"cleaned_{self.dataset.get('filename') or self.dataset.get('id')}.csv",
            "CSV Files (*.csv)"
        )
        if dest:
            try:
                self.client.download_clean_csv(self.dataset["id"], dest)
                QMessageBox.information(self, "Saved", "Cleaned CSV saved successfully")
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Dashboard Header
        head_layout = QHBoxLayout()
        
        title_v = QVBoxLayout()
        title = QLabel("Recent Datasets")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        title_v.addWidget(title)
        
        desc = QLabel("Analyze and visualize your chemical equipment data")
        desc.setStyleSheet("color: #64748b; font-size: 13px;")
        title_v.addWidget(desc)
        head_layout.addLayout(title_v)
        
        head_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFixedWidth(120)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load)
        head_layout.addWidget(refresh_btn)
        
        layout.addLayout(head_layout)

        # Search Bar Simulation
        search_container = QWidget()
        search_container.setObjectName("SearchBox")
        search_container.setFixedHeight(45)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 15, 0)
        
        search_icon = QLabel("🔍")
        search_layout.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search datasets by name...")
        self.search_input.setStyleSheet("background: transparent; border: none; padding: 0;")
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_container)

        # List section
        self.list = QListWidget()
        self.list.setFrameShape(QListWidget.NoFrame)
        self.list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list.itemDoubleClicked.connect(self.open_selected)
        
        layout.addWidget(self.list)
        self.load()

    def load(self):
        try:
            resp = self.client.list_datasets()
            data = resp.get("results") if isinstance(resp, dict) else resp
            self._all_items = data or []
            self.apply_filter()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_search(self):
        self.apply_filter()

    def apply_filter(self):
        query = self.search_input.text().lower().strip()
        filtered = []
        for d in self._all_items:
            name = (d.get('filename') or d.get('id') or "").lower()
            if query in name:
                filtered.append(d)
        
        self.display_data(filtered)

    def display_data(self, data):
        self._current_items = data
        self.list.clear()
        for d in data:
            item = QListWidgetItem(self.list)
            custom_widget = DatasetItemWidget(d)
            item.setSizeHint(custom_widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, custom_widget)

    def open_selected(self):
        idx = self.list.currentRow()
        if idx >= 0:
            self.open_fn(self._current_items[idx])


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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar (Navigation)
        top_widget = QWidget()
        top_widget.setObjectName("Navbar")
        top_widget.setFixedHeight(80)
        top = QHBoxLayout(top_widget)
        top.setContentsMargins(30, 0, 30, 0)
        top.setSpacing(20)

        brand_layout = QHBoxLayout()
        logo = QLabel("◢")
        logo.setStyleSheet("font-size: 24px; color: #6366f1; font-weight: bold;")
        brand_layout.addWidget(logo)
        
        brand = QLabel("FOSSEE")
        brand.setStyleSheet("font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: 1px;")
        brand_layout.addWidget(brand)
        top.addLayout(brand_layout)

        top.addStretch()

        self.nav_btns = QHBoxLayout()
        self.nav_btns.setSpacing(10)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.setObjectName("primary")
        self.btn_login.setFixedHeight(40)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.show_login)
        self.nav_btns.addWidget(self.btn_login)

        self.btn_upload = QPushButton("Upload CSV")
        self.btn_upload.setFixedHeight(40)
        self.btn_upload.setCursor(Qt.PointingHandCursor)
        self.btn_upload.clicked.connect(self.show_upload)
        self.nav_btns.addWidget(self.btn_upload)
        
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setObjectName("ghost")
        self.btn_logout.setFixedHeight(40)
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.clicked.connect(self.logout)
        self.nav_btns.addWidget(self.btn_logout)

        top.addLayout(self.nav_btns)

        layout.addWidget(top_widget)

        # Initial Nav Visibility
        self.update_nav_visibility(bool(self.client.access))

        # Stacked pages
        container = QWidget()
        inner_layout = QVBoxLayout(container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.login_widget = LoginWidget(self.client, self.on_logged)
        self.upload_widget = UploadWidget(self.client, self.on_uploaded)
        self.dashboard_widget = DashboardWidget(self.client, self.open_dataset)

        self.stack.addWidget(self.dashboard_widget)
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.upload_widget)
        
        # Connect Back buttons
        self.upload_widget.back_btn_upload.clicked.connect(self.show_dashboard)

        inner_layout.addWidget(self.stack)
        layout.addWidget(container)
        
        self.setLayout(layout)

        if self.client.access:
            self.stack.setCurrentWidget(self.dashboard_widget)
        else:
            self.stack.setCurrentWidget(self.login_widget)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_widget)

    def show_upload(self):
        self.stack.setCurrentWidget(self.upload_widget)

    def show_dashboard(self):
        self.dashboard_widget.load()
        self.stack.setCurrentWidget(self.dashboard_widget)

    def on_logged(self):
        self.update_nav_visibility(True)
        self.dashboard_widget.load()
        self.stack.setCurrentWidget(self.dashboard_widget)

    def on_uploaded(self, ds_id):
        self.dashboard_widget.load()
        if ds_id:
            for d in self.dashboard_widget._all_items:
                if str(d.get("id")) == str(ds_id):
                    self.open_dataset(d)
                    break

    def open_dataset(self, d):
        dlg = DatasetDialog(self.client, d)
        dlg.exec()

    def logout(self):
        self.client.clear_tokens()
        self.update_nav_visibility(False)
        QMessageBox.information(self, "Logout", "Logged out")
        self.stack.setCurrentWidget(self.login_widget)

    def update_nav_visibility(self, logged_in: bool):
        self.btn_login.setVisible(not logged_in)
        self.btn_upload.setVisible(logged_in)
        self.btn_logout.setVisible(logged_in)


# =============================
# Entry Point
# =============================
if __name__ == "__main__":
    try:
        print("Starting QApplication...", flush=True)
        _log("Starting QApplication")

        app = QApplication(sys.argv)
        app.setStyleSheet(STYLESHEET)

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
