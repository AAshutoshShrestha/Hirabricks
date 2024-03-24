def format_timedelta(td):
    total_minutes = td.days * 24 * 60 + td.seconds // 60
    hours, minutes = divmod(total_minutes, 60)

    parts = []
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")

    return ', '.join(parts)