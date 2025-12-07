/**
 * Generates natural language insights from dataset analytics.
 * @param {Object} analytics - The analytics object returned from the backend.
 * @param {Object} dataset - The dataset metadata object.
 * @returns {string[]} Array of insight strings.
 */
export function generateInsights(analytics, dataset) {
    const insights = []

    if (!analytics || !analytics.stats) {
        return ['Insights will appear after analysis is generated.']
    }

    // 1. Row Count & Quality
    const rowCount = dataset.total_rows || analytics.total_rows || 0
    if (rowCount > 10000) {
        insights.push(`Large dataset with ${rowCount.toLocaleString()} records, providing robust statistical significance.`)
    } else if (rowCount > 0) {
        insights.push(`Dataset contains ${rowCount.toLocaleString()} records.`)
    }

    // 2. Missing Values
    const missing = analytics.missing_values || {}
    const missingCols = Object.keys(missing).filter(k => missing[k] > 0)
    if (missingCols.length === 0) {
        insights.push('Data quality is high: No missing values detected across all columns.')
    } else {
        const totalMissing = missingCols.reduce((acc, col) => acc + missing[col], 0)
        insights.push(`Attention needed: ${totalMissing} missing values detected in ${missingCols.length} columns (${missingCols.join(', ')}).`)
    }

    // 3. Key Stats (Flowrate, Pressure, Temperature)
    const stats = analytics.stats || {}

    if (stats.flowrate) {
        const mean = stats.flowrate.mean.toFixed(2)
        const std = stats.flowrate.std ? stats.flowrate.std.toFixed(2) : '?'
        insights.push(`Average flowrate is ${mean} L/min (±${std}), indicating ${stats.flowrate.std > 10 ? 'high' : 'stable'} variability.`)
    }

    if (stats.pressure && stats.temperature) {
        insights.push(`Operating conditions range from ${stats.pressure.min}-${stats.pressure.max} bar pressure and ${stats.temperature.min}-${stats.temperature.max}°C temperature.`)
    }

    // 4. Correlations
    const corr = analytics.correlation_matrix || {}
    let strongCorr = []
    Object.keys(corr).forEach(k1 => {
        Object.keys(corr[k1] || {}).forEach(k2 => {
            if (k1 !== k2) {
                const val = corr[k1][k2]
                if (val > 0.8) strongCorr.push(`${k1} & ${k2} (positive)`)
                if (val < -0.8) strongCorr.push(`${k1} & ${k2} (negative)`)
            }
        })
    })

    // Deduplicate correlations (A&B is same as B&A)
    const uniqueCorrs = [...new Set(strongCorr.map(s => s.split(' & ').sort().join(' & ')))]
    if (uniqueCorrs.length > 0) {
        insights.push(`Strong correlations detected: ${uniqueCorrs.slice(0, 2).join(', ')}.${uniqueCorrs.length > 2 ? '..' : ''}`)
    }

    // 5. Anomalies (Mock logic if not in backend yet, or use outliers count if available)
    // Assuming backend might send 'anomalies' count or we infer from distribution
    if (stats.flowrate && (stats.flowrate.max > stats.flowrate.mean * 3)) {
        insights.push('Potential outliers detected: Maximum flowrate is significantly higher than the average.')
    }

    return insights
}
