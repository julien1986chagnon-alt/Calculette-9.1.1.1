import streamlit as st

# Configuration graphique de la page
st.set_page_config(page_title="Calculateur Disjoint", page_icon="🔢", layout="centered")

# ==========================================
# 1. VOTRE TABLEUR DES PASSAGES ZÉRO (L'ARBRE)
# ==========================================
TABLEUR_PASSAGES_ZERO = {
    10: "1",
    100: "11",
    1000: "221",
    10000: "2531",
    100000: "27841",
    1000000: "317351",
    10000000: "3491861",
    100000000: "38521571",
    1000000000: "434737381",
    10000000000: "4783222291",
    100000000000: "53725445311",
    1000000000000: "591979898421",
    10000000000000: "6622889993631",
    100000000000000: "73853112139941",
    1000000000000000: "823484233551451",
    10000000000000000: "9158437569165961",
    100000000000000000: "111753824371836671",
    1000000000000000000: "1229393168191314481",
    10000000000000000000: "13534434861214459391",
    100000000000000000000: "148878784573359164411",
    1000000000000000000000: "1648777741416961818521",
    10000000000000000000000: "18247666255587681114731",
    100000000000000000000000: "211735438822575592263141",
    1000000000000000000000000: "2329189838148442624894551",
    10000000000000000000000000: "25632199329643868874951161",
    100000000000000000000000000: "282954313637183668735562771",
}


# Mémoire dynamique de l'application (Session State)
if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}

# =====================================================================
# 2. FONCTIONS D'ADDITION ET DE SOUSTRACTION VERTICALE EN BASE 9
# =====================================================================

def addition_comptable_verticale_b9(str_n1, str_n2):
    n1, n2 = str_n1.strip(), str_n2.strip()
    if n1 == "0": return n2
    if n2 == "0": return n1
    max_len = max(len(n1), len(n2))
    n1, n2 = n1.zfill(max_len), n2.zfill(max_len)
    resultat, retenue = [], 0

    for i in range(max_len - 1, -1, -1):
        d1 = int(n1[i]) if n1[i] != '0' else 0
        d2 = int(n2[i]) if n2[i] != '0' else 0
        somme_colonne = d1 + d2 + retenue

        if somme_colonne >= 9:
            reste = somme_colonne % 9
            chiffre_ici = 9 if reste == 0 else reste
            retenue = (somme_colonne // 9) - 1 if reste == 0 else somme_colonne // 9
        else:
            chiffre_ici = somme_colonne
            retenue = 0
        resultat.append(str(chiffre_ici))

    if retenue > 0:
        resultat.append(str(retenue))

    res_final = "".join(reversed(resultat)).lstrip('0')
    return res_final if res_final != "" else "0"

def soustraction_comptable_verticale_b9(str_grand, str_petit):
    """Soustrait str_petit de str_grand dans votre système base 9 sans zéro."""
    val_grand = b9_vers_entier_bijectif(str_grand)
    val_petit = b9_vers_entier_bijectif(str_petit)
    diff = val_grand - val_petit
    return entier_bijectif_vers_b9(diff) if diff > 0 else "0"

def somme_verticale_multi_lignes_b9(liste_chaines):
    total = "0"
    for chaine in liste_chaines:
        total = addition_comptable_verticale_b9(total, chaine)
    return total

def multiplication_comptable_unitaire_b9(str_b9, chiffre_int):
    resultat = "0"
    for _ in range(chiffre_int):
        resultat = addition_comptable_verticale_b9(resultat, str_b9)
    return resultat

def b9_vers_entier_bijectif(str_b9):
    if not str_b9 or str_b9 == "0":
        return 0
    total = 0
    for c in str_b9:
        total = total * 9 + int(c)
    return total

def entier_bijectif_vers_b9(n_int):
    if n_int <= 0:
        return "0"
    chiffres = []
    while n_int > 0:
        n_int, reste = divmod(n_int - 1, 9)
        chiffres.append(str(reste + 1))
    return "".join(reversed(chiffres))

# =====================================================================
# 3. FONCTIONS ALLER (BASE 10 -> BASE 9) ET RETOUR (BASE 9 -> BASE 10)
# =====================================================================

def executer_etape_1(montant_b10_str):
    """Aller : Additionne directement la saisie avec votre TABLEUR_PASSAGES_ZERO."""
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None

    longueur = len(saisie)
    lignes_zeros_seules = []

    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partiel_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                lignes_zeros_seules.append(partiel_b9)

    somme_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    return addition_comptable_verticale_b9(saisie, somme_brute)

def executer_etape_2(chaine_b9_str):
    """Retour : Soustrait les paliers exacts générés par l'Étape 1 pour revenir en Base 10."""
    saisie = chaine_b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None

    reste_b9 = saisie
    resultat_b10_chiffres = []
    
    for exposant in range(26, -1, -1):
        p10 = 10 ** exposant
        cout_unitaire_b9 = executer_etape_1(str(p10))
        
        if cout_unitaire_b9 is None:
            continue
            
        chiffre_b10 = 0
        while b9_vers_entier_bijectif(reste_b9) >= b9_vers_entier_bijectif(cout_unitaire_b9) and chiffre_b10 < 9:
            reste_b9 = soustraction_comptable_verticale_b9(reste_b9, cout_unitaire_b9)
            chiffre_b10 += 1
            
        if resultat_b10_chiffres or chiffre_b10 > 0:
            resultat_b10_chiffres.append(str(chiffre_b10))

    res_final = "".join(resultat_b10_chiffres)
    return res_final if res_final != "" else "1"




# =====================================================================
# 4. INTERFACE APPLICATIVE GRAPHIQUE
# =====================================================================

st.title("🔢 Convertisseur base 9 bijective et 10")
st.caption("Calculateur Disjoint - Alignement des structures de bases numériques")

onglet_direct, onglet_inverse = st.tabs(["➡️ ÉTAPE 1 : Base 10 -> Base 9", "⬅️ ÉTAPE 2 : Base 9 -> Base 10"])

# --- CONVERTISSEUR DIRECT (BASE 10 -> BASE 9) ---
with onglet_direct:
    st.markdown("#### Génération Mathématique")
    saisie_b10 = st.text_input("Saisissez le montant décimal (Base 10) :", max_chars=27, key="txt_b10")
    
    if st.button("Calculer le format Bijectif", key="btn_direct"):
        res_final = convertir_b10_vers_b9(saisie_b10)
        if res_final is None:
            st.error("⚠️ Saisie invalide. Veuillez entrer un nombre entier supérieur à 0.")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 9 BIJECTIVE :** `{res_final}`")

# --- CONVERTISSEUR INVERSE (BASE 9 -> BASE 10) ---
with onglet_inverse:
    st.markdown("#### Restauration Exacte")
    saisie_b9 = st.text_input("Saisissez le nombre bijectif (Base 9, chiffres 1 à 9 uniquement) :", max_chars=27, key="txt_b9")
    
    if st.button("Convertir vers Base 10", key="btn_inverse"):
        res_b10 = convertir_b9_vers_b10(saisie_b9)
        if res_b10 is None:
            st.error("⚠️ Saisie invalide. En base 9 bijective, utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 10 :** `{res_b10}`")

g(f"💎 **[PHASE 3] EXCEPTION DE CALCUL ACTIVÉE (Vrai x 9) :** `{valeur_base10}`")
