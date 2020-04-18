import plotly.graph_objects as go
from plotly.offline import iplot
import plotly.figure_factory as ff
from plotly import subplots

def plot_variables(labels, plot, data):
    """
    Plot individual variables with dropdown menu selection
    param plot: One of the 3 plot types supported: 0 for barplot, 1 for histogram
    param labels: iterable containing the variable names
    """
    # Create individual figures
    fig = subplots.make_subplots(rows=1, cols=1)
    for var in labels:
        if plot == 0:
            counts = data[var].value_counts()
            fig.append_trace(go.Bar(x=counts, y=counts.index, orientation='h'), 1, 1)
        elif plot == 1:
            fig.append_trace(ff.create_distplot([list(data[var])], ['distplot'])['data'][0], 1, 1)
            fig.append_trace(ff.create_distplot([list(data[var])], ['distplot'])['data'][1], 1, 1)
        else:
            raise ValueError("plot number must be 0, 1")
    # Create buttons for drop down menu
    buttons = []
    for i, label in enumerate(labels):
        if plot == 0:
            visibility = [i == j for j in range(len(labels))]
        else:
            visibility = [j//2 == i for j in range(2*len(labels))]
        button = dict(
            label=label,
            method='update',
            args=[{'visible': visibility},
                  {'title': label}])
        buttons.append(button)
    updatemenus = list([
        dict(active=-1,
             x=1.06, y=1.27,
             buttons=buttons
             )
    ])
    # Setup layout
    if plot == 0:
        fig['layout']['title'] = "Distribution of categorical and discrete variables:"
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.7)
    elif plot == 1:
        fig['layout']['title'] = "Distribution of continuous variables:"
        fig.update_traces(marker_color='rgb(112, 125, 188)', opacity=0.8)
    elif plot == 2:
        fig['layout']['title'] = "Boxplot of continuous variables by score:"
    fig['layout']['showlegend'] = False
    fig['layout']['updatemenus'] = updatemenus
    iplot(fig, config={"displayModeBar": False})