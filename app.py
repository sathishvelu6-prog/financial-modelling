import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

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
  header[data-testid="stHeader"]{ display:none; }
  .block-container{ padding-top:0 !important; padding-bottom:1rem !important; }
  .banner{
    background:linear-gradient(135deg,#1F4E79 0%,#2E75B6 100%);
    padding:12px 28px; display:flex; align-items:center; gap:16px;
    border-radius:0 0 10px 10px; margin-bottom:16px;
    box-shadow:0 3px 14px rgba(0,0,0,0.18);
  }
  .banner-logo{ background:white; border-radius:50%; width:56px; height:56px;
    display:flex; align-items:center; justify-content:center;
    font-size:26px; flex-shrink:0; box-shadow:0 2px 8px rgba(0,0,0,0.2); }
  .banner-text h1{ color:white; font-size:18px; margin:0; font-weight:700; }
  .banner-text p{ color:rgba(255,255,255,0.8); font-size:11px; margin:2px 0 6px; }
  .badges{ display:flex; gap:8px; flex-wrap:wrap; }
  .badge{ background:rgba(255,255,255,0.15); color:white; padding:3px 10px; border-radius:20px; font-size:10px; }
  .kcard{ background:white; border-radius:10px; padding:14px 16px;
    border-left:4px solid #2E75B6; box-shadow:0 2px 8px rgba(0,0,0,0.07); margin-bottom:10px; }
  .kcard.green{ border-left-color:#1E8449; }
  .kcard.green .kval{ color:#1E8449; }
  .kcard.red{ border-left-color:#C0392B; }
  .kcard.red .kval{ color:#C0392B; }
  .kcard.gold{ border-left-color:#D4A017; }
  .kcard.gold .kval{ color:#D4A017; }
  .klabel{ font-size:10px; color:#888; text-transform:uppercase; letter-spacing:.4px; }
  .kval{ font-size:24px; font-weight:700; color:#1F4E79; line-height:1.2; }
  .ksub{ font-size:11px; color:#aaa; margin-top:2px; }
  .bc{ background:white; border-radius:10px; padding:12px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
  .bc .bi{ font-size:20px; margin-bottom:3px; }
  .bc .bl{ font-size:10px; color:#888; text-transform:uppercase; }
  .bc .bv{ font-size:20px; font-weight:700; margin:2px 0; }
  .bc .bs{ font-size:9px; color:#bbb; }
  .stitle{ font-size:19px; font-weight:700; color:#1F4E79; margin-bottom:2px; }
  .ssub{ font-size:12px; color:#888; margin-bottom:14px; }
  .pbox{ border-radius:10px; padding:14px; }
  .pbox h3{ font-size:13px; font-weight:700; margin-bottom:8px; }
  .pbox ul{ padding-left:16px; font-size:12px; line-height:1.9; margin:0; }
  .cons{ background:#d4edda; } .cons h3{ color:#155724; }
  .modr{ background:#d0e8ff; } .modr h3{ color:#004085; }
  .aggr{ background:#fde8e8; } .aggr h3{ color:#721c24; }
  .taxs{ background:#fff3cd; } .taxs h3{ color:#856404; }
</style>
""", unsafe_allow_html=True)

# ─── Banner ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
  <div class="banner-logo">🏛️</div>
  <div class="banner-text">
    <h1>Financial Modelling of Mutual Fund Returns</h1>
    <p>A Data-Driven Approach to Convert Potential Investors into Consistent Wealth Builders</p>
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

# ─── MASTER DATA ──────────────────────────────────────────────────────────────
FUNDS   = ['Mirae Large Cap','Bandhan Small Cap','HDFC Balanced Adv',
           'HDFC Flexi Cap','HDFC Money Market','ICICI ELSS',
           'Kotak Midcap','Nippon Gold ETF']
COLORS  = ['#2E75B6','#C0392B','#1E8449','#1F4E79','#7F8C8D','#8E44AD','#E67E22','#D4A017']
CAGRS   = [13.93,25.17,19.67,23.37, 6.10,16.75,21.94,20.95]
STDS    = [12.1, 17.9, 10.3, 13.0,  0.6, 12.9, 15.0, 13.0]
DDS     = [-14.97,-21.68,-9.15,-11.06,0.0,-16.33,-20.37,-10.20]
SHARPES = [0.63, 1.05, 1.26, 1.30,-0.73, 0.81,  1.03,  1.10]
SORTINOS= [0.60, 1.20, 1.65, 1.67, 0.00, 0.81,  0.97,  1.47]
ALPHAS  = [-0.57,11.2,  6.8,  7.5,-8.4,  2.3,   7.4,   5.9]
VAR95   = [-3.42,-5.56,-2.82,-3.49,-0.01,-3.67, -4.60, -3.31]
NAV_START=[61.93,23.86,42.11,45.67,4039, 88.75, 46.35, 4418]
NAV_END  =[117.99,73.45,96.42,131.95,5413,196.07,127.57,7571]
TOTAL_RET=[90.5,208.0,129.0,189.0,34.1,121.0,175.3,71.3]

CORR_LABELS=['Mirae LC','Bandhan SC','HDFC Bal','HDFC FC','HDFC MM','ICICI ELSS','Kotak MC','Nippon Gold']
CORR_MATRIX=np.array([
    [1.00,0.61,0.73,0.78,-0.02,0.79,0.72,-0.24],
    [0.61,1.00,0.55,0.65,-0.08,0.65,0.81,-0.32],
    [0.73,0.55,1.00,0.87, 0.05,0.77,0.63,-0.30],
    [0.78,0.65,0.87,1.00, 0.02,0.83,0.72,-0.31],
    [-0.02,-0.08,0.05,0.02,1.00,-0.01,-0.06,0.14],
    [0.79,0.65,0.77,0.83,-0.01,1.00,0.73,-0.26],
    [0.72,0.81,0.63,0.72,-0.06,0.73,1.00,-0.38],
    [-0.24,-0.32,-0.30,-0.31,0.14,-0.26,-0.38,1.00],
])
MONTHS_IDX=['Jan-21','Apr-21','Jul-21','Oct-21','Jan-22','Apr-22','Jul-22',
            'Oct-22','Jan-23','Apr-23','Jul-23','Oct-23','Jan-24','Apr-24',
            'Jul-24','Oct-24','Jan-25','Apr-25','Jul-25','Oct-25','Dec-25']
NAV_INDEXED=[
    [100,101.3,105.2,108.4,107.1,104.5,108.3,111.2,113.5,117.8,121.3,125.6,129.2,133.7,137.2,141.8,146.3,149.8,153.2,156.7,158.9],
    [100,108.5,121.3,136.7,142.1,130.2,138.5,150.3,162.7,178.5,195.2,208.4,222.1,238.7,252.3,268.4,282.1,295.7,305.2,308.8,312.5],
    [100,103.2,108.5,114.3,113.2,112.1,116.3,120.5,125.2,131.8,137.5,142.8,148.3,154.2,160.1,166.4,172.3,178.2,183.5,187.2,190.8],
    [100,106.3,115.2,124.5,122.3,119.8,126.5,133.2,141.5,152.3,162.8,172.5,182.3,193.7,204.5,215.2,225.8,234.3,241.2,246.8,251.3],
    [100,101.5,103.1,104.7,106.3,107.9,109.5,111.2,112.8,114.5,116.2,117.9,119.6,121.4,123.1,124.9,126.7,128.5,130.3,132.1,133.8],
    [100,104.5,112.3,120.5,118.2,115.3,120.8,126.5,133.2,141.8,150.3,158.7,166.2,175.3,183.8,191.2,198.5,205.3,210.2,213.8,216.5],
    [100,107.8,118.5,130.2,135.8,125.3,133.7,145.2,157.8,172.3,187.5,201.2,214.8,229.3,243.5,257.2,268.5,276.2,281.3,275.8,272.5],
    [100,105.2,110.8,116.3,125.7,131.5,138.2,142.8,150.3,158.7,163.5,169.2,178.5,185.3,193.8,202.5,210.3,218.7,225.2,230.8,235.2],
]

# ─── LOAD REAL NAV DATA ───────────────────────────────────────────────────────
NAV_FOLDER = os.path.join(os.path.dirname(__file__), '..', '06_NAV_Data')
NAV_FILES  = {
    'Mirae Large Cap'   : 'NAV_2021-01-01_to_2025-12-30  mirae asset large cap fund.xlsx',
    'Bandhan Small Cap' : 'NAV_2021-01-01_to_2025-12-30 Bandhan small cap Fund.xlsx',
    'HDFC Balanced Adv' : 'NAV_2021-01-01_to_2025-12-30 HDFC Balanced Advantage Fund.xlsx',
    'HDFC Flexi Cap'    : 'NAV_2021-01-01_to_2025-12-30 HDFC Flexi cap.xlsx',
    'HDFC Money Market' : 'NAV_2021-01-01_to_2025-12-30 HDFC Money Market Fund.xlsx',
    'ICICI ELSS'        : 'NAV_2021-01-01_to_2025-12-30 ICICI Prudential ELSS Tax Saver Fund.xlsx',
    'Kotak Midcap'      : 'NAV_2021-01-01_to_2025-12-30 Kotak Midcap fund.xlsx',
    'Nippon Gold ETF'   : 'NAV_2021-01-01_to_2025-12-30 Nippon India ETF Gold BeES.xlsx',
}

@st.cache_data
def load_nav_data():
    result = {}
    for fund, fname in NAV_FILES.items():
        path = os.path.join(NAV_FOLDER, fname)
        try:
            df = pd.read_excel(path, header=4)
            df.columns = ['NAV','Repurchase','Sale','Date']
            df = df[['Date','NAV']].dropna()
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date').reset_index(drop=True)
            result[fund] = df
        except Exception:
            result[fund] = None
    return result

nav_raw = load_nav_data()

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
            font=dict(family='Segoe UI,Arial', size=12))

def sip_fv(rate_pct, months):
    r = rate_pct / 100 / 12
    if r == 0:
        return 5000 * months
    return 5000 * (((1+r)**months - 1) / r) * (1+r)

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

    cols = st.columns(6)
    kcard(cols[0],"Best CAGR","25.17%","Bandhan Small Cap","green")
    kcard(cols[1],"Best Sharpe","1.30","HDFC Flexi Cap","")
    kcard(cols[2],"Safest Fund","−9.15%","HDFC Balanced Adv (Max DD)","")
    kcard(cols[3],"Gold CAGR","20.95%","Nippon Gold ETF","gold")
    kcard(cols[4],"Nifty 50","14.5%","Benchmark CAGR","")
    kcard(cols[5],"Risk-Free Rate","6.5%","RBI Repo Rate","red")

    st.markdown("**📌 Key Benchmark & Reference Rates**")
    bcols = st.columns(6)
    bcard(bcols[0],"📉","Nifty 50","14.5%","#1F4E79","NSE India")
    bcard(bcols[1],"🏦","RBI Risk-Free","6.5%","#2E75B6","rbi.org.in")
    bcard(bcols[2],"🏧","Bank FD","6.8%","#5b6abf","Avg. SBI/HDFC")
    bcard(bcols[3],"🥇","Gold (IBJA)","19.5%","#D4A017","ibja.co")
    bcard(bcols[4],"📬","NSC Rate","7.7%","#1E8449","India Post")
    bcard(bcols[5],"📊","CPI Inflation","5.5%","#C0392B","RBI/MOSPI")

    st.markdown("")
    cl, cr = st.columns(2)
    with cl:
        bar_c = ['rgba(30,132,73,0.85)' if c >= 14.5 else 'rgba(192,57,43,0.85)' for c in CAGRS]
        fig = go.Figure(go.Bar(
            y=FUNDS, x=CAGRS, orientation='h', marker_color=bar_c,
            text=[f"{v:.2f}%" for v in CAGRS], textposition='outside'))
        fig.add_vline(x=14.5, line_dash='dash', line_color='red',
                      annotation_text='Nifty 50 (14.5%)')
        fig.update_layout(title='CAGR Comparison — All 8 Funds',
                          xaxis_title='CAGR (%)', height=360, **BASE)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        fig2 = go.Figure()
        for i in range(len(FUNDS)):
            fig2.add_trace(go.Scatter(
                x=[STDS[i]], y=[CAGRS[i]], mode='markers+text',
                marker=dict(size=max(SHARPES[i]*16,8), color=COLORS[i],
                            opacity=0.8, line=dict(width=1,color='white')),
                text=[FUNDS[i].split()[0]], textposition='top center',
                name=FUNDS[i], showlegend=False))
        fig2.update_layout(title='Risk vs Return (bubble = Sharpe Ratio)',
                           xaxis_title='Std Dev (%)', yaxis_title='CAGR (%)',
                           height=360, **BASE)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════ TAB 2 — RETURNS ══════════════════
with tabs[1]:
    st.markdown('<div class="stitle">Return Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">CAGR · Absolute Return · NAV Growth — Jan 2021 to Dec 2025</div>', unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        'Fund': FUNDS,
        'Category': ['Large Cap','Small Cap','Hybrid','Flexi Cap','Debt','ELSS','Mid Cap','Gold'],
        'NAV Jan-21': [f'₹{v:,.2f}' for v in NAV_START],
        'NAV Dec-25': [f'₹{v:,.2f}' for v in NAV_END],
        'Total Return': [f'+{v:.1f}%' for v in TOTAL_RET],
        'CAGR (5Y)': [f'{v:.2f}%' for v in CAGRS],
        'vs Nifty 50': [f'+{v-14.5:.1f}% ✅' if v>=14.5 else f'{v-14.5:.1f}% ❌' for v in CAGRS],
    }), use_container_width=True, hide_index=True)

    fig = go.Figure()
    for i, fund in enumerate(FUNDS):
        fig.add_trace(go.Scatter(x=MONTHS_IDX, y=NAV_INDEXED[i],
                                 name=fund, line=dict(color=COLORS[i], width=2), mode='lines'))
    fig.add_hline(y=100, line_dash='dash', line_color='gray', opacity=0.5,
                  annotation_text='Base = 100')
    fig.update_layout(title='NAV Growth — All 8 Funds (Indexed to 100 at Jan 2021)',
                      xaxis_title='Period', yaxis_title='Indexed NAV', height=420,
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                      **BASE)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════ TAB 3 — RISK ══════════════════
with tabs[2]:
    st.markdown('<div class="stitle">Risk Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Standard Deviation · Maximum Drawdown · Value-at-Risk (95%)</div>', unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        'Fund': FUNDS,
        'Ann. Std Dev': [f'{v:.1f}%' for v in STDS],
        'Max Drawdown': [f'{v:.2f}%' for v in DDS],
        'VaR 95%': [f'{v:.2f}%' for v in VAR95],
        'Risk Level': ['Moderate','High','Low','Moderate','Very Low','High','High','Moderate'],
    }), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=FUNDS, y=STDS,
            marker_color=['rgba(192,57,43,0.85)' if v>15 else 'rgba(230,126,34,0.85)' if v>10 else 'rgba(30,132,73,0.85)' for v in STDS],
            text=[f'{v:.1f}%' for v in STDS], textposition='outside'))
        fig.update_layout(title='Standard Deviation (Annualised %)',
                          yaxis_title='Std Dev (%)', height=360,
                          xaxis_tickangle=-20, **BASE)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure(go.Bar(
            x=FUNDS, y=DDS,
            marker_color=['rgba(192,57,43,0.85)' if v<-18 else 'rgba(230,126,34,0.85)' if v<-10 else 'rgba(30,132,73,0.85)' for v in DDS],
            text=[f'{v:.2f}%' for v in DDS], textposition='outside'))
        fig2.update_layout(title='Maximum Drawdown (%)',
                           yaxis_title='Max DD (%)', height=360,
                           xaxis_tickangle=-20, **BASE)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure(go.Bar(
        x=FUNDS, y=VAR95,
        marker_color=['rgba(192,57,43,0.85)' if v<-4 else 'rgba(230,126,34,0.85)' if v<-2 else 'rgba(30,132,73,0.85)' for v in VAR95],
        text=[f'{v:.2f}%' for v in VAR95], textposition='outside'))
    fig3.update_layout(title='Value-at-Risk 95% — Worst Expected Monthly Loss (1-in-20 months)',
                       yaxis_title='VaR 95% (%)', height=340,
                       xaxis_tickangle=-20, **BASE)
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════ TAB 4 — RISK-ADJUSTED ══════════════════
with tabs[3]:
    st.markdown('<div class="stitle">Risk-Adjusted Returns</div>', unsafe_allow_html=True)
    st.markdown("<div class=\"ssub\">Sharpe · Sortino · Jensen's Alpha | Rf = 6.5% (RBI Rate)</div>", unsafe_allow_html=True)

    ra = pd.DataFrame({'Fund':FUNDS,'Sharpe':SHARPES,'Sortino':SORTINOS,'Alpha':ALPHAS})
    ra = ra.sort_values('Sharpe', ascending=False).reset_index(drop=True)
    ra.insert(0,'Rank',['🥇 #1','🥈 #2','🥉 #3','#4','#5','#6','#7','#8'])
    ra['Rating']=['★★★★★','★★★★★','★★★★☆','★★★★☆','★★★☆☆','★★★☆☆','★★☆☆☆','★☆☆☆☆']
    disp = ra.copy()
    disp['Sharpe']  = disp['Sharpe'].apply(lambda x: f'{x:.2f}')
    disp['Sortino'] = disp['Sortino'].apply(lambda x: f'{x:.2f}')
    disp['Alpha']   = disp['Alpha'].apply(lambda x: f'+{x:.1f}%' if x>=0 else f'{x:.1f}%')
    disp.rename(columns={'Alpha':"Jensen's Alpha"}, inplace=True)
    st.dataframe(disp[['Rank','Fund','Sharpe','Sortino',"Jensen's Alpha",'Rating']],
                 use_container_width=True, hide_index=True)

    sorted_funds = ra['Fund'].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sharpe',  x=sorted_funds,
                         y=[SHARPES[FUNDS.index(f)] for f in sorted_funds],
                         marker_color='rgba(31,78,121,0.85)'))
    fig.add_trace(go.Bar(name='Sortino', x=sorted_funds,
                         y=[SORTINOS[FUNDS.index(f)] for f in sorted_funds],
                         marker_color='rgba(30,132,73,0.75)'))
    fig.add_hline(y=1.0, line_dash='dash', line_color='red', annotation_text='Good ≥ 1.0')
    fig.add_hline(y=0.0, line_color='black', line_width=0.8)
    fig.update_layout(title='Sharpe & Sortino Ratios', barmode='group',
                      height=380, yaxis_title='Ratio', xaxis_tickangle=-20,
                      legend=dict(orientation='h', y=1.08, xanchor='right', x=1), **BASE)
    st.plotly_chart(fig, use_container_width=True)

    alpha_vals = [ALPHAS[FUNDS.index(f)] for f in sorted_funds]
    fig2 = go.Figure(go.Bar(
        y=sorted_funds, x=alpha_vals, orientation='h',
        marker_color=['rgba(30,132,73,0.85)' if v>=0 else 'rgba(192,57,43,0.85)' for v in alpha_vals],
        text=[f'+{v:.1f}%' if v>=0 else f'{v:.1f}%' for v in alpha_vals],
        textposition='outside'))
    fig2.add_vline(x=0, line_color='black', line_width=1)
    fig2.update_layout(title="Jensen's Alpha — Excess Return over CAPM",
                       xaxis_title='Alpha (%)', height=340,
                       margin=dict(l=10,r=70,t=40,b=20),
                       plot_bgcolor='white', paper_bgcolor='white',
                       font=dict(family='Segoe UI,Arial', size=12))
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════ TAB 5 — BENCHMARK ══════════════════
with tabs[4]:
    st.markdown('<div class="stitle">Benchmark Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">vs Nifty 50 · vs Bank FD · vs NSC · vs Gold (IBJA) · vs RBI Rate · vs CPI Inflation</div>', unsafe_allow_html=True)

    bcols = st.columns(6)
    bcard(bcols[0],"📉","Nifty 50 CAGR","14.5%","#1F4E79","Source: NSE India")
    bcard(bcols[1],"🏧","Bank FD Rate","6.8%","#5b6abf","Avg. 5-Year FD")
    bcard(bcols[2],"📬","NSC Rate","7.7%","#1E8449","Source: India Post")
    bcard(bcols[3],"🥇","Gold (IBJA)","19.5%","#D4A017","Source: ibja.co")
    bcard(bcols[4],"🏛","RBI Risk-Free","6.5%","#2E75B6","Source: rbi.org.in")
    bcard(bcols[5],"📊","CPI Inflation","5.5%","#C0392B","RBI / MOSPI")

    st.markdown("")
    all_lbls = ['Nifty 50','Bank FD','NSC','Gold (IBJA)','RBI Rf','CPI Inflation']+FUNDS
    all_vals = [14.5,6.8,7.7,19.5,6.5,5.5]+CAGRS
    all_clrs = (['rgba(100,100,180,0.75)']*6 +
                ['rgba(30,132,73,0.85)' if v>=14.5 else 'rgba(192,57,43,0.8)' for v in CAGRS])

    fig = go.Figure(go.Bar(
        y=all_lbls, x=all_vals, orientation='h', marker_color=all_clrs,
        text=[f'{v:.2f}%' for v in all_vals], textposition='outside'))
    fig.add_vline(x=14.5, line_dash='dash', line_color='red',
                  annotation_text='Nifty 50', annotation_position='top right')
    fig.update_layout(title='CAGR vs All Benchmarks', xaxis_title='CAGR (%)',
                      height=500, margin=dict(l=10,r=70,t=40,b=20),
                      plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(family='Segoe UI,Arial', size=12))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(pd.DataFrame({
        'Fund / Instrument': FUNDS+['Nifty 50 Index','Gold (IBJA)','NSC India Post','Bank FD'],
        'CAGR': [f'{v:.2f}%' for v in CAGRS]+['14.50%','19.50%','7.70%','6.80%'],
        'vs Nifty 50 (14.5%)': [f'+{v-14.5:.1f}% ✅' if v>=14.5 else f'{v-14.5:.1f}% ❌' for v in CAGRS]+['—','+5.0% ✅','−6.8% ❌','−7.7% ❌'],
        'vs Bank FD (6.8%)':   [f'+{v-6.8:.1f}%' for v in CAGRS]+['+7.7%','+12.7%','+0.9%','—'],
        'vs CPI (5.5%)':       [f'+{v-5.5:.1f}%' for v in CAGRS]+['+9.0%','+14.0%','+2.2%','+1.3%'],
        'Beat Market?':        ['✅ Yes' if v>=14.5 else '❌ No' for v in CAGRS]+['Benchmark','✅ Yes','Fixed','Fixed'],
    }), use_container_width=True, hide_index=True)

# ══════════════════ TAB 6 — SIP ══════════════════
with tabs[5]:
    st.markdown('<div class="stitle">SIP Analysis — Wealth Creation</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">₹5,000/month SIP | Power of Compounding across 5, 10, 15 Years</div>', unsafe_allow_html=True)

    kcols = st.columns(5)
    kcard(kcols[0],"Total Invested (5Y)","₹3.0L","₹5,000 × 60 months","")
    kcard(kcols[1],"Value @ 25.17%","₹5.11L","Bandhan Small Cap","green")
    kcard(kcols[2],"Value @ 19.67%","₹4.48L","HDFC Balanced Adv","")
    kcard(kcols[3],"Value @ 7.7% NSC","₹3.61L","India Post NSC","")
    kcard(kcols[4],"Value @ 6.8% FD","₹3.53L","Bank Fixed Deposit","red")

    horizon = st.radio("Investment Horizon:", ["5 Years","10 Years","15 Years"], horizontal=True)
    hm = {"5 Years":60,"10 Years":120,"15 Years":180}[horizon]
    invested = 5000 * hm

    sip_entries = [
        ('Bandhan Small Cap (25.17%)',25.17),('HDFC Flexi Cap (23.37%)',23.37),
        ('Kotak Midcap (21.94%)',21.94),('Nippon Gold ETF (20.95%)',20.95),
        ('HDFC Balanced (19.67%)',19.67),('ICICI ELSS (16.75%)',16.75),
        ('Nifty 50 (14.5%)',14.5),('Mirae Large Cap (13.93%)',13.93),
        ('Gold/IBJA (19.5%)',19.5),('NSC India Post (7.7%)',7.7),
        ('Bank FD (6.8%)',6.8),('RBI Risk-Free (6.5%)',6.5),
        ('HDFC Money Mkt (6.10%)',6.1),
    ]
    sip_vals   = sorted([(lbl, sip_fv(r,hm)/1e5) for lbl,r in sip_entries], key=lambda x:x[1])
    s_labels   = [x[0] for x in sip_vals]
    s_vals_num = [x[1] for x in sip_vals]
    s_colors   = ['rgba(127,140,141,0.8)' if any(k in l for k in ['NSC','FD','RBI','Money'])
                  else 'rgba(30,132,73,0.85)' if v*1e5>invested else 'rgba(192,57,43,0.8)'
                  for l,v in sip_vals]

    fig = go.Figure(go.Bar(
        y=s_labels, x=s_vals_num, orientation='h', marker_color=s_colors,
        text=[f'₹{v:.2f}L' for v in s_vals_num], textposition='outside'))
    fig.add_vline(x=invested/1e5, line_dash='dash', line_color='gray',
                  annotation_text=f'Invested ₹{invested/1e5:.1f}L')
    fig.update_layout(title=f'₹5,000/month SIP Future Value ({horizon})',
                      xaxis_title='Future Value (₹ Lakhs)', height=500,
                      margin=dict(l=10,r=90,t=40,b=20),
                      plot_bgcolor='white', paper_bgcolor='white',
                      font=dict(family='Segoe UI,Arial', size=12))
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(pd.DataFrame({
        'Fund / Rate': [e[0] for e in sip_entries],
        f'FV 5Y':  [f'₹{sip_fv(r,60)/1e5:.2f}L'  for _,r in sip_entries],
        f'FV 10Y': [f'₹{sip_fv(r,120)/1e5:.2f}L' for _,r in sip_entries],
        f'FV 15Y': [f'₹{sip_fv(r,180)/1e5:.2f}L' for _,r in sip_entries],
    }), use_container_width=True, hide_index=True)

# ══════════════════ TAB 7 — CORRELATION ══════════════════
with tabs[6]:
    st.markdown('<div class="stitle">Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Pearson Correlation Matrix — 1 = move together | −1 = move opposite | 0 = unrelated</div>', unsafe_allow_html=True)

    kcols = st.columns(4)
    kcard(kcols[0],"Highest Correlation","0.87","HDFC Balanced ↔ HDFC Flexi Cap","red")
    kcard(kcols[1],"Best Diversifier","−0.38","Nippon Gold ↔ Kotak Midcap","green")
    kcard(kcols[2],"Gold vs Equity","−0.24 to −0.38","Natural portfolio hedge","")
    kcard(kcols[3],"Debt Correlation","~0.00","HDFC Money Market — stable anchor","")

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
                      plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(pd.DataFrame({
        'Finding': ['Highest Equity Correlation','Gold as Portfolio Hedge',
                    'Debt Uncorrelated','Mid + Small Cap Pair','Best Diversified Pair'],
        'Fund Pair': ['HDFC Balanced ↔ HDFC Flexi Cap','Nippon Gold ↔ All Equity Funds',
                      'HDFC Money Market ↔ All Funds','Kotak Midcap ↔ Bandhan SC',
                      'HDFC Flexi Cap + Nippon Gold ETF'],
        'Correlation': ['0.87','−0.24 to −0.38','~0.00','0.81','−0.31'],
        'Interpretation': [
            'Very similar movement — limited diversification within equity category',
            'Moves opposite to equity — excellent inflation & crisis hedge',
            'Near-zero correlation — stable capital anchor for any portfolio',
            'Both growth-oriented — high co-movement in bull & bear markets',
            'Highest return fund + best natural hedge = optimal core pair',
        ],
    }), use_container_width=True, hide_index=True)

# ══════════════════ TAB 8 — SCORECARD ══════════════════
with tabs[7]:
    st.markdown('<div class="stitle">Overall Fund Scorecard</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Weighted Score: CAGR 25 + Sharpe 25 + Sortino 20 + Low Drawdown 15 + Low Volatility 15 = 100</div>', unsafe_allow_html=True)

    sc_data = [
        ('🥇 #1','HDFC Flexi Cap',     88,23.37,1.30,-11.06,'Moderate Investors',  '★★★★★'),
        ('🥈 #2','Bandhan Small Cap',  82,25.17,1.05,-21.68,'Aggressive Investors','★★★★☆'),
        ('🥉 #3','HDFC Balanced Adv',  79,19.67,1.26, -9.15,'Conservative',        '★★★★☆'),
        ('#4',   'Nippon Gold ETF',    72,20.95,1.10,-10.20,'Portfolio Hedge',      '★★★☆☆'),
        ('#5',   'Kotak Midcap',       70,21.94,1.03,-20.37,'Aggressive Investors','★★★☆☆'),
        ('#6',   'ICICI ELSS',         64,16.75,0.81,-16.33,'Tax Saving (80C)',     '★★☆☆☆'),
        ('#7',   'Mirae Large Cap',    58,13.93,0.63,-14.97,'Low-risk Equity',      '★★☆☆☆'),
        ('#8',   'HDFC Money Market',  20, 6.10,-0.73,  0.0,'Capital Preservation','★☆☆☆☆'),
    ]
    sc_df = pd.DataFrame(sc_data, columns=['Rank','Fund','Score /100','CAGR','Sharpe','Max DD','Best For','Rating'])
    sc_df['CAGR']   = sc_df['CAGR'].apply(lambda x:f'{x:.2f}%')
    sc_df['Sharpe'] = sc_df['Sharpe'].apply(lambda x:f'{x:.2f}')
    sc_df['Max DD'] = sc_df['Max DD'].apply(lambda x:f'{x:.2f}%')
    st.dataframe(sc_df, use_container_width=True, hide_index=True)

    sc_funds  = [d[1] for d in sc_data]
    sc_scores = [d[2] for d in sc_data]
    sc_clrs   = ['#1E8449','#2E75B6','#2E75B6','#D4A017','#8E44AD','#f39c12','#95a5a6','#C0392B']
    fig = go.Figure(go.Bar(x=sc_funds, y=sc_scores, marker_color=sc_clrs,
                           text=sc_scores, textposition='outside'))
    fig.add_hline(y=75, line_dash='dash', line_color='#1E8449', annotation_text='Excellent ≥ 75')
    fig.add_hline(y=60, line_dash='dot',  line_color='#E67E22', annotation_text='Good ≥ 60')
    fig.update_layout(title='Overall Score /100', yaxis_title='Score',
                      yaxis_range=[0,105], height=360, xaxis_tickangle=-20, **BASE)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 👤 Investor Profile Recommendations")
    p1,p2,p3,p4 = st.columns(4)
    for col, cls, title, items in [
        (p1,'cons','🟢 Conservative','HDFC Balanced Advantage — Max DD −9.15%|HDFC Money Market — Capital safe|NSC / Bank FD — Fixed return guarantee|Nippon Gold ETF — Inflation hedge'),
        (p2,'modr','🔵 Moderate',    'HDFC Flexi Cap — Best Sharpe 1.30|ICICI ELSS — Tax benefit + growth|Nippon Gold ETF — Portfolio diversifier|Kotak Midcap — Medium-high growth'),
        (p3,'aggr','🔴 Aggressive',  'Bandhan Small Cap — Highest CAGR 25.17%|Kotak Midcap — Strong mid-cap growth|HDFC Flexi Cap — High return + managed risk|Long horizon (5+ years) required'),
        (p4,'taxs','🟡 Tax Saver',   'ICICI ELSS — 80C deduction ₹1.5L/yr|Only 3-year lock-in period|CAGR 16.75% — beats FD & NSC|Best tax-saving + wealth creation combo'),
    ]:
        li = ''.join(f'<li>{i}</li>' for i in items.split('|'))
        col.markdown(f'<div class="pbox {cls}"><h3>{title}</h3><ul>{li}</ul></div>',
                     unsafe_allow_html=True)

# ══════════════════ TAB 9 — NAV DATA (REAL) ══════════════════
with tabs[8]:
    st.markdown('<div class="stitle">📂 NAV Data — Real Daily Data from AMFI India</div>', unsafe_allow_html=True)
    st.markdown('<div class="ssub">Actual NAV values from Excel files | Jan 2021 – Dec 2025 | Source: AMFI / MFAPI.in</div>', unsafe_allow_html=True)

    # Controls row
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([3,1,1,2])
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
    with ctrl4:
        chart_mode = st.radio("View:", ["Indexed to 100","Actual NAV","% Return"],
                              horizontal=True, key='nav_cm')

    # Define y_title before the loop so it's always available
    if chart_mode == "Indexed to 100":
        y_title = 'Indexed NAV (Base = 100)'
    elif chart_mode == "Actual NAV":
        y_title = 'NAV (₹)'
    else:
        y_title = 'Return (%)'

    if not sel_funds:
        st.warning("Select at least one fund above.")
    else:
        fig_n = go.Figure()
        summary_rows = []

        for fund in sel_funds:
            df = nav_raw.get(fund)
            if df is None:
                continue
            mask = (df['Date'] >= pd.Timestamp(d_start)) & (df['Date'] <= pd.Timestamp(d_end))
            dff = df[mask].copy().reset_index(drop=True)
            if dff.empty:
                continue

            color  = COLORS[FUNDS.index(fund)]
            first  = dff['NAV'].iloc[0]
            last   = dff['NAV'].iloc[-1]
            ret_p  = (last/first - 1)*100
            max_n  = dff['NAV'].max()
            min_n  = dff['NAV'].min()
            days_  = (dff['Date'].iloc[-1] - dff['Date'].iloc[0]).days
            cagr_r = ((last/first)**(365/max(days_,1)) - 1)*100 if days_ > 0 else 0

            summary_rows.append({
                'Fund': fund,
                'From':       dff['Date'].iloc[0].strftime('%d-%b-%Y'),
                'To':         dff['Date'].iloc[-1].strftime('%d-%b-%Y'),
                'Start NAV':  f'₹{first:,.4f}',
                'End NAV':    f'₹{last:,.4f}',
                'Max NAV':    f'₹{max_n:,.4f}',
                'Min NAV':    f'₹{min_n:,.4f}',
                'Total Return': f'+{ret_p:.2f}%' if ret_p>=0 else f'{ret_p:.2f}%',
                'CAGR (period)': f'{cagr_r:.2f}%',
                'Data Points': f'{len(dff):,}',
            })

            if chart_mode == "Indexed to 100":
                y = dff['NAV'] / first * 100
            elif chart_mode == "Actual NAV":
                y = dff['NAV']
            else:
                y = (dff['NAV'] / first - 1) * 100

            fig_n.add_trace(go.Scatter(
                x=dff['Date'], y=y, name=fund,
                line=dict(color=color, width=1.8), mode='lines',
                hovertemplate=f'<b>{fund}</b><br>%{{x|%d %b %Y}}<br>{chart_mode}: %{{y:.4f}}<extra></extra>'
            ))

        if chart_mode == "Indexed to 100":
            fig_n.add_hline(y=100, line_dash='dash', line_color='gray',
                            opacity=0.5, annotation_text='Base = 100')
        elif chart_mode == "% Return":
            fig_n.add_hline(y=0, line_dash='dash', line_color='gray', opacity=0.5)

        fig_n.update_layout(
            title=f'NAV — {chart_mode} | {d_start.strftime("%d %b %Y")} to {d_end.strftime("%d %b %Y")}',
            xaxis_title='Date', yaxis_title=y_title,
            height=460, hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=50,b=20),
            font=dict(family='Segoe UI,Arial', size=12)
        )
        st.plotly_chart(fig_n, use_container_width=True)

        # Summary metrics
        if summary_rows:
            st.markdown("**📊 Summary for Selected Period**")
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        # Raw NAV table with daily return
        st.markdown("---")
        st.markdown("**📄 Daily NAV Table**")
        fund_view = st.selectbox("Fund to view daily data:", sel_funds, key='nav_fv')
        df_v = nav_raw.get(fund_view)
        if df_v is not None:
            mask2 = (df_v['Date']>=pd.Timestamp(d_start)) & (df_v['Date']<=pd.Timestamp(d_end))
            df_show = df_v[mask2].copy().reset_index(drop=True)
            df_show['Daily Return (%)'] = df_show['NAV'].pct_change().mul(100).round(3)
            df_show['Daily Return (%)'] = df_show['Daily Return (%)'].apply(
                lambda x: f'+{x:.3f}%' if x>0 else (f'{x:.3f}%' if pd.notna(x) and x<0 else '—'))
            df_show['Date']   = df_show['Date'].dt.strftime('%d-%b-%Y')
            df_show['NAV']    = df_show['NAV'].apply(lambda x: f'₹{x:,.4f}')
            df_show.rename(columns={'NAV':'NAV (₹)'}, inplace=True)
            df_show = df_show[['Date','NAV (₹)','Daily Return (%)']]

            col_tbl, col_stat = st.columns([3,1])
            with col_tbl:
                st.dataframe(df_show, use_container_width=True, hide_index=True, height=420)
                st.caption(f"{len(df_show):,} trading days | {fund_view}")

            with col_stat:
                raw_nav = nav_raw[fund_view]
                mask3 = (raw_nav['Date']>=pd.Timestamp(d_start)) & (raw_nav['Date']<=pd.Timestamp(d_end))
                nav_arr = raw_nav[mask3]['NAV'].values
                if len(nav_arr) > 1:
                    daily_rets = pd.Series(nav_arr).pct_change().dropna()
                    st.markdown("**📈 Quick Stats**")
                    st.metric("Total Return", f"+{(nav_arr[-1]/nav_arr[0]-1)*100:.2f}%")
                    st.metric("Avg Daily Return", f"{daily_rets.mean()*100:.3f}%")
                    st.metric("Daily Std Dev",    f"{daily_rets.std()*100:.3f}%")
                    st.metric("Best Day",  f"+{daily_rets.max()*100:.2f}%")
                    st.metric("Worst Day", f"{daily_rets.min()*100:.2f}%")
                    pos_days = (daily_rets > 0).sum()
                    st.metric("Positive Days", f"{pos_days} / {len(daily_rets)}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>📊 <b>Financial Modelling of Mutual Fund Returns</b> | "
    "Salesqueen Software Solutions, Chennai | MBA Project 2025–2026 | "
    "Data: AMFI India · NSE India · RBI · IBJA · India Post</small></center>",
    unsafe_allow_html=True
)
