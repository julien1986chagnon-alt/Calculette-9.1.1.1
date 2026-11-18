import streamlit as st

# =====================================================================
# 1. VOTRE TABLE DES PASSAGES ZÉRO (À COMPLÉTER PAR VOS SOINS)
# =====================================================================
# Format : Puissance_de_10 : "Nombre_de_passages_zero_en_base_10"

TABLEUR_PASSAGES_ZERO = {
    10: "1",
    100: "11",
    1000: "221",
    10000: "2531",
    100000: "27941",
    1000000: "318661",
    10000000: "3416471",
    100000000: "37582381",
    1000000000: "424516391",
    10000000000: "4669681511",
    100000000000: "52477596721",
    1000000000000: "577364675131",
    10000000000000: "6462122536541",
    100000000000000: "72183347913151",
    1000000000000000: "794126838144761",
    10000000000000000: "8845396329593571",
    100000000000000000: "98299469636639481",
    1000000000000000000: "1192415277114135491",
    10000000000000000000: "13226568158255491611",
    100000000000000000000: "145493359751821517821",
    1000000000000000000000: "1611536968371136697231",
    10000000000000000000000: "17726917763182514779641",
    100000000000000000000000: "195997196495117663687251",
    1000000000000000000000000: "2267179272556295411669861",
    10000000000000000000000000: "24948982998229359528479671",
    100000000000000000000000000: "275549924191533965824387581",

}
# =====================================================================
# 2. FONCTIONS DE CONVERSION (BASE 10 -> BASE 9 PUIS BASE 9 -> BASE 10)
# =====================================================================

def base10_vers_base9(n_str):
    """Convertit n'importe quel entier (Base 10) vers la Base 9 bijective (chiffres 1 à 9)."""
    saisie = str(n_str).strip().replace(" ", "")
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
    saisie = str(b9_str).strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None
    
    total = 0
    for chiffre in saisie:
        total = total * 9 + int(chiffre)
        
    return str(total)

def calculer_passages_depuis_table(n_str):
    """Calcule le nombre de passages zéro d'après votre table et le traduit en Base 9."""
    saisie = str(n_str).strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None, None
    
    longueur = len(saisie)
    total_passages_b10 = 0
    
    for i, chiffre_char in enumerate(saisie):
        chiffre = int(chiffre_char)
        if chiffre > 0:
            puissance_dix = 10 ** (longueur - 1 - i)
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                val_table = int(TABLEUR_PASSAGES_ZERO[puissance_dix])
                total_passages_b10 += val_table * chiffre
                
    if total_passages_b10 == 0:
        return "0", "0"
        
    passages_en_b9 = base10_vers_base9(str(total_passages_b10))
    return str(total_passages_b10), passages_en_b9

# =====================================================================
# 3. INTERFACE STREAMLIT
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
    afficher_option = st.checkbox("Afficher le nombre de passages zéro (depuis ma table)", value=True)
    
    if st.button("Convertir en Base 9", key="btn_10"):
        resultat = base10_vers_base9(saisie_10)
        if resultat is None:
            st.error("⚠️ Veuillez entrer un nombre entier valide supérieur à 0.")
        else:
            st.success(f"🟢 **Résultat en Base 9 :** `{resultat}`")
            
            if afficher_option:
                passages_b10, passages_b9 = calculer_passages_depuis_table(saisie_10)
                st.info(
                    f"📊 **Passages zéro (selon votre table) :**\n\n"
                    f"* En Base 10 : `{passages_b10}`\n"
                    f"* En Base 9 bijective : `{passages_b9}`"
                )

with onglet_9_vers_10:
    saisie_9 = st.text_input("Entrez un nombre en Base 9 (chiffres de 1 à 9 uniquement) :", key="in_9")
    if st.button("Convertir en Base 10", key="btn_9"):
        resultat = base9_vers_base10(saisie_9)
        if resultat is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        else:
            st.success(f"🟢 **Résultat en Base 10 :** `{resultat}`")

