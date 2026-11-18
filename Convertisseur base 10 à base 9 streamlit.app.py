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

def executer_etape_2(chaine_b9_str):
    """Étape 1 de la reconstruction : reconnaît les paliers exacts de votre tableau."""
    saisie = chaine_b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None

    # 1. Recherche directe dans votre tableau (ex: "12531" -> 10000)
    for cle_b10, (passage, total_b9) in TABLEUR_PASSAGES_ZERO.items():
        if saisie == total_b9:
            return str(cle_b10)

    # 2. Recherche d'un multiple exact d'un palier (ex: 2 x "12531" -> 20000)
    for cle_b10, (passage, total_b9) in TABLEUR_PASSAGES_ZERO.items():
        for chiffre in range(2, 10):
            if saisie == multiplication_comptable_unitaire_b9(total_b9, chiffre):
                return str(cle_b10 * chiffre)

    return "Palier composé (étape suivante à construire)"def executer_etape_2(chaine_b9_str):
    """Décompte du plus grand palier au plus petit (multiples + unitaires)."""
    saisie = chaine_b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None

    reste_b9 = saisie
    total_base10 = 0
    
    # On trie vos paliers du plus grand (10^26) jusqu'aux unitaires (1)
    paliers_descendants = sorted(TABLEUR_PASSAGES_ZERO.keys(), reverse=True)
    
    for cle_b10 in paliers_descendants:
        passage, total_palier_b9 = TABLEUR_PASSAGES_ZERO[cle_b10]
        
        # On teste les multiples du plus grand (9) au plus petit (1) pour ce palier
        for multiple in range(9, 0, -1):
            valeur_multiple_b9 = multiplication_comptable_unitaire_b9(total_palier_b9, multiple)
            
            # Si ce multiple rentre dans ce qu'il nous reste
            if b9_vers_entier_bijectif(reste_b9) >= b9_vers_entier_bijectif(valeur_multiple_b9):
                # On ajoute ce palier à notre réponse Base 10
                total_base10 += cle_b10 * multiple
                # On soustrait ce multiple pour continuer avec le reste
                reste_b9 = soustraction_comptable_verticale_b9(reste_b9, valeur_multiple_b9)
                break

    return str(total_base10) if total_base10 > 0 else "1"



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


