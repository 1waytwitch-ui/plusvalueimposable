import streamlit as st

# --------- CONFIGURATION DE LA PAGE ----------
st.set_page_config(
    page_title="Calcul Plus-Value Crypto",
    page_icon="📈",
    layout="centered"
)

# --------- STYLE PERSONNALISÉ ----------
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
        .st-emotion-cache-1avcm0n {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --------- TITRE & DESCRIPTION ----------
st.markdown("## 🪙 Calculateur de Plus-Value Crypto / DeFi")
st.markdown("**Estime ta plus-value imposable et ton impôt sur les plus-values en crypto.**")

st.divider()

# --------- FORMULE EXPLICATIVE ----------
with st.expander("📘 Voir la formule de calcul utilisée"):
    st.markdown("""
    **🧮 Formule utilisée pour le calcul de la plus-value imposable :**

    _La plus-value imposable est calculée en proportion de la valeur totale du portefeuille._

    ### 🧾 Formule expliquée :

    > **Plus-value imposable** = Prix de vente − (Prix total d'acquisition × (Prix de vente ÷ Valeur totale du portefeuille avant la vente))

    ### 🧮 Formule mathématique :

    $$
    \text{Plus-value} = \text{Prix de vente} - \left( \text{Prix d'acquisition total} \times \frac{\text{Prix de vente}}{\text{Valeur totale du portefeuille}} \right)
    $$
    """, unsafe_allow_html=True)

# --------- SAISIE DES DONNÉES UTILISATEUR ----------
st.subheader("🔢 Paramètres d'entrée")

col1, col2 = st.columns(2)
with col1:
    prix_vente = st.number_input("💰 Prix de vente (€)", min_value=0.0, step=100.0, format="%.2f")
    prix_acquisition_total = st.number_input("📦 Prix total d'acquisition (€)", min_value=0.0, step=100.0, format="%.2f")
with col2:
    valeur_portefeuille = st.number_input("📊 Valeur totale du portefeuille avant vente (€)", min_value=0.01, step=100.0, format="%.2f")
    taux_flat_tax = st.slider("🧾 Taux de flat tax (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.1)

# --------- CALCUL ---------
if valeur_portefeuille > 0 and prix_vente > 0:
    # Calcul du coût d’acquisition proportionnel
    cout_acquisition_proportionnel = prix_acquisition_total * (prix_vente / valeur_portefeuille)
    plus_value = prix_vente - cout_acquisition_proportionnel
    impot = plus_value * (taux_flat_tax / 100)

    # --------- AFFICHAGE DES RÉSULTATS ---------
    st.divider()
    st.subheader("📄 Résultats")

    st.write(f"**🧮 Coût d'acquisition proportionnel :** `{cout_acquisition_proportionnel:.2f} €`")
    st.write(f"**📈 Plus-value imposable :** `{plus_value:.2f} €`")

    if plus_value > 0:
        st.write(f"**💸 Impôt estimé ({taux_flat_tax:.1f}%) :** `{impot:.2f} €`")
    else:
        st.write("✅ Aucune plus-value imposable (ou moins-value).")

# --------- FOOTER ---------
st.divider()
st.markdown("""
> ⚠️ **Disclaimer :** Ce calculateur est fourni à titre informatif uniquement.  
> Il ne constitue pas un conseil fiscal. Consulte un professionnel pour une déclaration officielle.

👨‍💻 Outil crypto-friendly développé pour la communauté Web3.
""")
