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
# 2. FONCTIONS DE CONVERSION BIJECTIVE PURE (SANS TROUS)
# =====================================================================

def base10_vers_bijectif9(n_int):
    """Convertit un entier base 10 en chaîne base 9 sans zéro (chiffres 1 à 9)."""
    if n_int <= 0:
        return "0"
    chiffres = []
    while n_int > 0:
        n_int, reste = divmod(n_int - 1, 9)
        chiffres.append(str(reste + 1))
    return "".join(reversed(chiffres))

def bijectif9_vers_base10(str_b9):
    """Convertit une chaîne base 9 sans zéro vers son entier base 10 exact."""
    total = 0
    for c in str_b9:
        total = total * 9 + int(c)
    return total

def lire_reference_tableau(nb_chiffres):
    """Utilise votre TABLEUR_PASSAGES_ZERO pour vérifier le palier correspondant."""
    puissance_dix = 10 ** (nb_chiffres - 1)
    return TABLEUR_PASSAGES_ZERO.get(puissance_dix, "0")

# =====================================================================
# 3. FONCTIONS ALLER (BASE 10 -> BASE 9) ET RETOUR (BASE 9 -> BASE 10)
# =====================================================================

def convertir_b10_vers_b9(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None
    
    n_b10 = int(saisie)
    # Conversion bijective directe : chaque nombre en base 10 a un unique voisin en base 9 sans zéro
    resultat_b9 = base10_vers_bijectif9(n_b10)
    return resultat_b9

def convertir_b9_vers_b10(chaine_b9_str):
    saisie = chaine_b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None
    
    # Conversion inverse directe : garantit un retour à 100% identique à l'original
    resultat_b10 = bijectif9_vers_base10(saisie)
    return str(resultat_b10)


# =====================================================================
# 4. INTERFACE APPLICATIVE GRAPHIQUE
# =====================================================================

st.title("🔢 Convertisseur base 9 bijective et 10")
st.caption("Calculateur Disjoint - Alignement des structures de bases numériques")

onglet_direct, onglet_inverse = st.tabs(["➡️ ÉTAPE 1 : Base 10 -> Base 9", "⬅️ ÉTAPE 2 : Base 9 -> Base 10"])

with onglet_direct:
    st.markdown("#### Génération Mathématique")
    saisie_b10 = st.text_input("Saisissez le montant décimal (Base 10) :", max_chars=26, key="txt_b10")
    
    if st.button("Calculer le format Bijectif", key="btn_direct"):
        res_final = executer_etape_1(saisie_b10)
        if res_final is None:
            st.error("⚠️ Saisie invalide. Entrez un nombre entier supérieur à 0.")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 9 BIJECTIVE :** `{res_final}`")

with onglet_inverse:
    st.markdown("#### Restauration Exacte")
    saisie_b9 = st.text_input("Saisissez le nombre bijectif (Base 9, chiffres 1 à 9 uniquement) :", max_chars=27, key="txt_b9")
    
    if st.button("Convertir vers Base 10", key="btn_inverse"):
        res_b10 = executer_etape_2(saisie_b9)
        if res_b10 is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 10 :** `{res_b10}`")


