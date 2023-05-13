from django.shortcuts import render
from .models import Dataset
from plotly.offline import plot
import plotly.graph_objs as go
from .utils import process_data


def data_view(request):
    # Process data
    data = process_data('data.csv')
    
    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data['value'], mode='lines', name='Value'))
    fig.update_layout(title='Data Visualization', xaxis_title='Date', yaxis_title='Value')
    plot_div = plot(fig, output_type='div')
    
    # Render template with the Plotly figure
    return render(request, 'data_view.html', {'plot_div': plot_div})


def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets.html', {'datasets': datasets})

