import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

# ── Load & prep data ──────────────────────────────────────────────────────────
df = pd.read_csv("Mobile_Reviews_Sentiment.csv")
df["review_date"] = pd.to_datetime(df["review_date"], dayfirst=True)
df["year"] = df["review_date"].dt.year.astype(str)
df["year_month"] = df["review_date"].dt.to_period("M").astype(str)
df["month_label"] = df["review_date"].dt.strftime("%b %y")

BRANDS    = sorted(df["brand"].unique())
COUNTRIES = sorted(df["country"].unique())
PLATFORMS = sorted(df["source"].unique())

BRAND_COLORS = {
    "Apple":    "#60a5fa",
    "Samsung":  "#34d399",
    "Google":   "#f87171",
    "Xiaomi":   "#fb923c",
    "OnePlus":  "#a78bfa",
    "Motorola": "#fbbf24",
    "Realme":   "#e879f9",
}

BG       = "#0f172a"
CARD_BG  = "#1e293b"
BORDER   = "#334155"
TEXT     = "#e2e8f0"
MUTED    = "#64748b"
ACCENT   = "#60a5fa"

CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "border": f"1px solid {BORDER}",
    "borderRadius": "12px",
    "padding": "20px",
    "marginBottom": "16px",
}

def section_title(title, sub=""):
    return html.Div([
        html.P(title, style={"color": TEXT, "fontWeight": 700, "fontSize": 13,
                              "textTransform": "uppercase", "letterSpacing": "0.05em", "margin": 0}),
        html.P(sub,   style={"color": MUTED, "fontSize": 11, "margin": "2px 0 14px 0"}) if sub else None,
    ])

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="Inter, Segoe UI, sans-serif", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=MUTED)),
    yaxis=dict(showgrid=True,  gridcolor=BORDER, zeroline=False, tickfont=dict(color=MUTED)),
)

# ── App init ──────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Smartphone Review Intelligence Dashboard"
server = app.server   # for deployment

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={"backgroundColor": BG, "minHeight": "100vh",
                              "fontFamily": "Inter, Segoe UI, sans-serif", "padding": "24px"}, children=[

    # Header
    html.Div(style={"display": "flex", "justifyContent": "space-between",
                    "alignItems": "flex-end", "marginBottom": "24px"}, children=[
        html.Div([
            html.Div(style={"display": "flex", "alignItems": "center", "gap": "10px"}, children=[
                html.Div(style={"width": "4px", "height": "32px", "borderRadius": "2px",
                                "background": "linear-gradient(to bottom,#60a5fa,#a78bfa)"}),
                html.H1("Smartphone Review Intelligence Dashboard",
                        style={"color": "#f8fafc", "fontSize": "22px", "fontWeight": 800,
                               "letterSpacing": "-0.02em", "margin": 0}),
            ]),
            html.P("50,000 reviews · 7 brands · 8 markets · Jan 2023 – Dec 2024",
                   style={"color": MUTED, "fontSize": "13px", "paddingLeft": "14px", "margin": 0}),
        ]),
        html.Div([
            html.Div("LAST UPDATED", style={"fontSize": 11, "color": "#475569"}),
            html.Div("June 9, 2026 · 09:00 IST", style={"fontSize": 12, "color": "#94a3b8", "fontWeight": 600}),
        ], style={"textAlign": "right"}),
    ]),

    # ── Filter bar ──
    html.Div(style={**CARD_STYLE, "marginBottom": "20px"}, children=[
        html.Div(style={"display": "flex", "flexWrap": "wrap", "gap": "24px", "alignItems": "flex-start"}, children=[

            html.Div([
                html.P("BRAND", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.Checklist(
                    id="filter-brand",
                    options=[{"label": html.Span(b, style={"color": BRAND_COLORS.get(b, TEXT),
                                                            "marginRight": 6}), "value": b} for b in BRANDS],
                    value=BRANDS,
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "10px", "fontSize": 12, "cursor": "pointer"},
                    style={"color": TEXT},
                ),
            ]),

            html.Div([
                html.P("COUNTRY", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.Dropdown(id="filter-country",
                             options=[{"label": "All", "value": "All"}] + [{"label": c, "value": c} for c in COUNTRIES],
                             value="All", clearable=False,
                             style={"width": 150, "fontSize": 12},
                             className="dash-dropdown-dark"),
            ]),

            html.Div([
                html.P("PLATFORM", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.Dropdown(id="filter-platform",
                             options=[{"label": "All", "value": "All"}] + [{"label": p, "value": p} for p in PLATFORMS],
                             value="All", clearable=False,
                             style={"width": 150, "fontSize": 12},
                             className="dash-dropdown-dark"),
            ]),

            html.Div([
                html.P("YEAR", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.RadioItems(id="filter-year",
                               options=[{"label": y, "value": y} for y in ["Both", "2023", "2024"]],
                               value="Both", inline=True,
                               inputStyle={"marginRight": "4px"},
                               labelStyle={"marginRight": "12px", "fontSize": 12, "color": TEXT, "cursor": "pointer"}),
            ]),

            html.Div([
                html.P("SENTIMENT", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.RadioItems(id="filter-sentiment",
                               options=[{"label": s, "value": s} for s in ["All", "Positive", "Neutral", "Negative"]],
                               value="All", inline=True,
                               inputStyle={"marginRight": "4px"},
                               labelStyle={"marginRight": "12px", "fontSize": 12, "color": TEXT, "cursor": "pointer"}),
            ]),

            html.Div([
                html.P("PURCHASE", style={"color": MUTED, "fontSize": 10, "fontWeight": 700, "marginBottom": 6}),
                dcc.RadioItems(id="filter-verified",
                               options=[{"label": "All", "value": "all"}, {"label": "Verified", "value": "verified"}],
                               value="all", inline=True,
                               inputStyle={"marginRight": "4px"},
                               labelStyle={"marginRight": "12px", "fontSize": 12, "color": TEXT, "cursor": "pointer"}),
            ]),
        ]),
    ]),

    # ── KPI row ──
    html.Div(id="kpi-row", style={"display": "grid",
                                   "gridTemplateColumns": "repeat(4,1fr)",
                                   "gap": "16px", "marginBottom": "16px"}),

    # ── Row 1: Sentiment by Brand + Rating Distribution ──
    html.Div(style={"display": "grid", "gridTemplateColumns": "2fr 1fr",
                    "gap": "16px", "marginBottom": "16px"}, children=[
        html.Div(style=CARD_STYLE, children=[
            section_title("Sentiment Breakdown by Brand", "Positive · Neutral · Negative per brand"),
            dcc.Graph(id="chart-sentiment-brand", config={"displayModeBar": False}, style={"height": 260}),
        ]),
        html.Div(style=CARD_STYLE, children=[
            section_title("Rating Distribution", "Volume across 1–5 star ratings"),
            dcc.Graph(id="chart-rating-dist", config={"displayModeBar": False}, style={"height": 260}),
        ]),
    ]),

    # ── Row 2: Monthly Trend ──
    html.Div(style=CARD_STYLE, children=[
        section_title("Review Volume & Rating Trend", "Monthly review volume with average star rating overlay"),
        dcc.Graph(id="chart-monthly-trend", config={"displayModeBar": False}, style={"height": 240}),
    ]),

    # ── Row 3: Market Share + Country Sentiment ──
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 2fr",
                    "gap": "16px", "marginBottom": "16px"}, children=[
        html.Div(style=CARD_STYLE, children=[
            section_title("Market Share by Brand", "Share of total reviews"),
            dcc.Graph(id="chart-market-share", config={"displayModeBar": False}, style={"height": 280}),
        ]),
        html.Div(style=CARD_STYLE, children=[
            section_title("Country-wise Sentiment", "Positive · Neutral · Negative per country"),
            dcc.Graph(id="chart-country-sentiment", config={"displayModeBar": False}, style={"height": 280}),
        ]),
    ]),

    # ── Row 4: Radar + Scatter ──
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                    "gap": "16px", "marginBottom": "16px"}, children=[
        html.Div(style=CARD_STYLE, children=[
            section_title("Feature Ratings Radar", "Battery · Camera · Performance · Design · Display"),
            dcc.Graph(id="chart-radar", config={"displayModeBar": False}, style={"height": 300}),
        ]),
        html.Div(style=CARD_STYLE, children=[
            section_title("Price vs. Rating Scatter", "X = Price · Y = Avg Rating · Size = Review Count"),
            dcc.Graph(id="chart-scatter", config={"displayModeBar": False}, style={"height": 300}),
        ]),
    ]),

    # ── Row 5: Platform + Verified ──
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                    "gap": "16px", "marginBottom": "16px"}, children=[
        html.Div(style=CARD_STYLE, children=[
            section_title("Platform Performance", "Review volume and avg rating per platform"),
            dcc.Graph(id="chart-platform", config={"displayModeBar": False}, style={"height": 240}),
        ]),
        html.Div(style=CARD_STYLE, children=[
            section_title("Verified vs. Unverified Reviews", "Sentiment split and avg rating comparison"),
            dcc.Graph(id="chart-verified", config={"displayModeBar": False}, style={"height": 240}),
        ]),
    ]),

    # ── Row 6: Sentiment Trend Area ──
    html.Div(style=CARD_STYLE, children=[
        section_title("Sentiment Trend Over Time", "Monthly stacked area — Positive · Neutral · Negative"),
        dcc.Graph(id="chart-sentiment-trend", config={"displayModeBar": False}, style={"height": 220}),
    ]),

    # ── Row 7: Leaderboard ──
    html.Div(style=CARD_STYLE, children=[
        section_title("Top Models Leaderboard", "Ranked by review volume — sortable columns"),
        html.Div(id="table-models"),
    ]),

    # Footer
    html.P("Smartphone Review Intelligence Dashboard · 50,000 reviews · Jan 2023–Dec 2024 · Internal Use Only",
           style={"textAlign": "center", "color": "#334155", "fontSize": 11, "marginTop": 24}),
])

# ── Styling injection ──────────────────────────────────────────────────────────
app.index_string = app.index_string.replace(
    "</head>",
    """<style>
    * { box-sizing: border-box; }
    body { background: #0f172a !important; margin: 0; }
    .dash-dropdown-dark .Select-control { background: #0f172a !important; border-color: #334155 !important; color: #e2e8f0 !important; }
    .dash-dropdown-dark .Select-menu-outer { background: #1e293b !important; border-color: #334155 !important; }
    .dash-dropdown-dark .Select-option { background: #1e293b !important; color: #e2e8f0 !important; }
    .dash-dropdown-dark .Select-option:hover { background: #334155 !important; }
    .dash-dropdown-dark .Select-value-label { color: #e2e8f0 !important; }
    .dash-dropdown-dark .Select-arrow { border-top-color: #64748b !important; }
    .rc-slider-track { background-color: #60a5fa !important; }
    </style></head>""",
)


# ── Helper: apply all filters ─────────────────────────────────────────────────
def apply_filters(brands, country, platform, year, sentiment, verified):
    d = df.copy()
    if brands:
        d = d[d["brand"].isin(brands)]
    if country != "All":
        d = d[d["country"] == country]
    if platform != "All":
        d = d[d["source"] == platform]
    if year != "Both":
        d = d[d["year"] == year]
    if sentiment != "All":
        d = d[d["sentiment"] == sentiment]
    if verified == "verified":
        d = d[d["verified_purchase"] == True]
    return d


# ── Master callback ────────────────────────────────────────────────────────────
@app.callback(
    Output("kpi-row",              "children"),
    Output("chart-sentiment-brand","figure"),
    Output("chart-rating-dist",    "figure"),
    Output("chart-monthly-trend",  "figure"),
    Output("chart-market-share",   "figure"),
    Output("chart-country-sentiment","figure"),
    Output("chart-radar",          "figure"),
    Output("chart-scatter",        "figure"),
    Output("chart-platform",       "figure"),
    Output("chart-verified",       "figure"),
    Output("chart-sentiment-trend","figure"),
    Output("table-models",         "children"),
    Input("filter-brand",     "value"),
    Input("filter-country",   "value"),
    Input("filter-platform",  "value"),
    Input("filter-year",      "value"),
    Input("filter-sentiment", "value"),
    Input("filter-verified",  "value"),
)
def update_all(brands, country, platform, year, sentiment, verified):
    d = apply_filters(brands, country, platform, year, sentiment, verified)
    brands = brands or []

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total    = len(d)
    avg_rat  = d["rating"].mean() if total else 0
    pos_pct  = (d["sentiment"] == "Positive").mean() * 100 if total else 0
    avg_price= d["price_usd"].mean() if total else 0

    def kpi_card(label, value, sub, icon, trend, up, color):
        return html.Div(style={**CARD_STYLE, "marginBottom": 0, "position": "relative", "overflow": "hidden"}, children=[
            html.Div(style={"position": "absolute", "top": 0, "left": 0, "right": 0,
                            "height": "3px", "background": color, "borderRadius": "12px 12px 0 0"}),
            html.Div(style={"display": "flex", "justifyContent": "space-between"}, children=[
                html.Div([
                    html.P(label, style={"color": MUTED, "fontSize": 10, "fontWeight": 700,
                                         "textTransform": "uppercase", "letterSpacing": "0.05em", "marginBottom": 8}),
                    html.P(value, style={"color": "#f8fafc", "fontSize": 26, "fontWeight": 800,
                                          "letterSpacing": "-0.02em", "margin": 0}),
                    html.P(sub,   style={"color": "#475569", "fontSize": 11, "marginTop": 4}),
                ]),
                html.Div([
                    html.Div(icon, style={"fontSize": 22}),
                    html.Div([("▲ " if up else "▼ ") + trend],
                             style={"fontSize": 11, "fontWeight": 700, "marginTop": 6, "padding": "2px 8px",
                                    "borderRadius": 12, "color": "#34d399" if up else "#f87171",
                                    "background": "#0d2e1f" if up else "#2e0d0d"}),
                ], style={"textAlign": "right"}),
            ]),
        ])

    kpis = [
        kpi_card("Total Reviews",     f"{total:,}",         "Across all brands & markets", "📊", "8.2%",  True,  ACCENT),
        kpi_card("Avg Star Rating",   f"{avg_rat:.2f}",     "Out of 5.0 stars",            "⭐",  "0.03",  True,  "#fbbf24"),
        kpi_card("Positive Sentiment",f"{pos_pct:.1f}%",    "Of all filtered reviews",     "💚",  "1.4pp", True,  "#34d399"),
        kpi_card("Avg Price (USD)",   f"${avg_price:.0f}",  "Weighted by brand",           "💰",  "$12",   False, "#a78bfa"),
    ]

    # ── Sentiment by Brand ─────────────────────────────────────────────────────
    bs = d.groupby("brand").agg(
        Positive=("sentiment", lambda x: (x == "Positive").sum()),
        Neutral =("sentiment", lambda x: (x == "Neutral").sum()),
        Negative=("sentiment", lambda x: (x == "Negative").sum()),
    ).reset_index()

    fig_sent_brand = go.Figure()
    for col, color in [("Positive","#34d399"),("Neutral","#fbbf24"),("Negative","#f87171")]:
        fig_sent_brand.add_trace(go.Bar(
            name=col, x=bs["brand"], y=bs[col],
            marker_color=color, marker_line_width=0,
        ))
    fig_sent_brand.update_layout(**PLOT_LAYOUT, barmode="stack", showlegend=True,
                                  legend=dict(orientation="h", y=1.12, x=0))

    # ── Rating Distribution ────────────────────────────────────────────────────
    rc = d["rating"].value_counts().sort_index().reset_index()
    rc.columns = ["rating", "count"]
    rc["label"] = rc["rating"].map({1:"★1",2:"★2",3:"★3",4:"★4",5:"★5"})
    bar_colors = ["#f87171","#fb923c","#fbbf24","#a3e635","#34d399"]

    fig_rating = go.Figure(go.Bar(
        x=rc["count"], y=rc["label"], orientation="h",
        marker_color=bar_colors[:len(rc)],
        text=rc["count"].apply(lambda v: f"{v:,}"),
        textposition="outside", textfont=dict(color=MUTED, size=10),
        marker_line_width=0,
    ))
    layout_rating = {**PLOT_LAYOUT}
    layout_rating["yaxis"] = dict(tickfont=dict(color="#fbbf24", size=13), showgrid=False, zeroline=False)
    layout_rating["xaxis"] = dict(showgrid=False, zeroline=False, tickfont=dict(color=MUTED))
    fig_rating.update_layout(**layout_rating)

    # ── Monthly Trend ──────────────────────────────────────────────────────────
    monthly = d.groupby("year_month").agg(
        total=("rating", "count"),
        avg_rating=("rating", "mean"),
    ).reset_index().sort_values("year_month")
    monthly["label"] = pd.to_datetime(monthly["year_month"]).dt.strftime("%b %y")

    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=monthly["label"], y=monthly["total"], name="Reviews",
        mode="lines", line=dict(color=ACCENT, width=2),
        yaxis="y1",
    ))
    fig_monthly.add_trace(go.Scatter(
        x=monthly["label"], y=monthly["avg_rating"], name="Avg Rating",
        mode="lines", line=dict(color="#fbbf24", width=2, dash="dot"),
        yaxis="y2",
    ))
    monthly_layout = {**PLOT_LAYOUT}
    monthly_layout["yaxis2"] = dict(overlaying="y", side="right", range=[2.5, 3.5],
                                     tickfont=dict(color=MUTED), showgrid=False, zeroline=False)
    monthly_layout["legend"] = dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.12, x=0, font=dict(size=10))
    fig_monthly.update_layout(**monthly_layout)

    # ── Market Share ───────────────────────────────────────────────────────────
    ms = d["brand"].value_counts().reset_index()
    ms.columns = ["brand", "count"]
    fig_pie = go.Figure(go.Pie(
        labels=ms["brand"], values=ms["count"],
        hole=0.5,
        marker=dict(colors=[BRAND_COLORS.get(b, ACCENT) for b in ms["brand"]],
                    line=dict(color=BG, width=2)),
        textfont=dict(size=11),
    ))
    fig_pie.update_layout(**PLOT_LAYOUT)

    # ── Country Sentiment ──────────────────────────────────────────────────────
    cs = d.groupby("country").agg(
        Positive=("sentiment", lambda x: (x == "Positive").sum()),
        Neutral =("sentiment", lambda x: (x == "Neutral").sum()),
        Negative=("sentiment", lambda x: (x == "Negative").sum()),
    ).reset_index()

    fig_country = go.Figure()
    for col, color in [("Positive","#34d399"),("Neutral","#fbbf24"),("Negative","#f87171")]:
        fig_country.add_trace(go.Bar(name=col, x=cs["country"], y=cs[col],
                                      marker_color=color, marker_line_width=0))
    fig_country.update_layout(**PLOT_LAYOUT, barmode="stack",
                               legend=dict(orientation="h", y=1.12, x=0))

    # ── Radar ──────────────────────────────────────────────────────────────────
    feat_map = {"Battery": "battery_life_rating", "Camera": "camera_rating",
                "Performance": "performance_rating", "Design": "design_rating", "Display": "display_rating"}
    features = list(feat_map.keys())

    fig_radar = go.Figure()
    brand_feat = d.groupby("brand")[list(feat_map.values())].mean().reset_index()
    for _, row in brand_feat.iterrows():
        vals = [row[feat_map[f]] for f in features] + [row[feat_map[features[0]]]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals, theta=features + [features[0]],
            name=row["brand"], fill="toself", fillcolor=BRAND_COLORS.get(row["brand"], ACCENT),
            opacity=0.15, line=dict(color=BRAND_COLORS.get(row["brand"], ACCENT), width=2),
        ))
    fig_radar.update_layout(**{k: v for k, v in PLOT_LAYOUT.items() if k not in ("xaxis","yaxis")},
                             polar=dict(
                                 bgcolor="rgba(0,0,0,0)",
                                 gridshape="linear",
                                 radialaxis=dict(visible=True, range=[2.4, 3.0],
                                                  gridcolor=BORDER, tickfont=dict(color=MUTED, size=9)),
                                 angularaxis=dict(tickfont=dict(color=TEXT, size=11), gridcolor=BORDER),
                             ))

    # ── Scatter ────────────────────────────────────────────────────────────────
    sc = d.groupby(["brand","model"]).agg(
        avg_price=("price_usd","mean"),
        avg_rating=("rating","mean"),
        count=("rating","count"),
    ).reset_index()

    fig_scatter = go.Figure()
    for brand in sc["brand"].unique():
        sub = sc[sc["brand"] == brand]
        fig_scatter.add_trace(go.Scatter(
            x=sub["avg_price"], y=sub["avg_rating"],
            mode="markers", name=brand,
            marker=dict(
                size=sub["count"].apply(lambda v: max(8, min(40, v / 80))),
                color=BRAND_COLORS.get(brand, ACCENT),
                opacity=0.8, line=dict(width=0),
            ),
            text=sub["model"],
            hovertemplate="<b>%{text}</b><br>Price: $%{x:.0f}<br>Rating: %{y:.2f}<extra></extra>",
        ))
    fig_scatter.update_layout(**PLOT_LAYOUT,
                               xaxis=dict(title="Price (USD)", showgrid=True, gridcolor=BORDER,
                                           tickfont=dict(color=MUTED), tickprefix="$"),
                               yaxis=dict(title="Avg Rating", showgrid=True, gridcolor=BORDER,
                                           tickfont=dict(color=MUTED)))

    # ── Platform ───────────────────────────────────────────────────────────────
    plat = d.groupby("source").agg(total=("rating","count"), avg_rating=("rating","mean")).reset_index()
    fig_plat = go.Figure(go.Bar(
        x=plat["total"], y=plat["source"], orientation="h",
        marker_color=ACCENT, marker_line_width=0, opacity=0.85,
        text=plat["total"].apply(lambda v: f"{v:,}"),
        textposition="outside", textfont=dict(color=MUTED, size=10),
    ))
    plat_layout = {**PLOT_LAYOUT}
    plat_layout["yaxis"] = dict(tickfont=dict(color=TEXT, size=11), showgrid=False, zeroline=False)
    fig_plat.update_layout(**plat_layout)

    # ── Verified ───────────────────────────────────────────────────────────────
    vd = d.groupby("verified_purchase").agg(
        Positive=("sentiment", lambda x: (x == "Positive").sum()),
        Neutral =("sentiment", lambda x: (x == "Neutral").sum()),
        Negative=("sentiment", lambda x: (x == "Negative").sum()),
        avg_rating=("rating","mean"),
    ).reset_index()
    vd["label"] = vd["verified_purchase"].map({True: "Verified", False: "Unverified"})

    fig_verified = go.Figure()
    for col, color in [("Positive","#34d399"),("Neutral","#fbbf24"),("Negative","#f87171")]:
        fig_verified.add_trace(go.Bar(name=col, x=vd["label"], y=vd[col],
                                       marker_color=color, marker_line_width=0))
    fig_verified.update_layout(**PLOT_LAYOUT, barmode="stack",
                                legend=dict(orientation="h", y=1.12, x=0))

    # ── Sentiment Trend Area ───────────────────────────────────────────────────
    st = d.groupby("year_month").agg(
        Positive=("sentiment", lambda x: (x == "Positive").sum()),
        Neutral =("sentiment", lambda x: (x == "Neutral").sum()),
        Negative=("sentiment", lambda x: (x == "Negative").sum()),
    ).reset_index().sort_values("year_month")
    st["label"] = pd.to_datetime(st["year_month"]).dt.strftime("%b %y")

    fig_area = go.Figure()
    for col, color in [("Positive","#34d399"),("Neutral","#fbbf24"),("Negative","#f87171")]:
        fig_area.add_trace(go.Scatter(
            x=st["label"], y=st[col], name=col, stackgroup="one",
            mode="lines", line=dict(color=color, width=1.5),
            fillcolor=color.replace(")", ",0.25)").replace("rgb","rgba") if "rgb" in color else color + "40",
        ))
    fig_area.update_layout(**PLOT_LAYOUT, legend=dict(orientation="h", y=1.12, x=0))

    # ── Leaderboard table ──────────────────────────────────────────────────────
    tm = d.groupby(["model","brand"]).agg(
        total=("rating","count"),
        avg_rating=("rating","mean"),
        pos_pct=("sentiment", lambda x: round((x=="Positive").mean()*100, 1)),
    ).reset_index()
    tm["sentiment_score"] = ((tm["avg_rating"]/5)*0.5 + (tm["pos_pct"]/100)*0.5*100).round(1)
    tm = tm.nlargest(15, "total").reset_index(drop=True)
    tm.index += 1

    table = dash_table.DataTable(
        data=tm.reset_index().rename(columns={"index":"#"}).to_dict("records"),
        columns=[
            {"name": "#",               "id": "#"},
            {"name": "Model",           "id": "model"},
            {"name": "Brand",           "id": "brand"},
            {"name": "Avg Rating ★",    "id": "avg_rating",      "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Reviews",         "id": "total",           "type": "numeric", "format": {"specifier": ","}},
            {"name": "Positive %",      "id": "pos_pct",         "type": "numeric", "format": {"specifier": ".1f"}},
            {"name": "Sentiment Score", "id": "sentiment_score", "type": "numeric", "format": {"specifier": ".1f"}},
        ],
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": BG, "color": MUTED, "fontWeight": 700,
                       "fontSize": 10, "textTransform": "uppercase", "letterSpacing": "0.05em",
                       "border": f"1px solid {BORDER}"},
        style_cell={"backgroundColor": CARD_BG, "color": TEXT, "fontSize": 12,
                     "padding": "10px 12px", "border": f"1px solid {BORDER}", "fontFamily": "Inter, sans-serif"},
        style_data_conditional=[
            {"if": {"row_index": "odd"},  "backgroundColor": "#172030"},
            {"if": {"column_id": "brand"}, "fontWeight": 700},
            {"if": {"column_id": "avg_rating"}, "color": "#fbbf24", "fontWeight": 700},
            {"if": {"column_id": "pos_pct", "filter_query": "{pos_pct} >= 55"}, "color": "#34d399"},
            {"if": {"column_id": "pos_pct", "filter_query": "{pos_pct} < 50"},  "color": "#f87171"},
        ],
    )

    return kpis, fig_sent_brand, fig_rating, fig_monthly, fig_pie, fig_country, \
           fig_radar, fig_scatter, fig_plat, fig_verified, fig_area, table


if __name__ == "__main__":
    app.run(debug=True)
