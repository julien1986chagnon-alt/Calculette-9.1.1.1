import streamlit as st

# Configuration graphique de la page
st.set_page_config(page_title="Calculateur Disjoint", page_icon="🔢", layout="centered")

# ==========================================
# 1. VOTRE TABLEUR DES PASSAGES ZÉRO (L'ARBRE)
# ==========================================
TABLEUR_PASSAGES_ZERO = {
    1: ("0", "1"),
    10: ("1","11"),
    100: ("11","111"), 
    1000: ("221","1221"),
    10000: ("2531","12531"),
    100000: ("27841","127841"),
    1000000: ("317351","1317351"),
    10000000: ("3491861","13491861"),
    100000000: ("38521571","138521571"),
    1000000000: ("434737381","1434737381"),
    10000000000: ("4783222291","14783222291"),
    100000000000: ("53725445311","153725445311"),
    1000000000000: ("591979898421","1591979898421"),
    10000000000000: ("6622889993631","16622889993631"),
    100000000000000: ("73853112139941","173853112139941"),
    1000000000000000: ("823484233551451","1823484233551451"),
    10000000000000000: ("9158437569165961","19158437569165961"),
    100000000000000000: ("111753824371836671","211753824371836671"),
    1000000000000000000: ("1229393168191314481","2229393168191314481"),
    10000000000000000000: ("13534434861214459391","23534434861214459391"),
    100000000000000000000: ("148878784573359164411","248878784573359164411"),
    1000000000000000000000: ("1648777741416961818521","2648777741416961818521"),
    10000000000000000000000: ("18247666255587681114731","28247666255587681114731"),
    100000000000000000000000: ("211735438822575592263141","311735438822575592263141"),
    1000000000000000000000000: ("2329189838148442624894551","3329189838148442624894551"),
    10000000000000000000000000: ("25632199329643868874951161","35632199329643868874951161"),
    100000000000000000000000000: ("282954313637183668735562771","382954313637183668735562771"),
}


# Mémoire dynamique de l'application (Session State)
if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}
# =====================================================================
# 2. LECTURE DIRECTE DE VOTRE TABLE DE CONVERGENCE (PASSAGES ZÉRO)
# =====================================================================

def lire_passages_dans_ma_table(n_str):
    """Lit vos paliers directement dans TABLEUR_PASSAGES_ZERO et additionne vos passages."""
    saisie = n_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None
    
    longueur = len(saisie)
    total_passages = 0
    total_cumule_table = 0
    
    for i, chiffre_char in enumerate(saisie):
        chiffre = int(chiffre_char)
        if chiffre > 0:
            puissance_dix = 10 ** (longueur - 1 - i)
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                passage_palier, total_palier = TABLEUR_PASSAGES_ZERO[puissance_dix]
                total_passages += int(passage_palier) * chiffre
                total_cumule_table += int(total_palier) * chiffre
                
    return str(total_passages), str(total_cumule_table)

# =====================================================================
# 3. CONVERSION UNIVERSELLE BASE 9 BIJECTIVE (ALLER & RETOUR EXACT)
# =====================================================================

def base10_vers_base9_bijective(n_str):
    """Convertit n'importe quel entier (Base 10) vers la Base 9 bijective officielle."""
    saisie = n_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None
    
    n = int(saisie)
    chiffres = []
    while n > 0:
        n, reste = divmod(n - 1, 9)
        chiffres.append(str(reste + 1))
        
    return "".join(reversed(chiffres))

def base9_bijective_vers_base10(b9_str):
    """Convertit n'importe quel nombre Base 9 bijective vers la Base 10 (avec lecture directe de votre table)."""
    saisie = b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None, False
    
    # 1. Vérifie d'abord si le nombre est un palier exact de votre table
    for palier_b10, (passage, total_table) in TABLEUR_PASSAGES_ZERO.items():
        if saisie == total_table:
            return str(palier_b10), True
            
    # 2. Sinon, applique le calcul universel de retour en Base 10
    total_b10 = 0
    for chiffre_char in saisie:
        total_b10 = total_b10 * 9 + int(chiffre_char)
        
    return str(total_b10), False

# =====================================================================
# 4. INTERFACE STREAMLIT (VOTRE TABLE + BASE 9 UNIVERSELLE)
# =====================================================================

st.title("🔢 Convertisseur Base 9 Bijective & Table de Convergence")
st.caption("Alliance de votre table des passages zéro et de la numération bijective universelle")

onglet_aller, onglet_retour = st.tabs([
    "➡️ ÉTAPE 1 : Base 10 ➡️ Base 9", 
    "⬅️ ÉTAPE 2 : Base 9 ➡️ Base 10"
])

with onglet_aller:
    st.markdown("#### Analyse depuis la Base 10")
    saisie_b10 = st.text_input("Entrez un nombre entier en Base 10 :", max_chars=26, key="in_b10")
    
    if st.button("Lancer l'analyse complète", key="btn_aller"):
        res_table = lire_passages_dans_ma_table(saisie_b10)
        vrai_b9 = base10_vers_base9_bijective(saisie_b10)
        
        if vrai_b9 is None or res_table is None:
            st.error("⚠️ Veuillez entrer un nombre entier valide supérieur à 0.")
        else:
            passages_lus, cumule_lu = res_table
            st.info(f"📊 **Passages zéro (d'après votre table) :** `{passages_lus}`")
            st.success(f"🟢 **Total en Base 9 bijective :** `{vrai_b9}`")

with onglet_retour:
    st.markdown("#### Conversion vers la Base 10")
    saisie_b9 = st.text_input("Entrez un nombre en Base 9 (chiffres 1 à 9 uniquement) :", max_chars=27, key="in_b9")
    
    if st.button("Convertir vers la Base 10", key="btn_retour"):
        res_b10, trouve_dans_table = base9_bijective_vers_base10(saisie_b9)
        
        if res_b10 is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        elif trouve_dans_table:
            st.success(f"🟢 **PALIER RECONNU DANS VOTRE TABLE :** `{res_b10}`")
        else:
            st.success(f"🟢 **RÉSULTAT EN BASE 10 :** `{res_b10}`")


            st.success(f"🟢 **RÉSULTAT BASE 10 :** `{res_b10}`")

