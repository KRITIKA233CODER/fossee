import os
import uuid
import tempfile
import shutil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.conf import settings
from .models import Dataset
from .analytics import analyze_dataframe, clean_dataframe

REQUIRED_COLUMNS = ['equipment name', 'type', 'flowrate', 'pressure', 'temperature']


def ensure_media_dirs():
    uploads = os.path.join(settings.MEDIA_ROOT, 'uploads')
    reports = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(uploads, exist_ok=True)
    os.makedirs(reports, exist_ok=True)
    return uploads, reports


def validate_and_read_csv(infile):
    # Read with pandas, check columns case-insensitively
    try:
        df = pd.read_csv(infile)
    except Exception as e:
        raise ValueError(f'Error reading CSV: {e}')

    # Normalize columns
    cols_lower = [c.strip().lower() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in cols_lower]
    if missing:
        raise ValueError(f'Missing required columns: {missing}. Found columns: {df.columns.tolist()}')

    # Map existing columns to canonical names
    col_map = {}
    for orig in df.columns:
        lower = orig.strip().lower()
        if lower in REQUIRED_COLUMNS:
            col_map[orig] = lower

    df = df.rename(columns=col_map)

    # Coerce numeric columns
    numeric_cols = ['flowrate', 'pressure', 'temperature']
    coercion_errors = {}
    for col in numeric_cols:
        # Coerce and note NaNs
        coerced = pd.to_numeric(df[col], errors='coerce')
        n_invalid = coerced.isna().sum()
        coercion_errors[col] = int(n_invalid)
        df[col] = coerced

    return df, coercion_errors


def compute_summary_from_df(df):
    total = len(df)
    avg_flow = float(df['flowrate'].mean(skipna=True)) if total > 0 else None
    avg_pressure = float(df['pressure'].mean(skipna=True)) if total > 0 else None
    avg_temp = float(df['temperature'].mean(skipna=True)) if total > 0 else None
    type_dist = df['type'].value_counts(dropna=True).to_dict()

    min_max = {
        'flowrate': {'min': float(df['flowrate'].min(skipna=True)), 'max': float(df['flowrate'].max(skipna=True))} if total>0 else None,
        'pressure': {'min': float(df['pressure'].min(skipna=True)), 'max': float(df['pressure'].max(skipna=True))} if total>0 else None,
        'temperature': {'min': float(df['temperature'].min(skipna=True)), 'max': float(df['temperature'].max(skipna=True))} if total>0 else None,
    }

    return {
        'total_count': int(total),
        'averages': {'flowrate': avg_flow, 'pressure': avg_pressure, 'temperature': avg_temp},
        'type_distribution': type_dist,
        'min_max': min_max,
    }


def save_csv_file(src_path, dest_dir, dataset_id):
    dest = os.path.join(dest_dir, f"{dataset_id}.csv")
    shutil.copy(src_path, dest)
    return dest


def generate_charts(df, tmpdir, analytics=None):
    """
    Generate professional, high-fidelity chart images for the PDF report.
    Args:
        df: Processed pandas DataFrame.
        tmpdir: Directory to save PNGs.
        analytics: Pre-calculated analysis dictionary.
    Returns:
        Dict mapping chart keys to absolute file paths.
    """
    images = {}
    plt.rcParams.update({'font.size': 10, 'figure.titlesize': 12, 'axes.titlesize': 11})
    
    # 1. Equipment Type Distribution (Bar Chart)
    try:
        type_counts = df['type'].value_counts()
        if not type_counts.empty:
            plt.figure(figsize=(7, 5), dpi=120)
            colors_list = plt.cm.get_cmap('tab10')(np.linspace(0, 1, len(type_counts)))
            type_counts.plot(kind='bar', color='#6366f1', alpha=0.9, edgecolor='white')
            plt.title('Equipment Inventory by Category', fontweight='bold', pad=20)
            plt.xlabel('Equipment Type', labelpad=10)
            plt.ylabel('Unit Count', labelpad=10)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            
            img_path = os.path.join(tmpdir, 'type_dist.png')
            plt.savefig(img_path, bbox_inches='tight')
            plt.close()
            images['type_dist'] = img_path
    except Exception as e:
        print(f"[PDF] System Error during Type Distribution render: {e}")

    # 2. Operating Envelope: Flowrate vs Temperature (Scatter)
    try:
        if not df[['temperature', 'flowrate']].dropna().empty:
            plt.figure(figsize=(7, 5), dpi=120)
            plt.scatter(df['temperature'], df['flowrate'], color='#fb7185', alpha=0.6, edgecolors='none', s=40)
            plt.title('Operational Correlation: Flowrate vs. Temperature', fontweight='bold', pad=20)
            plt.xlabel('Measured Temperature (°C)', labelpad=10)
            plt.ylabel('Measured Flowrate (units/hr)', labelpad=10)
            plt.grid(True, linestyle=':', alpha=0.4)
            plt.tight_layout()
            
            img_path = os.path.join(tmpdir, 'flow_vs_temp.png')
            plt.savefig(img_path, bbox_inches='tight')
            plt.close()
            images['flow_vs_temp'] = img_path
    except Exception as e:
        print(f"[PDF] System Error during Flow vs Temp render: {e}")

    # 3. Parameter Distributions (Histograms)
    hist_specs = [
        ('flowrate', 'Flowrate', '#818cf8'), 
        ('pressure', 'Pressure', '#34d399'), 
        ('temperature', 'Temperature', '#f472b6')
    ]
    for key, label, color in hist_specs:
        try:
            plt.figure(figsize=(7, 4), dpi=120)
            data = df[key].dropna().astype(float)
            if not data.empty:
                plt.hist(data, bins=15, color=color, alpha=0.8, edgecolor='white')
                plt.title(f'{label} Frequency Distribution', fontweight='bold', pad=15)
                plt.xlabel(label, labelpad=8)
                plt.ylabel('Frequency', labelpad=8)
                plt.grid(axis='y', linestyle='--', alpha=0.2)
                plt.tight_layout()
                
                img_path = os.path.join(tmpdir, f'{key}_hist.png')
                plt.savefig(img_path, bbox_inches='tight')
                plt.close()
                images[f'{key}_hist'] = img_path
        except Exception as e:
            print(f"[PDF] Failure rendering histogram for {key}: {e}")
            plt.close()

    # 4. Feature Inter-dependency (Correlation Matrix)
    try:
        numeric_cols = ['flowrate', 'pressure', 'temperature']
        valid_df = df[numeric_cols].dropna()
        if len(valid_df) > 1:
            corr_df = valid_df.corr()
            plt.figure(figsize=(6, 5), dpi=120)
            im = plt.imshow(corr_df.values, cmap='RdBu_r', vmin=-1, vmax=1)
            plt.colorbar(im, fraction=0.046, pad=0.04)
            
            plt.xticks(range(len(numeric_cols)), [c.title() for c in numeric_cols], rotation=0)
            plt.yticks(range(len(numeric_cols)), [c.title() for c in numeric_cols])
            
            # Annotate values
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    val = corr_df.iloc[i, j]
                    plt.text(j, i, f"{val:.2f}", ha='center', va='center', 
                             color='white' if abs(val) > 0.5 else 'black', fontweight='bold')
            
            plt.title('Parameter Correlation Heatmap', fontweight='bold', pad=20)
            plt.tight_layout()
            
            img_path = os.path.join(tmpdir, 'correlation.png')
            plt.savefig(img_path, bbox_inches='tight')
            plt.close()
            images['correlation'] = img_path
    except Exception as e:
        print(f"[PDF] Correlation Matrix engine failure: {e}")
        plt.close()

    return images


def create_pdf_report(dataset: Dataset, df):
    """
    Senior Developer Grade PDF Report Engine.
    Uses a template system and strict coordinate management.
    """
    ensure_media_dirs()
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    tmpdir = tempfile.mkdtemp()
    
    try:
        analytics = getattr(dataset, 'analytics', None) or {}
        print(f"[PDF] Initializing professional report generation for dataset {dataset.id}...")
        
        # 1. Generate High-Fidelity Charts
        images = generate_charts(df, tmpdir, analytics=analytics)
        pdf_path = os.path.join(reports_dir, f"{dataset.id}.pdf")

        # 2. Setup Canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        page_num = 1

        def draw_template(page_canvas, title="Chemical Equipment Analysis"):
            # Header Bar
            page_canvas.saveState()
            page_canvas.setFillColor(colors.HexColor("#6366f1"))
            page_canvas.rect(0, height - 50, width, 50, fill=1, stroke=0)
            
            # Header Text
            page_canvas.setFillColor(colors.white)
            page_canvas.setFont('Helvetica-Bold', 14)
            page_canvas.drawString(40, height - 32, title)
            
            # Branding / Date
            page_canvas.setFont('Helvetica', 8)
            page_canvas.drawRightString(width - 40, height - 32, f"Report ID: {dataset.id}")
            
            # Footer
            page_canvas.setStrokeColor(colors.lightgrey)
            page_canvas.line(40, 40, width - 40, 40)
            page_canvas.setFillColor(colors.grey)
            page_canvas.setFont('Helvetica-Oblique', 8)
            page_canvas.drawString(40, 25, "FOSSEE Chemical Visualizer | Confidential Analysis Report")
            page_canvas.drawRightString(width - 40, 25, f"Page {page_num}")
            page_canvas.restoreState()

        # --- PAGE 1: COVER PAGE ---
        c.setFillColor(colors.HexColor("#1e293b")) # Dark slate cover
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Center Banner
        c.setFillColor(colors.HexColor("#6366f1"))
        c.rect(0, height/2 - 60, width, 120, fill=1, stroke=0)
        
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 28)
        c.drawCentredString(width/2, height/2 + 10, "ANALYSIS REPORT")
        c.setFont('Helvetica', 14)
        c.drawCentredString(width/2, height/2 - 25, f"DATASET: {dataset.filename or 'Unnamed Source'}")
        
        # Metadata at bottom
        c.setFont('Helvetica', 10)
        c.drawCentredString(width/2, 120, f"Generated On: {dataset.uploaded_at.strftime('%B %d, %Y | %H:%M:%S')}")
        if dataset.uploaded_by:
            c.drawCentredString(width/2, 100, f"Authorized Operator: {dataset.uploaded_by.username}")
        
        c.showPage()
        page_num += 1

        # --- PAGE 2: EXECUTIVE SUMMARY & STATS ---
        draw_template(c, "Section 1: Executive Summary")
        y = height - 100
        
        c.setFillColor(colors.black)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(40, y, "Dataset Snapshot")
        y -= 30
        
        # Snapshot Table
        c.setStrokeColor(colors.lightgrey)
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.rect(40, y - 80, 530, 80, fill=1, stroke=1)
        
        c.setFillColor(colors.black)
        c.setFont('Helvetica-Bold', 11)
        stats_data = [
            ("Sample Size", f"{dataset.total_rows} Equipment Units"),
            ("Mean Flowrate", f"{dataset.avg_flowrate or 0:.2f} Units/hr"),
            ("Operational Pressure", f"{dataset.avg_pressure or 0:.2f} bar (Avg)"),
            ("Mean Temperature", f"{dataset.avg_temperature or 0:.2f} °C")
        ]
        
        row_y = y - 20
        for label, val in stats_data:
            c.drawString(60, row_y, label)
            c.drawRightString(550, row_y, val)
            row_y -= 18
            
        y -= 120
        # Equipment Type Dist Chart
        if images.get('type_dist'):
            c.setFont('Helvetica-Bold', 13)
            c.drawString(40, y, "Equipment Inventory Composition")
            y -= 10
            c.drawImage(images['type_dist'], 60, y - 260, width=480, height=240)
            y -= 300

        c.showPage()
        page_num += 1

        # --- PAGE 3: PARAMETER DISTRIBUTIONS ---
        draw_template(c, "Section 2: Statistical Distributions")
        y = height - 80
        
        # Draw histograms in a grid
        chart_grid = [('flowrate_hist', 'Flowrate'), ('pressure_hist', 'Pressure'), ('temperature_hist', 'Temperature')]
        for i, (key, label) in enumerate(chart_grid):
            img = images.get(key)
            if not img: continue
            
            # 2 charts per page if large, or check Y
            if y < 350:
                c.showPage()
                page_num += 1
                draw_template(c, "Section 2: Statistical Distributions (Cont.)")
                y = height - 80
            
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(width/2, y - 20, f"{label} Profile Analysis")
            c.drawImage(img, (width-450)/2, y - 310, width=450, height=280)
            y -= 330

        c.showPage()
        page_num += 1

        # --- PAGE 4: CORRELATIONS & TRENDS ---
        draw_template(c, "Section 3: Correlation & Trend Analysis")
        y = height - 80
        
        if images.get('correlation'):
            c.setFont('Helvetica-Bold', 12)
            # FIXED POSITION: Top of Page
            c.drawCentredString(width/2, y - 20, "Feature Inter-dependency Matrix")
            c.drawImage(images['correlation'], (width-420)/2, y - 320, width=420, height=280)
            y -= 340

        if images.get('flow_vs_temp'):
            if y < 350:
                c.showPage()
                page_num += 1
                draw_template(c, "Section 3: Correlation & Trend Analysis (Cont.)")
                y = height - 80
            
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(width/2, y - 20, "Operating Envelope: Flow vs Temperature")
            c.drawImage(images['flow_vs_temp'], (width-420)/2, y - 320, width=420, height=280)
            y -= 340

        c.showPage()
        page_num += 1

        # --- PAGE 5: DATA AUDIT & INSIGHTS ---
        draw_template(c, "Section 4: Expert Insights & Data Audit")
        y = height - 80
        
        # AI Insights Section
        insights = analytics.get('insights', [])
        if insights:
            c.setFillColor(colors.HexColor("#f1f5f9"))
            c.rect(40, y - 100, 530, 100, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#6366f1"))
            c.setFont('Helvetica-Bold', 13)
            c.drawString(60, y - 25, "Key Analytical Observations")
            
            c.setFillColor(colors.black)
            c.setFont('Helvetica', 10)
            ins_y = y - 45
            for ins in insights[:5]: # Top 5
                c.drawString(70, ins_y, f"• {ins}")
                ins_y -= 16
            y -= 120

        # Audit Table
        c.setFont('Helvetica-Bold', 14)
        c.drawString(40, y, "Equipment Log Preview")
        y -= 30
        
        # Table Header
        c.setFillColor(colors.HexColor("#334155"))
        c.rect(40, y-2, 530, 20, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(45, y+4, "Equipment Name")
        c.drawString(200, y+4, "Type")
        c.drawString(320, y+4, "Flowrate")
        c.drawString(400, y+4, "Pressure")
        c.drawString(480, y+4, "Temp")
        
        y -= 15
        c.setFillColor(colors.black)
        c.setFont('Helvetica', 8)
        
        # Loop through rows
        for idx, row in enumerate(df.head(30).fillna('-').to_dict(orient='records')):
            if idx % 2 == 1:
                c.setFillColor(colors.HexColor("#f8fafc"))
                c.rect(40, y-3, 530, 14, fill=1, stroke=0)
            
            c.setFillColor(colors.black)
            c.drawString(45, y, str(row.get('equipment name', ''))[:45])
            c.drawString(200, y, str(row.get('type', ''))[:25])
            c.drawString(320, y, f"{row.get('flowrate')}")
            c.drawString(400, y, f"{row.get('pressure')}")
            c.drawString(480, y, f"{row.get('temperature')}")
            
            y -= 14
            if y < 60:
                c.showPage()
                page_num += 1
                draw_template(c, "Section 4: Data Audit (Cont.)")
                y = height - 80
        
        c.save()
        print(f"[PDF] Professional Report finalized: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"[PDF] Critical Failure in Report Engine: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


def process_csv_and_create_dataset(uploaded_file, uploader=None):
    ensure_media_dirs()
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    # Write uploaded file to temp file for pandas
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    try:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp.flush()
        tmp.close()

        df, coercion_errors = validate_and_read_csv(tmp.name)

        # Clean dataframe and compute enhanced analytics
        df_clean = clean_dataframe(df)
        analytics = analyze_dataframe(df)

        # Compute summary (legacy simple summary) for compatibility
        summary = compute_summary_from_df(df)

        # Create Dataset record
        dataset = Dataset.objects.create(
            filename=getattr(uploaded_file, 'name', 'uploaded.csv'),
            uploaded_by=uploader,
            total_rows=summary['total_count'],
            avg_flowrate=summary['averages']['flowrate'],
            avg_pressure=summary['averages']['pressure'],
            avg_temperature=summary['averages']['temperature'],
            type_distribution=summary['type_distribution']
        )

        # Save original CSV to media/uploads/<uuid>.csv
        dest_csv = save_csv_file(tmp.name, uploads_dir, dataset.id)
        dataset.csv_file.name = os.path.relpath(dest_csv, settings.MEDIA_ROOT).replace('\\', '/')

        # Save cleaned CSV to media/clean/<uuid>.csv
        clean_dir = os.path.join(settings.MEDIA_ROOT, 'clean')
        os.makedirs(clean_dir, exist_ok=True)
        clean_path = os.path.join(clean_dir, f"{dataset.id}.csv")
        df_clean.to_csv(clean_path, index=False)
        dataset.cleaned_csv.name = os.path.relpath(clean_path, settings.MEDIA_ROOT).replace('\\', '/')

        # Attach analytics to dataset and generate PDF (use cleaned dataframe for charts)
        dataset.analytics = analytics

        pdf_path = create_pdf_report(dataset, df_clean)
        dataset.summary_pdf.name = os.path.relpath(pdf_path, settings.MEDIA_ROOT).replace('\\', '/')

        dataset.save()

        # Trim to last 5 datasets
        trim_old_datasets()

        return dataset, coercion_errors, summary, analytics
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass


def trim_old_datasets():
    qs = Dataset.objects.order_by('-uploaded_at')
    keep = qs[:5]
    keep_ids = [d.id for d in keep]
    to_delete = Dataset.objects.exclude(id__in=keep_ids)
    # Delete files then records
    for d in to_delete:
        try:
            if d.csv_file and os.path.exists(d.csv_file.path):
                os.remove(d.csv_file.path)
        except Exception:
            pass
        try:
            if d.summary_pdf and os.path.exists(d.summary_pdf.path):
                os.remove(d.summary_pdf.path)
        except Exception:
            pass
    to_delete.delete()
