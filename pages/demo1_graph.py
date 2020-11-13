import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import time

# Plotly Graph objects is a low-level interface to graphs
import plotly.graph_objects as go

import numpy as np
import pandas as pd


title = "Graphs and callbacks"


description = "Visualize samples from a selected stochastic process"


layout = html.Div([
    "Stochastic process:",
    dcc.Dropdown(
        id="demo1-sampler",
        placeholder="Choose distribution..",
        options=[
            {
                "label": "Normal",
                "value": "normal",
            },
            {
                "label": "Log-normal",
                "value": "lognormal",
            },
        ],
    ),
    html.Br(),
    "Number of traces:",
    dcc.Slider(
        id="demo1-count-slider",
        min=1,
        max=10,
        value=1,
        step=1,
        marks={i: str(i) for i in range(1, 11)},
    ),
    # By wrapping any element inside Loading, there will be a loading animation
    # while the element is being updated. Note that there can be any complex
    # hierarchy of multiple elements inside.
    dcc.Loading(
        id="demo1-loading-graph",
        children=dcc.Graph(id="demo1-graph"),
    )
])


def set_callbacks(app):

    @app.callback(
        # Outputs: List the elements that are modified in the callback. Specify
        # the ID and the property for each.
        [
            Output("demo1-graph", "figure"),
        ],
        # Inputs: List the elements that trigger an update of the outputs when
        # the inputs are modified. Specify the ID and the property for each.
        [
            Input("demo1-sampler", "value"),
            Input("demo1-count-slider", "value"),
        ],
        # States: List the elements that don't trigger an update but that are
        # otherwise needed. Specify the ID and the property for each.
        [
        ],
    )
    def update_figure(sampler, count):
        """Update the graph when parameters are changed"""

        # Sleep a bit so one can see the loading animation
        time.sleep(1)

        df = pd.DataFrame(
            (
                np.random.randn(100, count).cumsum(axis=0)
                if sampler == "normal" else
                np.exp(0.01 * np.random.randn(100, count).cumsum(axis=0))
                if sampler == "lognormal" else
                None
            ),
            columns=["series-{}".format(i+1) for i in range(count)]
        )

        fig = go.Figure()
        fig.update_layout(
            # Transition animation might be useful sometimes (maybe not in this
            # demo really)
            transition_duration=500,
            title="Random walk",
            xaxis_title="Time",
        )

        for (_, x) in df.T.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=x.index,
                    y=x.values,
                    name=x.name,
                )
            )

        return [fig]

    return
