def determine_priority(row):
    """Determine recruiting priority for each position."""
    if row['Current Count'] < row['Min Required']:
        return 'HIGH'
    elif row['Grade'] in ['D', 'F']:
        return 'HIGH'
    elif row['Grade'] in ['C']:
        return 'MEDIUM'
    else:
        return 'LOW'