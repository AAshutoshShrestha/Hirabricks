# vercel_app/generategraphs.py

from django.core.serializers import serialize
import json
from collections import defaultdict

def generate_dryer_efficiency_graph(dataset, title):
    """
    Generate a Plotly graph for dryer efficiency count over time.

    Args:
        dataset: Queryset containing Dryer Efficiency objects.
        title: Title for the Plotly graph.

    Returns:
        JSON string representing Plotly graph data.
    """
    # Extracting date and total duration from queryset and aggregating durations for the same date
    date_duration_dict = defaultdict(str)
    for entry in dataset:
        # Extracting date from entry and converting it to a date string
        date = entry['date'].strftime('%Y-%m-%d')
        duration = entry['total_duration']
        # Accumulating durations for the corresponding date
        date_duration_dict[date] += duration

    # Convert dictionary to lists for Plotly
    dates_plotly = list(date_duration_dict.keys())
    durations_plotly = list(date_duration_dict.values())

    # Creating Plotly compatible JSON
    fig_data = {
        'data': [{
            'x': dates_plotly,
            'y': durations_plotly,
            'type': 'line',
            'mode': 'markers+lines',
            'marker': {'symbol': 'circle-open-dot'},
            'line': {'shape': 'linear'},
            'name': title
        }],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Total Duration'}
        }
    }

    # Convert Plotly figure data to JSON string
    fig_json = json.dumps(fig_data)

    return fig_json
