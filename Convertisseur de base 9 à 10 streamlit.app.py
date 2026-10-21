import streamlit as st

# =============================================================================
# APPLICATION STREAMLIT : ARCHITECTURE MATHEMATIQUE UNIVERSELLE
# HARMONISATION TOTALE : CHIFFRES RONDS & CHIFFRES PLEINS SANS COLLISION
# CONCEPTEUR : CHAGNON JULIEN CHRISTIAN ROBERT - TOUS DROITS RÉSERVÉS
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
    1000000: "318561", # Ligne 6
    10000000: "3515271", # Ligne 7
    100000000: "38667981", # Ligne 8
    1000000000: "436458891", # Ligne 9
    10000000000: "4812158911", # Ligne 10
    100000000000: "53933759121", # Ligne 11
    1000000000000: "594372461331", # Ligne 12
    10000000000000: "6648197174641", # Ligne 13
    100000000000000: "74241278932151", # Ligne 14
    1000000000000000: "826654179353661", # Ligne 15
    10000000000000000: "9194295983891371", # Ligne 16
    100000000000000000: "112247366933915181", # Ligne 17
    1000000000000000000: "1234732147374166991", # Ligne 18
    10000000000000000000: "13563153632226848111", # Ligne 19
    100000000000000000000: "149524689954496439221", # Ligne 20
    1000000000000000000000: "1655772711549571852431", # Ligne 21
    10000000000000000000000: "18324599827716391476741", # Ligne 22
    100000000000000000000000: "212571719215881416355251" # Ligne 23
}

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

# L'unique et véritable addition en colonne bijective
def addition_comptable_verticale_b9(str_n1, str_n2):
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
            
        resultat.append(str(chiffre_ici))
            
    if retenue > 0:
        resultat.append(str(retenue))
        
    res_final = "".join(reversed(resultat)).lstrip('0')
    return res_final if res_final != "" else "0"

# Somme multiple pour gérer de grandes listes de rangs alignés
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

def comparaison_chaines_numeriques(str_b9_1, str_b9_2):
    s1 = str_b9_1.lstrip('0')
    s2 = str_b9_2.lstrip('0')
    if s1 == "": s1 = "0"
    if s2 == "": s2 = "0"
    
    if len(s1) > len(s2): return 1
    if len(s1) < len(s2): return -1
    
    if s1 > s2: return 1
    if s1 < s2: return -1
    return 0

# La simulation universelle par injection positionnelle stricte
def simuler_etape_1_pure(saisie_b10):
    longueur = len(saisie_b10)
    lignes_a_additionner = []
    
    # Étape 1 : Traitement du montant de départ comme brique de base
    lignes_a_additionner.append(int_vers_b9_bijective_pure(int(saisie_b10)))
    
    # Étape 2 : Projection des puissances de votre tableur
    for i, chiffre_str in enumerate(saisie_b10):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partiel_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                
                # Alignement comptable pur par décalage de rang (votre structure)
                partiel_decale = partiel_b9 + ("0" * nb_zeros_droite)
                lignes_a_additionner.append(partiel_decale)
                
    return somme_verticale_multi_lignes_b9(lignes_a_additionner)

def executer_etape_1(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) == 0:
        return None, "ERREUR : Saisie invalide.", "0"
        
    longueur = len(saisie)
    lignes_details = []
    lignes_a_additionner = []
    lignes_zeros_seules = []
    
    # Enregistrement de la valeur initiale
    montant_initial_b9 = int_vers_b9_bijective_pure(int(saisie))
    lignes_a_additionner.append(montant_initial_b9)
    
    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partiel_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                partiel_decale = partiel_b9 + ("0" * nb_zeros_droite)
                
                lignes_a_additionner.append(partiel_decale)
                lignes_zeros_seules.append(partiel_decale)
                
                lignes_details.append(f"Rang 10^{nb_zeros_droite} -> {chiffre} x {ref_tableur} = {partiel_b9} (Alignement : {partiel_decale})")
        else:
            lignes_details.append(f"Rang 10^{nb_zeros_droite} -> Repère de position 0 (Glissement)")
                
    somme_zeros_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    resultat_final_b9 = somme_verticale_multi_lignes_b9(lignes_a_additionner)
    
    return lignes_details, somme_zeros_brute, resultat_final_b9

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip()
    if not saisie.isdigit():
        return "ERREUR : Saisie invalide."
        
    longueur_b10 = 1
    
    # Recherche précise de l'échelle par encadrement de chaînes pures
    while True:
        max_test = "9" * longueur_b10
        val_max_b9 = simuler_etape_1_pure(max_test)
        if comparaison_chaines_numeriques(val_max_b9, saisie) >= 0:
            break
        longueur_b10 += 1
        
    # Reconstruction anatomique positionnelle chiffre par chiffre
    candidat_b10 = ["0"] * longueur_b10
    for position in range(longueur_b10):
        for test_chiffre in "123456789":
            candidat_b10[position] = test_chiffre
            chaine_test = "".join(candidat_b10)
            resultat_b9_simule = simuler_etape_1_pure(chaine_test)
            
            if comparaison_chaines_numeriques(resultat_b9_simule, saisie) > 0:
                candidat_b10[position] = str(max(0, int(test_chiffre) - 1))
                break
        else:
            candidat_b10[position] = "9"
            
    solution_finale = "".join(candidat_b10).lstrip("0")
    if solution_finale == "": solution_finale = "0"
    
    if simuler_etape_1_pure(solution_finale) == saisie:
        return solution_finale
    return "ERREUR : Déviation détectée dans la pyramide des constantes."

# =============================================================================
# INTERFACE GRAPHIQUE STREAMLIT D'ORIGINE RESTAURÉE
# =============================================================================

st.title("Architecture Mathématique")
st.subheader("Calculateur Disjoint Comptable – Par Chagnon Julien Christian Robert")
st.markdown("---")

onglet1, onglet2 = st.tabs([
    "1️⃣ ÉTAPE 1 : Base 10 -> Base 9 Bijective",
    "2️⃣ ÉTAPE 2 : Base 9 Bijective -> Base 10"
])

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
