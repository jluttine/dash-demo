from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Plotly Express is a high-level easy-to-use interface to graphs
import plotly.express as px

import pandas as pd
import numpy as np


title = "Data tables and pie charts"


description = "Demonstrate dynamic options, editable data tables and pie charts"


layout = html.Div([
    "Segment:",
    dcc.Dropdown(
        id="demo2-segment",
        placeholder="Choose segment..",
        options=[
            {
                "label": "Heating",
                "value": "heating",
            },
            {
                "label": "Cooling",
                "value": "cooling",
            }
        ]
    ),
    "Product:",
    # These options will be dynamically updated when the segment is chosen
    dcc.Dropdown(
        id="demo2-product",
        placeholder="Choose product..",
    ),
    dash_table.DataTable(
        id="demo2-table",
        columns=[
            {
                "name": "Country",
                "id": "country",
                "editable": False,
            },
            {
                "name": "Units sold",
                "id": "amount",
                "editable": True,
                "type": "numeric",
                "format": {
                    # Integers (no decimals)
                    "specifier": ".0f",
                },
            },
            {
                "name": "Unit price",
                "id": "price",
                "editable": True,
                "type": "numeric",
                "format": {
                    # Two decimals. Note that in order to show the currency,
                    # one must prepend with $ but the actual currency and its
                    # formatting is defined under locale.
                    "specifier": "$.2f",
                    "locale": {
                        # Here we define how the symbol is actually shown:
                        # Empty prefix and euro symbol as a suffix.
                        "symbol": ["", " €"],
                    }
                },

            },
        ],
        editable=True,
        filter_action="native",
        sort_action="native",
        export_format="csv",
        page_size=3,

    ),
    dcc.Graph(id="demo2-graph"),
])


def set_callbacks(app):

    @app.callback(
        [
            Output("demo2-product", "options"),
        ],
        [
            Input("demo2-segment", "value"),
        ],
    )
    def update_products(segment):
        if segment is None:
            return [[]]

        return [
            [
                {
                    "label": "Thermostat",
                    "value": "thermostat",
                },
                {
                    "label": "ECL",
                    "value": "ecl",
                },
            ] if segment == "heating" else [
                {
                    "label": "Compressor",
                    "value": "compressor",
                },
                {
                    "label": "Condensing unit",
                    "value": "condensing",
                },
            ]
        ]

    @app.callback(
        [
            Output("demo2-table", "data"),
        ],
        [
            Input("demo2-product", "value"),
        ],
    )
    def update_table(product):
        if product is None:
            return [[]]
        return [
            # In reality, this data would probably be loaded from a file or a
            # database. Here we just use random data to fill the table.
            pd.DataFrame(
                {
                    "country": ["Denmark", "Finland", "Germany"],
                    "price": np.random.uniform(10, 30, size=3),
                    "amount": np.random.randint(0, 100, size=3),
                }
            ).to_dict("records")
        ]

    @app.callback(
        [
            Output("demo2-graph", "figure"),
        ],
        [
            Input("demo2-table", "data"),
        ]
    )
    def update_graph(data):
        """Update the bar plot based on the data table"""
        df = pd.DataFrame(
            [
                [
                    d["country"],
                    d["price"] * d["amount"],
                ]
                for d in data
            ],
            columns=["country", "sales"]
        )
        fig = px.pie(
            df,
            values="sales",
            names="country",
            title="Total sales"
        )
        return [fig]

    return
