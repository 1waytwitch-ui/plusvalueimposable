import streamlit as st

# --------- CONFIGURATION GÉNÉRALE ----------
st.set_page_config(
    page_title="Calcul Plus-Value Crypto",
    page_icon="📈",
    layout="centered"
)

# --------- STYLE CSS ---------
st.markdown("""
    <style>
        body {
            background-color: #0d0d1a;
            color: #ffffff;
        }
        .main {
            background-color: #1a1a2e;
            padding: 20px;
            border-radius: 10px;
        }
        .stNumberInput input {
            background-color: #2e2e4d;
            color: white;
        }
        .stSlider > div > div {
            background-color: #2e2e4d;
        }
        h1, h2, h3 {
            color: #a29bfe;
        }
    </style>
""", unsafe_allow_html=True)

# --------- HEADER ----------
st.markdown("## 🪙 Calculateur de Plus-Value Crypto / DeFi")
st.markdown("**Estime ta plus-value imposable et ton impôt sur les plus-values en crypto.**")

st.divider()

# --------- FORMULE EXPLICATIVE ----------
with st.expander("📘 Voir la formule de calcul utilisée"):
    st.markdown("""
    **Formule utilisée pour le calcul de la plus-value imposable :**
    
    $$
    \text{Plus-value} = \text{Prix de vente} - \left[ \text{Prix total d'acquisition} \times \left( \frac{\text{Prix de vente}}{\text{Valeur totale du portefeuille avant la vente}} \right) \right]
    $$

    Cette formule prend en compte la **proportion de la vente** par rapport à la **valeur totale du portefeuille** avant la vente.
    """, unsafe_allow_html=True)

# --------- INPUTS ----------
st.subheader("🔢 Paramètres d'entrée")

col1, col2 = st.columns(2)
with col1:
    prix_vente = st.number_input("💰 Prix de vente (€)", min_value=0.0, step=100.0, format="%.2f")
    prix_acquisition_total = st.number_input("📦 Prix total d'acquisition (€)", min_value=0.0, step=100.0, format="%.2f")
with col2:
    valeur_portefeuille = st.number_input("📊 Valeur totale du portefeuille avant vente (€)", min_value=0.01, step=100.0, format="%.2f")
    taux_flat_tax = st.slider("🧾 Taux de flat tax (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.1)

# --------- CALCULS ----------
if valeur_portefeuille > 0:
    cout_acquisition_proportionnel = prix_acquisition_total * (prix_vente / valeur_portefeuille)
    plus_value = prix_vente - cout_acquisition_proportionnel
    impot = plus_value * (taux_flat_tax / 100)

    # --------- RÉSULTATS ---------
    st.divider()
    st.subheader("📄 Résultats")

    st.write(f"**🧮 Coût d'acquisition proportionnel :** `{cout_acquisition_proportionnel:.2f} €`")
    st.write(f"**📈 Plus-value imposable :** `{plus_value:.2f} €`")

    if plus_value > 0:
        st.write(f"**💸 Impôt estimé ({taux_flat_tax:.1f}%) :** `{impot:.2f} €`")
    else:
        st.write("✅ Aucune plus-value imposable (ou une moins-value).")

# --------- FOOTER ----------
st.divider()
st.markdown("""
> ⚠️ **Disclaimer :** Ce calculateur est fourni à titre indicatif et ne remplace pas un avis fiscal professionnel.  
> Les règles fiscales peuvent varier selon le pays, la situation et le régime en vigueur.

👨‍💻 App crypto-friendly par un passionné du Web3.
""")
