import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
from docx import Document

INPUT_CSV = "psx_data.csv"
W_TECH = 0.7
W_FUND = 0.3

st.set_page_config(page_title="PSX SmartAdvisor Pro", layout="wide")

# Dark theme CSS + centered heading
st.markdown("""
    <style>
    .main {background-color: #0E1117; color: white;}
    .stButton>button {background-color: #1f1f1f; color: white;}
    .css-1aumxhk {color: white;}
    .css-1d391kg {color: white;}
    .stTextInput>div>input {background-color: #1f1f1f; color:white;}
    .stNumberInput>div>input {background-color: #1f1f1f; color:white;}
    .centered-heading {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: ##FFFFFF;
        font-family: 'Arial', sans-serif;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Add the front page heading
st.markdown('<div class="centered-heading">STOCK MARKET ADVISOR</div>', unsafe_allow_html=True)

# --- Functions ---
def sma(series, window):
    return series.rolling(window=window, min_periods=1).mean()

def momentum(series, window=10):
    return series / series.shift(window) - 1

def compute_rsi(close, window=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=window, min_periods=1).mean()
    ma_down = down.rolling(window=window, min_periods=1).mean()
    rs = ma_up / (ma_down + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def technical_score(row):
    score = 0.0
    if row['Close'] > row['SMA_50']: score += 0.4
    if row['Close'] > row['SMA_200']: score += 0.3
    if row['Momentum_10'] > 0: score += 0.15
    if 30 < row['RSI'] < 70: score += 0.15
    return score

def fundamental_score(row):
    score = 0.0
    if 'PE' in row and not pd.isna(row['PE']):
        if row['PE'] < 10: score += 0.5
        elif row['PE'] < 20: score += 0.3
    if 'EPS' in row and not pd.isna(row['EPS']):
        if row['EPS'] > 0: score += 0.5
    return score

def action_from_score(s):
    if s >= 0.65: return "STRONG BUY"
    elif s >= 0.45: return "BUY"
    elif s >= 0.25: return "HOLD"
    else: return "SELL"

def generate_reason(row, action):
    reason = ""
    if action in ["STRONG BUY","BUY"]:
        reason += f"Stock price is above SMA50/SMA200 and momentum is positive. "
        reason += f"EPS={row.get('EPS',0)}, PE={row.get('PE',0)} indicates good fundamentals."
    else:
        reason += "Stock may be weak technically or fundamentals not very strong. "
    return reason

def generate_word_report(df_top, filename="PSX_SmartAdvisor_Summary.docx"):
    doc = Document()
    doc.add_heading('PSX SmartAdvisor - Summary', level=1)
    doc.add_paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    doc.add_heading('Top Recommendations', level=2)
    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Ticker'
    hdr_cells[1].text = 'Score'
    hdr_cells[2].text = 'Action'
    hdr_cells[3].text = 'Close'
    hdr_cells[4].text = 'Reason'
    for _, r in df_top.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(r['Ticker'])
        row_cells[1].text = f"{r['Score']:.3f}"
        row_cells[2].text = r['Action']
        row_cells[3].text = f"{r['Close']:.2f}"
        row_cells[4].text = r.get('Reason','')
    doc.save(filename)
    return filename

# Load data
try:
    df = pd.read_csv(INPUT_CSV, parse_dates=["Date"])
except FileNotFoundError:
    st.error(f"{INPUT_CSV} not found! Please place your CSV in this folder.")
    st.stop()

tickers = df['Ticker'].unique()

# Sidebar input
st.sidebar.header("Investment Details")
selected_ticker = st.sidebar.selectbox("Select Stock", tickers)
investment_amount = st.sidebar.number_input("Investment Amount (PKR)", min_value=1000, value=10000, step=1000)
get_recommendation = st.sidebar.button("Get Recommendation")

if get_recommendation:
    df_sorted = df.sort_values(['Ticker','Date']).copy()
    sub_data = df_sorted[df_sorted['Ticker']==selected_ticker].copy()
    sub_data['SMA_50'] = sma(sub_data['Close'],50)
    sub_data['SMA_200'] = sma(sub_data['Close'],200)
    sub_data['RSI'] = compute_rsi(sub_data['Close'],14)
    sub_data['Momentum_10'] = momentum(sub_data['Close'],10)
    latest = sub_data.iloc[-1]
    ts = technical_score(latest)
    fs = fundamental_score(latest)
    score = W_TECH*ts + W_FUND*fs
    action = action_from_score(score)
    reason = generate_reason(latest,action)

    # Display info
    st.header(f"{selected_ticker} - Recommendation")
    st.markdown(f"**Action:** {action}")
    st.markdown(f"**Score:** {score:.2f}")
    st.markdown(f"**Reason:** {reason}")
    st.markdown(f"**Investment Amount:** PKR {investment_amount}")

    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sub_data['Date'], y=sub_data['Close'], mode='lines', name='Close', line=dict(color='white')))
    fig.add_trace(go.Scatter(x=sub_data['Date'], y=sub_data['SMA_50'], mode='lines', name='SMA50', line=dict(color='yellow')))
    fig.add_trace(go.Scatter(x=sub_data['Date'], y=sub_data['SMA_200'], mode='lines', name='SMA200', line=dict(color='cyan')))
    fig.update_layout(title=f"{selected_ticker} Price & SMA", plot_bgcolor='black', paper_bgcolor='black', font=dict(color='white'),
                      xaxis=dict(showgrid=True,gridcolor='gray'), yaxis=dict(showgrid=True,gridcolor='gray'))
    st.plotly_chart(fig,use_container_width=True)

    # RSI chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=sub_data['Date'], y=sub_data['RSI'], mode='lines', name='RSI', line=dict(color='orange')))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
    fig_rsi.update_layout(title=f"{selected_ticker} RSI", plot_bgcolor='black', paper_bgcolor='black', font=dict(color='white'),
                          xaxis=dict(showgrid=True,gridcolor='gray'), yaxis=dict(showgrid=True,gridcolor='gray'))
    st.plotly_chart(fig_rsi,use_container_width=True)

    # Export
    df_export = pd.DataFrame([{'Ticker':selected_ticker,'Score':score,'Action':action,'Close':latest['Close'],'Reason':reason}])
    excel_filename = f"{selected_ticker}_Recommendation.xlsx"
    df_export.to_excel(excel_filename,index=False)
    st.download_button("Download Excel", excel_filename)
    word_filename = generate_word_report(df_export, f"{selected_ticker}_Summary.docx")
    st.download_button("Download Word", word_filename)
