import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Modelling of Mutual Fund Returns",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Hide Streamlit default header */
  header[data-testid="stHeader"] { display: none; }
  .block-container { padding-top: 0rem !important; }

  /* Top banner */
  .top-banner {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    padding: 14px 32px;
    display: flex;
    align-items: center;
    gap: 18px;
    border-radius: 0 0 12px 12px;
    margin-bottom: 18px;
    box-shadow: 0 3px 16px rgba(0,0,0,0.18);
  }
  .banner-logo {
    background: white; border-radius: 50%;
    width: 58px; height: 58px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; font-size: 28px;
  }
  .banner-text h1 { color: white; font-size: 19px; margin: 0; font-weight: 700; }
  .banner-text p  { color: rgba(255,255,255,0.82); font-size: 11px; margin: 3px 0 7px; }
  .badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .badge {
    background: rgba(255,255,255,0.16);
    color: white; padding: 3px 10px;
    border-radius: 20px; font-size: 10px;
  }

  /* Metric card */
  .mcard {
    background: white; border-radius: 10px;
    padding: 16px 18px; border-left: 4px solid #2E75B6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 12px;
  }
  .mcard-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 0.4px; }
  .mcard-value { font-size: 26px; font-weight: 700; color: #1F4E79; }
  .mcard-sub   { font-size: 11px; color: #999; margin-top: 3px; }
  .mcard.green  { border-left-color: #1E8449; }
  .mcard.green .mcard-value { color: #1E8449; }
  .mcard.red    { border-left-color: #C0392B; }
  .mcard.red .mcard-value { color: #C0392B; }
  .mcard.gold   { border-left-color: #D4A017; }
  .mcard.gold .mcard-value { color: #D4A017; }

  /* Profile boxes */
  .prof-box { border-radius: 10px; padding: 16px; }
  .prof-box h3 { font-size: 14px; font-weight: 700; margin-bottom: 8px; }
  .prof-box ul { padding-left: 18px; font-size: 13px; line-height: 1.85; }
  .cons  { background: #d4edda; } .cons h3  { color: #155724; }
  .mod   { background: #d0e8ff; } .mod h3   { color: #004085; }
  .aggr  { background: #fde8e8; } .aggr h3  { color: #721c24; }
  .taxs  { background: #fff3cd; } .taxs h3  { color: #856404; }

  /* Section header */
  .sec-title { font-size: 20px; font-weight: 700; color: #1F4E79; margin-bottom: 2px; }
  .sec-sub   { font-size: 13px; color: #888; margin-bottom: 16px; }

  /* Bench card */
  .bcard {
    background: white; border-radius: 10px; padding: 14px;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .bcard .bicon  { font-size: 22px; margin-bottom: 4px; }
  .bcard .blabel { font-size: 10px; color: #888; text-transform: uppercase; }
  .bcard .bvalue { font-size: 22px; font-weight: 700; margin: 3px 0; }
  .bcard .bsrc   { font-size: 10px; color: #aaa; }
</style>
""", unsafe_allow_html=True)

# ─── Top Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
  <div class="banner-logo">🏛️</div>
  <div class="banner-text">
    <h1>Financial Modelling of Mutual Fund Returns</h1>
    <p>A Data-Driven Approach to Convert Potential Investors into Consistent Wealth Builders</p>
    <div class="badge-row">
      <span class="badge">📊 8 Mutual Funds</span>
      <span class="badge">📅 Jan 2021 – Dec 2025</span>
      <span class="badge">🧮 8 Financial Models</span>
      <span class="badge">🏢 Salesqueen Software Solutions</span>
      <span class="badge">📍 Chennai, India</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
FUNDS = [
    "Bandhan Small Cap","HDFC Flexi Cap","Kotak Midcap",
    "Nippon Gold ETF","HDFC Balanced Adv","ICICI ELSS",
    "Mirae Large Cap","HDFC Money Market"
]
COLORS = ["#e74c3c","#2E75B6","#8e44ad","#D4A017","#1E8449","#f39c12","#3498db","#95a5a6"]

returns_df = pd.DataFrame({
    "Fund": FUNDS,
    "Category": ["Small Cap","Flexi Cap","Mid Cap","Gold","Hybrid","ELSS","Large Cap","Debt"],
    "NAV_Start": [23.86, 45.67, 46.35, 4418, 42.11, 88.75, 61.93, 4039],
    "NAV_End":   [73.45, 131.95, 127.57, 7571, 96.42, 196.07, 117.99, 5413],
    "Total_Return": [213.8, 189.2, 175.3, 143.6, 145.3, 117.5, 90.5, 34.1],
    "CAGR": [25.2, 23.4, 21.9, 21.0, 19.7, 16.8, 13.9, 6.1],
    "vs_Nifty": [10.7, 8.9, 7.4, 6.5, 5.2, 2.3, -0.6, -8.4],
})

risk_df = pd.DataFrame({
    "Fund": FUNDS,
    "Std_Dev": [17.9, 13.0, 15.0, 13.0, 10.3, 12.9, 12.1, 0.6],
    "Max_DD":  [-21.7, -11.1, -20.4, -10.2, -9.2, -16.3, -15.0, 0.0],
    "VaR_95":  [-5.56, -3.49, -4.60, -3.31, -2.82, -3.67, -3.42, -0.01],
    "Risk_Level": ["High","Moderate","High","Moderate","Low","High","Moderate","Very Low"],
})

ra_df = pd.DataFrame({
    "Fund": FUNDS,
    "Sharpe":  [1.05, 1.30, 1.03, 1.10, 1.26, 0.81, 0.63, -0.73],
    "Sortino": [1.20, 1.67, 0.97, 1.47, 1.65, 0.81, 0.60, 0.00],
    "Alpha":   [10.7, 9.2, 7.4, 6.5, 5.2, 2.3, -0.6, -8.4],
    "Rating":  ["★★★★☆","★★★★★","★★★☆☆","★★★★☆","★★★★★","★★★☆☆","★★☆☆☆","★☆☆☆☆"],
})

sip_df = pd.DataFrame({
    "Fund / Rate":  ["Bandhan SC (25.2%)","HDFC Flexi Cap (23.4%)","HDFC Balanced (19.7%)",
                     "Kotak Midcap (21.9%)","Nippon Gold (21.0%)","ICICI ELSS (16.8%)",
                     "Mirae Large Cap (13.9%)","HDFC Money Market (6.1%)",
                     "Nifty 50 (14.5%)","NSC India Post (7.7%)","Bank FD (6.8%)","RBI Rate (6.5%)"],
    "FV_5Y":  [5.11, 4.89, 4.48, 4.66, 4.46, 4.18, 3.89, 3.41, 4.18, 3.61, 3.53, 3.51],
    "FV_10Y": [19.27, 16.50, 14.27, 15.30, 14.10, 11.70, 9.80, 6.95, 12.10, 7.29, 7.05, 6.95],
    "FV_15Y": [57.94, 46.20, 35.98, 40.50, 35.30, 27.00, 20.50, 10.35, 27.50, 11.09, 10.58, 10.35],
})

score_df = pd.DataFrame({
    "Rank": ["🥇 #1","🥈 #2","🥉 #3","#4","#5","#6","#7","#8"],
    "Fund": ["HDFC Flexi Cap","Bandhan Small Cap","HDFC Balanced Adv",
             "Nippon Gold ETF","Kotak Midcap","ICICI ELSS","Mirae Large Cap","HDFC Money Market"],
    "Score": [88, 82, 79, 72, 70, 64, 58, 20],
    "CAGR": [23.4, 25.2, 19.7, 21.0, 21.9, 16.8, 13.9, 6.1],
    "Sharpe": [1.30, 1.05, 1.26, 1.10, 1.03, 0.81, 0.63, -0.73],
    "Max_DD": [-11.1, -21.7, -9.2, -10.2, -20.4, -16.3, -15.0, 0.0],
    "Best_For": ["Moderate Investors","Aggressive Investors","Conservative Investors",
                 "Portfolio Hedge","Aggressive Investors","Tax Saving (80C)",
                 "Low-risk Equity","Capital Preservation"],
})

# Correlation matrix
corr_funds = ["Bandhan SC","HDFC Flexi","Kotak Mid","Nippon Gold","HDFC Bal","ICICI ELSS","Mirae LC","HDFC MM"]
corr_matrix = np.array([
    [1.00, 0.82, 0.85, -0.34, 0.79, 0.83, 0.80, 0.04],
    [0.82, 1.00, 0.79, -0.31, 0.87, 0.81, 0.84, 0.06],
    [0.85, 0.79, 1.00, -0.38, 0.76, 0.82, 0.78, 0.02],
    [-0.34,-0.31,-0.38, 1.00,-0.24,-0.29,-0.27, 0.01],
    [0.79, 0.87, 0.76, -0.24, 1.00, 0.78, 0.85, 0.08],
    [0.83, 0.81, 0.82, -0.29, 0.78, 1.00, 0.80, 0.05],
    [0.80, 0.84, 0.78, -0.27, 0.85, 0.80, 1.00, 0.07],
    [0.04, 0.06, 0.02,  0.01, 0.08, 0.05, 0.07, 1.00],
])

# Simulated NAV growth (indexed to 100)
months = pd.date_range("2021-01", periods=60, freq="ME")
np.random.seed(42)
nav_data = {}
for i, (fund, cagr, std) in enumerate(zip(
    FUNDS,
    [25.2, 23.4, 21.9, 21.0, 19.7, 16.8, 13.9, 6.1],
    [17.9, 13.0, 15.0, 13.0, 10.3, 12.9, 12.1, 0.6]
)):
    monthly_ret = cagr / 100 / 12
    monthly_std = std / 100 / np.sqrt(12)
    rets = np.random.normal(monthly_ret, monthly_std, 60)
    prices = 100 * np.cumprod(1 + rets)
    nav_data[fund] = prices

nav_df = pd.DataFrame(nav_data, index=months)

# ─── TABS ────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📌 Overview","📈 Returns","⚠️ Risk Metrics",
                "🎯 Risk-Adjusted","🏁 Benchmark","💰 SIP Analysis",
                "🔗 Correlation","🏆 Scorecard"])

# ═══════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="sec-title">Project Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">8 funds analysed across 5 years using 8 financial models | Data: AMFI India, NSE, RBI, IBJA, India Post</div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1,"Best CAGR","25.2%","Bandhan Small Cap","green"),
        (c2,"Best Sharpe","1.30","HDFC Flexi Cap",""),
        (c3,"Safest Fund","−9.2%","HDFC Balanced Adv (Max DD)",""),
        (c4,"Gold Return","21.0%","Nippon Gold ETF CAGR","gold"),
        (c5,"Nifty 50","14.5%","Benchmark CAGR",""),
        (c6,"Risk-Free Rate","6.5%","RBI Repo Rate","red"),
    ]
    for col, label, val, sub, cls in cards:
        col.markdown(f'<div class="mcard {cls}"><div class="mcard-label">{label}</div><div class="mcard-value">{val}</div><div class="mcard-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("**📌 Key Benchmark & Reference Rates**")
    b1,b2,b3,b4,b5,b6 = st.columns(6)
    bench = [
        (b1,"📉","Nifty 50","14.5%","#1F4E79","NSE India"),
        (b2,"🏦","RBI Risk-Free","6.5%","#2E75B6","rbi.org.in"),
        (b3,"🏧","Bank FD","6.8%","#5b6abf","Avg. SBI/HDFC FD"),
        (b4,"🥇","Gold (IBJA)","19.5%","#D4A017","ibja.co"),
        (b5,"📬","NSC Rate","7.7%","#1E8449","India Post"),
        (b6,"📊","CPI Inflation","5.5%","#C0392B","RBI / MOSPI"),
    ]
    for col, icon, lbl, val, clr, src in bench:
        col.markdown(f'<div class="bcard"><div class="bicon">{icon}</div><div class="blabel">{lbl}</div><div class="bvalue" style="color:{clr};">{val}</div><div class="bsrc">{src}</div></div>', unsafe_allow_html=True)

    st.markdown("")
    col_l, col_r = st.columns(2)

    with col_l:
        fig = go.Figure(go.Bar(
            x=returns_df["CAGR"], y=returns_df["Fund"],
            orientation="h",
            marker_color=COLORS,
            text=[f"{v}%" for v in returns_df["CAGR"]],
            textposition="outside"
        ))
        fig.add_vline(x=14.5, line_dash="dash", line_color="red", annotation_text="Nifty 50 (14.5%)")
        fig.update_layout(title="CAGR Comparison — All 8 Funds", height=380,
                          xaxis_title="CAGR (%)", margin=dict(l=10,r=40,t=40,b=20),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = go.Figure()
        for i, row in returns_df.iterrows():
            risk_row = risk_df[risk_df["Fund"] == row["Fund"]].iloc[0]
            ra_row   = ra_df[ra_df["Fund"] == row["Fund"]].iloc[0]
            fig2.add_trace(go.Scatter(
                x=[risk_row["Std_Dev"]], y=[row["CAGR"]],
                mode="markers+text",
                marker=dict(size=ra_row["Sharpe"]*40, color=COLORS[i], opacity=0.75, line=dict(width=1,color="white")),
                text=[row["Fund"].split()[0]], textposition="top center",
                name=row["Fund"], showlegend=False
            ))
        fig2.update_layout(title="Risk vs Return (bubble = Sharpe Ratio)", height=380,
                           xaxis_title="Std Dev (%)", yaxis_title="CAGR (%)",
                           margin=dict(l=10,r=10,t=40,b=20),
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════
# TAB 2 — RETURNS
# ═══════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-title">Return Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">CAGR · Absolute Return · NAV Growth from Jan 2021 to Dec 2025</div>', unsafe_allow_html=True)

    display = returns_df.copy()
    display["NAV Jan-21"] = display["NAV_Start"].apply(lambda x: f"₹{x:,.0f}")
    display["NAV Dec-25"] = display["NAV_End"].apply(lambda x: f"₹{x:,.0f}")
    display["Total Return"] = display["Total_Return"].apply(lambda x: f"+{x:.1f}%")
    display["CAGR (5Y)"]   = display["CAGR"].apply(lambda x: f"{x:.1f}%")
    display["vs Nifty 50"] = display["vs_Nifty"].apply(lambda x: f"+{x:.1f}% ✅" if x>0 else f"{x:.1f}% ❌")
    st.dataframe(display[["Fund","Category","NAV Jan-21","NAV Dec-25","Total Return","CAGR (5Y)","vs Nifty 50"]],
                 use_container_width=True, hide_index=True)

    fig = go.Figure()
    for i, fund in enumerate(FUNDS):
        fig.add_trace(go.Scatter(
            x=nav_df.index, y=nav_df[fund],
            name=fund, line=dict(color=COLORS[i], width=2)
        ))
    fig.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Base = 100")
    fig.update_layout(title="NAV Growth — All 8 Funds (Indexed to 100 at Jan 2021)",
                      height=420, xaxis_title="Date", yaxis_title="Indexed NAV",
                      plot_bgcolor="white", paper_bgcolor="white",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════
# TAB 3 — RISK METRICS
# ═══════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec-title">Risk Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Standard Deviation · Maximum Drawdown · Value-at-Risk (95%)</div>', unsafe_allow_html=True)

    disp = risk_df.copy()
    disp["Ann. Std Dev"] = disp["Std_Dev"].apply(lambda x: f"{x:.1f}%")
    disp["Max Drawdown"] = disp["Max_DD"].apply(lambda x: f"{x:.1f}%")
    disp["VaR 95%"]      = disp["VaR_95"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(disp[["Fund","Ann. Std Dev","Max Drawdown","VaR 95%","Risk_Level"]],
                 use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            y=risk_df["Fund"], x=risk_df["Std_Dev"], orientation="h",
            marker_color=["#e74c3c" if v > 15 else "#f39c12" if v > 11 else "#2ecc71" for v in risk_df["Std_Dev"]],
            text=[f"{v}%" for v in risk_df["Std_Dev"]], textposition="outside"
        ))
        fig.update_layout(title="Standard Deviation (Annualised %)", height=360,
                          plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(l=10,r=50,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure(go.Bar(
            y=risk_df["Fund"], x=risk_df["Max_DD"], orientation="h",
            marker_color=["#e74c3c" if v < -18 else "#f39c12" if v < -12 else "#2ecc71" for v in risk_df["Max_DD"]],
            text=[f"{v}%" for v in risk_df["Max_DD"]], textposition="outside"
        ))
        fig2.update_layout(title="Maximum Drawdown (%)", height=360,
                           plot_bgcolor="white", paper_bgcolor="white",
                           margin=dict(l=10,r=50,t=40,b=20))
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════
# TAB 4 — RISK-ADJUSTED
# ═══════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec-title">Risk-Adjusted Returns</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Sharpe · Sortino · Jensen\'s Alpha | Rf = 6.5% (RBI Rate)</div>', unsafe_allow_html=True)

    disp = ra_df.copy()
    disp["Sharpe Ratio"]  = disp["Sharpe"].apply(lambda x: f"{x:.2f}")
    disp["Sortino Ratio"] = disp["Sortino"].apply(lambda x: f"{x:.2f}")
    disp["Jensen Alpha"]  = disp["Alpha"].apply(lambda x: f"+{x:.1f}%" if x>=0 else f"{x:.1f}%")
    ranks = ["🥇 #1","🥈 #2","🥉 #3","#4","#5","#6","#7","#8"]
    # Sort by Sharpe
    sorted_ra = ra_df.sort_values("Sharpe", ascending=False).reset_index(drop=True)
    sorted_ra["Rank"] = ranks
    sorted_ra["Sharpe Ratio"]  = sorted_ra["Sharpe"].apply(lambda x: f"{x:.2f}")
    sorted_ra["Sortino Ratio"] = sorted_ra["Sortino"].apply(lambda x: f"{x:.2f}")
    sorted_ra["Jensen Alpha"]  = sorted_ra["Alpha"].apply(lambda x: f"+{x:.1f}%" if x>=0 else f"{x:.1f}%")
    sorted_ra["Rating"]        = sorted_ra["Rating"]
    st.dataframe(sorted_ra[["Rank","Fund","Sharpe Ratio","Sortino Ratio","Jensen Alpha","Rating"]],
                 use_container_width=True, hide_index=True)

    fig = go.Figure()
    order = sorted_ra["Fund"].tolist()
    sharpe_vals  = sorted_ra["Sharpe"].tolist()
    sortino_vals = sorted_ra["Sortino"].tolist()
    fig.add_trace(go.Bar(name="Sharpe Ratio",  x=order, y=sharpe_vals,  marker_color="#2E75B6"))
    fig.add_trace(go.Bar(name="Sortino Ratio", x=order, y=sortino_vals, marker_color="#1E8449"))
    fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Good (≥1.0)")
    fig.update_layout(title="Sharpe & Sortino Ratios — All Funds", barmode="group",
                      height=380, plot_bgcolor="white", paper_bgcolor="white",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    # Alpha bar
    alpha_df = sorted_ra.sort_values("Alpha", ascending=True)
    fig2 = go.Figure(go.Bar(
        y=alpha_df["Fund"], x=alpha_df["Alpha"], orientation="h",
        marker_color=["#1E8449" if v >= 0 else "#C0392B" for v in alpha_df["Alpha"]],
        text=[f"+{v:.1f}%" if v>=0 else f"{v:.1f}%" for v in alpha_df["Alpha"]],
        textposition="outside"
    ))
    fig2.add_vline(x=0, line_color="black", line_width=1)
    fig2.update_layout(title="Jensen's Alpha (Excess Return over CAPM)",
                       height=340, plot_bgcolor="white", paper_bgcolor="white",
                       margin=dict(l=10,r=60,t=40,b=20))
    st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════
# TAB 5 — BENCHMARK
# ═══════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec-title">Benchmark Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">vs Nifty 50 · vs Bank FD · vs NSC · vs Gold (IBJA) · vs CPI Inflation</div>', unsafe_allow_html=True)

    b1,b2,b3,b4,b5,b6 = st.columns(6)
    bench2 = [
        (b1,"📉","Nifty 50 CAGR","14.5%","#1F4E79","Source: NSE India"),
        (b2,"🏦","Bank FD Rate","6.8%","#5b6abf","Avg. 5-Year FD Rate"),
        (b3,"📬","NSC Rate","7.7%","#1E8449","Source: India Post"),
        (b4,"🥇","Gold (IBJA)","19.5%","#D4A017","Source: ibja.co"),
        (b5,"🏛","RBI Risk-Free","6.5%","#2E75B6","Source: rbi.org.in"),
        (b6,"📊","CPI Inflation","5.5%","#C0392B","Source: RBI/MOSPI"),
    ]
    for col, icon, lbl, val, clr, src in bench2:
        col.markdown(f'<div class="bcard"><div class="bicon">{icon}</div><div class="blabel">{lbl}</div><div class="bvalue" style="color:{clr};">{val}</div><div class="bsrc">{src}</div></div>', unsafe_allow_html=True)

    st.markdown("")
    benchmarks = {"Nifty 50": 14.5, "Bank FD": 6.8, "NSC": 7.7, "Gold/IBJA": 19.5, "CPI Inflation": 5.5}
    all_labels = FUNDS + list(benchmarks.keys())
    all_cagrs  = list(returns_df["CAGR"]) + list(benchmarks.values())
    bar_colors = COLORS + ["#1F4E79","#5b6abf","#1E8449","#D4A017","#C0392B"]

    fig = go.Figure(go.Bar(
        x=all_labels, y=all_cagrs,
        marker_color=bar_colors,
        text=[f"{v:.1f}%" for v in all_cagrs], textposition="outside"
    ))
    fig.update_layout(title="CAGR vs All Benchmarks", height=400,
                      yaxis_title="CAGR (%)",
                      plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(l=10,r=10,t=40,b=80),
                      xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

    bench_tbl = pd.DataFrame({
        "Fund": FUNDS + ["Nifty 50 Index","Gold (IBJA)","NSC (India Post)","Bank FD"],
        "CAGR": [25.2,23.4,21.9,21.0,19.7,16.8,13.9,6.1,14.5,19.5,7.7,6.8],
        "vs Nifty 50 (14.5%)": ["+10.7%","+8.9%","+7.4%","+6.5%","+5.2%","+2.3%","−0.6%","−8.4%","—","+5.0%","−6.8%","−7.7%"],
        "vs Bank FD (6.8%)":   ["+18.4%","+16.6%","+15.1%","+14.2%","+12.9%","+10.0%","+7.1%","−0.7%","+7.7%","+12.7%","+0.9%","—"],
        "vs CPI (5.5%)":       ["+19.7%","+17.9%","+16.4%","+15.5%","+14.2%","+11.3%","+8.4%","+0.6%","+9.0%","+14.0%","+2.2%","+1.3%"],
        "Beat Market?":        ["✅ Yes","✅ Yes","✅ Yes","✅ Yes","✅ Yes","✅ Yes","❌ No","❌ No","Benchmark","✅ Yes","Fixed","Fixed"],
    })
    st.dataframe(bench_tbl, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════
# TAB 6 — SIP ANALYSIS
# ═══════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec-title">SIP Analysis — Wealth Creation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">₹5,000/month SIP | Power of Compounding across 5, 10, 15 Years</div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    sip_cards = [
        (c1,"Total Invested (5Y)","₹3.0L","₹5,000 × 60 months",""),
        (c2,"Value @ 25% CAGR","₹5.11L","Bandhan Small Cap level","green"),
        (c3,"Value @ 18% CAGR","₹4.48L","HDFC Balanced level",""),
        (c4,"Value @ 7.7% NSC","₹3.61L","India Post NSC Rate",""),
        (c5,"Value @ 6.5% FD","₹3.53L","RBI Risk-Free Rate","red"),
    ]
    for col, label, val, sub, cls in sip_cards:
        col.markdown(f'<div class="mcard {cls}"><div class="mcard-label">{label}</div><div class="mcard-value">{val}</div><div class="mcard-sub">{sub}</div></div>', unsafe_allow_html=True)

    horizon = st.radio("Select Horizon:", ["5 Years","10 Years","15 Years"], horizontal=True)
    col_map = {"5 Years":"FV_5Y","10 Years":"FV_10Y","15 Years":"FV_15Y"}
    col_sel = col_map[horizon]

    sip_plot = sip_df.sort_values(col_sel, ascending=True)
    bar_c = ["#e74c3c" if "Bandhan" in r else "#2E75B6" if "Flexi" in r
             else "#D4A017" if "Gold" in r else "#8e44ad" if "Kotak" in r
             else "#1E8449" if "Balanced" in r else "#f39c12" if "ELSS" in r
             else "#95a5a6" for r in sip_plot["Fund / Rate"]]

    fig = go.Figure(go.Bar(
        y=sip_plot["Fund / Rate"], x=sip_plot[col_sel], orientation="h",
        marker_color=bar_c,
        text=[f"₹{v:.2f}L" for v in sip_plot[col_sel]], textposition="outside"
    ))
    fig.add_vline(x=3.0, line_dash="dash", line_color="gray", annotation_text="Invested ₹3L")
    fig.update_layout(title=f"₹5,000/month SIP — Future Value ({horizon})",
                      height=480, plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_title="Future Value (₹ Lakhs)",
                      margin=dict(l=10,r=80,t=40,b=20))
    st.plotly_chart(fig, use_container_width=True)

    sip_show = sip_df.copy()
    sip_show["FV 5Y"]  = sip_show["FV_5Y"].apply(lambda x: f"₹{x:.2f}L")
    sip_show["FV 10Y"] = sip_show["FV_10Y"].apply(lambda x: f"₹{x:.2f}L")
    sip_show["FV 15Y"] = sip_show["FV_15Y"].apply(lambda x: f"₹{x:.2f}L")
    st.dataframe(sip_show[["Fund / Rate","FV 5Y","FV 10Y","FV 15Y"]],
                 use_container_width=True, hide_index=True)

# ═══════════════════════════════════════
# TAB 7 — CORRELATION
# ═══════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="sec-title">Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Pearson Correlation Matrix — Values close to 1 = move together | Values close to −1 = move opposite</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    corr_cards = [
        (c1,"Highest Correlation","0.87","HDFC Balanced ↔ Flexi Cap","red"),
        (c2,"Best Diversifier","−0.38","Nippon Gold ↔ Kotak Midcap","green"),
        (c3,"Gold vs Equity","−0.24 to −0.38","Natural portfolio hedge",""),
        (c4,"Risk Reduction","~25%","Adding 15% Gold to portfolio",""),
    ]
    for col, label, val, sub, cls in corr_cards:
        col.markdown(f'<div class="mcard {cls}"><div class="mcard-label">{label}</div><div class="mcard-value" style="font-size:20px;">{val}</div><div class="mcard-sub">{sub}</div></div>', unsafe_allow_html=True)

    fig = go.Figure(go.Heatmap(
        z=corr_matrix, x=corr_funds, y=corr_funds,
        colorscale=[
            [0.0, "#1E8449"],
            [0.5, "#ffffff"],
            [1.0, "#C0392B"],
        ],
        zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in corr_matrix],
        texttemplate="%{text}",
        textfont={"size": 11},
        hoverongaps=False,
        showscale=True,
        colorbar=dict(title="Correlation")
    ))
    fig.update_layout(title="Pearson Correlation Heatmap", height=480,
                      plot_bgcolor="white", paper_bgcolor="white",
                      xaxis=dict(tickangle=-30),
                      margin=dict(l=10,r=10,t=40,b=80))
    st.plotly_chart(fig, use_container_width=True)

    findings_tbl = pd.DataFrame({
        "Finding": ["Highest Equity Correlation","Gold as Hedge","Debt Uncorrelated","Mid + Small Correlation","Best Diversified Pair"],
        "Funds": ["HDFC Balanced ↔ HDFC Flexi Cap","Nippon Gold ↔ Equity Funds","HDFC Money Market ↔ All","Kotak Midcap ↔ Bandhan SC","HDFC Flexi Cap + Gold ETF"],
        "Correlation": ["0.87","−0.24 to −0.38","~0.00","0.81","−0.31"],
        "Interpretation": [
            "Very similar movement — limited diversification benefit",
            "Moves opposite to equity — excellent hedge",
            "Near-zero correlation — stable portfolio anchor",
            "High — both are growth-oriented funds",
            "Highest return + best hedge combination",
        ],
    })
    st.dataframe(findings_tbl, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════
# TAB 8 — SCORECARD
# ═══════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="sec-title">Overall Fund Scorecard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Weighted Score: CAGR 25 + Sharpe 25 + Sortino 20 + Low Drawdown 15 + Low Volatility 15 = 100</div>', unsafe_allow_html=True)

    disp = score_df.copy()
    disp["CAGR %"] = disp["CAGR"].apply(lambda x: f"{x:.1f}%")
    disp["Sharpe"] = disp["Sharpe"].apply(lambda x: f"{x:.2f}")
    disp["Max DD"] = disp["Max_DD"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(disp[["Rank","Fund","Score","CAGR %","Sharpe","Max DD","Best_For"]],
                 use_container_width=True, hide_index=True)

    fig = go.Figure(go.Bar(
        x=score_df["Fund"], y=score_df["Score"],
        marker_color=["#1E8449","#2E75B6","#2E75B6","#D4A017","#8e44ad","#f39c12","#95a5a6","#C0392B"],
        text=score_df["Score"], textposition="outside"
    ))
    fig.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Excellent (≥75)")
    fig.add_hline(y=60, line_dash="dot",  line_color="orange", annotation_text="Good (≥60)")
    fig.update_layout(title="Overall Score /100 — All Funds", height=360,
                      yaxis_title="Score", yaxis_range=[0, 100],
                      plot_bgcolor="white", paper_bgcolor="white",
                      xaxis_tickangle=-20, margin=dict(l=10,r=10,t=40,b=80))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 👤 Investor Profile Recommendations")
    p1,p2,p3,p4 = st.columns(4)
    profiles = [
        (p1,"cons","🟢 Conservative Investor",
         ["HDFC Balanced Advantage — Max DD −9.2%","HDFC Money Market — Capital safe",
          "NSC / Bank FD — Fixed return guarantee","Nippon Gold ETF — Inflation hedge"]),
        (p2,"mod","🔵 Moderate Investor",
         ["HDFC Flexi Cap — Best Sharpe 1.30","ICICI ELSS — Tax benefit + growth",
          "Nippon Gold ETF — Portfolio diversifier","Kotak Midcap — Medium-high growth"]),
        (p3,"aggr","🔴 Aggressive Investor",
         ["Bandhan Small Cap — Highest CAGR 25.2%","Kotak Midcap — Strong mid-cap growth",
          "HDFC Flexi Cap — High return + managed risk","Long horizon (5+ years) required"]),
        (p4,"taxs","🟡 Tax Saver Investor",
         ["ICICI ELSS — 80C deduction ₹1.5L/yr","3-year lock-in period only",
          "CAGR 16.8% — beats FD and NSC","Best tax-saving + wealth creation combo"]),
    ]
    for col, cls, title, items in profiles:
        items_html = "".join(f"<li>{i}</li>" for i in items)
        col.markdown(f'<div class="prof-box {cls}"><h3>{title}</h3><ul>{items_html}</ul></div>',
                     unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>📊 <b>Financial Modelling of Mutual Fund Returns</b> | "
    "Salesqueen Software Solutions, Chennai | MBA Project 2025–2026 | "
    "Data: AMFI India, NSE, RBI, IBJA, India Post</small></center>",
    unsafe_allow_html=True
)
