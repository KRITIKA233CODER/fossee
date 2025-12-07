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
    Generate a set of chart images into `tmpdir` using either raw `df`
    or precomputed `analytics` (which may contain histograms and correlation).
    Returns dict of image paths.
    """
    images = {}
    # Bar chart for type distribution
    try:
        type_counts = df['type'].value_counts()
        plt.figure(figsize=(6, 4))
        type_counts.plot(kind='bar', color='#60a5fa')
        plt.title('Equipment Type Distribution')
        plt.tight_layout()
        img1 = os.path.join(tmpdir, 'type_dist.png')
        plt.savefig(img1)
        plt.close()
        images['type_dist'] = img1
    except Exception:
        pass

    # Scatter: flowrate vs temperature
    try:
        plt.figure(figsize=(6, 4))
        plt.scatter(df['temperature'], df['flowrate'], c='#fb7185', alpha=0.8)
        plt.xlabel('Temperature')
        plt.ylabel('Flowrate')
        plt.title('Flowrate vs Temperature')
        plt.tight_layout()
        img2 = os.path.join(tmpdir, 'flow_vs_temp.png')
        plt.savefig(img2)
        plt.close()
        images['flow_vs_temp'] = img2
    except Exception:
        pass

    # Histograms: if analytics provided prefer counts/bins else compute from df
    hist_specs = [('flowrate', 'Flowrate'), ('pressure', 'Pressure'), ('temperature', 'Temperature')]
    for key, label in hist_specs:
        try:
            img_path = os.path.join(tmpdir, f'{key}_hist.png')
            plt.figure(figsize=(6, 3.5))
            if analytics and analytics.get('histograms', {}).get(key):
                h = analytics['histograms'][key]
                # bars centered on bin ranges
                bins = h.get('bins', [])
                counts = h.get('counts', [])
                if len(bins) > 1 and len(counts) > 0:
                    # create bar positions and widths
                    lefts = bins[:-1]
                    widths = [bins[i+1] - bins[i] for i in range(len(bins)-1)]
                    plt.bar(lefts, counts, width=widths, align='edge', color='#7c3aed', alpha=0.9)
            else:
                plt.hist(df[key].dropna().astype(float), bins=12, color='#7c3aed', alpha=0.9)
            plt.title(f'{label} Distribution')
            plt.tight_layout()
            plt.savefig(img_path)
            plt.close()
            images[f'{key}_hist'] = img_path
        except Exception:
            pass

    # Correlation heatmap
    try:
        corr = None
        if analytics and analytics.get('correlation_matrix'):
            corr = analytics['correlation_matrix']
            # convert to DataFrame
            corr_df = pd.DataFrame(corr)
        else:
            corr_df = df[['flowrate', 'pressure', 'temperature']].corr()

        if corr_df is not None and not corr_df.empty:
            plt.figure(figsize=(5, 4))
            im = plt.imshow(corr_df.values, cmap='coolwarm', vmin=-1, vmax=1)
            plt.colorbar(im, fraction=0.046, pad=0.04)
            plt.xticks(range(len(corr_df.columns)), corr_df.columns, rotation=45)
            plt.yticks(range(len(corr_df.index)), corr_df.index)
            plt.title('Correlation Matrix')
            plt.tight_layout()
            img_corr = os.path.join(tmpdir, 'correlation.png')
            plt.savefig(img_corr)
            plt.close()
            images['correlation'] = img_corr
    except Exception:
        pass

    return images


def create_pdf_report(dataset: Dataset, df):
    ensure_media_dirs()
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    tmpdir = tempfile.mkdtemp()
    try:
        # use persisted analytics if available to make richer charts
        analytics = getattr(dataset, 'analytics', None) or {}
        images = generate_charts(df, tmpdir, analytics=analytics)
        pdf_path = os.path.join(reports_dir, f"{dataset.id}.pdf")

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Cover page
        c.setFont('Helvetica-Bold', 20)
        c.drawCentredString(width / 2, height - 80, 'Chemical Equipment Parameter Visualizer')
        c.setFont('Helvetica', 12)
        c.drawCentredString(width / 2, height - 110, f'Report for: {dataset.filename}')
        c.setFont('Helvetica', 10)
        c.drawCentredString(width / 2, height - 130, f'Uploaded at: {dataset.uploaded_at}')
        c.setFont('Helvetica', 9)
        if dataset.uploaded_by:
            c.drawCentredString(width / 2, height - 146, f'Uploaded by: {dataset.uploaded_by.username}')

        c.showPage()

        # Summary / Key stats
        c.setFont('Helvetica-Bold', 14)
        c.drawString(40, height - 50, 'Summary & Key Statistics')
        c.setFont('Helvetica', 10)
        y = height - 80
        c.drawString(40, y, f"Total rows: {dataset.total_rows}")
        y -= 18
        c.drawString(40, y, f"Average Flowrate: {dataset.avg_flowrate}")
        y -= 14
        c.drawString(40, y, f"Average Pressure: {dataset.avg_pressure}")
        y -= 14
        c.drawString(40, y, f"Average Temperature: {dataset.avg_temperature}")
        y -= 20

        # Type distribution small table
        try:
            c.setFont('Helvetica-Bold', 12)
            c.drawString(40, y, 'Type Distribution')
            c.setFont('Helvetica', 9)
            y -= 14
            for t, cnt in (dataset.type_distribution or {}).items():
                c.drawString(50, y, f"{t}: {cnt}")
                y -= 12
                if y < 120:
                    c.showPage()
                    y = height - 40
        except Exception:
            pass

        # Charts page(s)
        # Place histograms in a grid
        chart_x = 40
        chart_w = 240
        chart_h = 140
        chart_y = height - 80
        imgs = [('flowrate_hist', 'Flowrate'), ('pressure_hist', 'Pressure'), ('temperature_hist', 'Temperature')]
        i = 0
        for key, label in imgs:
            img = images.get(key)
            if not img:
                continue
            x = chart_x + (i % 2) * (chart_w + 20)
            if i % 2 == 0 and i != 0:
                chart_y -= (chart_h + 40)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(x, chart_y + chart_h + 6, label)
            try:
                c.drawImage(img, x, chart_y, width=chart_w, height=chart_h)
            except Exception:
                pass
            i += 1
            if chart_y < 120:
                c.showPage()
                chart_y = height - 80

        c.showPage()

        # Correlation and scatter
        c.setFont('Helvetica-Bold', 12)
        c.drawString(40, height - 50, 'Correlation & Scatter')
        if images.get('correlation'):
            try:
                c.drawImage(images['correlation'], 40, height - 360, width=420, height=280)
            except Exception:
                pass

        if images.get('flow_vs_temp'):
            try:
                c.drawImage(images['flow_vs_temp'], 480 - 40, height - 360, width=240, height=280)
            except Exception:
                pass

        c.showPage()

        # Top rows
        c.setFont('Helvetica-Bold', 12)
        c.drawString(40, height - 50, 'Top rows (first 20)')
        c.setFont('Helvetica', 8)
        rows = df.head(20).fillna('').to_dict(orient='records')
        y = height - 70
        for r in rows:
            line = f"{r.get('equipment name','')[:30]:30} {r.get('type','')[:15]:15} {r.get('flowrate',''):8} {r.get('pressure',''):8} {r.get('temperature',''):8}"
            c.drawString(40, y, line)
            y -= 12
            if y < 40:
                c.showPage()
                y = height - 40

        # Insights list (if available)
        insights = (analytics or {}).get('insights') or []
        if insights:
            c.showPage()
            c.setFont('Helvetica-Bold', 12)
            c.drawString(40, height - 50, 'Insights')
            c.setFont('Helvetica', 10)
            y = height - 80
            for ins in insights:
                # wrap long lines simply
                lines = []
                text = str(ins)
                while len(text) > 120:
                    lines.append(text[:120])
                    text = text[120:]
                lines.append(text)
                for ln in lines:
                    c.drawString(48, y, f"- {ln}")
                    y -= 14
                    if y < 60:
                        c.showPage()
                        y = height - 40

        c.showPage()
        c.save()

        return pdf_path
    finally:
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
