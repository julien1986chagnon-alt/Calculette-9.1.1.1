import streamlit as st

# =====================================================================
# 1. FONCTIONS DE CONVERSION (BASE 10 -> BASE 9 PUIS BASE 9 -> BASE 10)
# =====================================================================

def base10_vers_base9(n_str):
    """Convertit n'importe quel entier (Base 10) vers la Base 9 bijective (chiffres 1 à 9)."""
    saisie = n_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None
    
    n = int(saisie)
    chiffres = []
    while n > 0:
        n, reste = divmod(n - 1, 9)
        chiffres.append(str(reste + 1))
        
    return "".join(reversed(chiffres))

def base9_vers_base10(b9_str):
    """Convertit n'importe quel nombre Base 9 bijective (chiffres 1 à 9) vers la Base 10."""
    saisie = b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None
    
    total = 0
    for chiffre in saisie:
        total = total * 9 + int(chiffre)
        
    return str(total)

# =====================================================================
# 2. INTERFACE STREAMLIT
# =====================================================================

st.set_page_config(page_title="Convertisseur Base 10 & Base 9", page_icon="🔢")

st.title("🔢 Convertisseur Base 10 ↔ Base 9")
st.caption("Numération bijective sans zéro (chiffres de 1 à 9)")

onglet_10_vers_9, onglet_9_vers_10 = st.tabs([
    "➡️ Base 10 vers Base 9", 
    "⬅️ Base 9 vers Base 10"
])

with onglet_10_vers_9:
    saisie_10 = st.text_input("Entrez un nombre entier en Base 10 :", key="in_10")
    if st.button("Convertir en Base 9", key="btn_10"):
        resultat = base10_vers_base9(saisie_10)
        if resultat is None:
            st.error("⚠️ Veuillez entrer un nombre entier valide supérieur à 0.")
        else:
            st.success(f"🟢 **Résultat en Base 9 :** `{resultat}`")

with onglet_9_vers_10:
    saisie_9 = st.text_input("Entrez un nombre en Base 9 (chiffres de 1 à 9 uniquement) :", key="in_9")
    if st.button("Convertir en Base 10", key="btn_9"):
        resultat = base9_vers_base10(saisie_9)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        else:
            st.success(f"🟢 **Résultat en Base 10 :** `{resultat}`")
