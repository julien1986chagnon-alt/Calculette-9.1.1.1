import streamlit as st

# =============================================================================
# CONFIGURATION DEFINITIVE : LA PYRAMIDE RECTIFIÉE DE CHAGNON JULIEN
# =============================================================================

TABLE_DES_ZEROS_PURS = {
    "10": "1", # CORRECTION : Un seul passage pour 10
    "100": "11",
    "1000": "221",
    "10000": "1221",
    "100000": "127951", # Ligne 100.000 = 127.951
    "1000000": "1318561", # Ligne 1.000.000 = 1.318.561
    "10000000": "13515271", # Ligne 10.000.000 = 13.515.271
    "100000000": "138667981", # Ligne 100.000.000 = 138.667.981
    "1000000000": "1436458891", # Ligne 1.000.000.000 = 1.436.458.891
    "10000000000": "14812158911", # Ligne 10.000.000.000 = 14.812.158.911
    "100000000000": "153933759121", # Ligne 100.000.000.000 = 153.393.759.121
    "1000000000000": "1594372461331", # Ligne 1.000.000.000.000 = 1.594.372.461.331
    "10000000000000": "16648197174641", # Ligne 10.000.000.000.000 = 16.648.197.174.641
    "100000000000000": "174241278932151", # Ligne 100.000.000.000.000 = 174.241.278.932.151
    "1000000000000000": "1826654179353661", # Ligne 1.000.000.000.000.000 = 1.826.654.179.353.661
    "10000000000000000": "19194295983891371", # Ligne 10.000.000.000.000.000 = 19.194.295.983.891.371
    "100000000000000000": "212247366933915181", # Ligne 100.000.000.000.000.000 = 212.247.366.933.915.181
    "1000000000000000000": "2234732147374166991", # Ligne 1.000.000.000.000.000.000 = 2.234.732.147.374.669.991
    "10000000000000000000": "23583153632226848111", # Ligne 10.000.000.000.000.000.000 = 23.583.153.632.226.848.111
    "100000000000000000000": "249524689954496434221", # Ligne 100.000.000.000.000.000.000 = 249.524.689.954.496.434.221
    "1000000000000000000000": "2655772711549571852431" # Ligne à 21 zéros = 2.655.772.711.549.571.852.431
}


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

# MOTEUR 2 : ADDITION PURE EN BASE 9 (AVEC SUPPORT DU 0 DE DÉPART)
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

# CONVERSION DIRECTE ENTIÈREMENT EN BASE 9
def convertisseur_par_segments(montant_str):
    montant_str = montant_str.replace(" ", "")
    if not montant_str.isdigit():
        return "ERREUR : Saisie non numérique"
        
    if montant_str == "0" or not montant_str.lstrip("0"):
        return "0"
        
    premier_chiffre = int(montant_str[0])
    longueur = len(montant_str)
    
    str_palier = "1" + "0" * (longueur - 1)
    
    if str_palier in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[str_palier]
        produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
        resultat_final = additionner_b9(montant_str, produit_b9)
        return resultat_final
        
    return "PALIER NON PARAMÉTRÉ (Limite maximale de 20 chiffres atteinte)"

# =============================================================================
# INTERFACE GRAPHIQUE STREAMLIT UNIFIÉE
# =============================================================================

st.set_page_config(page_title="Projet 9 - Chagnon Julien", page_icon="🌐", layout="centered")

st.title("🌐 Architecture Mathématique - Projet 9")
st.subheader("Calculs 100% Base 9 par Chagnon Julien Christian Robert")

st.markdown("""
Cette application applique les tables de correspondances géométriques de la base 9 bijective rectifiée.
Entrez un montant en Base 10 pour extraire sa composante continue, dense et sans aucun zéro de valeur.
""")

st.write("---")

# Zone de saisie unique
montant_saisi = st.text_input(
    "Entrez le montant en Base 10 à convertir (Jusqu'à 20 chiffres) :", 
    value="10020030040050060070",
    max_chars=20
)

if st.button("Lancer la conversion bijective ➔", type="primary"):
    with st.spinner("Calcul des décalages matriciels..."):
        resultat = convertisseur_par_segments(montant_saisi)
        
        if "ERREUR" in resultat or "NON PARAMÉTRÉ" in resultat:
            st.error(resultat)
        else:
            st.success("Conversion réussie avec succès !")
            st.markdown("### 🎯 COMPOSANTE BASE 9 PLEINE :")
            st.code(resultat, language="text")
            st.caption(f"Longueur du résultat : {len(resultat)} chiffres actifs (de 1 à 9). Aucun déchet numérique.")

st.write("---")
st.caption("© 2026 - Chagnon Julien Christian Robert. Tous droits réservés. Publication officielle Zenodo ID: 23418847.")
