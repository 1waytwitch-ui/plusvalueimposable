# streamlit_crypto_defi_app.py
# Application Streamlit: calcul de plus-value pour ventes partielles + dashboard style Crypto/DeFi
# Encodage: français

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Configuration de la page ---
st.set_page_config(page_title="Crypto & DeFi — Calcul Plus-value", page_icon="🪙", layout="wide")

# --- CSS style 'crypto/defi' ---
st.markdown(
    """
    <style>
    :root{
      --bg: linear-gradient(180deg,#0f172a 0%, #071032 100%);
      --card: rgba(255,255,255,0.03);
      --muted: #9aa6c0;
      --accent: #7c3aed;
      --accent-2: #06b6d4;
    }
    .stApp {
      background: var(--bg);
      color: #e6eef8;
      font-family: 'Inter', sans-serif;
    }
    .card {
      background: var(--card);
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 6px 18px rgba(2,6,23,0.6);
    }
    .muted { color: var(--muted); }
    .kpi { font-size:28px; font-weight:700; }
    .small { font-size:12px; color:var(--muted); }
    .accent { color: var(--accent); font-weight:700 }
    .accent-2 { color: var(--accent-2); font-weight:700 }
    .divider{ height:1px; background:rgba(255,255,255,0.04); margin:12px 0 }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
col1, col2 = st.columns([3,1])
with col1:
    st.markdown("""
    <div style='display:flex;gap:14px;align-items:center'>
      <div style='font-size:28px;font-weight:800'>Crypto & DeFi — Calculateur de plus-value</div>
      <div class='small muted'>Calculer la plus-value imposable pour des ventes partielles de portefeuille</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=60)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# --- Sidebar: paramètres d'entrée ---
st.sidebar.header("Paramètres de la vente")
PA = st.sidebar.number_input("Prix total d'acquisition (PA)", value=10000.0, min_value=0.0, step=100.0, format="%.2f")
V = st.sidebar.number_input("Valeur totale du portefeuille avant la vente (V)", value=25000.0, min_value=0.0, step=100.0, format="%.2f")
PV = st.sidebar.number_input("Montant vendu / Prix de vente (PV)", value=5000.0, min_value=0.0, step=50.0, format="%.2f")
rate = st.sidebar.slider("Taux d'imposition (%)", min_value=0.0, max_value=100.0, value=30.0)

st.sidebar.markdown("---")
show_history = st.sidebar.checkbox("Afficher évolution portefeuille (simulée)", True)

# --- Calculs ---
if V == 0:
    st.error("La valeur totale du portefeuille (V) doit être > 0")
    st.stop()

pv_ratio = 1.0 - (PA / V)
plus_value = PV * pv_ratio
impot = plus_value * (rate / 100.0) if plus_value > 0 else 0.0

# --- KPI cards ---
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='small muted'>Prix de vente</div>")
    st.markdown(f"<div class='kpi'>€ {PV:,.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with k2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='small muted'>Prix total d'acquisition</div>")
    st.markdown(f"<div class='kpi'>€ {PA:,.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with k3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='small muted'>Plus-value (imposable)</div>")
    st.markdown(f"<div class='kpi accent'>€ {plus_value:,.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with k4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='small muted'>Impôt estimé</div>")
    st.markdown(f"<div class='kpi accent-2'>€ {impot:,.2f}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# --- Explication et formule ---
with st.expander("Voir la formule et l'explication"):
    st.markdown("""
    **Formule utilisée** :

    $$\text{Plus-value} = \text{Prix de vente} \times \left(1 - \frac{\text{Prix total d'acquisition}}{\text{Valeur totale du portefeuille avant la vente}}\right)$$

    Cette formule répartit proportionnellement le coût d'acquisition sur la fraction du portefeuille vendue.
    """)

# --- Visualisations ---
colA, colB = st.columns([2,1])

with colA:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Détail de la vente & simulation")
    st.write("Répartition du montant vendu : coût imputé vs gain")

    cost_imputed = PA * (PV / V)
    df_pie = pd.DataFrame({
        'part': ['Coût imputé', 'Plus-value'],
        'value': [cost_imputed, max(plus_value, 0.0)]
    })
    fig_pie = px.pie(df_pie, names='part', values='value', hole=0.6,
                     title='Imputation du prix de vente')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.write("**Détails numériques**")
    st.write(pd.DataFrame({
        'Libellé': ['Montant vendu (PV)', 'Coût imputé', 'Plus-value', 'Taux portefeuille (1-PA/V)', 'Impôt estimé'],
        'Valeur': [f"€ {PV:,.2f}", f"€ {cost_imputed:,.2f}", f"€ {plus_value:,.2f}", f"{pv_ratio*100:.2f} %", f"€ {impot:,.2f}"]
    }))
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Allocation (exemple)")
    demo = pd.DataFrame({
        'asset': ['BTC', 'ETH', 'SOL', 'USDC'],
        'qty': [0.12, 1.8, 10, 2000],
        'price': [30000, 1800, 30, 1]
    })
    demo['value'] = demo['qty'] * demo['price']
    st.table(demo)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Evolution simulée du portefeuille ---
if show_history:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Évolution simulée du portefeuille")

    days = pd.date_range(end=pd.Timestamp.today(), periods=60)
    start_val = PA
    end_val = V
    vals = np.linspace(start_val, end_val, len(days))
    vals = vals * (1 + 0.02 * np.sin(np.linspace(0, 6.28, len(days))))
    df_hist = pd.DataFrame({'date': days, 'value': vals})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_hist['date'], y=df_hist['value'], mode='lines', name='Valeur portefeuille'))
    fig.add_vline(x=pd.Timestamp.today(), line_dash='dash', line_color='rgba(124,58,237,0.6)')
    fig.update_layout(yaxis_title='€', xaxis_title='Date', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.markdown("<div class='small muted'>⚠️ Ceci est une simulation à titre informatif — consultez un conseiller fiscal pour calculs officiels.</div>", unsafe_allow_html=True)
