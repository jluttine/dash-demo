import dash
import dash_html_components as html
import dash_core_components as dcc

from pages import demo1_graph, demo2_datatable


# Create the Dash app/server
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ],
    # We need to suppress these errors because when we define the callbacks,
    # the subpage layouts haven't been defined yet.. So there would be errors
    # about missing IDs. Is there some better solution?
    suppress_callback_exceptions=True,
)


# List separate pages
subpages = [
    ("/demo-graph", demo1_graph),
    ("/demo-datatable", demo2_datatable),
]


# Generic page layout for the entire app
app.layout = html.Div(
    [
        # This element is used to read the current URL. Not visible to the
        # user.
        dcc.Location(id="url", refresh=False),
        # The content will be rendered in this element so the children of this
        # element will change when browsing to a different page
        html.Div(
            id="page-content",
            className="DashboardContainer",
        ),
    ]
)


# Set callbacks for each page
for (_, page) in subpages:
    page.set_callbacks(app)


# Layout of the main page
main_layout = html.Div(
    className="Container",
    children=[
        html.H1("Plotly Dash demo"),
        html.P(html.I("Jaakko Luttinen - November 16, 2020")),
        html.P(html.I("Lead Data Scientist @ Leanheat by Danfoss")),
        html.Ul(
            [
                html.Li("What is Plotly Dash?"),
                html.Li("Why not Jupyter Notebooks?"),
            ]
        ),
    ] + [
        html.A(
            html.Div(
                className="Card",
                children=[
                    html.H2(page.title),
                    html.P(page.description),
                ]
            ),
            href=url,
        ) for (url, page) in subpages
    ] + [
        html.Ul(
            html.Li("Show our real production Dash")
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")]
)
def display_page(pathname):
    """Render the newly selected page when the URL changes"""

    if pathname == "/":
        return main_layout

    page = dict(subpages)[pathname]

    return html.Div(
        [
            # For subpages, add a few fixed elements at the top of the page
            dcc.Link("< Back to main page", href="/"),
            html.H1(page.title),
            html.P(page.description),
            # Then, the actual subpage content
            page.layout,
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
