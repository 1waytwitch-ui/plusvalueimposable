import streamlit as st

st.title("Calcul de la Plus-Value Imposable")

st.markdown("""
Utilise cette application pour calculer ta **plus-value imposable** et l'**impôt estimé** selon le taux de flat tax.
""")

# Entrées utilisateur
prix_vente = st.number_input("Prix de vente (€)", min_value=0.0, step=100.0, format="%.2f")
valeur_portefeuille = st.number_input("Valeur totale du portefeuille avant la vente (€)", min_value=0.01, step=100.0, format="%.2f")
prix_acquisition_total = st.number_input("Prix total d'acquisition (€)", min_value=0.0, step=100.0, format="%.2f")
taux_flat_tax = st.slider("Taux de flat tax (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.1)

# Calcul
if valeur_portefeuille > 0:
    cout_acquisition_proportionnel = prix_acquisition_total * (prix_vente / valeur_portefeuille)
    plus_value = prix_vente - cout_acquisition_proportionnel
    impot = plus_value * (taux_flat_tax / 100)

    # Résultats
    st.subheader("Résultats")
    st.write(f"**Coût d'acquisition proportionnel :** {cout_acquisition_proportionnel:.2f} €")
    st.write(f"**Plus-value imposable :** {plus_value:.2f} €")

    if plus_value > 0:
        st.write(f"**Impôt estimé (flat tax {taux_flat_tax:.1f}%) :** {impot:.2f} €")
    else:
        st.write("Pas de plus-value imposable (ou une moins-value).")
