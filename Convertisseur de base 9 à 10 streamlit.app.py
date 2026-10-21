import streamlit as st

st.set_page_config(
    page_title="Architecture Mathématique",
    page_icon="🧮",
    layout="centered"
)

# ==============================================================================
# --- MATRICE DE COEFFICIENTS D'ORIGINE ---
# ==============================================================================
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


# ==============================================================================
# --- FONCTIONS ALGORITHMIQUES COMPTABLES ---
# ==============================================================================

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

# ==============================================================================
# --- LOGIQUE UNIVERSELLE ET EXÉCUTION ---
# ==============================================================================

def simuler_etape_1_pure(saisie_b10):
    longueur = len(saisie_b10)
    lignes_zeros_seules = []
    
    for i, chiffre_str in enumerate(saisie_b10):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partial_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                lignes_zeros_seules.append(partial_b9)
                
    somme_zeros_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    return addition_comptable_verticale_b9(saisie_b10, somme_zeros_brute)

def executer_etape_1(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) == 0:
        return None, "ERREUR : Saisie invalide.", "0"
        
    longueur = len(saisie)
    lignes_details = []
    lignes_zeros_seules = []
    
    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partial_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                lignes_zeros_seules.append(partial_b9)
                lignes_details.append(f"Rang 10^{nb_zeros_droite} ➔ {chiffre} x {ref_tableur} = {partial_b9}")
        else:
            lignes_details.append(f"Rang 10^{nb_zeros_droite} ➔ Repère de position 0 (Glissement)")
            
    somme_zeros_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    resultat_final_b9 = addition_comptable_verticale_b9(saisie, somme_zeros_brute)
    
    return lignes_details, somme_zeros_brute, resultat_final_b9

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip()
    if not saisie.isdigit():
        return "ERREUR : Saisie invalide."
    
    # 1. RECHERCHE GLOBALE : Approximation rapide de la zone numérique
    low = 1
    high = 99999999999999999999
    base_proche = None
    
    while low <= high:
        mid = (low + high) // 2
        candidat_str = str(mid)
        res_simule = simuler_etape_1_pure(candidat_str)
        
        if res_simule == saisie:
            return candidat_str
            
        # Comparaison de chaînes
        s1 = res_simule.lstrip('0')
        s2 = saisie.lstrip('0')
        if len(s1) < len(s2) or (len(s1) == len(s2) and s1 < s2):
            low = mid + 1
        else:
            high = mid - 1
            base_proche = mid

    # 2. FILE DE SÉCURITÉ LOCAL (Balayage de précision)
    # Inspecte minutieusement la zone pour corriger les anomalies dues aux zéros (comme pour 991 -> 1000)
    point_depart = base_proche if base_proche is not None else low
    for offset in range(-150, 150):
        valeur_test = point_depart + offset
        if valeur_test > 0:
            candidat_str = str(valeur_test)
            if simuler_etape_1_pure(candidat_str) == saisie:
                return candidat_str
                
    return "ERREUR : Saisie hors matrice ou déviation détectée."

# ==============================================================================
# --- INTERFACE GRAPHIQUE STREAMLIT ---
# ==============================================================================

st.title("Architecture Mathématique")
st.markdown("### Calculateur Disjoint Comptable - Par Chagnon Julien Christian Robert")
st.markdown("---")

onglet1, onglet2 = st.tabs([
    " 🟧 ÉTAPE 1 : Base 10 ➔ Base 9 Bijective",
    " 🟦 ÉTAPE 2 : Base 9 Bijective ➔ Base 10"
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
            st.markdown("#### 📖 Décomposition brute selon votre architecture :")
            for lignement in lignes:
                if "Glissement" not in lignement:
                    st.markdown(lignement)
            
            st.markdown("---")
            st.info(f"**Passages extraits (en Base 9 Bijective) :** {zeros_b9}")
            st.success(f"**🟩 RÉSULTAT COMPTABILISÉ EN BASE 9 PURE :** {res_final}")
            
            # Bande bleue de vérification synchronisée et corrigée
            resultat_inverse_direct = executer_etape_2(res_final)
            if "ERREUR" not in resultat_inverse_direct:
                st.info(f"**🔷 Vérification Automatique Inverse (Retour à la Base 10) : {resultat_inverse_direct}**")
            else:
                st.error(resultat_inverse_direct)

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
            st.success("#### 🟢 ANATOMIE RESTAURÉE EN COMPTABILITÉ BASE 10 :")
            st.code(resultat_b10, language="text")

st.markdown("---")
st.caption("© Architecture Mathématique Appliquée - Tous droits réservés.")
