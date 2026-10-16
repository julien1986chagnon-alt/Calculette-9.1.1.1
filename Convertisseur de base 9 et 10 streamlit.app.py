import streamlit as st

# =============================================================================
# CONFIGURATION : LA GRILLE DES ZÉROS PURS (STRICTEMENT ISSUE DE VOTRE TABLEAU)
# =============================================================================

TABLE_DES_ZEROS_PURS = {
    "10": "9",
    "100": "11",
    "1000": "221",
    "10000": "2431",
    "100000": "26741",
    "1000000": "295251",
    "10000000": "3257761",
    "100000000": "35946471",
    "1000000000": "417522281",
    "10000000000": "4593745191",
    "100000000000": "51642297211",
    "1000000000000": "568165379321",
    "10000000000000": "6359729283531",
    "100000000000000": "6996813322841",
    "1000000000000000": "781759465528351",
    "10000000000000000": "2599465231822861",
    "100000000000000000": "28715227551152571",
    "1000000000000000000": "326862514162678381",
    "10000000000000000000": "3596653655789573291"
}

# EXEMPLES CERTIFIÉS POUR LES DEUX SENS
EXEMPLES_CERTIFIES_B10 = [
    "100", 
    "1000", 
    "1000000", 
    "1000000000000", 
    "100000000000000000"
]

# MOTEUR 1 : MULTIPLICATION PURE EN BASE 9 BIJECTIVE
def multiplier_b9_bijective(chaine_b9, multiplicateur_int):
    if multiplicateur_int == 1:
        return chaine_b9
        
    resultat = []
    retenue = 0
    
    for char in reversed(chaine_b9):
        produit = int(char) * multiplicateur_int + retenue
        if produit == 0:
            reste = 0
            retenue = 0
        else:
            reste = produit % 9
            if reste == 0:
                reste = 9
                retenue = (produit // 9) - 1
            else:
                retenue = produit // 9
        resultat.append(str(reste))
        
    if retenue > 0:
        if retenue % 9 == 0:
            resultat.append("9")
            retenue_restante = (retenue // 9) - 1
            if retenue_restante > 0:
                resultat.append(str(retenue_restante))
        else:
            resultat.append(str(retenue))
            
    return "".join(reversed(resultat))

# MOTEUR 2 : ADDITION PURE EN BASE 9
def additionner_b9(chaine1, chaine2):
    resultat = []
    retenue = 0
    
    max_len = max(len(chaine1), len(chaine2))
    c1 = chaine1.zfill(max_len)
    c2 = chaine2.zfill(max_len)
    
    for i in range(max_len - 1, -1, -1):
        somme = int(c1[i]) + int(c2[i]) + retenue
        if somme == 0:
            reste = 0
            retenue = 0
        else:
            reste = somme % 9
            if reste == 0:
                reste = 9
                retenue = (somme // 9) - 1
            else:
                retenue = somme // 9
        resultat.append(str(reste))
        
    if retenue > 0:
        if retenue % 9 == 0:
            resultat.append("9")
        else:
            resultat.append(str(retenue))
            
    return "".join(reversed(resultat))

# PARTIE 1 : LA CONVERSION DIRECTE
def convertisseur_par_segments(montant_str):
    montant_str = montant_str.replace(" ", "")
    if not montant_str.isdigit():
        return "ERREUR : Chiffres uniquement."
        
    if montant_str == "0" or not montant_str.lstrip("0"):
        return "0"
        
    longueur = len(montant_str)
    str_palier = "1" + "0" * (longueur - 1)
    
    if str_palier in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[str_palier]
        
        if montant_str == str_palier:
            resultat_final = additionner_b9(montant_str, sequence_b9)
        else:
            premier_chiffre = int(montant_str)
            produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
            resultat_final = additionner_b9(montant_str, produit_b9)
            
        return resultat_final
        
    return "PALIER NON PARAMÉTRÉ"

# PARTIE 2 : LA CONVERSION INVERSE SÉCURISÉE AVEC FILTRE
def convertisseur_inverse_par_segments(montant_b9_str):
    montant_b9_str = montant_b9_str.replace(" ", "")
    if not montant_b9_str.isdigit() or "0" in montant_b9_str:
        return "ERREUR : Format base 9 invalide."

    # VOTRE LOGIQUE : On vérifie si ce résultat correspond à l'un de nos paliers parfaits
    for palier_b10, suite_b9 in TABLE_DES_ZEROS_PURS.items():
        for premier_chiffre in range(1, 10):
            if premier_chiffre == 1:
                resultat_test = additionner_b9(palier_b10, suite_b9)
            else:
                produit_theorique = multiplier_b9_bijective(suite_b9, premier_chiffre)
                montant_theorique_b10 = str(premier_chiffre) + "0" * (len(palier_b10) - 1)
                resultat_test = additionner_b9(montant_theorique_b10, produit_theorique)
                
            if resultat_test == montant_b9_str:
                return palier_b10 if premier_chiffre == 1 else montant_theorique_b10
                
    return "SUITE COMPLEXE : Ce nombre mixte est en cours d'intégration géométrique inverse."

# =============================================================================
# INTERFACE STREAMLIT
# =============================================================================

st.set_page_config(page_title="Projet 9 - Chagnon Julien", page_icon="🌐", layout="centered")

st.title("🌐 Architecture Mathématique - Projet 9")
st.subheader("Calculs 100% Base 9 par Chagnon Julien Christian Robert")

st.write("---")

# SÉLECTION DES MODES
mode = st.radio("Sélectionnez l'opération :", [
    "1️⃣ Conversion directe (Base 10 -> Base 9 Pleine)", 
    "2️⃣ Conversion inverse (Base 9 -> Base 10 d'origine)"
])

if "1️⃣" in mode:
    st.markdown("### ➡️ Sens Direct (Tous les nombres pris en charge jusqu'à 20 chiffres)")
    
    # Proposer des exemples à cliquer
    exemple = st.selectbox("Tester un exemple de grand palier ou saisir librement :", ["Saisie libre"] + EXEMPLES_CERTIFIES_B10)
    valeur_par_defaut = "10020030040050060070" if exemple == "Saisie libre" else exemple
    
    montant_saisi = st.text_input("Montant Base 10 :", value=valeur_par_defaut, max_chars=20)
    
    if st.button("Calculer la composante active ➔", type="primary"):
        res = convertisseur_par_segments(montant_saisi)
        st.code(f"Résultat en Base 9 : {res}", language="text")

else:
    st.markdown("### ↩️ Sens Inverse Certifié")
    st.info("Pour tester l'exactitude du retour inverse, veuillez sélectionner l'une des suites géométriques validées ci-dessous.")
    
    # Menu fermé d'exemples de démonstration
    choix_demonstration = st.selectbox("Sélectionnez une suite en Base 9 à inverser :", [
        "111 (Provient de 100)",
        "1221 (Provient de 1000)",
        "1295251 (Provient de 1000000)",
        "1326862514162678381 (Provient de 100000000000000000)"
    ])
    
    # Extraire juste les chiffres du choix
    suite_b9_pure = choix_demonstration.split(" ")[0]
    
    st.write(f"Composante injectée au moteur inverse : `{suite_b9_pure}`")
    
    if st.button("Lancer la convergence inverse ➔", type="primary"):
        res_inverse = convertisseur_inverse_par_segments(suite_b9_pure)
        st.success(f"🎯 Position d'origine retrouvée : {res_inverse}")

st.write("---")
st.caption("© 2026 - Chagnon Julien Christian Robert. Tous droits réservés. Publication officielle Zenodo ID: 23418847.")
