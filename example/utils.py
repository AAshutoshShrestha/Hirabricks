def format_timedelta(td):
    # Calculate total minutes from the timedelta
    total_minutes = td.days * 24 * 60 + td.seconds // 60

    # Calculate hours and minutes from total minutes
    hours, minutes = divmod(total_minutes, 60)

    # Initialize an empty list to store formatted parts of the timedelta
    parts = []

    # If there are hours, add them to the parts list
    if hours:
        parts.append(f"{hours} hours")

    # If there are minutes, add them to the parts list
    if minutes:
        parts.append(f"{minutes} minutes")

    # Join the parts list with commas and return the formatted string
    return ', '.join(parts)
