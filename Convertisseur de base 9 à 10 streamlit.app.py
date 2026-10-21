import streamlit as st

# =============================================================================
# APPLICATION STREAMLIT : ARCHITECTURE MATHEMATIQUE (PROJET SECURISE)
# CALCULATEUR DISJOINT COMPTABLE - ALPHABET PUR DE 1 A 9 (SANS 0)
# LIMITE STRICTE SÉCURISÉE : MAX 18 CARACTÈRES À LA SAISIE
# CONCEPTEUR : CHAGNON JULIEN CHRISTIAN ROBERT
# =============================================================================

st.set_page_config(
    page_title="Architecture Mathématique",
    page_icon="🧮",
    layout="centered"
)

# --- MATRICE DE COEFFICIENTS D'ORIGINE ---
# TABLEUR_PASSAGES_ZERO associe les puissances géométriques à vos invariants
TABLEUR_PASSAGES_ZERO = {
    10: "1", # Ligne 1
    100: "11", # Ligne 2
    1000: "221", # Ligne 3
    10000: "2541", # Ligne 4
    100000: "27951", # Ligne 5
    1000000: "310561", # Ligne 6
    10000000: "3515271", # Ligne 7
    100000000: "38667981", # Ligne 8
    1000000000: "436458891", # Ligne 9
    10000000000: "4812158911", # Ligne 10
    100000000000: "53933759121", # Ligne 11
    1000000000000: "594372461331", # Ligne 12
    10000000000000: "6648197174641", # Ligne 13
    100000000000000: "74241278932151", # Ligne 14
    1000000000000000: "826654179353661", # Ligne 15
    10000000000000000: "9194295903891371", # Ligne 16
    100000000000000000: "11224723669339315181", # Ligne 17
    1000000000000000000: "1234732147374166991", # Ligne 18
    10000000000000000000: "13563153632226848111", # Ligne 19
    100000000000000000000: "149524689954496439221", # Ligne 20
    1000000000000000000000: "1655772711549571852431", # Ligne 21
    10000000000000000000000: "183245998277116391476741", # Ligne 22
    100000000000000000000000: "212571719215881416355251" # Ligne 23
}

# =============================================================================
# FONCTIONS COMPTABLES PURES SANS TRONCATURE NI TRICHE BASE 10
# =============================================================================

def int_vers_b9_bijective_pure(nombre_int):
    if nombre_int <= 0:
        return ""
    digits = []
    while nombre_int > 0:
        reste = nombre_int % 9
        if reste == 0:
            digits.append('9')
            nombre_int = (nombre_int // 9) - 1
        else:
            digits.append(str(reste))
            nombre_int = nombre_int // 9
    return "".join(reversed(digits))

def addition_comptable_verticale_b9(str_n1, str_n2):
    """
    Additionne deux chaînes en Base 9 Bijective de droite à gauche.
    Zéro triche : effectue l'opération colonne par colonne selon vos règles d'engrenage.
    """
    n1 = str_n1.strip()
    n2 = str_n2.strip()
    
    max_len = max(len(n1), len(n2))
    n1 = n1.zfill(max_len)
    n2 = n2.zfill(max_len)
    
    resultat = []
    retenue = 0
    
    for i in range(max_len - 1, -1, -1):
        d1 = int(n1[i]) if n1[i] != '0' else 0
        d2 = int(n2[i]) if n2[i] != '0' else 0
        
        somme_colonne = d1 + d2 + retenue
        
        if somme_colonne >= 9:
            reste = somme_colonne % 9
            if reste == 0:
                chiffre_ici = 9
                retenue = (somme_colonne // 9) - 1
            else:
                chiffre_ici = reste
                retenue = somme_colonne // 9
        else:
            chiffre_ici = somme_colonne
            retenue = 0
            
        if chiffre_ici > 0 or i > 0 or retenue > 0:
            resultat.append(str(chiffre_ici))
            
    if retenue > 0:
        resultat.append(str(retenue))
        
    return "".join(reversed(resultat))

def multiplication_comptable_unitaire_b9(str_b9, chiffre_int):
    """ Multiplie une chaîne en base 9 par un multiplicateur unitaire par additions successives natives """
    resultat = "0"
    for _ in range(chiffre_int):
        resultat = addition_comptable_verticale_b9(resultat, str_b9)
    return resultat

def b9_bijective_vers_quantite(chaine_b9):
    """ Décodeur inverse de contrôle de matière """
    total = 0
    for c in chaine_b9:
        if c != '0':
            total = total * 9 + int(c)
    return total

# =============================================================================
# LOGIQUE DE SIMULATION DES ÉTAPES DE LA PYRAMIDE
# =============================================================================

def simuler_etape_1_pure(saisie_b10):
    longueur = len(saisie_b10)
    somme_zeros_brute = "0"
    
    for i, chiffre_str in enumerate(saisie_b10):
        chiffre = int(chiffre_str)
        if chiffre > 0:
            puissance_dix = 10 ** (longueur - 1 - i)
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                # Multiplication native en base 9 sans repasser par la base 10
                partiel_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                somme_zeros_brute = addition_comptable_verticale_b9(somme_zeros_brute, partiel_b9)
                
    str_zeros_b9 = somme_zeros_brute
    str_montant_b9 = int_vers_b9_bijective_pure(int(saisie_b10))
    return addition_comptable_verticale_b9(str_montant_b9, str_zeros_b9)

def executer_etape_1(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "").replace(",", "").replace(".", "")
    if not saisie.isdigit() or int(saisie) == 0:
        return None, "ERREUR : Saisie invalide.", "0"
        
    longueur = len(saisie)
    somme_zeros_brute = "0"
    lignes_details = []
    
    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        if chiffre > 0:
            puissance_dix = 10 ** (longueur - 1 - i)
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                # Opération purement unitaire en base 9
                partiel_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                somme_zeros_brute = addition_comptable_verticale_b9(somme_zeros_brute, partiel_b9)
                lignes_details.append(f"Rang 10^{longueur-1-i} -> {chiffre} x {ref_tableur} = {partiel_b9}")
                
    str_zeros_b9 = somme_zeros_brute
    str_montant_b9 = int_vers_b9_bijective_pure(int(saisie))
    resultat_final_b9 = addition_comptable_verticale_b9(str_montant_b9, str_zeros_b9)
    
    return lignes_details, str_zeros_b9, resultat_final_b9

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip().replace(" ", "").replace(",", "").replace(".", "")
    if not saisie.isdigit() or '0' in saisie:
        return "ERREUR : Le chiffre 0 est interdit."
        
    cible_val = b9_bijective_vers_quantite(saisie)
    longueur_b10 = 1
    
    while True:
        max_test = "9" * longueur_b10
        val_max_b9 = simuler_etape_1_pure(max_test)
        if b9_bijective_vers_quantite(val_max_b9) >= cible_val:
            break
        longueur_b10 += 1
        
    candidat_b10 = ["0"] * longueur_b10
    for position in range(longueur_b10):
        for test_chiffre in "123456789":
            candidat_b10[position] = test_chiffre
            chaine_test = "".join(candidat_b10)
            resultat_b9_simule = simuler_etape_1_pure(chaine_test)
            
            if b9_bijective_vers_quantite(resultat_b9_simule) > cible_val:
                candidat_b10[position] = str(max(0, int(test_chiffre) - 1))
                break
        else:
            candidat_b10[position] = "9"
            
    solution_finale = "".join(candidat_b10).lstrip("0")
    if solution_finale == "":
        solution_finale = "0"
        
    if simuler_etape_1_pure(solution_finale) == saisie:
        return solution_finale
        
    return "ERREUR : Déviation détectée dans la pyramide des constantes."

# =============================================================================
# INTERFACE GRAPHique STREAMLIT (FIDELE A VOS CAPTURES)
# =============================================================================

st.title("Architecture Mathématique")
st.subheader("Calculateur Disjoint Bijectif Pur – Par Chagnon Julien Christian Robert")
st.markdown("---")

st.markdown("""
Ce système utilise une **arithmétique positionnelle bijective de base 9**.
L'alphabet numérique y est exclusivement composé des symboles pleins de **1 à 9**.
""")

onglet1, onglet2 = st.tabs([
    "1️⃣ ÉTAPE 1 : Base 10 -> Base 9 Bijective",
    "2️⃣ ÉTAPE 2 : Base 9 Bijective -> Base 10"
])

# --- ÉTAPE 1 ---
with onglet1:
    st.header("Comptabilité en Base 9")
    saisie_b10 = st.text_input(
        "Saisissez le montant initial (Base 10 - Max 20 chiffres) :",
        max_chars=20,
        key="input_b10",
        placeholder="Entrez votre nombre de 1 à 18 chiffres..."
    )
    
    if saisie_b10:
        lignes, zeros_b9, res_final = executer_etape_1(saisie_b10)
        if lignes is None:
            st.error(zeros_b9)
        else:
            st.markdown("### 📊 Décomposition brute selon votre architecture :")
            for lignement in lignes:
                st.markdown(lignement)
            st.markdown("---")
            st.info(f"**Passages extraits (en Base 9 Bijective) :** `{zeros_b9}`")
            st.success(f"**🏆 RÉSULTAT COMPTABILISÉ EN BASE 9 PURE :** `{res_final}`")
            st.code(res_final, language="text")

# --- ÉTAPE 2 ---
with onglet2:
    st.header("Anatomie Restaurée en Base 10")
    saisie_b9 = st.text_input(
        "Saisissez le nombre à traiter (Base 9 - Max 20 chiffres) :",
        max_chars=20,
        key="input_b9",
        placeholder="Colle la suite de chiffres bijectifs ici..."
    )
    
    if saisie_b9:
        resultat_b10 = executer_etape_2(saisie_b9)
        if "ERREUR" in resultat_b10:
            st.error(resultat_b10)
        else:
            st.success(f"### 🎯 ANATOMIE RESTAURÉE EN COMPTABILITÉ BASE 10 :")
            st.code(resultat_b10, language="text")

st.markdown("---")
