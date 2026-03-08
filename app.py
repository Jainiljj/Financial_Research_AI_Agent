import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS  – dark editorial / terminal feel
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0a0c0f;
    --surface:   #111318;
    --border:    #1e2229;
    --accent:    #00e5a0;
    --accent2:   #ff6b35;
    --muted:     #4a5568;
    --text:      #e2e8f0;
    --text-dim:  #718096;
}

/* ── Global ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Inputs ── */
input, textarea, select,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] select {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
}
input:focus, textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(0,229,160,.15) !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    transition: all .2s ease !important;
    padding: .5rem 1.5rem !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 18px rgba(0,229,160,.35) !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 1rem !important;
}
div[data-testid="metric-container"] label { color: var(--text-dim) !important; font-size: .7rem !important; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: var(--accent) !important; font-size: 1.4rem !important; }

/* ── Tabs ── */
button[data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: .75rem !important;
    font-weight: 700 !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
div[data-baseweb="tab-list"] { border-bottom: 1px solid var(--border) !important; }

/* ── Expander ── */
details { border: 1px solid var(--border) !important; border-radius: 6px !important; background: var(--surface) !important; }
summary { color: var(--text-dim) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Selectbox ── */
div[data-baseweb="select"] > div { background: var(--surface) !important; border-color: var(--border) !important; }

/* ── Spinner ── */
.stSpinner > div > div { border-top-color: var(--accent) !important; }

/* ── Info / warning / success ── */
.stAlert { background: var(--surface) !important; border: 1px solid var(--border) !important; }

/* ── Custom card classes ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem;
    margin-bottom: .75rem;
}
.card-accent { border-left: 3px solid var(--accent) !important; }
.card-warn   { border-left: 3px solid var(--accent2) !important; }

.tag {
    display: inline-block;
    background: rgba(0,229,160,.12);
    color: var(--accent);
    border-radius: 3px;
    padding: 2px 8px;
    font-size: .65rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-right: 4px;
}
.tag-orange { background: rgba(255,107,53,.12) !important; color: var(--accent2) !important; }

.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -.02em;
    line-height: 1;
    margin: 0;
}
.hero-sub {
    color: var(--text-dim);
    font-size: .75rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-top: .5rem;
}
.accent { color: var(--accent); }
.dim { color: var(--text-dim); }

.news-item {
    border-bottom: 1px solid var(--border);
    padding: .9rem 0;
}
.news-item:last-child { border-bottom: none; }

.risk-bar-wrap { background: var(--border); border-radius: 4px; height: 8px; overflow: hidden; }
.risk-bar { height: 100%; border-radius: 4px; transition: width .6s ease; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

INDIAN_STOCKS = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "State Bank of India": "SBIN.NS",
}

US_STOCKS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Meta": "META",
    "Netflix": "NFLX",
}

@st.cache_data(ttl=300)
def fetch_stock_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_stock_info(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception:
        return {}

def compute_risk_metrics(hist: pd.DataFrame) -> dict:
    if hist.empty:
        return {}
    returns = hist["Close"].pct_change().dropna()
    vol = returns.std()
    annual_vol = vol * np.sqrt(252)
    sharpe = (returns.mean() / vol) * np.sqrt(252) if vol != 0 else 0
    max_dd = ((hist["Close"] / hist["Close"].cummax()) - 1).min()
    beta_approx = vol / 0.012  # normalised proxy
    return {
        "daily_vol": float(vol),
        "annual_vol": float(annual_vol),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_dd),
        "beta": float(beta_approx),
    }

def risk_level(annual_vol: float) -> tuple:
    if annual_vol < 0.15:  return "LOW",    "#00e5a0", 25
    if annual_vol < 0.30:  return "MEDIUM", "#f6c90e", 55
    if annual_vol < 0.50:  return "HIGH",   "#ff6b35", 75
    return "VERY HIGH", "#ff3860", 95

def candlestick_chart(hist: pd.DataFrame, ticker: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"],
        increasing_line_color="#00e5a0", decreasing_line_color="#ff6b35",
        name=ticker
    ))
    ma20 = hist["Close"].rolling(20).mean()
    ma50 = hist["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=hist.index, y=ma20, name="MA20",
                             line=dict(color="#60a5fa", width=1, dash="dot")))
    fig.add_trace(go.Scatter(x=hist.index, y=ma50, name="MA50",
                             line=dict(color="#a78bfa", width=1, dash="dot")))
    fig.update_layout(
        paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
        font=dict(family="Space Mono", color="#e2e8f0", size=11),
        xaxis=dict(gridcolor="#1e2229", showgrid=True, rangeslider_visible=False),
        yaxis=dict(gridcolor="#1e2229", showgrid=True),
        margin=dict(l=0, r=0, t=8, b=0),
        legend=dict(bgcolor="#111318", bordercolor="#1e2229", borderwidth=1),
        height=360,
    )
    return fig

def volume_chart(hist: pd.DataFrame) -> go.Figure:
    colors = ["#00e5a0" if c >= o else "#ff6b35"
              for c, o in zip(hist["Close"], hist["Open"])]
    fig = go.Figure(go.Bar(x=hist.index, y=hist["Volume"], marker_color=colors, name="Volume"))
    fig.update_layout(
        paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
        font=dict(family="Space Mono", color="#e2e8f0", size=11),
        xaxis=dict(gridcolor="#1e2229"), yaxis=dict(gridcolor="#1e2229"),
        margin=dict(l=0, r=0, t=8, b=0), height=180,
        showlegend=False,
    )
    return fig

def returns_distribution(hist: pd.DataFrame) -> go.Figure:
    returns = hist["Close"].pct_change().dropna() * 100
    fig = go.Figure(go.Histogram(
        x=returns, nbinsx=50,
        marker_color="#00e5a0", opacity=.75,
        name="Daily Returns %"
    ))
    fig.update_layout(
        paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
        font=dict(family="Space Mono", color="#e2e8f0", size=11),
        xaxis=dict(gridcolor="#1e2229", title="Return (%)"),
        yaxis=dict(gridcolor="#1e2229", title="Frequency"),
        margin=dict(l=0, r=0, t=8, b=0), height=280,
        showlegend=False,
    )
    return fig

def portfolio_pie(tickers_weights: dict) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=list(tickers_weights.keys()),
        values=list(tickers_weights.values()),
        hole=.55,
        marker=dict(colors=["#00e5a0","#ff6b35","#60a5fa","#f6c90e","#a78bfa",
                             "#fb7185","#34d399","#fb923c"]),
        textfont=dict(family="Space Mono", size=10),
    ))
    fig.update_layout(
        paper_bgcolor="#111318",
        font=dict(family="Space Mono", color="#e2e8f0"),
        margin=dict(l=0, r=0, t=8, b=0), height=300,
        legend=dict(bgcolor="#111318", bordercolor="#1e2229", borderwidth=1),
        showlegend=True,
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title"><span class="accent">Fin</span>Sight</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">AI Research Agent · v1.0</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Keys from manam.py — pre-filled so agent works immediately
    _GROQ_KEY = "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"
    _NEWS_KEY = "03d6fc122d4e4aa687e3ac01b7f945ca"

    st.markdown("#### ⚙️ API Configuration")
    groq_key = st.text_input("GROQ API Key", value=_GROQ_KEY, type="password",
                              help="Pre-filled from manam.py")
    news_key = st.text_input("NewsAPI Key", value=_NEWS_KEY, type="password",
                              help="Pre-filled from manam.py")

    st.markdown("---")
    st.markdown("#### 📍 Market Selection")
    market = st.selectbox("Market", ["Indian (NSE/BSE)", "US Markets", "Custom Ticker"])

    if market == "Indian (NSE/BSE)":
        preset_map = INDIAN_STOCKS
    elif market == "US Markets":
        preset_map = US_STOCKS
    else:
        preset_map = {}

    if preset_map:
        selected_name = st.selectbox("Stock", list(preset_map.keys()))
        ticker_input = preset_map[selected_name]
    else:
        ticker_input = st.text_input("Ticker Symbol", value="AAPL",
                                      placeholder="e.g. RELIANCE.NS").upper().strip()

    period = st.select_slider("History Period",
                               options=["1mo","3mo","6mo","1y","2y","5y"],
                               value="6mo")

    st.markdown("---")
    st.markdown("#### 🤖 AI Analysis")
    ai_query = st.text_area("Ask the AI Agent",
                             placeholder="Analyse Reliance stock risk and latest news...",
                             height=100)
    run_ai = st.button("▶ RUN ANALYSIS", use_container_width=True)

    st.markdown("---")
    st.caption("Track A • Week 1–2 Milestone\nBuilt with Streamlit + LangChain + yfinance")


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:1rem;margin-bottom:.25rem;">
  <h1 class="hero-title"><span class="accent">Fin</span>Sight AI</h1>
  <span class="tag">LIVE</span><span class="tag tag-orange">{market.split()[0].upper()}</span>
</div>
<p class="hero-sub">Financial Research Agent · Powered by LLaMA 3.3 · Real-time Market Intelligence</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Load data ──
hist = fetch_stock_data(ticker_input, period)
info = fetch_stock_info(ticker_input)

if hist.empty:
    st.error(f"⚠️ Could not fetch data for **{ticker_input}**. Check the ticker symbol.")
    st.stop()

risk = compute_risk_metrics(hist)
latest_close = float(hist["Close"].iloc[-1])
prev_close   = float(hist["Close"].iloc[-2]) if len(hist) > 1 else latest_close
day_chg      = (latest_close - prev_close) / prev_close * 100
week_chg     = (latest_close - float(hist["Close"].iloc[-6])) / float(hist["Close"].iloc[-6]) * 100 if len(hist) >= 6 else 0
month_start  = float(hist["Close"].iloc[max(0, len(hist)-22)])
month_chg    = (latest_close - month_start) / month_start * 100

rl, rl_color, rl_pct = risk_level(risk.get("annual_vol", 0))

# ── KPI Row ──
c1, c2, c3, c4, c5, c6 = st.columns(6)
currency = "₹" if ".NS" in ticker_input or ".BO" in ticker_input else "$"
c1.metric("Latest Price", f"{currency}{latest_close:,.2f}")
c2.metric("Day Change",   f"{day_chg:+.2f}%", delta=f"{day_chg:+.2f}%")
c3.metric("1-Week",       f"{week_chg:+.2f}%")
c4.metric("1-Month",      f"{month_chg:+.2f}%")
c5.metric("Annual Vol",   f"{risk.get('annual_vol',0)*100:.1f}%")
c6.metric("Sharpe Ratio", f"{risk.get('sharpe',0):.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  PRICE CHART", "⚡  RISK ANALYSIS", "💼  FUNDAMENTALS",
    "📰  NEWS FEED", "🤖  AI AGENT"
])

# ════════════════════════════════════════════
# TAB 1 – PRICE CHART
# ════════════════════════════════════════════
with tab1:
    chart_type = st.radio("Chart Type", ["Candlestick", "Line", "OHLC"],
                           horizontal=True, label_visibility="collapsed")

    if chart_type == "Candlestick":
        fig = candlestick_chart(hist, ticker_input)
    elif chart_type == "Line":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"],
                                  line=dict(color="#00e5a0", width=2), fill="tozeroy",
                                  fillcolor="rgba(0,229,160,.07)", name="Close"))
        fig.update_layout(paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
                           font=dict(family="Space Mono", color="#e2e8f0"),
                           xaxis=dict(gridcolor="#1e2229"),
                           yaxis=dict(gridcolor="#1e2229"),
                           margin=dict(l=0,r=0,t=8,b=0), height=360, showlegend=False)
    else:  # OHLC
        fig = go.Figure(go.Ohlc(
            x=hist.index, open=hist["Open"], high=hist["High"],
            low=hist["Low"], close=hist["Close"],
            increasing_line_color="#00e5a0", decreasing_line_color="#ff6b35"))
        fig.update_layout(paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
                           font=dict(family="Space Mono", color="#e2e8f0"),
                           xaxis=dict(gridcolor="#1e2229", rangeslider_visible=False),
                           yaxis=dict(gridcolor="#1e2229"),
                           margin=dict(l=0,r=0,t=8,b=0), height=360)

    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(volume_chart(hist), use_container_width=True)

    # Raw data table
    with st.expander("📋 Raw OHLCV Data"):
        df_show = hist[["Open","High","Low","Close","Volume"]].tail(30).copy()
        df_show.index = df_show.index.strftime("%Y-%m-%d")
        st.dataframe(df_show.style
                     .format("{:.2f}", subset=["Open","High","Low","Close"])
                     .format("{:,.0f}", subset=["Volume"]),
                     use_container_width=True)

# ════════════════════════════════════════════
# TAB 2 – RISK ANALYSIS
# ════════════════════════════════════════════
with tab2:
    left, right = st.columns([1, 1])

    with left:
        st.markdown(f"""
        <div class="card card-accent">
          <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;">Risk Profile · {ticker_input}</div>
          <div style="font-size:2rem;font-family:'Syne',sans-serif;font-weight:800;color:{rl_color};">{rl}</div>
          <div class="risk-bar-wrap" style="margin:.75rem 0;">
            <div class="risk-bar" style="width:{rl_pct}%;background:{rl_color};"></div>
          </div>
          <table style="width:100%;font-size:.72rem;border-collapse:collapse;">
            <tr><td class="dim">Daily Volatility</td><td style="text-align:right;color:#e2e8f0;">{risk.get('daily_vol',0)*100:.2f}%</td></tr>
            <tr><td class="dim">Annual Volatility</td><td style="text-align:right;color:#e2e8f0;">{risk.get('annual_vol',0)*100:.1f}%</td></tr>
            <tr><td class="dim">Sharpe Ratio</td><td style="text-align:right;color:#e2e8f0;">{risk.get('sharpe',0):.3f}</td></tr>
            <tr><td class="dim">Max Drawdown</td><td style="text-align:right;color:#ff6b35;">{risk.get('max_drawdown',0)*100:.2f}%</td></tr>
            <tr><td class="dim">Beta (approx)</td><td style="text-align:right;color:#e2e8f0;">{risk.get('beta',0):.2f}</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        # Value at Risk
        returns_series = hist["Close"].pct_change().dropna()
        var_95 = np.percentile(returns_series, 5) * 100
        var_99 = np.percentile(returns_series, 1) * 100
        st.markdown(f"""
        <div class="card card-warn">
          <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;">Value at Risk (Daily)</div>
          <div style="display:flex;justify-content:space-between;font-size:.8rem;margin-top:.5rem;">
            <span>VaR 95%</span><span style="color:#ff6b35;font-weight:700;">{var_95:.2f}%</span>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:.8rem;margin-top:.4rem;">
            <span>VaR 99%</span><span style="color:#ff3860;font-weight:700;">{var_99:.2f}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.plotly_chart(returns_distribution(hist), use_container_width=True)

        # Rolling volatility
        roll_vol = hist["Close"].pct_change().rolling(20).std() * np.sqrt(252) * 100
        fig_rv = go.Figure(go.Scatter(x=hist.index, y=roll_vol,
                                       line=dict(color="#ff6b35", width=1.5),
                                       fill="tozeroy", fillcolor="rgba(255,107,53,.08)"))
        fig_rv.update_layout(
            title=dict(text="20-Day Rolling Volatility (Annualised %)",
                       font=dict(family="Space Mono", size=11, color="#718096")),
            paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
            font=dict(family="Space Mono", color="#e2e8f0"),
            xaxis=dict(gridcolor="#1e2229"),
            yaxis=dict(gridcolor="#1e2229"),
            margin=dict(l=0,r=0,t=30,b=0), height=200, showlegend=False,
        )
        st.plotly_chart(fig_rv, use_container_width=True)

    # Drawdown chart
    drawdown = (hist["Close"] / hist["Close"].cummax()) - 1
    fig_dd = go.Figure(go.Scatter(x=hist.index, y=drawdown * 100,
                                   fill="tozeroy", fillcolor="rgba(255,56,96,.12)",
                                   line=dict(color="#ff3860", width=1)))
    fig_dd.update_layout(
        title=dict(text="Drawdown from Peak (%)",
                   font=dict(family="Space Mono", size=11, color="#718096")),
        paper_bgcolor="#111318", plot_bgcolor="#0a0c0f",
        font=dict(family="Space Mono", color="#e2e8f0"),
        xaxis=dict(gridcolor="#1e2229"), yaxis=dict(gridcolor="#1e2229"),
        margin=dict(l=0,r=0,t=30,b=0), height=200, showlegend=False,
    )
    st.plotly_chart(fig_dd, use_container_width=True)


# ════════════════════════════════════════════
# TAB 3 – FUNDAMENTALS
# ════════════════════════════════════════════
with tab3:
    if not info:
        st.warning("Fundamental data not available for this ticker.")
    else:
        col_a, col_b = st.columns(2)

        def info_row(label, key, fmt=None, prefix="", suffix=""):
            val = info.get(key)
            if val is None: return f'<tr><td class="dim">{label}</td><td style="text-align:right;color:#718096;">N/A</td></tr>'
            try:
                if fmt == "large":
                    if val >= 1e12: fval = f"{prefix}{val/1e12:.2f}T{suffix}"
                    elif val >= 1e9: fval = f"{prefix}{val/1e9:.2f}B{suffix}"
                    elif val >= 1e6: fval = f"{prefix}{val/1e6:.2f}M{suffix}"
                    else: fval = f"{prefix}{val:,.0f}{suffix}"
                elif fmt == "pct": fval = f"{val*100:.2f}%"
                elif fmt == "2f":  fval = f"{prefix}{val:.2f}{suffix}"
                else: fval = str(val)
            except: fval = str(val)
            return f'<tr><td class="dim">{label}</td><td style="text-align:right;color:#e2e8f0;">{fval}</td></tr>'

        with col_a:
            st.markdown(f"""
            <div class="card card-accent">
              <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.75rem;">Company Overview</div>
              <div style="font-size:1.1rem;font-family:'Syne',sans-serif;font-weight:700;margin-bottom:.25rem;">{info.get('longName', ticker_input)}</div>
              <div class="dim" style="font-size:.72rem;margin-bottom:.75rem;">{info.get('sector','—')} · {info.get('industry','—')}</div>
              <div class="dim" style="font-size:.7rem;line-height:1.6;">{(info.get('longBusinessSummary','') or '')[:300]}{'...' if len(info.get('longBusinessSummary','') or '') > 300 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
              <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;">Valuation</div>
              <table style="width:100%;font-size:.72rem;border-collapse:collapse;">
                {info_row("Market Cap",      "marketCap",          "large", currency)}
                {info_row("P/E (TTM)",        "trailingPE",         "2f")}
                {info_row("Forward P/E",      "forwardPE",          "2f")}
                {info_row("P/B Ratio",        "priceToBook",        "2f")}
                {info_row("EV/EBITDA",        "enterpriseToEbitda", "2f")}
                {info_row("52-Week High",     "fiftyTwoWeekHigh",   "2f", currency)}
                {info_row("52-Week Low",      "fiftyTwoWeekLow",    "2f", currency)}
              </table>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="card">
              <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;">Financials</div>
              <table style="width:100%;font-size:.72rem;border-collapse:collapse;">
                {info_row("Revenue (TTM)",    "totalRevenue",       "large", currency)}
                {info_row("Net Income",       "netIncomeToCommon",  "large", currency)}
                {info_row("Gross Margin",     "grossMargins",       "pct")}
                {info_row("Profit Margin",    "profitMargins",      "pct")}
                {info_row("ROE",              "returnOnEquity",     "pct")}
                {info_row("ROA",              "returnOnAssets",     "pct")}
                {info_row("Debt/Equity",      "debtToEquity",       "2f")}
              </table>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
              <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.5rem;">Dividends & Growth</div>
              <table style="width:100%;font-size:.72rem;border-collapse:collapse;">
                {info_row("Dividend Yield",   "dividendYield",      "pct")}
                {info_row("Payout Ratio",     "payoutRatio",        "pct")}
                {info_row("EPS (TTM)",        "trailingEps",        "2f", currency)}
                {info_row("Revenue Growth",   "revenueGrowth",      "pct")}
                {info_row("Earnings Growth",  "earningsGrowth",     "pct")}
                {info_row("Employees",        "fullTimeEmployees")}
              </table>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 4 – NEWS FEED
# ════════════════════════════════════════════
with tab4:
    company_name = info.get("longName", ticker_input.replace(".NS","").replace(".BO",""))
    st.markdown(f'<div class="dim" style="font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1rem;">Latest News · {company_name}</div>', unsafe_allow_html=True)

    if not news_key:
        st.info("🔑 Enter your **NewsAPI Key** in the sidebar to load live news.")
        st.markdown("""
        <div class="card card-accent" style="margin-top:.75rem;">
          <div style="font-size:.75rem;">
            <strong>How to get a free NewsAPI key:</strong><br><br>
            1. Visit <code>newsapi.org</code><br>
            2. Click <em>Get API Key</em> — free tier gives 100 req/day<br>
            3. Paste the key in the sidebar
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Fetching latest news..."):
            try:
                from newsapi import NewsApiClient
                newsapi = NewsApiClient(api_key=news_key)
                articles = newsapi.get_everything(
                    q=company_name, language="en",
                    sort_by="publishedAt", page_size=10
                )["articles"]
            except Exception as e:
                articles = []
                st.error(f"News fetch failed: {e}")

        if articles:
            sentiment_scores = []
            for art in articles:
                title = art.get("title", "") or ""
                desc  = art.get("description", "") or ""
                text  = (title + " " + desc).lower()
                pos_words = ["rise","gain","profit","growth","strong","beat","record","surge","bull","up","high"]
                neg_words = ["fall","drop","loss","risk","weak","miss","decline","bear","down","low","cut"]
                pos = sum(w in text for w in pos_words)
                neg = sum(w in text for w in neg_words)
                score = (pos - neg) / max(pos + neg, 1)
                sentiment_scores.append(score)

                color = "#00e5a0" if score > 0 else "#ff6b35" if score < 0 else "#718096"
                label = "POSITIVE" if score > 0 else "NEGATIVE" if score < 0 else "NEUTRAL"
                pub   = art.get("publishedAt","")[:10]

                st.markdown(f"""
                <div class="news-item">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.35rem;">
                    <span class="tag" style="background:rgba(255,255,255,.05);color:#718096;">{art.get('source',{}).get('name','—')}</span>
                    <span style="font-size:.65rem;color:#718096;">{pub}</span>
                    <span class="tag" style="background:rgba(0,0,0,.3);color:{color};">{label}</span>
                  </div>
                  <div style="font-size:.82rem;font-weight:700;line-height:1.4;margin-bottom:.3rem;">{title}</div>
                  <div style="font-size:.72rem;color:#718096;line-height:1.5;">{desc[:180] if desc else '—'}...</div>
                  <a href="{art.get('url','#')}" target="_blank" style="font-size:.65rem;color:#00e5a0;text-decoration:none;letter-spacing:.08em;">READ FULL ARTICLE →</a>
                </div>
                """, unsafe_allow_html=True)

            # Sentiment summary
            avg_sent = np.mean(sentiment_scores)
            sent_label = "BULLISH 🟢" if avg_sent > 0.1 else "BEARISH 🔴" if avg_sent < -0.1 else "NEUTRAL ⚪"
            st.markdown(f"""
            <div class="card card-accent" style="margin-top:1rem;">
              <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;">Sentiment Summary · {len(articles)} articles</div>
              <div style="font-size:1.4rem;font-family:'Syne',sans-serif;font-weight:700;margin:.4rem 0;">{sent_label}</div>
              <div class="dim" style="font-size:.72rem;">Avg sentiment score: <span style="color:#e2e8f0;">{avg_sent:.3f}</span></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No articles found.")



# ════════════════════════════════════════════
# TAB 5 – AI AGENT
# ════════════════════════════════════════════

# ── Watchlist of stocks the agent can fetch data for ──
WATCHLIST_INDIAN = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "WIPRO.NS": "Wipro",
    "HCLTECH.NS": "HCL Tech",
    "BAJFINANCE.NS": "Bajaj Finance",
    "ADANIENT.NS": "Adani Enterprises",
    "SBIN.NS": "SBI",
    "HINDUNILVR.NS": "HUL",
    "MARUTI.NS": "Maruti Suzuki",
    "TATAMOTORS.NS": "Tata Motors",
    "SUNPHARMA.NS": "Sun Pharma",
    "BHARTIARTL.NS": "Airtel",
}

WATCHLIST_US = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "NFLX": "Netflix",
    "JPM": "JPMorgan",
    "V": "Visa",
    "WMT": "Walmart",
    "XOM": "ExxonMobil",
    "JNJ": "Johnson & Johnson",
    "UNH": "UnitedHealth",
    "BRK-B": "Berkshire Hathaway",
}

@st.cache_data(ttl=600, show_spinner=False)
def fetch_multi_stock_summary(tickers: tuple, period: str = "1y") -> dict:
    """Fetch summary stats for multiple tickers — used for comparison queries."""
    results = {}
    for ticker in tickers:
        try:
            h = yf.Ticker(ticker).history(period=period)
            if h.empty:
                continue
            start_price = float(h["Close"].iloc[0])
            end_price   = float(h["Close"].iloc[-1])
            total_return = (end_price - start_price) / start_price * 100
            daily_returns = h["Close"].pct_change().dropna()
            vol = float(daily_returns.std() * (252 ** 0.5) * 100)
            sharpe = float((daily_returns.mean() / daily_returns.std()) * (252 ** 0.5)) if daily_returns.std() != 0 else 0
            max_dd = float(((h["Close"] / h["Close"].cummax()) - 1).min() * 100)
            results[ticker] = {
                "name": WATCHLIST_INDIAN.get(ticker, WATCHLIST_US.get(ticker, ticker)),
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "total_return_pct": round(total_return, 2),
                "annual_volatility_pct": round(vol, 2),
                "sharpe_ratio": round(sharpe, 3),
                "max_drawdown_pct": round(max_dd, 2),
                "period": period,
            }
        except Exception:
            pass
    return results

def detect_intent(question: str) -> dict:
    """
    Detect what kind of question the user is asking so we can fetch
    the right data before sending it to the LLM.
    Returns a dict with: intent, period, market, tickers
    """
    q = question.lower()

    # Period detection
    period = "1y"
    if any(x in q for x in ["4 year", "4year", "four year", "48 month"]): period = "4y" if False else "5y"
    elif any(x in q for x in ["5 year", "5year", "five year"]): period = "5y"
    elif any(x in q for x in ["3 year", "3year", "three year"]): period = "3y" if False else "2y"
    elif any(x in q for x in ["2 year", "2year", "two year"]): period = "2y"
    elif any(x in q for x in ["6 month", "6month", "six month", "half year"]): period = "6mo"
    elif any(x in q for x in ["3 month", "3month", "three month", "quarter"]): period = "3mo"
    elif any(x in q for x in ["1 month", "1month", "one month", "last month"]): period = "1mo"
    elif any(x in q for x in ["1 year", "1year", "one year", "last year", "annual"]): period = "1y"

    # Market selection
    is_indian = any(x in q for x in ["india", "indian", "nse", "bse", "nifty", "sensex",
                                       "reliance", "tcs", "infosys", "hdfc", "wipro",
                                       "airtel", "sbi", "bajaj", "adani", "maruti"])
    market = "indian" if is_indian else "us"
    watchlist = WATCHLIST_INDIAN if market == "indian" else WATCHLIST_US

    # Intent classification
    if any(x in q for x in ["best performing", "top performing", "best stock", "top stock",
                              "highest return", "most gain", "top gainer", "best return"]):
        return {"intent": "rank_by_return", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["worst performing", "biggest loser", "worst stock", "most loss",
                              "lowest return", "biggest drop", "worst return"]):
        return {"intent": "rank_by_return_worst", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["least risky", "safest", "lowest risk", "most stable",
                              "low volatility", "defensive"]):
        return {"intent": "rank_by_risk_low", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["most risky", "highest risk", "most volatile", "riskiest",
                              "high volatility"]):
        return {"intent": "rank_by_risk_high", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["best sharpe", "risk adjusted", "risk-adjusted", "efficient",
                              "best ratio"]):
        return {"intent": "rank_by_sharpe", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["compare", "vs", "versus", "which is better", "between"]):
        return {"intent": "compare", "period": period, "market": market,
                "tickers": tuple(watchlist.keys()[:6])}

    if any(x in q for x in ["portfolio", "diversif", "allocat", "mix", "basket"]):
        return {"intent": "portfolio_advice", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    if any(x in q for x in ["sector", "industry", "tech", "bank", "pharma", "energy",
                              "consumer", "infra"]):
        return {"intent": "sector_analysis", "period": period, "market": market,
                "tickers": tuple(watchlist.keys())}

    # Default: single stock analysis of the currently selected ticker
    return {"intent": "single_stock", "period": period, "market": market,
            "tickers": (ticker_input,)}

def build_prompt(question: str, intent_data: dict, live_data: dict,
                 current_hist, current_info, current_risk, curr_ticker, curr_currency) -> str:
    """Build a rich, data-dense prompt tailored to the detected intent."""

    base_sys = """You are FinSight — an expert AI financial research analyst with deep knowledge of global and Indian markets.
You think step-by-step, back every claim with data, and give actionable insights.
You NEVER make up numbers — only use the data provided to you.
Format your response cleanly using markdown headers, bold key figures, and bullet points where helpful.
Always end with a clear, opinionated summary that directly answers what the user asked."""

    # ── Format the live multi-stock data into a readable table ──
    data_section = ""
    if live_data:
        rows = sorted(live_data.items(),
                      key=lambda x: x[1].get("total_return_pct", 0), reverse=True)
        header = f"\n\n## MARKET DATA ({intent_data['period']} period)\n"
        col_hdr = f"{'Ticker':<14} {'Name':<22} {'Return%':>9} {'Ann.Vol%':>10} {'Sharpe':>8} {'MaxDD%':>9}\n"
        divider = "-" * 76 + "\n"
        rows_str = ""
        for ticker, d in rows:
            rows_str += (f"{ticker:<14} {d['name']:<22} "
                         f"{d['total_return_pct']:>+8.1f}% "
                         f"{d['annual_volatility_pct']:>9.1f}% "
                         f"{d['sharpe_ratio']:>8.3f} "
                         f"{d['max_drawdown_pct']:>8.1f}%\n")
        data_section = header + col_hdr + divider + rows_str

    # ── Current stock context ──
    price_now  = float(current_hist["Close"].iloc[-1])
    price_prev = float(current_hist["Close"].iloc[-2]) if len(current_hist) > 1 else price_now
    day_chg    = (price_now - price_prev) / price_prev * 100
    start_p    = float(current_hist["Close"].iloc[0])
    period_ret = (price_now - start_p) / start_p * 100

    single_ctx = f"""
## CURRENTLY SELECTED STOCK: {curr_ticker}
- Company: {current_info.get("longName", curr_ticker)}
- Sector: {current_info.get("sector","N/A")} | Industry: {current_info.get("industry","N/A")}
- Latest Price: {curr_currency}{price_now:,.2f}  |  Day Change: {day_chg:+.2f}%  |  Period Return: {period_ret:+.2f}%
- Annual Volatility: {current_risk.get("annual_vol",0)*100:.1f}%  |  Sharpe: {current_risk.get("sharpe",0):.3f}  |  Max Drawdown: {current_risk.get("max_drawdown",0)*100:.2f}%
- Market Cap: {current_info.get("marketCap","N/A")}  |  P/E: {current_info.get("trailingPE","N/A")}
- Profit Margin: {str(round(current_info["profitMargins"]*100,2))+"%" if current_info.get("profitMargins") else "N/A"}
- ROE: {str(round(current_info["returnOnEquity"]*100,2))+"%" if current_info.get("returnOnEquity") else "N/A"}
- Dividend Yield: {str(round(current_info["dividendYield"]*100,2))+"%" if current_info.get("dividendYield") else "N/A"}"""

    # ── Intent-specific instructions ──
    intent = intent_data["intent"]
    if intent == "rank_by_return":
        task = f"""The user wants to know the BEST PERFORMING stocks over the {intent_data['period']} period.
Using the market data table above:
1. Rank all stocks by total return (highest to lowest)
2. Highlight the top 3-5 winners with analysis of WHY they outperformed
3. Note any sector patterns
4. Compare against a typical market benchmark
5. Give a clear verdict on which stock delivered the best risk-adjusted returns"""

    elif intent == "rank_by_return_worst":
        task = f"""The user wants to know the WORST PERFORMING stocks over the {intent_data['period']} period.
1. Rank all stocks by total return (lowest to highest)
2. Analyse what drove underperformance for the bottom 3-5
3. Identify if there are recovery signals or if the trend will continue
4. Give a clear verdict"""

    elif intent == "rank_by_risk_low":
        task = f"""The user wants the SAFEST / LEAST RISKY stocks over {intent_data['period']}.
1. Rank by Annual Volatility (lowest first) 
2. Also check Sharpe ratio and Max Drawdown
3. Identify which stocks are truly defensive vs just slow-moving
4. Recommend a defensive portfolio combination"""

    elif intent == "rank_by_risk_high":
        task = f"""The user wants to know the MOST VOLATILE / RISKIEST stocks over {intent_data['period']}.
1. Rank by Annual Volatility (highest first)
2. Discuss whether the risk was rewarded (check returns vs vol)
3. Identify momentum vs speculative risk"""

    elif intent == "rank_by_sharpe":
        task = f"""The user wants the BEST RISK-ADJUSTED returns over {intent_data['period']}.
1. Rank all stocks by Sharpe Ratio (highest = best risk-adjusted performance)
2. Explain what Sharpe ratio means in simple terms
3. Highlight stocks that gave great returns without taking excessive risk
4. Clear recommendation for a quality-focused investor"""

    elif intent == "compare":
        task = f"""The user wants to COMPARE stocks. Use the full data table.
1. Group by return performance (winners/losers)
2. Group by risk (volatile vs stable)
3. Identify the best all-round stock
4. Give a direct comparison verdict"""

    elif intent == "portfolio_advice":
        task = f"""The user wants PORTFOLIO / ALLOCATION advice.
Using the data table:
1. Suggest a balanced portfolio of 5-7 stocks
2. Recommend weightings based on risk/return profiles
3. Explain diversification across sectors
4. Give expected portfolio risk level (weighted avg volatility)
5. State your reasoning clearly"""

    elif intent == "sector_analysis":
        task = f"""The user wants SECTOR analysis.
1. Group the stocks by sector (Tech, Finance, Consumer, Energy, etc.)
2. Compare sector-level average returns and volatility
3. Identify the best and worst performing sector
4. Give an outlook"""

    else:  # single_stock
        task = f"""The user is asking about {curr_ticker} specifically.
Provide a deep, structured analysis:
## Overview
## Price Performance Analysis  
## Risk Assessment
## Fundamental Strength
## Peer Comparison (if data available)
## Investment Outlook & Verdict
Be specific with numbers. Give a clear BUY / HOLD / AVOID opinion with reasoning."""

    return f"""{base_sys}

{data_section}
{single_ctx}

## USER QUESTION
{question}

## YOUR TASK
{task}

Think through the data carefully before writing your response. Show your reasoning.
"""


# ── The actual Tab 5 UI ──
with tab5:
    # Header
    st.markdown("""
    <div class="card card-accent" style="margin-bottom:1rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.3rem;">
            FinSight AI · LLaMA 3.3 70B · Groq Streaming
          </div>
          <div style="font-size:.8rem;line-height:1.6;">
            Ask <strong>anything</strong> — single stock deep-dive, market comparisons, sector analysis, 
            best performers, portfolio advice. The AI fetches the right data for your question automatically.
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Example questions
    st.markdown('<div class="dim" style="font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.4rem;">Try asking:</div>', unsafe_allow_html=True)
    ex_cols = st.columns(4)
    example_qs = [
        "Best performing Indian stocks in last 2 years",
        "Which US stocks have the lowest risk?",
        "Compare Reliance vs TCS vs Infosys",
        f"Deep analyse {ticker_input} stock",
    ]
    example_clicked = None
    for i, (col, eq) in enumerate(zip(ex_cols, example_qs)):
        if col.button(eq, key=f"ex_{i}", use_container_width=True):
            example_clicked = eq

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input box
    default_val = example_clicked if example_clicked else (
        st.session_state.get("last_query", f"Analyse {ticker_input} stock and give an investment outlook")
    )
    user_query = st.text_area("💬 Ask the AI Agent", value=default_val, height=85,
                               label_visibility="visible", key="ai_input")

    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 1, 2])
    with btn_col1:
        run_btn = st.button("▶  ANALYSE", use_container_width=True)
    with btn_col2:
        quick_btn = st.button("⚡  QUICK", use_container_width=True)
    with btn_col3:
        clear_btn = st.button("🗑  CLEAR", use_container_width=True)

    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    should_run = run_btn or run_ai or quick_btn or (example_clicked is not None)

    if should_run and user_query.strip():
        if not groq_key:
            st.error("Groq API Key missing in sidebar.")
        else:
            active_q = example_clicked if example_clicked else user_query

            # ── Step 1: Detect intent
            with st.status("🔍 Analysing your question...", expanded=True) as status:
                intent_data = detect_intent(active_q)
                st.write(f"Intent: `{intent_data['intent']}` | Period: `{intent_data['period']}` | Market: `{intent_data['market']}`")

                # ── Step 2: Fetch data based on intent
                live_data = {}
                if intent_data["intent"] != "single_stock":
                    st.write(f"Fetching data for {len(intent_data['tickers'])} stocks...")
                    live_data = fetch_multi_stock_summary(intent_data["tickers"], intent_data["period"])
                    st.write(f"✅ Got data for {len(live_data)} stocks")
                else:
                    st.write(f"Fetching data for {intent_data['tickers'][0]}...")
                    st.write("✅ Using cached page data")

                status.update(label="✅ Data ready — generating analysis...", state="complete")

            # ── Step 3: Build prompt and stream response
            current_risk = compute_risk_metrics(hist)
            prompt = build_prompt(
                question=active_q,
                intent_data=intent_data,
                live_data=live_data,
                current_hist=hist,
                current_info=info,
                current_risk=current_risk,
                curr_ticker=ticker_input,
                curr_currency=currency,
            )

            st.markdown("""
            <div style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;
                 color:#718096;margin:1rem 0 .5rem;">── AI FINANCIAL REPORT ──</div>
            """, unsafe_allow_html=True)

            try:
                from langchain_groq import ChatGroq as _ChatGroq
                _llm = _ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=0.1,
                    groq_api_key=groq_key,
                    streaming=True,
                    max_tokens=2048,
                )

                full_response = ""

                def token_gen():
                    for chunk in _llm.stream(prompt):
                        yield chunk.content

                full_response = st.write_stream(token_gen())

                # Save to history
                st.session_state.chat_history.append({
                    "question": active_q,
                    "response": full_response,
                    "intent": intent_data["intent"],
                    "period": intent_data["period"],
                })
                st.session_state.last_query = ""

            except Exception as e:
                st.error(f"Agent error: {e}")

    # ── Chat history
    if st.session_state.get("chat_history"):
        st.markdown("---")
        st.markdown('<div class="dim" style="font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.75rem;">Previous Analyses</div>', unsafe_allow_html=True)
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Q: {chat['question'][:80]}...  [{chat['intent']} · {chat['period']}]"):
                st.markdown(chat["response"])

    # ── Portfolio Analyser
    st.markdown("---")
    st.markdown("#### 💼 Portfolio Analyser")
    st.caption("Build a portfolio and check its combined risk profile")

    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {"RELIANCE.NS": 30, "TCS.NS": 25, "INFY.NS": 20, "HDFCBANK.NS": 25}

    pf_col1, pf_col2 = st.columns([1, 1])
    with pf_col1:
        new_tick   = st.text_input("Ticker", placeholder="e.g. WIPRO.NS")
        new_weight = st.number_input("Weight %", min_value=1, max_value=100, value=10)
        if st.button("+ ADD TO PORTFOLIO"):
            if new_tick:
                st.session_state.portfolio[new_tick.upper()] = new_weight

        if st.session_state.portfolio:
            st.markdown('<div class="card" style="margin-top:.5rem;">', unsafe_allow_html=True)
            for t, w in list(st.session_state.portfolio.items()):
                r1, r2 = st.columns([3, 1])
                r1.markdown(f'<span style="font-size:.75rem;">{t}</span>', unsafe_allow_html=True)
                r2.markdown(f'<span style="font-size:.75rem;color:#00e5a0;">{w}%</span>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("CLEAR PORTFOLIO"):
                st.session_state.portfolio = {}

    with pf_col2:
        if st.session_state.portfolio:
            st.plotly_chart(portfolio_pie(st.session_state.portfolio), use_container_width=True)
            pf_vols = []
            for t in st.session_state.portfolio:
                h_pf = fetch_stock_data(t, "6mo")
                if not h_pf.empty:
                    r_pf = compute_risk_metrics(h_pf)
                    pf_vols.append(r_pf.get("annual_vol", 0) * st.session_state.portfolio[t] / 100)
            if pf_vols:
                total_w_vol = sum(pf_vols)
                pl, plc, plp = risk_level(total_w_vol)
                st.markdown(f"""
                <div class="card card-accent">
                  <div class="dim" style="font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;">Portfolio Risk</div>
                  <div style="font-size:1.3rem;font-family:'Syne',sans-serif;font-weight:700;color:{plc};">{pl}</div>
                  <div class="dim" style="font-size:.72rem;">Weighted Annual Vol: <span style="color:#e2e8f0;">{total_w_vol*100:.1f}%</span></div>
                </div>
                """, unsafe_allow_html=True)



# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem 0;">
  <span class="dim" style="font-size:.65rem;">FinSight AI · Track A · Week 1–2 Milestone</span>
  <span class="dim" style="font-size:.65rem;">Data: Yahoo Finance · News: NewsAPI · LLM: Groq / LLaMA 3.3</span>
  <span class="dim" style="font-size:.65rem;">⚠ Not financial advice</span>
</div>
""", unsafe_allow_html=True)