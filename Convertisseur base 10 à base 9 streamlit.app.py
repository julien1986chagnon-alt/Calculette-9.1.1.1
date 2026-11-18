import streamlit as st

# ==============================================================================
# 1. FONCTIONS DE CONVERSION (BASE 10 BIJECTIVE <-> BASE 9 BIJECTIVE)
# ==============================================================================

def base10_bijective_vers_entier(b10_str):
    """Traduit un nombre écrit en Base 10 bijective (1-9, A=10) en entier standard."""
    saisie = str(b10_str).strip().replace(" ", "").upper()
    if not saisie:
        return None

    total = 0
    for caractere in saisie:
        if caractere in "123456789":
            valeur = int(caractere)
        elif caractere == "A":
            valeur = 10
        else:
            return None
        total = total * 10 + valeur

    return total


def entier_vers_base10_bijective(n):
    """Traduit un entier standard (> 0) en Base 10 bijective (1-9, A=10)."""
    if n <= 0:
        return None

    chiffres = []
    while n > 0:
        n, reste = divmod(n - 1, 10)
        valeur = reste + 1
        chiffres.append("A" if valeur == 10 else str(valeur))

    return "".join(reversed(chiffres))


def base10_bij_vers_base9_bij(b10_str):
    """Convertit de la Base 10 bijective vers la Base 9 bijective sans limite de taille."""
    n = base10_bijective_vers_entier(b10_str)
    if n is None or n <= 0:
        return None

    chiffres = []
    while n > 0:
        n, reste = divmod(n - 1, 9)
        chiffres.append(str(reste + 1))

    return "".join(reversed(chiffres))


def base9_bij_vers_base10_bij(b9_str):
    """Convertit de la Base 9 bijective vers la Base 10 bijective sans limite de taille."""
    saisie = str(b9_str).strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None

    total = 0
    for chiffre in saisie:
        total = total * 9 + int(chiffre)

    return entier_vers_base10_bijective(total)


# ==============================================================================
# 2. INTERFACE STREAMLIT
# ==============================================================================

st.set_page_config(page_title="Convertisseur Base 10 & Base 9 Bijectives", page_icon="🔢")

st.title("🔢 Convertisseur Base 10 ↔ Base 9 Bijectives")
st.caption("Numération bijective sans zéro et sans limite de chiffres (Base 10 : 1-9 et A | Base 9 : 1-9)")

onglet_10_vers_9, onglet_9_vers_10 = st.tabs([
    "➡️ Base 10 bijective vers Base 9 bijective",
    "⬅️ Base 9 bijective vers Base 10 bijective"
])

with onglet_10_vers_9:
    saisie_10 = st.text_input(
        "Entrez un nombre en Base 10 bijective (chiffres 1-9 et A pour 10) :",
        key="in_10"
    )

    if st.button("Convertir en Base 9 bijective", key="btn_10"):
        resultat = base10_bij_vers_base9_bij(saisie_10)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 et la lettre A (sans 0).")
        else:
            st.success(f"🟢 **Résultat en Base 9 bijective :** `{resultat}`")

with onglet_9_vers_10:
    saisie_9 = st.text_input(
        "Entrez un nombre en Base 9 bijective (chiffres de 1 à 9) :",
        key="in_9"
    )

    if st.button("Convertir en Base 10 bijective", key="btn_9"):
        resultat = base9_bij_vers_base10_bij(saisie_9)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 sans zéro.")
        else:
            st.success(f"🟢 **Résultat en Base 10 bijective :** `{resultat}`")

