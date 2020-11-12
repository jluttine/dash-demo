import dash
import dash_html_components as html
import dash_core_components as dcc

from pages import demo1, demo2


app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ],
)


subpages = [
    ("/demo1", demo1),
    ("/demo2", demo2),
]


main_layout = html.Div(
    className="Container",
    children=[
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
    ]
)


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # The content will be rendered in this element
        html.Div(id="page-content"),
    ]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")]
)
def display_page(pathname):

    if pathname == "/":
        return main_layout

    page = dict(subpages)[pathname]

    return html.Div(
        [
            dcc.Link("Back to main page", href="/"),
            html.H1(page.title),
            html.P(page.description),
            page.layout,
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
