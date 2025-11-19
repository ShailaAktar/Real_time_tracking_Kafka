import os
from datetime import datetime

import psycopg2
import pandas as pd
from dotenv import load_dotenv

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go


# load your .env settings
load_dotenv()

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGUSER = os.getenv("PGUSER", "market_user")
PGPASS = os.getenv("PGPASSWORD", "Market@123")
PGDB   = os.getenv("PGDATABASE", "marketdb")

DSN = f"host={PGHOST} port={PGPORT} dbname={PGDB} user={PGUSER} password={PGPASS}"


# Pull data from DB, use your query according to the DB connection
def fetch_trades(symbol: str, limit: int = 200) -> pd.DataFrame:
    conn = psycopg2.connect(DSN)
    try:
        query = """
            SELECT
                trade_time,
                price,
                quantity
            FROM market.trades
            WHERE symbol = %s
            ORDER BY trade_time DESC
            LIMIT %s;
        """
        df = pd.read_sql(query, conn, params=(symbol, limit))
    finally:
        conn.close()

    if not df.empty:
        df["trade_time"] = pd.to_datetime(df["trade_time"])
        # we want time moving forward on the x-axis
        df = df.sort_values("trade_time")

    return df


# Dashboard setup
app = Dash(__name__)
app.title = "Live Crypto Dashboard"

# Pushing the same symbol from binance 
DEFAULT_SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "TRXUSDT",
    "LINKUSDT",
]

app.layout = html.Div(
    style={"fontFamily": "Georgia, serif", "padding": "20px", "backgroundColor": "#B5EFEF"},
    children=[
        html.H1(
            "Live Crypto Dashboard",
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        # I pick which symbol I want to watch
        dcc.Dropdown(
            id="symbol-dropdown",
            options=[{"label": s, "value": s} for s in DEFAULT_SYMBOLS],
            value="BTCUSDT",
            clearable=False,
            style={"width": "300px", "margin": "0 auto 20px auto"},
        ),

        # Slider: how many recent trades we show
        html.Div(
            style={"textAlign": "center", "marginBottom": "10px"},
            children=[
                html.Span("Show last "),
                dcc.Slider(
                    id="points-slider",
                    min=50,
                    max=400,
                    step=50,
                    value=200,
                    marks={i: str(i) for i in range(50, 401, 50)},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                html.Div(id="points-label", style={"marginTop": "8px"}),
            ],
        ),

        # Main price chart
        dcc.Graph(
            id="price-chart",
            style={"height": "500px"},
        ),

        # Auto-refresh timer → every 0.5 seconds
        
        dcc.Interval(
            id="update-interval",
            interval=5000,  # 500 milliseconds (0.5s)
            n_intervals=0,
        ),
    ],
)


@app.callback(
    Output("points-label", "children"),
    Input("points-slider", "value"),
)
def update_points_label(n_points):
    # Just show a friendly line under the slider
    return f"Currently showing last {n_points} trades."


@app.callback(
    Output("price-chart", "figure"),
    [
        Input("symbol-dropdown", "value"),
        Input("points-slider", "value"),
        Input("update-interval", "n_intervals"),
    ],
)
def update_chart(selected_symbol, n_points, n_intervals):
    # Every 0.5s we come here, pull fresh rows, and redraw the chart
    df = fetch_trades(selected_symbol, limit=n_points)

    # If the DB is empty or Kafka is down, we handle it nicely
    if df.empty:
        return go.Figure(
            layout=go.Layout(
                title=f"{selected_symbol} – no data found",
                xaxis=dict(title="Time"),
                yaxis=dict(title="Price (USDT)"),
            )
        )

    # Price trace
    price_trace = go.Scatter(
        x=df["trade_time"],
        y=df["price"],
        mode="lines+markers",
        name="Price",
    )

    # Simple 10-point moving average so the line looks smoother
    traces = [price_trace]
    if len(df) >= 10:
        df["ma_10"] = df["price"].rolling(window=10).mean()
        ma_trace = go.Scatter(
            x=df["trade_time"],
            y=df["ma_10"],
            mode="lines",
            name="MA(10)",
            line=dict(dash="dash"),
        )
        traces.append(ma_trace)

    layout = go.Layout(
        title=f"{selected_symbol} – last {len(df)} trades",
        xaxis=dict(title="Trade Time"),
        yaxis=dict(title="Price (USDT)"),
        hovermode="x unified",
        margin=dict(l=60, r=30, t=70, b=60),
        paper_bgcolor="#C0F6CE",     # background outside chart
        plot_bgcolor="#CEE6F1",      # background inside chart
        font=dict(color="black")
    )

    return go.Figure(data=traces, layout=layout)


if __name__ == "__main__":
    # debug=False → hides the Dash dev toolbar at the bottom
    app.run(debug=False)


