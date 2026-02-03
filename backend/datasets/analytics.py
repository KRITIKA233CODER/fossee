import pandas as pd
import numpy as np

NUMERIC_COLS = ['flowrate', 'pressure', 'temperature']
REQUIRED_COLS = ['equipment name', 'type'] + NUMERIC_COLS


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Keep only relevant columns if extra columns present
    for c in REQUIRED_COLS:
        if c not in df.columns:
            df[c] = pd.NA

    df = df[REQUIRED_COLS]

    # Coerce numeric columns
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Trim whitespace on text
    df['equipment name'] = df['equipment name'].astype(str).str.strip()
    df['type'] = df['type'].astype(str).str.strip()

    # Option: drop rows that are completely empty
    df = df.dropna(how='all')

    return df


def _missing_values(df: pd.DataFrame):
    return df.isna().sum().to_dict()


def _basic_stats(df: pd.DataFrame):
    stats = {}
    for col in NUMERIC_COLS:
        series = df[col].dropna()
        stats[col] = {
            'mean': float(series.mean()) if len(series) > 0 else None,
            'median': float(series.median()) if len(series) > 0 else None,
            'std': float(series.std()) if len(series) > 0 else None,
            'min': float(series.min()) if len(series) > 0 else None,
            'max': float(series.max()) if len(series) > 0 else None,
            'count': int(series.count()),
        }
    return stats


def _type_distribution(df: pd.DataFrame):
    return df['type'].value_counts(dropna=True).to_dict()


def _top_values(df: pd.DataFrame, n=5):
    out = {}
    for col in NUMERIC_COLS:
        s = df[['equipment name', col]].dropna(subset=[col])
        top = s.nlargest(n, col).to_dict(orient='records')
        low = s.nsmallest(n, col).to_dict(orient='records')
        out[col] = {'top': top, 'low': low}
    return out


def _histogram(df: pd.DataFrame, col: str, bins=10):
    series = df[col].dropna()
    if series.empty:
        return {'bins': [], 'counts': []}
    counts, edges = np.histogram(series, bins=bins)
    bins_list = [float(e) for e in edges]
    return {'bins': bins_list, 'counts': [int(c) for c in counts]}


def _outliers_iqr(df: pd.DataFrame):
    outliers = {}
    for col in NUMERIC_COLS:
        series = df[col].dropna()
        if series.empty:
            outliers[col] = {'count': 0, 'examples': []}
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        mask = (df[col] < low) | (df[col] > high)
        examples = df.loc[mask, ['equipment name', 'type', col]].head(10).to_dict(orient='records')
        outliers[col] = {'count': int(mask.sum()), 'examples': examples}
    return outliers


def _correlation(df: pd.DataFrame):
    corr = df[NUMERIC_COLS].corr()
    return corr.fillna(0).to_dict()


def generate_insights(df: pd.DataFrame):
    insights = []
    # zero flowrate
    zero_flow = df[df['flowrate'] == 0]
    if len(zero_flow) > 0:
        insights.append(f"{len(zero_flow)} equipment items have zero flowrate")

    # high temp alert
    high_temp = df[df['temperature'] > 100]
    if len(high_temp) > 0:
        insights.append(f"{len(high_temp)} rows have temperature > 100")

    # correlation hint
    corr = _correlation(df)
    # inspect flowrate vs temperature
    ft = corr.get('flowrate', {}).get('temperature', 0)
    if abs(ft) > 0.6:
        insights.append('Strong correlation detected between Flowrate and Temperature')

    return insights


def replace_special_floats(obj):
    """
    Recursively replace NaN/Infinity with None to ensure JSON compliance.
    """
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: replace_special_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_special_floats(v) for v in obj]
    return obj


def analyze_dataframe(df: pd.DataFrame):
    df_clean = clean_dataframe(df)
    total = len(df_clean)
    missing = _missing_values(df_clean)
    stats = _basic_stats(df_clean)
    type_dist = _type_distribution(df_clean)
    outliers = _outliers_iqr(df_clean)
    corr = _correlation(df_clean)
    top_values = _top_values(df_clean, n=5)
    histograms = {
        'flowrate': _histogram(df_clean, 'flowrate'),
        'pressure': _histogram(df_clean, 'pressure'),
        'temperature': _histogram(df_clean, 'temperature'),
    }
    insights = generate_insights(df_clean)

    raw_analytics = {
        'row_count': int(total),
        'missing_values': missing,
        'stats': stats,
        'type_distribution': type_dist,
        'outliers': outliers,
        'correlation_matrix': corr,
        'top_values': top_values,
        'histograms': histograms,
        'insights': insights,
    }
    
    # Sanitize to ensure valid JSON for SQLite
    return replace_special_floats(raw_analytics)
