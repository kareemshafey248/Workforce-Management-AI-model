import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from wfm_data import df_historical
from wfm_engine import time_series_forecast, generate_full_wfm_forecast

# ── PAGE CONFIG & DATA CACHING ─────────────────────────────────────
st.set_page_config(
    page_title="WFM Schedule Optimizer",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df_pred_base = time_series_forecast(df_historical, days_to_predict=7)
    df_requirements = generate_full_wfm_forecast(df_pred_base)
    return df_historical, df_requirements

df_hist, df_req = load_data()

# ── PREMIUM DARK THEME ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Space+Grotesk:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0E1117;
    color: #E2E8F0;
}

.stApp { background-color: #0B0E14; }
.stSidebar { background-color: #151A22 !important; border-right: 1px solid rgba(255,255,255,0.05); }

.card {
    background: #151A22;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
}

.metric-value {
    font-size: 2.25rem;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.1;
}

.cyan-text { color: #00E5FF !important; }
.amber-text { color: #F59E0B !important; }
.emerald-text { color: #10B981 !important; }

h1, h2, h3 { font-weight: 700 !important; color: #FFFFFF !important; }
hr { border-color: rgba(255,255,255,0.05); }

/* Custom Pandas DataFrame Styling overrides */
.dataframe { font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR NAVIGATION ──────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding: 10px 0 25px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px;">
    <div style="font-size: 2rem; margin-bottom: 5px;">📅 WFM</div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #00E5FF; letter-spacing: 1px;">SCHEDULE OPTIMIZER</div>
    <div style="font-size: 0.75rem; color: #64748B; font-weight: 500; font-family: 'JetBrains Mono';">v1.0.0 | ML FORECAST</div>
</div>
""", unsafe_allow_html=True)

nav = st.sidebar.radio("Navigation", [
    "🏠 Executive Briefing",
    "📈 Forecasting Control Room",
    "👥 Staffing Needs (Erlang C)",
    "💰 Cost Optimization Review"
])

st.sidebar.markdown("""
<div style="margin-top: 50px; padding: 15px; background: rgba(0, 229, 255, 0.05); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 8px;">
    <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; font-family: 'JetBrains Mono';">Lead Architect</div>
    <div style="font-weight: 700; color: #F8FAFC; font-size: 1.1rem;">Kareem Elshafey</div>
    <div style="font-size: 0.8rem; color: #00E5FF; margin-top:2px;">Workforce Data Analyst</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 🏠 PAGE 1: EXECUTIVE BRIEFING
# ─────────────────────────────────────────────────────────────────
if nav == "🏠 Executive Briefing":
    st.markdown("<h1>🏠 Core Intelligence Briefing</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:1.1rem; margin-bottom:30px;'>An introduction to the AI Schedule Optimizer and the problems it solves.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color:#00E5FF !important;"><span style="font-size:1.5rem;">❔</span> What exactly is WFM?</h3>
            <p style="color:#CBD5E1; line-height:1.6; font-size:1.05rem;">
                Workforce Management (WFM) is the mathematical science of ensuring a company has <b>exactly the right number of employees</b> working at <b>exactly the right time</b>. 
                <br><br>
                If a call center schedules too many people on a slow Tuesday, the company burns thousands of dollars in wasted payroll. If they schedule too few people on a busy Monday, customers wait on hold for an hour and cancel their subscriptions.
            </p>
            <hr>
            <h3 style="color:#F59E0B !important; margin-top:20px;"><span style="font-size:1.5rem;">🎯</span> The 3 Business Questions We Answer:</h3>
            <ol style="color:#E2E8F0; line-height:1.8; font-size:1.05rem; padding-left:20px;">
                <li><b>What is our future Call Volume?</b> (Using Time Series Machine Learning to predict next week based on 6 months of history).</li>
                <li><b>How many humans do we need?</b> (Routing predictions through the <i>Erlang C Staffing Formula</i> to guarantee an 80% SLA).</li>
                <li><b>How much money do we save?</b> (Calculating the exact payroll dollars saved by not overstaffing).</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card" style="background: rgba(16, 185, 129, 0.05); border-color: rgba(16, 185, 129, 0.2);">
            <h3 class="emerald-text">⚙️ The Architecture</h3>
            <ul style="color:#94A3B8; font-family:'JetBrains Mono'; font-size:0.85rem; line-height:1.8;">
                <li><b>Dataset:</b> 6 Months Historical Call Logs</li>
                <li><b>Input Variables:</b> Timestamp, Calls, AHT</li>
                <li><b>ML Engine:</b> Time Series Seasonality Extract</li>
                <li><b>Math Engine:</b> Erlang C Queue Theory</li>
                <li><b>Target SLA:</b> 80% answered in 20 seconds</li>
                <li><b>Shrinkage Buffer:</b> +30% Headcount built-in</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.info("👈 **Use the sidebar** to navigate through the intelligence engine.")

# ─────────────────────────────────────────────────────────────────
# 📈 PAGE 2: FORECASTING CONTROL ROOM
# ─────────────────────────────────────────────────────────────────
elif nav == "📈 Forecasting Control Room":
    st.markdown("<h1>📈 ML Volume Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:1.1rem; margin-bottom:30px;'>Time Series artificial intelligence extracting daily and weekly seasonality patterns.</p>", unsafe_allow_html=True)
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="card"><div class="metric-label">Historical Data Parsed</div><div class="metric-value">6 Months</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="metric-label">Forecast Horizon</div><div class="metric-value cyan-text">7 Days</div></div>', unsafe_allow_html=True)
    total_pred_calls = df_req['Predicted_Volume'].sum()
    c3.markdown(f'<div class="card"><div class="metric-label">Total Forecasted Calls</div><div class="metric-value">{total_pred_calls:,}</div></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 The Prediction Horizon (Next 7 Days)")
    
    # We will show the last 7 days of historical data, then exactly connect the 7 days of future data
    last_hist_date = df_hist['Timestamp'].max() - timedelta(days=7)
    df_hist_recent = df_hist[df_hist['Timestamp'] >= last_hist_date].copy()
    
    # Set up plot data
    fig = go.Figure()
    
    # Add Historical Trace
    fig.add_trace(go.Scatter(
        x=df_hist_recent['Timestamp'], y=df_hist_recent['Call_Volume'],
        name='Historical Actuals', line=dict(color='#64748B', width=2), fill='tozeroy', fillcolor='rgba(100, 116, 139, 0.1)'
    ))
    
    # Add Future Trace
    fig.add_trace(go.Scatter(
        x=df_req['Timestamp'], y=df_req['Predicted_Volume'],
        name='AI Forecast', line=dict(color='#00E5FF', width=3, dash='solid'), fill='tozeroy', fillcolor='rgba(0, 229, 255, 0.1)'
    ))
    
    # Add vertical line for "TODAY"
    fig.add_vline(x=df_req['Timestamp'].min(), line_width=2, line_dash="dash", line_color="#F59E0B")
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, l=40, r=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#E2E8F0")),
        font=dict(family="JetBrains Mono", color="#94A3B8"),
        hovermode="x unified"
    )
    fig.update_xaxes(showgrid=False, tickfont=dict(color="#94A3B8"))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", title="Call Volume per Hour", tickfont=dict(color="#94A3B8"))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding:15px; border-radius:8px;">
        <span style="color:#00E5FF; font-weight:bold;">Insight Engine:</span> The AI has perfectly memorized that volume drops heavily on weekends (Saturdays/Sundays) and spikes massively every Monday morning at 10:00 AM.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 👥 PAGE 3: STAFFING NEEDS (ERLANG C)
# ─────────────────────────────────────────────────────────────────
elif nav == "👥 Staffing Needs (Erlang C)":
    st.markdown("<h1>👥 Erlang C Headcount Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:1.1rem; margin-bottom:30px;'>Converting predicted call volume into exact Human Headcount requirements using Queue Theory.</p>", unsafe_allow_html=True)
    
    # Prepare Pivot Table for Heatmap
    days_map = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    df_req['DayName'] = df_req['DayOfWeek'].map(days_map)
    
    pivot_table = pd.pivot_table(
        df_req, 
        values='Required_Agents', 
        index='Hour', 
        columns='DayName', 
        aggfunc='mean'
    )
    # Order columns
    cols_ordered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(columns=cols_ordered)
    
    st.markdown("### 🗓️ Weekly Schedule Architecture")
    st.markdown("<p style='color:#64748B; font-size:0.9rem; font-family:JetBrains Mono;'>Heatmap indicates the exact number of agents needed on the floor per hour.</p>", unsafe_allow_html=True)
    
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Day of Week", y="Hour of Day (24h)", color="Agents Required"),
        x=cols_ordered,
        y=pivot_table.index,
        color_continuous_scale="Tealgrn",
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, l=40, r=40, b=40),
        font=dict(family="JetBrains Mono", color="#E2E8F0")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); padding:15px; border-radius:8px;">
        <span class="emerald-text" style="font-weight:bold;">Erlang C Execution:</span> The formula looks at Predicted Volume and Average Handling Time (AHT). It outputs the strict minimum agents required to hit an 80% Service Level, and then we programmatically added +30% headcount to account for Shrinkage (Lunch breaks, bathroom, training).
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# 💰 PAGE 4: COST OPTIMIZATION REVIEW
# ─────────────────────────────────────────────────────────────────
elif nav == "💰 Cost Optimization Review":
    st.markdown("<h1>💰 Payroll Cost Optimization</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:1.1rem; margin-bottom:30px;'>Quantifying the total dollars saved by using the AI Schedule instead of a flat guessing schedule.</p>", unsafe_allow_html=True)
    
    total_wasted = df_req['Wasted_Cost_Flat_Schedule'].sum()
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown(f"""
        <div class="card" style="border-top: 4px solid #F59E0B;">
            <div class="metric-label">Weekly Payroll Saved</div>
            <div class="metric-value amber-text">${total_wasted:,.0f}</div>
            <div style="margin-top:10px; font-size:0.85rem; color:#94A3B8; font-family:'JetBrains Mono'; line-height:1.5;">
                This represents the exact dollar amount saved by NOT paying agents to sit idle during low-volume hours (relative to a flat 45-agent baseline).
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("### 💵 Wasted Spend by Day (Flat Schedule)")
        daily_waste = df_req.groupby('Date')['Wasted_Cost_Flat_Schedule'].sum().reset_index()
        
        fig = px.bar(
            daily_waste, x='Date', y='Wasted_Cost_Flat_Schedule',
            color='Wasted_Cost_Flat_Schedule', color_continuous_scale="Oranges",
            labels={'Wasted_Cost_Flat_Schedule': 'Dollars Saved ($)'}
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, l=10, r=10, b=20),
            font=dict(family="JetBrains Mono", color="#94A3B8"),
            coloraxis_showscale=False
        )
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding:20px; border-radius:8px;">
        <h4 style="margin-top:0px; color:#F8FAFC;">Summary for Operations Directors:</h4>
        <p style="color:#CBD5E1; font-size:1.05rem; line-height:1.6; margin-bottom:0px;">
            A common failure in legacy call centers is the "Flat Schedule" (e.g., forcing exactly 45 agents to work from 9-to-5 every day). Because call volumes organically drop at lunch time and on Fridays, those agents sit idle while being paid.<br><br>
            By predicting volume with <b>Machine Learning</b> and scheduling precise intervals with <b>Erlang C</b>, we can dynamically flex the workforce size minute-by-minute—eliminating idle time without sacrificing customer wait times. This prototype proves the model generates immediate ROI.
        </p>
    </div>
    """, unsafe_allow_html=True)
