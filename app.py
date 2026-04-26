import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os, base64

_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MF Financial Modelling | Salesqueen",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Force light background everywhere ── */
  .stApp,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stMainBlockContainer"],
  section[data-testid="stSidebar"],
  [data-testid="stVerticalBlock"] {
    background-color: #F4F7FB !important;
    color: #1a1a1a !important;
  }
  /* Tab bar background */
  [data-testid="stTabs"] { background-color: #F4F7FB !important; }
  /* Tab labels */
  button[data-baseweb="tab"] { color: #3A4D63 !important; }
  button[data-baseweb="tab"][aria-selected="true"] { color: #0C3C6E !important; font-weight:700; }
  /* Metrics */
  [data-testid="metric-container"] { background:white; border-radius:10px; padding:10px;
    border:1px solid #D8E4F0; }
  [data-testid="stMetricValue"]{ color:#0C3C6E !important; }
  [data-testid="stMetricLabel"]{ color:#3A4D63 !important; }
  /* General text — black for readability */
  p, span, label { color: #1a1a1a; }
  div { color: #1a1a1a; }
  h2,h3,h4 { color: #0C3C6E !important; }
  /* Banner title colours set in banner section below */
  /* Selectbox / multiselect */
  [data-baseweb="select"] { background:white !important; }
  /* ── Force Plotly chart SVG text to black ── */
  .js-plotly-plot .plotly svg text { fill: #111111 !important; }
  .js-plotly-plot .plotly .g-gtitle text { fill: #0C3C6E !important; }
  .js-plotly-plot .plotly .xtitle, .js-plotly-plot .plotly .ytitle { fill: #111111 !important; }
  /* ── Fix dark selectbox / multiselect — all states ── */
  [data-testid="stSelectbox"],
  [data-testid="stMultiSelect"] { background-color: white !important; }
  [data-testid="stSelectbox"] > div,
  [data-testid="stSelectbox"] > div > div,
  [data-testid="stMultiSelect"] > div,
  [data-testid="stMultiSelect"] > div > div { background-color: white !important; }
  [data-baseweb="select"],
  [data-baseweb="select"] > div { background-color: white !important; color: #1a1a1a !important; }
  [data-baseweb="select"] input { color: #1a1a1a !important; background: white !important; }
  [data-baseweb="select"] * { color: #1a1a1a !important; }
  /* Dropdown popup list — force white background + dark text */
  [data-baseweb="popover"],
  [data-baseweb="popover"] *,
  [data-baseweb="menu"],
  [data-baseweb="menu"] * { background-color: white !important; color: #1a1a1a !important; }
  /* Each option row on hover */
  [role="option"]:hover { background-color: #EEF4FB !important; }
  [role="option"] { background-color: white !important; color: #1a1a1a !important; }
  /* "Select all" row */
  [data-baseweb="menu"] li { background-color: white !important; color: #1a1a1a !important; }
  /* Selected chips */
  [data-baseweb="tag"] { background-color: #EEEDFE !important; }
  [data-baseweb="tag"] span { color: #534AB7 !important; }
  /* ── Fix Plotly hover tooltip ── */
  .hoverlayer .hovertext rect { fill: white !important; stroke: #D8E4F0 !important; }
  .hoverlayer .hovertext text  { fill: #1a1a1a !important; }
  .hoverlayer .hovertext path  { fill: white !important; stroke: #D8E4F0 !important; }
  /* ── Styled HTML table helper ── */
  .htbl { width:100%; border-collapse:collapse; font-family:'Segoe UI',Arial,sans-serif;
          font-size:13px; border-radius:10px; overflow:hidden;
          box-shadow:0 2px 8px rgba(0,0,0,0.07); }
  .htbl thead tr { background:#0C3C6E; }
  .htbl thead th { padding:10px 14px; text-align:left; color:white !important;
                   font-weight:600; white-space:nowrap; }
  .htbl tbody tr:nth-child(even) { background:#F4F7FB; }
  .htbl tbody tr:nth-child(odd)  { background:white; }
  .htbl tbody td { padding:8px 14px; color:#1a1a1a;
                   border-bottom:1px solid #EEF2F7; }

  header[data-testid="stHeader"]{ display:none; }
  .block-container{ padding-top:0 !important; padding-bottom:1rem !important; }
  /* ── Sticky tab navigation bar ── */
  [data-testid="stTabs"] > div:first-child {
    position: sticky !important;
    top: 0 !important;
    z-index: 998 !important;
    background-color: #F4F7FB !important;
    padding: 6px 0 0 !important;
    box-shadow: 0 2px 8px rgba(12,60,110,0.12) !important;
  }
  .banner{
    background:linear-gradient(135deg,#0C3C6E 0%,#1A6DB5 100%);
    padding:18px 28px; display:flex; align-items:center;
    border-radius:0 0 12px 12px; margin-bottom:16px;
    box-shadow:0 4px 16px rgba(12,60,110,0.3);
  }
  .banner-logo{ background:white; border-radius:50%; width:90px; height:90px;
    display:flex; align-items:center; justify-content:center;
    font-size:36px; flex-shrink:0; box-shadow:0 2px 8px rgba(0,0,0,0.2); }
  .banner-center{ flex:1; text-align:center; padding:0 20px; }
  .banner-center h1{ color:#FFD700 !important; font-size:22px; margin:0; font-weight:700; letter-spacing:0.3px; font-family:'Times New Roman',Times,serif; }
  .banner-center p{ color:#FFA500 !important; font-size:12px; margin:6px 0 10px; font-family:'Times New Roman',Times,serif; }
  .badges{ display:flex; gap:6px; flex-wrap:wrap; justify-content:center; align-items:center; }
  .badge{ background:rgba(255,255,255,0.15); color:white; padding:3px 10px; border-radius:20px; font-size:10px; }
  .badge-funds{
    background:#EEEDFE; color:#534AB7; padding:4px 12px; border-radius:20px;
    font-size:10px; font-weight:700; cursor:default; position:relative; display:inline-block;
  }
  .badge-funds .tip{
    visibility:hidden; opacity:0; transition:opacity 0.2s;
    position:absolute; top:calc(100% + 8px); right:0;
    background:#0C3C6E; color:white; padding:10px 14px; border-radius:10px;
    font-size:11px; z-index:9999; min-width:220px;
    box-shadow:0 6px 20px rgba(0,0,0,0.3); line-height:1.9; white-space:nowrap;
  }
  .badge-funds:hover .tip{ visibility:visible; opacity:1; }
  .kcard{ background:white; border-radius:10px; padding:14px 16px;
    border-left:4px solid #1A6DB5; box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-bottom:10px; }
  .kcard.green{ border-left-color:#1D9E75; }
  .kcard.green .kval{ color:#1D9E75; }
  .kcard.red{ border-left-color:#E24B4A; }
  .kcard.red .kval{ color:#E24B4A; }
  .kcard.gold{ border-left-color:#BA7517; }
  .kcard.gold .kval{ color:#BA7517; }
  .klabel{ font-size:10px; color:#6B7F99; text-transform:uppercase; letter-spacing:.4px; }
  .kval{ font-size:24px; font-weight:700; color:#0C3C6E; line-height:1.2; }
  .ksub{ font-size:11px; color:#6B7F99; margin-top:2px; }
  .bc{ background:white; border-radius:10px; padding:12px; text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.06); border:1px solid #D8E4F0; }
  .bc .bi{ font-size:20px; margin-bottom:3px; }
  .bc .bl{ font-size:10px; color:#6B7F99; text-transform:uppercase; }
  .bc .bv{ font-size:20px; font-weight:700; margin:2px 0; }
  .bc .bs{ font-size:9px; color:#6B7F99; }
  .stitle{ font-size:19px; font-weight:700; color:#0C3C6E; margin-bottom:2px; }
  .ssub{ font-size:12px; color:#6B7F99; margin-bottom:14px; }
  .pbox{ border-radius:10px; padding:16px; border:1px solid #D8E4F0; }
  .pbox h3{ font-size:13px; font-weight:700; margin-bottom:8px; }
  .pbox ul{ padding-left:16px; font-size:12px; line-height:1.9; margin:0; }
  .cons{ background:#d4edda; } .cons h3{ color:#155724; }
  .modr{ background:#d0e8ff; } .modr h3{ color:#004085; }
  .aggr{ background:#fde8e8; } .aggr h3{ color:#721c24; }
  .taxs{ background:#fff3cd; } .taxs h3{ color:#856404; }
</style>
""", unsafe_allow_html=True)

# ─── Banner ───────────────────────────────────────────────────────────────────
# Load Salesqueen logo — save salesqueen_logo.png in the same folder as app.py
_logo_path = os.path.join(_APP_DIR, 'salesqueen_logo.png')
if os.path.isfile(_logo_path):
    with open(_logo_path, 'rb') as _f:
        _logo_b64 = base64.b64encode(_f.read()).decode()
    _logo_html = (f'<div class="banner-logo" style="padding:4px;background:white;">'
                  f'<img src="data:image/png;base64,{_logo_b64}" '
                  f'style="width:82px;height:82px;object-fit:contain;border-radius:50%;display:block;">'
                  f'</div>')
else:
    _logo_html = '<div class="banner-logo">🏛️</div>'

st.markdown(f"""
<div class="banner">
  {_logo_html}
  <div class="banner-center">
    <div style="color:#FFD700;font-size:22px;font-weight:700;letter-spacing:0.3px;font-family:'Times New Roman',Times,serif;margin:0;">Financial Modelling of Mutual Fund Returns</div>
    <div style="color:#FFA500;font-size:12px;font-family:'Times New Roman',Times,serif;margin:6px 0 10px;">A Data-Driven Approach to Convert Potential Investors into Consistent Wealth Builders</div>
    <div class="badges">
      <span class="badge">📊 8 Mutual Funds</span>
      <span class="badge">📅 Jan 2021 – Dec 2025</span>
      <span class="badge">🧮 8 Financial Models</span>
      <span class="badge">🏢 Salesqueen Software Solutions</span>
      <span class="badge">📍 Chennai, India</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────
FUNDS  = ['Mirae Large Cap','Bandhan Small Cap','HDFC Balanced Adv',
          'HDFC Flexi Cap','HDFC Money Market','ICICI ELSS',
          'Kotak Midcap','Nippon Gold ETF']
COLORS = ['#2E75B6','#C0392B','#1D9E75','#0C3C6E','#7F8C8D','#8E44AD','#E67E22','#BA7517']
CATEGORIES = ['Large Cap','Small Cap','Hybrid','Flexi Cap','Debt','ELSS','Mid Cap','Gold']
CORR_LABELS = ['Mirae LC','Bandhan SC','HDFC Bal','HDFC FC','HDFC MM','ICICI ELSS','Kotak MC','Nippon Gold']

RF        = 6.5   # Risk-free rate — RBI Repo Rate (%)
MKT_CAGR  = 14.5  # Nifty 50 benchmark CAGR (%)
MKT_STD   = 14.0  # Nifty 50 approximate annual std dev (%)

# Nifty 50 indexed to 100 at Jan-21 (14.5% CAGR — no raw Nifty data available)
_NM = [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,59]
NIFTY_INDEXED = [round(100*(1.145)**(m/12),1) for m in _NM]

# ─── LOAD NAV DATA FROM EMBEDDED MODULE ─────────────────────────────────────
# Data is pre-loaded in nav_data.py so the app works on Streamlit Cloud
# without needing the 06_NAV_Data Excel files at runtime.
from nav_data import NAV_DATA

@st.cache_data
def load_nav_data():
    """Convert embedded NAV_DATA dict → dict of DataFrames."""
    result = {}
    for fund, d in NAV_DATA.items():
        df = pd.DataFrame({'Date': pd.to_datetime(d['dates']),
                           'NAV':  d['navs']})
        result[fund] = df
    return result

nav_raw = load_nav_data()

# ─── COMPUTE METRICS FROM REAL NAV DATA ───────────────────────────────────────
BEST_FOR = {
    'Mirae Large Cap':    'Low-risk Equity',
    'Bandhan Small Cap':  'Aggressive Investors',
    'HDFC Balanced Adv':  'Conservative',
    'HDFC Flexi Cap':     'Moderate Investors',
    'HDFC Money Market':  'Capital Preservation',
    'ICICI ELSS':         'Tax Saving (80C)',
    'Kotak Midcap':       'Aggressive Investors',
    'Nippon Gold ETF':    'Portfolio Hedge',
}

def compute_metrics(nav_raw):
    """Compute all financial metrics directly from NAV data — no caching."""
    from math import sqrt

    cagrs, stds, dds, sharpes, sortinos, alphas, var95 = [], [], [], [], [], [], []
    nav_start_list, nav_end_list, total_ret_list = [], [], []
    dr_dict        = {}
    nav_indexed_list = []

    # Quarterly snapshot points Jan-21 → Dec-25 (matches NIFTY_INDEXED length=21)
    _NM_pts   = [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,59]
    base_dt   = pd.Timestamp('2021-01-01')
    snap_dates = [base_dt + pd.DateOffset(months=m) for m in _NM_pts]

    for fund in FUNDS:
        df = nav_raw.get(fund)
        empty = (df is None or df.empty)

        if not empty:
            nav = df.set_index('Date')['NAV'].sort_index()
            nav = nav[(nav.index >= '2021-01-01') & (nav.index <= '2025-12-31')]
            empty = len(nav) < 2

        if empty:
            for lst in [cagrs, stds, dds, sharpes, sortinos, alphas, var95,
                        nav_start_list, nav_end_list, total_ret_list]:
                lst.append(0.0)
            dr_dict[fund] = pd.Series(dtype=float)
            nav_indexed_list.append([100.0] * len(_NM_pts))
            continue

        first_nav = float(nav.iloc[0])
        last_nav  = float(nav.iloc[-1])
        days      = (nav.index[-1] - nav.index[0]).days

        nav_start_list.append(round(first_nav, 4))
        nav_end_list.append(round(last_nav, 4))

        tr   = (last_nav / first_nav - 1) * 100
        total_ret_list.append(round(tr, 2))

        cagr = ((last_nav / first_nav) ** (365.0 / max(days, 1)) - 1) * 100
        cagrs.append(round(cagr, 2))

        dr = nav.pct_change().dropna()
        dr_dict[fund] = dr

        std = dr.std() * sqrt(252) * 100
        stds.append(round(std, 2))

        dd = float(((nav / nav.cummax()) - 1).min()) * 100
        dds.append(round(dd, 2))

        var_val = float(dr.quantile(0.05)) * 100
        var95.append(round(var_val, 2))

        sharpe = (cagr - RF) / std if std > 0 else 0.0
        sharpes.append(round(sharpe, 2))

        downside_std = dr[dr < 0].std() * sqrt(252) * 100
        sortino = (cagr - RF) / downside_std if downside_std > 0 else 0.0
        sortinos.append(round(sortino, 2))

        alphas.append(round(cagr - MKT_CAGR, 2))

        # Monthly indexed NAV: find nearest trading day to each snap date
        idxed = []
        for sd in snap_dates:
            diffs = abs(nav.index - pd.Timestamp(sd))
            pos   = int(diffs.argmin())
            idxed.append(round(float(nav.iloc[pos]) / first_nav * 100, 1))
        nav_indexed_list.append(idxed)

    # Correlation matrix — align on common trading days
    dr_df_raw = pd.DataFrame(dr_dict)
    dr_df_raw = dr_df_raw.dropna(axis=1, how='all')
    dr_aligned = dr_df_raw.dropna(axis=0, how='any')

    if len(dr_aligned) > 1:
        corr = dr_aligned.corr()
        corr_matrix = []
        for i in range(len(FUNDS)):
            row = []
            for j in range(len(FUNDS)):
                fi, fj = FUNDS[i], FUNDS[j]
                if fi in corr.columns and fj in corr.columns:
                    row.append(round(float(corr.loc[fi, fj]), 2))
                else:
                    row.append(1.0 if i == j else 0.0)
            corr_matrix.append(row)
    else:
        corr_matrix = [[1.0 if i == j else 0.0 for j in range(len(FUNDS))]
                       for i in range(len(FUNDS))]

    # Weighted scores (0–100): CAGR 25 + Sharpe 25 + Sortino 20 + MaxDD 15 + Std 15
    def norm(vals, higher_better=True):
        mn, mx = min(vals), max(vals)
        if mx == mn:
            return [50.0] * len(vals)
        return [(v - mn) / (mx - mn) * 100 if higher_better
                else (mx - v) / (mx - mn) * 100 for v in vals]

    n_c  = norm(cagrs,    True)
    n_sh = norm(sharpes,  True)
    n_so = norm(sortinos, True)
    n_dd = norm(dds,      False)   # less negative = better
    n_st = norm(stds,     False)   # lower volatility = better

    scores  = [round(n_c[i]*0.25 + n_sh[i]*0.25 + n_so[i]*0.20 +
                     n_dd[i]*0.15 + n_st[i]*0.15, 1)
               for i in range(len(FUNDS))]
    max_sc  = max(scores) if scores else 100.0

    def to_stars(s):
        pct = s / max_sc if max_sc > 0 else 0
        if pct >= 0.85: return '★★★★★'
        if pct >= 0.70: return '★★★★☆'
        if pct >= 0.50: return '★★★☆☆'
        if pct >= 0.30: return '★★☆☆☆'
        return '★☆☆☆☆'

    ratings = [to_stars(s) for s in scores]
    months_labels = [pd.Timestamp(snap_dates[i]).strftime('%b-%Y') for i in range(len(_NM_pts))]

    return dict(
        CAGRS=cagrs,    STDS=stds,       DDS=dds,
        SHARPES=sharpes, SORTINOS=sortinos, ALPHAS=alphas,
        VAR95=var95,    NAV_START=nav_start_list,  NAV_END=nav_end_list,
        TOTAL_RET=total_ret_list,        CORR_MATRIX=corr_matrix,
        MONTHS=months_labels,            NAV_INDEXED=nav_indexed_list,
        SCORES=scores,  RATINGS=ratings,
    )

with st.spinner("📊 Computing financial metrics from real NAV data…"):
    m = compute_metrics(nav_raw)
CAGRS       = m['CAGRS']
STDS        = m['STDS']
DDS         = m['DDS']
SHARPES     = m['SHARPES']
SORTINOS    = m['SORTINOS']
ALPHAS      = m['ALPHAS']
VAR95       = m['VAR95']
NAV_START   = m['NAV_START']
NAV_END     = m['NAV_END']
TOTAL_RET   = m['TOTAL_RET']
CORR_MATRIX = m['CORR_MATRIX']
MONTHS_IDX  = m['MONTHS']
NAV_INDEXED = m['NAV_INDEXED']
SCORES      = m['SCORES']
RATINGS     = m['RATINGS']

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def kcard(col, label, val, sub, cls=""):
    col.markdown(
        f'<div class="kcard {cls}"><div class="klabel">{label}</div>'
        f'<div class="kval">{val}</div><div class="ksub">{sub}</div></div>',
        unsafe_allow_html=True)

def bcard(col, icon, label, val, color, src):
    col.markdown(
        f'<div class="bc"><div class="bi">{icon}</div>'
        f'<div class="bl">{label}</div>'
        f'<div class="bv" style="color:{color};">{val}</div>'
        f'<div class="bs">{src}</div></div>',
        unsafe_allow_html=True)

BASE = dict(plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=20,t=40,b=20),
            font=dict(family='Segoe UI,Arial', size=12, color='black'))

def sip_fv(rate_pct, months):
    r = rate_pct / 100 / 12
    if r == 0:
        return 5000 * months
    return 5000 * (((1+r)**months - 1) / r) * (1+r)

def html_table(data_dict):
    """Render dict {col:[values]} as styled HTML table — white bg, navy header, black text."""
    cols = list(data_dict.keys())
    rows = list(zip(*[data_dict[c] for c in cols]))
    h = '<div style="overflow-x:auto;margin-bottom:8px;">'
    h += '<table class="htbl">'
    h += '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr></thead>'
    h += '<tbody>'
    for row in rows:
        h += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    h += '</tbody></table></div>'
    return h

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📌 Overview","📈 Returns","⚠️ Risk Metrics",
    "🎯 Risk-Adjusted","🏁 Benchmark","💰 SIP Analysis",
    "🔗 Correlation","🏆 Scorecard","📂 NAV Data"
])

# ══════════════════ TAB 1 — OVERVIEW ══════════════════
with tabs[0]:
    st.markdown('<div class="stitle">Project Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">8 funds analysed across 5 years using 8 financial models | Data: AMFI India, NSE, RBI, IBJA, India Post</div>', unsafe_allow_html=True)

    _best_cagr_i  = int(np.argmax(CAGRS))
    _best_sh_i    = int(np.argmax(SHARPES))
    _safest_i     = int(np.argmax(DDS))        # max drawdown closest to 0
    _gold_i       = FUNDS.index('Nippon Gold ETF')
    cols = st.columns(6)
    kcard(cols[0],"Best CAGR",     f"{CAGRS[_best_cagr_i]:.2f}%",  FUNDS[_best_cagr_i], "green")
    kcard(cols[1],"Best Sharpe",   f"{SHARPES[_best_sh_i]:.2f}",   FUNDS[_best_sh_i], "")
    kcard(cols[2],"Safest Fund",   f"{DDS[_safest_i]:.2f}%",       f"{FUNDS[_safest_i]} (Max DD)", "")
    kcard(cols[3],"Gold CAGR",     f"{CAGRS[_gold_i]:.2f}%",       "Nippon Gold ETF", "gold")
    kcard(cols[4],"Nifty 50",      "14.5%",                         "Benchmark CAGR", "")
    kcard(cols[5],"Risk-Free Rate","6.5%",                          "RBI Repo Rate", "red")

    st.markdown("**📌 Key Benchmark & Reference Rates**")
    bcols = st.columns(6)
    bcard(bcols[0],"📉","Nifty 50","14.5%","#0C3C6E","NSE India")
    bcard(bcols[1],"🏦","RBI Risk-Free","6.5%","#1A6DB5","rbi.org.in")
    bcard(bcols[2],"🏧","Bank FD","6.8%","#534AB7","Avg. SBI/HDFC")
    bcard(bcols[3],"🥇","Gold (IBJA)","19.5%","#BA7517","ibja.co")
    bcard(bcols[4],"📬","NSC Rate","7.7%","#1D9E75","India Post")
    bcard(bcols[5],"📊","CPI Inflation","5.5%","#E24B4A","RBI/MOSPI")

    st.markdown("")
    cl, cr = st.columns(2)
    with cl:
        bar_c = ['rgba(29,158,117,0.85)' if c >= 14.5 else 'rgba(226,75,74,0.85)' for c in CAGRS]
        fig = go.Figure(go.Bar(
            y=FUNDS, x=CAGRS, orientation='h', marker_color=bar_c,
            text=[f"{v:.2f}%" for v in CAGRS], textposition='outside'))
        fig.add_vline(x=14.5, line_dash='dash', line_color='#E24B4A',
                      annotation_text='Nifty 50 (14.5%)')
        fig.update_layout(title='CAGR Comparison — All 8 Funds',
                          xaxis_title='CAGR (%)', height=360, **BASE)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        # Efficient Frontier via Monte Carlo simulation
        np.random.seed(42)
        n_port = 3000
        p_rets, p_stds, p_sharpes = [], [], []
        cov_mat = np.outer(np.array(STDS), np.array(STDS)) * CORR_MATRIX
        for _ in range(n_port):
            w = np.random.random(len(FUNDS))
            w /= w.sum()
            pr = float(np.dot(w, CAGRS))
            pv = float(w @ cov_mat @ w)
            ps = float(np.sqrt(pv))
            p_rets.append(pr)
            p_stds.append(ps)
            p_sharpes.append((pr - 6.5) / ps if ps > 0 else 0)

        ret_arr = np.array(p_rets)
        std_arr = np.array(p_stds)
        sh_arr  = np.array(p_sharpes)

        # Build efficient frontier (pareto-optimal: non-decreasing return as risk increases)
        sort_idx = np.argsort(std_arr)
        s_stds = std_arr[sort_idx]
        s_rets = ret_arr[sort_idx]
        ef_stds, ef_rets = [s_stds[0]], [s_rets[0]]
        cur_max = s_rets[0]
        for sv, rv in zip(s_stds[1:], s_rets[1:]):
            if rv >= cur_max:
                cur_max = rv
                ef_stds.append(sv)
                ef_rets.append(rv)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=p_stds, y=p_rets, mode='markers',
            marker=dict(size=4, color=p_sharpes,
                        colorscale=[[0,'#E24B4A'],[0.5,'#BA7517'],[1,'#1D9E75']],
                        opacity=0.35, showscale=True,
                        colorbar=dict(title='Sharpe', thickness=12, len=0.7)),
            name='Portfolios',
            hovertemplate='Risk: %{x:.1f}%<br>Return: %{y:.1f}%<extra></extra>'))
        fig2.add_trace(go.Scatter(
            x=ef_stds, y=ef_rets, mode='lines',
            line=dict(color='#E24B4A', width=2.5),
            name='Efficient Frontier'))
        for i in range(len(FUNDS)):
            fig2.add_trace(go.Scatter(
                x=[STDS[i]], y=[CAGRS[i]], mode='markers+text',
                marker=dict(size=11, color=COLORS[i], symbol='diamond',
                            line=dict(width=1.5, color='white')),
                text=[FUNDS[i].split()[0]], textposition='top center',
                name=FUNDS[i], showlegend=False,
                hovertemplate=f'<b>{FUNDS[i]}</b><br>Risk: {STDS[i]}%<br>Return: {CAGRS[i]}%<extra></extra>'))
        fig2.update_layout(title='Efficient Frontier — Risk vs Return Tradeoff',
                           xaxis_title='Risk / Std Dev (%)', yaxis_title='CAGR (%)',
                           height=360, showlegend=False, **BASE)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════ TAB 2 — RETURNS ══════════════════
with tabs[1]:
    st.markdown('<div class="stitle">Return Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">CAGR · Absolute Return · NAV Growth — Jan 2021 to Dec 2025</div>', unsafe_allow_html=True)

    st.markdown(html_table({
        'Fund': FUNDS,
        'Category': ['Large Cap','Small Cap','Hybrid','Flexi Cap','Debt','ELSS','Mid Cap','Gold'],
        'NAV Jan-21': [f'₹{v:,.2f}' for v in NAV_START],
        'NAV Dec-25': [f'₹{v:,.2f}' for v in NAV_END],
        'Total Return': [f'+{v:.1f}%' for v in TOTAL_RET],
        'CAGR (5Y)': [f'{v:.2f}%' for v in CAGRS],
        'vs Nifty 50': [f'+{v-14.5:.1f}% ✅' if v>=14.5 else f'{v-14.5:.1f}% ❌' for v in CAGRS],
    }), unsafe_allow_html=True)

    sel_ret_funds = st.multiselect(
        "Select Funds to Compare (Nifty 50 always shown):",
        FUNDS, default=FUNDS, key='ret_funds')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=MONTHS_IDX, y=NIFTY_INDEXED,
        name='📊 Nifty 50 (Benchmark)',
        line=dict(color='#534AB7', width=2.5, dash='dash'), mode='lines'))
    for i, fund in enumerate(FUNDS):
        if fund in sel_ret_funds:
            fig.add_trace(go.Scatter(
                x=MONTHS_IDX, y=NAV_INDEXED[i],
                name=fund, line=dict(color=COLORS[i], width=2), mode='lines'))
    fig.add_hline(y=100, line_dash='dot', line_color='gray', opacity=0.4,
                  annotation_text='Base = 100')
    fig.update_layout(
        title='NAV Growth — Indexed to 100 at Jan 2021 (vs Nifty 50 Benchmark)',
        xaxis_title='Period', yaxis_title='Indexed NAV', height=480,
        legend=dict(orientation='h', yanchor='top', y=-0.18, xanchor='left', x=0,
                    font=dict(size=11)),
        margin=dict(l=10, r=20, t=50, b=120),
        **{k: v for k, v in BASE.items() if k != 'margin'})
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════ TAB 3 — RISK ══════════════════
with tabs[2]:
    st.markdown('<div class="stitle">Risk Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Standard Deviation · Maximum Drawdown | Jan 2021 – Dec 2025</div>', unsafe_allow_html=True)

    st.markdown(html_table({
        'Fund': FUNDS,
        'Ann. Std Dev': [f'{v:.1f}%' for v in STDS],
        'Max Drawdown': [f'{v:.2f}%' for v in DDS],
        'VaR 95%': [f'{v:.2f}%' for v in VAR95],
        'Risk Level': ['Moderate','High','Low','Moderate','Very Low','High','High','Moderate'],
    }), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=FUNDS, y=STDS,
            marker_color=['rgba(226,75,74,0.85)' if v>15 else 'rgba(186,117,23,0.85)' if v>10 else 'rgba(29,158,117,0.85)' for v in STDS],
            text=[f'{v:.1f}%' for v in STDS], textposition='outside'))
        fig.update_layout(title='Standard Deviation (Annualised %)',
                          yaxis_title='Std Dev (%)', height=360,
                          xaxis_tickangle=-20, **BASE)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure(go.Bar(
            x=FUNDS, y=DDS,
            marker_color=['rgba(226,75,74,0.85)' if v<-18 else 'rgba(186,117,23,0.85)' if v<-10 else 'rgba(29,158,117,0.85)' for v in DDS],
            text=[f'{v:.2f}%' for v in DDS], textposition='outside'))
        fig2.update_layout(title='Maximum Drawdown (%)',
                           yaxis_title='Max DD (%)', height=360,
                           xaxis_tickangle=-20, **BASE)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════ TAB 4 — RISK-ADJUSTED ══════════════════
with tabs[3]:
    st.markdown('<div class="stitle">Risk-Adjusted Returns</div>', unsafe_allow_html=True)
    st.markdown("<div class=\"ssub\">Sharpe · Sortino · Jensen's Alpha | Rf = 6.5% (RBI Rate)</div>", unsafe_allow_html=True)

    ra = pd.DataFrame({'Fund':FUNDS,'Sharpe':SHARPES,'Sortino':SORTINOS,'Alpha':ALPHAS})
    ra = ra.sort_values('Sharpe', ascending=False).reset_index(drop=True)
    ra.insert(0,'Rank',['🥇 #1','🥈 #2','🥉 #3','#4','#5','#6','#7','#8'])
    ra['Rating']=['★★★★★','★★★★★','★★★★☆','★★★★☆','★★★☆☆','★★★☆☆','★★☆☆☆','★☆☆☆☆']

    STAR_COLORS = {5:'#1D9E75', 4:'#27AE60', 3:'#E67E22', 2:'#E24B4A', 1:'#922B21'}

    tbl = '<table style="width:100%;border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px;border-radius:10px;overflow:hidden;">'
    tbl += '<thead><tr style="background:#0C3C6E;color:white;">'
    for h in ['Rank','Fund','Sharpe','Sortino',"Jensen's Alpha",'Rating']:
        tbl += f'<th style="padding:10px 14px;text-align:left;font-weight:600;">{h}</th>'
    tbl += '</tr></thead><tbody>'
    for idx, row in ra.iterrows():
        sc = STAR_COLORS.get(row['Rating'].count('★'), '#888')
        av = row['Alpha']
        as_ = f'+{av:.1f}%' if av >= 0 else f'{av:.1f}%'
        ac = '#1D9E75' if av >= 0 else '#E24B4A'
        bg = '#F4F7FB' if idx % 2 == 0 else 'white'
        tbl += f'<tr style="background:{bg};">'
        tbl += f'<td style="padding:9px 14px;">{row["Rank"]}</td>'
        tbl += f'<td style="padding:9px 14px;font-weight:600;color:#0C3C6E;">{row["Fund"]}</td>'
        tbl += f'<td style="padding:9px 14px;text-align:center;">{row["Sharpe"]:.2f}</td>'
        tbl += f'<td style="padding:9px 14px;text-align:center;">{row["Sortino"]:.2f}</td>'
        tbl += f'<td style="padding:9px 14px;text-align:center;"><span style="color:{ac};font-weight:600;">{as_}</span></td>'
        tbl += f'<td style="padding:9px 14px;text-align:center;"><span style="color:{sc};font-size:18px;">{row["Rating"]}</span></td>'
        tbl += '</tr>'
    tbl += '</tbody></table>'
    st.markdown(tbl, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin:10px 0;padding:8px 14px;background:white;border-radius:8px;
         border:1px solid #D8E4F0;display:flex;gap:18px;align-items:center;font-size:12px;flex-wrap:wrap;">
      <strong style="color:#0C3C6E;">Star Rating:</strong>
      <span style="color:#1D9E75;font-weight:600;">★★★★★ Excellent</span>
      <span style="color:#27AE60;font-weight:600;">★★★★☆ Very Good</span>
      <span style="color:#E67E22;font-weight:600;">★★★☆☆ Good</span>
      <span style="color:#E24B4A;font-weight:600;">★★☆☆☆ Below Average</span>
      <span style="color:#922B21;font-weight:600;">★☆☆☆☆ Poor</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    sorted_funds = ra['Fund'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sharpe',  x=sorted_funds,
                         y=[SHARPES[FUNDS.index(f)] for f in sorted_funds],
                         marker_color='rgba(12,60,110,0.85)'))
    fig.add_trace(go.Bar(name='Sortino', x=sorted_funds,
                         y=[SORTINOS[FUNDS.index(f)] for f in sorted_funds],
                         marker_color='rgba(29,158,117,0.75)'))
    fig.add_hline(y=1.0, line_dash='dash', line_color='#E24B4A', annotation_text='Good ≥ 1.0')
    fig.add_hline(y=0.0, line_color='black', line_width=0.8)
    fig.update_layout(title='Sharpe & Sortino Ratios', barmode='group',
                      height=360, yaxis_title='Ratio', xaxis_tickangle=-20,
                      legend=dict(orientation='h', y=1.08, xanchor='right', x=1), **BASE)
    st.plotly_chart(fig, use_container_width=True)

    alpha_vals = [ALPHAS[FUNDS.index(f)] for f in sorted_funds]
    fig2 = go.Figure(go.Bar(
        y=sorted_funds, x=alpha_vals, orientation='h',
        marker_color=['rgba(29,158,117,0.85)' if v>=0 else 'rgba(226,75,74,0.85)' for v in alpha_vals],
        text=[f'+{v:.1f}%' if v>=0 else f'{v:.1f}%' for v in alpha_vals],
        textposition='outside'))
    fig2.add_vline(x=0, line_color='black', line_width=1)
    fig2.update_layout(title="Jensen's Alpha — Excess Return over CAPM",
                       xaxis_title='Alpha (%)', height=340,
                       margin=dict(l=10,r=70,t=40,b=20),
                       plot_bgcolor='white', paper_bgcolor='white',
                       font=dict(family='Segoe UI,Arial', size=12, color='black'))
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════ TAB 5 — BENCHMARK ══════════════════
with tabs[4]:
    st.markdown('<div class="stitle">Benchmark Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">vs Nifty 50 · vs Bank FD · vs NSC · vs Gold (IBJA) · vs RBI Rate · vs CPI Inflation</div>', unsafe_allow_html=True)

    bcols = st.columns(6)
    bcard(bcols[0],"📉","Nifty 50 CAGR","14.5%","#0C3C6E","Source: NSE India")
    bcard(bcols[1],"🏧","Bank FD Rate","6.8%","#534AB7","Avg. 5-Year FD")
    bcard(bcols[2],"📬","NSC Rate","7.7%","#1D9E75","Source: India Post")
    bcard(bcols[3],"🥇","Gold (IBJA)","19.5%","#BA7517","Source: ibja.co")
    bcard(bcols[4],"🏛","RBI Risk-Free","6.5%","#1A6DB5","Source: rbi.org.in")
    bcard(bcols[5],"📊","CPI Inflation","5.5%","#E24B4A","RBI / MOSPI")

    st.markdown("""
    <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap;
         padding:9px 14px;background:white;border-radius:8px;border:1px solid #D8E4F0;
         margin-bottom:12px;font-size:12px;color:#3A4D63;">
      <strong style="color:#0C3C6E;">Chart Colours:</strong>
      <span style="display:flex;align-items:center;gap:6px;">
        <span style="width:13px;height:13px;border-radius:50%;background:#1D9E75;display:inline-block;"></span>
        <b style="color:#1D9E75;">Green</b> — Beat Market (CAGR ≥ Nifty 50 14.5%)
      </span>
      <span style="display:flex;align-items:center;gap:6px;">
        <span style="width:13px;height:13px;border-radius:50%;background:#E24B4A;display:inline-block;"></span>
        <b style="color:#E24B4A;">Red</b> — Below Market (CAGR &lt; Nifty 50)
      </span>
      <span style="display:flex;align-items:center;gap:6px;">
        <span style="width:13px;height:13px;border-radius:50%;background:#534AB7;display:inline-block;"></span>
        <b style="color:#534AB7;">Purple</b> — Benchmark Instruments (Nifty 50, FD, NSC, Gold, RBI, CPI)
      </span>
    </div>
    """, unsafe_allow_html=True)

    all_lbls = ['Nifty 50','Bank FD','NSC','Gold (IBJA)','RBI Rf','CPI Inflation']+FUNDS
    all_vals = [14.5,6.8,7.7,19.5,6.5,5.5]+CAGRS
    all_clrs = (['rgba(83,74,183,0.75)']*6 +
                ['rgba(29,158,117,0.85)' if v>=14.5 else 'rgba(226,75,74,0.8)' for v in CAGRS])

    fig = go.Figure(go.Bar(
        y=all_lbls, x=all_vals, orientation='h', marker_color=all_clrs,
        text=[f'{v:.2f}%' for v in all_vals], textposition='outside'))
    fig.add_vline(x=14.5, line_dash='dash', line_color='#E24B4A',
                  annotation_text='Nifty 50', annotation_position='top right')
    fig.update_layout(title='CAGR vs All Benchmarks', xaxis_title='CAGR (%)',
                      height=520, margin=dict(l=10,r=70,t=40,b=20),
                      plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(family='Segoe UI,Arial', size=12, color='black'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(html_table({
        'Fund / Instrument': FUNDS+['Nifty 50 Index','Gold (IBJA)','NSC India Post','Bank FD'],
        'CAGR': [f'{v:.2f}%' for v in CAGRS]+['14.50%','19.50%','7.70%','6.80%'],
        'vs Nifty 50 (14.5%)': [f'+{v-14.5:.1f}% ✅' if v>=14.5 else f'{v-14.5:.1f}% ❌' for v in CAGRS]+['—','+5.0% ✅','−6.8% ❌','−7.7% ❌'],
        'vs Bank FD (6.8%)':   [f'+{v-6.8:.1f}%' for v in CAGRS]+['+7.7%','+12.7%','+0.9%','—'],
        'vs CPI (5.5%)':       [f'+{v-5.5:.1f}%' for v in CAGRS]+['+9.0%','+14.0%','+2.2%','+1.3%'],
        'Beat Market?':        ['✅ Yes' if v>=14.5 else '❌ No' for v in CAGRS]+['Benchmark','✅ Yes','Fixed','Fixed'],
    }), unsafe_allow_html=True)

# ══════════════════ TAB 6 — SIP ══════════════════
with tabs[5]:
    st.markdown('<div class="stitle">SIP Analysis — Wealth Creation</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">₹5,000/month SIP | Power of Compounding across 5, 10, 15 Years</div>', unsafe_allow_html=True)

    # Build SIP entries from real CAGRS, sorted high→low
    _fund_sip = sorted([(FUNDS[i], CAGRS[i], COLORS[i]) for i in range(len(FUNDS))],
                       key=lambda x: x[1], reverse=True)
    _sip_fund_entries = [(f'{f} ({c:.2f}%)', c, col) for f, c, col in _fund_sip]
    # Benchmarks always shown
    _bench_entries = [
        ('Gold/IBJA (19.5%)',     19.5,  '#D4A017'),
        ('Nifty 50 (14.5%)',      14.5,  '#534AB7'),
        ('NSC India Post (7.7%)',  7.7,  '#7F8C8D'),
        ('Bank FD (6.8%)',         6.8,  '#95a5a6'),
        ('RBI Risk-Free (6.5%)',   6.5,  '#AEB6BF'),
    ]
    sip_entries = _sip_fund_entries + _bench_entries
    # Sort all by rate desc for display
    sip_entries = sorted(sip_entries, key=lambda x: x[1], reverse=True)

    _top_fund = _fund_sip[0]
    _second   = _fund_sip[1]
    kcols = st.columns(5)
    kcard(kcols[0],"Total Invested (5Y)","₹3.0L","₹5,000 × 60 months","")
    kcard(kcols[1],f"Value @ {_top_fund[1]:.2f}%",
          f"₹{sip_fv(_top_fund[1],60)/1e5:.2f}L", _top_fund[0], "green")
    kcard(kcols[2],f"Value @ {_second[1]:.2f}%",
          f"₹{sip_fv(_second[1],60)/1e5:.2f}L", _second[0], "")
    kcard(kcols[3],"Value @ 7.7% NSC",
          f"₹{sip_fv(7.7,60)/1e5:.2f}L","India Post NSC","")
    kcard(kcols[4],"Value @ 6.8% FD",
          f"₹{sip_fv(6.8,60)/1e5:.2f}L","Bank Fixed Deposit","red")

    horizon = st.radio("Investment Horizon:", ["5 Years","10 Years","15 Years"], horizontal=True)
    hm = {"5 Years":60,"10 Years":120,"15 Years":180}[horizon]
    invested = 5000 * hm

    months_range = list(range(1, hm + 1))
    fig = go.Figure()
    # Capital invested baseline
    fig.add_trace(go.Scatter(
        x=months_range, y=[5000*m/1e5 for m in months_range],
        name='Capital Invested',
        line=dict(color='#6B7F99', width=1.5, dash='dot'), mode='lines'))
    for lbl, r, c in sip_entries:
        vals = [sip_fv(r, m)/1e5 for m in months_range]
        width = 2.5 if r >= 20 else 1.8
        fig.add_trace(go.Scatter(
            x=months_range, y=vals, name=lbl,
            line=dict(color=c, width=width), mode='lines',
            hovertemplate=f'<b>{lbl}</b><br>Month %{{x}}<br>Value: ₹%{{y:.2f}}L<extra></extra>'))
    fig.update_layout(
        title=f'₹5,000/month SIP — Wealth Growth Over Time ({horizon})',
        xaxis_title=f'Months (1 – {hm})', yaxis_title='Corpus Value (₹ Lakhs)',
        height=560,
        legend=dict(orientation='h', yanchor='top', y=-0.22,
                    xanchor='left', x=0, font=dict(size=10)),
        margin=dict(l=10, r=20, t=50, b=140),
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI,Arial', size=12, color='black'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(html_table({
        'Fund / Rate': [e[0] for e in sip_entries],
        'FV 5Y':  [f'₹{sip_fv(e[1],60)/1e5:.2f}L'  for e in sip_entries],
        'FV 10Y': [f'₹{sip_fv(e[1],120)/1e5:.2f}L' for e in sip_entries],
        'FV 15Y': [f'₹{sip_fv(e[1],180)/1e5:.2f}L' for e in sip_entries],
    }), unsafe_allow_html=True)

# ══════════════════ TAB 7 — CORRELATION ══════════════════
with tabs[6]:
    st.markdown('<div class="stitle">Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Pearson Correlation Matrix — 1 = move together | −1 = move opposite | 0 = unrelated</div>', unsafe_allow_html=True)

    # Compute correlation insights dynamically
    _cm = np.array(CORR_MATRIX)
    _np = len(FUNDS)
    # Highest off-diagonal correlation
    _hi_val, _hi_i, _hi_j = -1, 0, 1
    for _ii in range(_np):
        for _jj in range(_ii+1, _np):
            if _cm[_ii,_jj] > _hi_val:
                _hi_val, _hi_i, _hi_j = _cm[_ii,_jj], _ii, _jj
    # Best diversifier (lowest off-diagonal correlation)
    _lo_val, _lo_i, _lo_j = 1, 0, 1
    for _ii in range(_np):
        for _jj in range(_ii+1, _np):
            if _cm[_ii,_jj] < _lo_val:
                _lo_val, _lo_i, _lo_j = _cm[_ii,_jj], _ii, _jj
    # Gold vs equity average
    _gold_i_c = FUNDS.index('Nippon Gold ETF')
    _gold_eq_corrs = [_cm[_gold_i_c,j] for j in range(_np) if j != _gold_i_c and FUNDS[j] != 'HDFC Money Market']
    _gold_avg = np.mean(_gold_eq_corrs)
    # HDFC Money Market avg correlation
    _mm_i = FUNDS.index('HDFC Money Market')
    _mm_avg = np.mean([_cm[_mm_i,j] for j in range(_np) if j != _mm_i])

    kcols = st.columns(4)
    kcard(kcols[0],"Highest Correlation",f"{_hi_val:.2f}",
          f"{CORR_LABELS[_hi_i]} ↔ {CORR_LABELS[_hi_j]}","red")
    kcard(kcols[1],"Best Diversifier",f"{_lo_val:.2f}",
          f"{CORR_LABELS[_lo_i]} ↔ {CORR_LABELS[_lo_j]}","green")
    kcard(kcols[2],"Gold vs Equity",f"{_gold_avg:.2f} avg","Natural portfolio hedge","")
    kcard(kcols[3],"Debt Correlation",f"{_mm_avg:.2f} avg","HDFC Money Market — stable anchor","")

    fig = go.Figure(go.Heatmap(
        z=CORR_MATRIX, x=CORR_LABELS, y=CORR_LABELS,
        colorscale=[[0.0,'#2980B9'],[0.35,'#AED6F1'],[0.5,'#FDFEFE'],
                    [0.65,'#F7DC6F'],[0.82,'#E74C3C'],[1.0,'#922B21']],
        zmin=-0.5, zmax=1.0, showscale=True,
        text=[[f'{v:.2f}' for v in row] for row in CORR_MATRIX],
        texttemplate='%{text}', textfont=dict(size=11),
        colorbar=dict(title='ρ', thickness=14)))
    fig.update_layout(title='Pearson Correlation Heatmap — 8 Funds',
                      height=500, xaxis_tickangle=-30,
                      margin=dict(l=10,r=10,t=40,b=80),
                      plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(family='Segoe UI,Arial', size=12, color='black'))
    st.plotly_chart(fig, use_container_width=True)

    # Kotak ↔ Bandhan SC correlation
    _kt_i  = FUNDS.index('Kotak Midcap')
    _bd_i  = FUNDS.index('Bandhan Small Cap')
    _fc_i  = FUNDS.index('HDFC Flexi Cap')
    _kt_bd = _cm[_kt_i, _bd_i]
    _gold_fc = _cm[_gold_i_c, _fc_i]
    st.markdown(html_table({
        'Finding': ['Highest Equity Correlation','Gold as Portfolio Hedge',
                    'Debt Uncorrelated','Mid + Small Cap Pair','Best Diversified Pair'],
        'Fund Pair': [f'{CORR_LABELS[_hi_i]} ↔ {CORR_LABELS[_hi_j]}',
                      'Nippon Gold ↔ All Equity Funds',
                      'HDFC Money Market ↔ All Funds',
                      'Kotak Midcap ↔ Bandhan SC',
                      'HDFC Flexi Cap + Nippon Gold ETF'],
        'Correlation': [f'{_hi_val:.2f}',
                        f'{min(_gold_eq_corrs):.2f} to {max(_gold_eq_corrs):.2f}',
                        f'~{_mm_avg:.2f}',
                        f'{_kt_bd:.2f}',
                        f'{_gold_fc:.2f}'],
        'Interpretation': [
            'Very similar movement — limited diversification within equity category',
            'Near-zero / slightly negative — effective inflation & crisis hedge',
            'Near-zero correlation — stable capital anchor for any portfolio',
            'Both growth-oriented — high co-movement in bull & bear markets',
            'Highest return fund + natural hedge = optimal core diversified pair',
        ],
    }), unsafe_allow_html=True)

# ══════════════════ TAB 8 — SCORECARD ══════════════════
with tabs[7]:
    st.markdown('<div class="stitle">Overall Fund Scorecard</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Weighted Score: CAGR 25 + Sharpe 25 + Sortino 20 + Low Drawdown 15 + Low Volatility 15 = 100</div>', unsafe_allow_html=True)

    # Build scorecard from real computed metrics, sorted by score desc
    _sc_raw = sorted(
        [(i, FUNDS[i], SCORES[i], CAGRS[i], SHARPES[i], DDS[i],
          BEST_FOR.get(FUNDS[i], '—'), RATINGS[i])
         for i in range(len(FUNDS))],
        key=lambda x: x[2], reverse=True
    )
    _rank_medals = ['🥇 #1','🥈 #2','🥉 #3','#4','#5','#6','#7','#8']
    sc_data = [
        (_rank_medals[r], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        for r, row in enumerate(_sc_raw)
    ]
    # Styled HTML table matching Risk-Adjusted tab style
    STAR_COLORS_SC = {5:'#1D9E75', 4:'#27AE60', 3:'#E67E22', 2:'#E24B4A', 1:'#922B21'}
    sc_tbl  = '<table class="htbl">'
    sc_tbl += '<thead><tr>'
    for h in ['Rank','Fund','Score /100','CAGR (5Y)','Sharpe','Max DD','Best For','Rating']:
        sc_tbl += f'<th>{h}</th>'
    sc_tbl += '</tr></thead><tbody>'
    for idx, row in enumerate(sc_data):
        rank, fund, score, cagr, sharpe, maxdd, bestfor, rating = row
        sc = STAR_COLORS_SC.get(rating.count('★'), '#888')
        bg = '#F4F7FB' if idx % 2 == 0 else 'white'
        sc_tbl += f'<tr style="background:{bg};">'
        dd_c = '#E24B4A' if maxdd < -15 else '#E67E22' if maxdd < -9 else '#1D9E75'
        sc_tbl += f'<td style="padding:9px 14px;">{rank}</td>'
        sc_tbl += f'<td style="padding:9px 14px;"><span style="color:#0C3C6E;font-weight:600;">{fund}</span></td>'
        sc_tbl += f'<td style="padding:9px 14px;text-align:center;"><span style="color:#0C3C6E;font-weight:700;">{score}</span></td>'
        sc_tbl += f'<td style="padding:9px 14px;text-align:center;">{cagr:.2f}%</td>'
        sc_tbl += f'<td style="padding:9px 14px;text-align:center;">{sharpe:.2f}</td>'
        sc_tbl += f'<td style="padding:9px 14px;text-align:center;"><span style="color:{dd_c};font-weight:600;">{maxdd:.2f}%</span></td>'
        sc_tbl += f'<td style="padding:9px 14px;">{bestfor}</td>'
        sc_tbl += f'<td style="padding:9px 14px;text-align:center;"><span style="color:{sc};font-size:18px;">{rating}</span></td>'
        sc_tbl += '</tr>'
    sc_tbl += '</tbody></table>'
    st.markdown(f'<div style="overflow-x:auto;margin-bottom:8px;">{sc_tbl}</div>', unsafe_allow_html=True)

    # ── 2×2 Investor Profile Matrix ──────────────────────────────────────────
    st.markdown("### 👤 Investor Profile Recommendations")
    _hdfc_bal_dd = DDS[FUNDS.index('HDFC Balanced Adv')]
    _flexi_sh    = SHARPES[FUNDS.index('HDFC Flexi Cap')]
    _sc_idx      = FUNDS.index('Bandhan Small Cap')
    _elss_cagr   = CAGRS[FUNDS.index('ICICI ELSS')]
    profile_data = [
        ('cons','🟢 Conservative',
         f'HDFC Balanced Advantage — Max DD {_hdfc_bal_dd:.2f}%|HDFC Money Market — Capital safe|NSC / Bank FD — Fixed return guarantee|Nippon Gold ETF — Inflation hedge'),
        ('modr','🔵 Moderate',
         f'HDFC Flexi Cap — Best Sharpe {_flexi_sh:.2f}|ICICI ELSS — Tax benefit + growth|Nippon Gold ETF — Portfolio diversifier|Kotak Midcap — Medium-high growth'),
        ('aggr','🔴 Aggressive',
         f'Bandhan Small Cap — Highest CAGR {CAGRS[_sc_idx]:.2f}%|Kotak Midcap — Strong mid-cap growth|HDFC Flexi Cap — High return + managed risk|Long horizon (5+ years) required'),
        ('taxs','🟡 Tax Saver',
         f'ICICI ELSS — 80C deduction ₹1.5L/yr|Only 3-year lock-in period|CAGR {_elss_cagr:.2f}% — beats FD & NSC|Best tax-saving + wealth creation combo'),
    ]
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)
    cols_matrix = [row1_c1, row1_c2, row2_c1, row2_c2]
    for col, (cls, title, items) in zip(cols_matrix, profile_data):
        li = ''.join(f'<li>{i}</li>' for i in items.split('|'))
        col.markdown(f'<div class="pbox {cls}"><h3>{title}</h3><ul>{li}</ul></div>',
                     unsafe_allow_html=True)

# ══════════════════ TAB 9 — NAV DATA (REAL) ══════════════════
with tabs[8]:
    st.markdown('<div class="stitle">📂 NAV Data — Real Daily Data from AMFI India</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Actual NAV values from Excel files | Jan 2021 – Dec 2025 | Source: AMFI / MFAPI.in</div>', unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([3,1,1])
    with ctrl1:
        sel_funds = st.multiselect("Select Funds:", FUNDS, default=FUNDS, key='nav_sel')
    with ctrl2:
        d_start = st.date_input("From", value=pd.Timestamp('2021-01-01'),
                                min_value=pd.Timestamp('2021-01-01'),
                                max_value=pd.Timestamp('2025-12-31'), key='nav_ds')
    with ctrl3:
        d_end = st.date_input("To", value=pd.Timestamp('2025-12-31'),
                              min_value=pd.Timestamp('2021-01-01'),
                              max_value=pd.Timestamp('2025-12-31'), key='nav_de')

    if not sel_funds:
        st.warning("Select at least one fund above.")
    else:
        # ── Summary table ──
        summary_rows = []
        for fund in sel_funds:
            df = nav_raw.get(fund)
            if df is None:
                continue
            mask = (df['Date'] >= pd.Timestamp(d_start)) & (df['Date'] <= pd.Timestamp(d_end))
            dff = df[mask].copy().reset_index(drop=True)
            if dff.empty:
                continue
            first  = dff['NAV'].iloc[0]
            last   = dff['NAV'].iloc[-1]
            ret_p  = (last/first - 1)*100
            days_  = (dff['Date'].iloc[-1] - dff['Date'].iloc[0]).days
            cagr_r = ((last/first)**(365/max(days_,1)) - 1)*100 if days_ > 0 else 0
            summary_rows.append({
                'Fund': fund,
                'From':       dff['Date'].iloc[0].strftime('%d-%b-%Y'),
                'To':         dff['Date'].iloc[-1].strftime('%d-%b-%Y'),
                'Start NAV':  f'₹{first:,.4f}',
                'End NAV':    f'₹{last:,.4f}',
                'Max NAV':    f'₹{dff["NAV"].max():,.4f}',
                'Min NAV':    f'₹{dff["NAV"].min():,.4f}',
                'Total Return': f'+{ret_p:.2f}%' if ret_p>=0 else f'{ret_p:.2f}%',
                'CAGR (period)': f'{cagr_r:.2f}%',
                'Data Points': f'{len(dff):,}',
            })

        if summary_rows:
            st.markdown("**📊 Summary for Selected Period**")
            sdf = pd.DataFrame(summary_rows)
            st.markdown(html_table({c: list(sdf[c]) for c in sdf.columns}), unsafe_allow_html=True)

        # ── Daily NAV Table ──
        st.markdown("---")
        st.markdown("**📄 Daily NAV Data — Indexed to 100 · Actual NAV · % Return**")
        fund_view = st.selectbox("Fund to view daily data:", sel_funds, key='nav_fv')
        df_v = nav_raw.get(fund_view)

        if df_v is None:
            # File not found — show path info
            fpath = os.path.join(NAV_FOLDER, NAV_FILES.get(fund_view,''))
            st.warning(f"⚠️ NAV file not found. Expected path:\n`{fpath}`\n\nPlease ensure the 06_NAV_Data folder is present.")
        else:
            mask2 = (df_v['Date']>=pd.Timestamp(d_start)) & (df_v['Date']<=pd.Timestamp(d_end))
            df_show = df_v[mask2].copy().reset_index(drop=True)

            if df_show.empty:
                st.info("No data available for this fund in the selected date range.")
            else:
                base_nav = df_show['NAV'].iloc[0]
                df_show['Indexed'] = (df_show['NAV'] / base_nav * 100).round(2)
                df_show['Cum Return (%)'] = ((df_show['NAV'] / base_nav - 1) * 100).round(3)
                df_show['Daily Return (%)'] = df_show['NAV'].pct_change().mul(100).round(3)

                col_tbl, col_stat = st.columns([3,1])
                with col_tbl:
                    # Build rows with color-coded returns
                    rows_html = ''
                    for i, row in df_show.iterrows():
                        dr = row['Daily Return (%)']
                        cr = row['Cum Return (%)']
                        dr_str = f'+{dr:.3f}%' if pd.notna(dr) and dr>0 else (f'{dr:.3f}%' if pd.notna(dr) and dr<0 else '—')
                        dr_c = '#1D9E75' if pd.notna(dr) and dr>0 else ('#E24B4A' if pd.notna(dr) and dr<0 else '#888')
                        cr_str = f'+{cr:.2f}%' if cr>0 else f'{cr:.2f}%'
                        cr_c = '#1D9E75' if cr>0 else '#E24B4A'
                        bg = '#F4F7FB' if i%2==0 else 'white'
                        rows_html += (
                            f'<tr style="background:{bg};">'
                            f'<td style="padding:6px 12px;">{row["Date"].strftime("%d-%b-%Y")}</td>'
                            f'<td style="padding:6px 12px;">₹{row["NAV"]:,.4f}</td>'
                            f'<td style="padding:6px 12px;">{row["Indexed"]:.2f}</td>'
                            f'<td style="padding:6px 12px;"><span style="color:{cr_c};font-weight:600;">{cr_str}</span></td>'
                            f'<td style="padding:6px 12px;"><span style="color:{dr_c};">{dr_str}</span></td>'
                            f'</tr>'
                        )
                    nav_html = f'''
                    <div style="overflow-y:auto;max-height:440px;border-radius:10px;
                                border:1px solid #D8E4F0;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                      <table style="width:100%;border-collapse:collapse;font-family:Segoe UI,Arial;font-size:13px;">
                        <thead style="position:sticky;top:0;">
                          <tr style="background:#0C3C6E;">
                            <th style="padding:9px 12px;text-align:left;color:white;white-space:nowrap;">Date</th>
                            <th style="padding:9px 12px;text-align:left;color:white;white-space:nowrap;">NAV (₹)</th>
                            <th style="padding:9px 12px;text-align:left;color:white;white-space:nowrap;">Indexed (Base=100)</th>
                            <th style="padding:9px 12px;text-align:left;color:white;white-space:nowrap;">Cumulative Return</th>
                            <th style="padding:9px 12px;text-align:left;color:white;white-space:nowrap;">Daily Return</th>
                          </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                      </table>
                    </div>
                    <p style="font-size:11px;color:#6B7F99;margin-top:4px;">
                      {len(df_show):,} trading days | {fund_view} | Base NAV: ₹{base_nav:,.4f}
                    </p>'''
                    st.markdown(nav_html, unsafe_allow_html=True)

                with col_stat:
                    nav_arr = df_show['NAV'].values
                    if len(nav_arr) > 1:
                        daily_rets = pd.Series(nav_arr).pct_change().dropna()
                        st.markdown("**📈 Quick Stats**")
                        st.metric("Total Return",     f"+{(nav_arr[-1]/nav_arr[0]-1)*100:.2f}%")
                        st.metric("Avg Daily Return", f"{daily_rets.mean()*100:.3f}%")
                        st.metric("Daily Std Dev",    f"{daily_rets.std()*100:.3f}%")
                        st.metric("Best Day",         f"+{daily_rets.max()*100:.2f}%")
                        st.metric("Worst Day",        f"{daily_rets.min()*100:.2f}%")
                        pos = (daily_rets > 0).sum()
                        st.metric("Positive Days",    f"{pos} / {len(daily_rets)}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>📊 <b>Financial Modelling of Mutual Fund Returns</b> | "
    "Salesqueen Software Solutions, Chennai | MBA Project 2025–2026 | "
    "Data: AMFI India · NSE India · RBI · IBJA · India Post</small></center>",
    unsafe_allow_html=True
)
