import streamlit as st

# ==========================================================
# 1. FONCTIONS DE CONVERSION (BASE 10 CLASSIQUE <-> BASE 9 BIJECTIVE)
# ==========================================================

def base10_vers_base9_bij(b10_str):
    """Convertit de la Base 10 classique (0-9) vers la Base 9 bijective (1-9) sans limite de taille."""
    saisie = str(b10_str).strip().replace(" ", "")
    if not saisie or not saisie.isdigit():
        return None

    n = int(saisie)
    if n <= 0:
        return None

    chiffres = []
    while n > 0:
        n, reste = divmod(n - 1, 9)
        chiffres.append(str(reste + 1))

    return "".join(reversed(chiffres))


def base9_bij_vers_base10(b9_str):
    """Convertit de la Base 9 bijective (1-9, sans 0) vers la Base 10 classique sans limite de taille."""
    saisie = str(b9_str).strip().replace(" ", "")
    if not saisie or not saisie.isdigit() or "0" in saisie:
        return None

    total = 0
    for chiffre in saisie:
        total = total * 9 + int(chiffre)

    return str(total)


# ==========================================================
# 2. INTERFACE STREAMLIT
# ==========================================================

st.set_page_config(page_title="Convertisseur Base 10 & Base 9 Bijective", page_icon="🔢")

st.title("🔢 Convertisseur Base 10 ↔ Base 9 Bijective")
st.caption("Base 10 classique (0-9) vers Base 9 bijective (1-9 sans zéro) et inversement")

onglet_10_vers_9, onglet_9_vers_10 = st.tabs([
    "Base 10 classique vers Base 9 bijective",
    "Base 9 bijective vers Base 10 classique"
])

with onglet_10_vers_9:
    saisie_10 = st.text_input(
        "Entrez un nombre en Base 10 classique (chiffres 0 à 9) :",
        key="in_10"
    )

    if st.button("Convertir en Base 9 bijective", key="btn_10"):
        resultat = base10_vers_base9_bij(saisie_10)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 0 à 9 (nombre entier supérieur à 0).")
        else:
            st.success(f"**Résultat en Base 9 bijective :** `{resultat}`")

with onglet_9_vers_10:
    saisie_9 = st.text_input(
        "Entrez un nombre en Base 9 bijective (chiffres de 1 à 9, sans 0) :",
        key="in_9"
    )

    if st.button("Convertir en Base 10 classique", key="btn_9"):
        resultat = base9_bij_vers_base10(saisie_9)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 sans zéro.")
        else:
            st.success(f"**Résultat en Base 10 classique :** `{resultat}`")

