import streamlit as st

# ==============================================================================
# CONFIGURATION DÉFINITIVE : LA PYRAMIDE RECTIFIÉE DE CHAGNON JULIEN
# ==============================================================================

TABLE_DES_ZEROS_PURS = {
    "10": "11", # 10 = 1 passages zéro
    "100": "111", # 100 = 11 passages zéro
    "1000": "1221", # 1.000 = 221 passages zéro
    "10000": "12541", # 10.000 = 2.541 passages zéro
    "100000": "127951", # 100.000 = 27.951 passages zéro
    "1000000": "1318561", # 1.000.000 = 318.561 passages zéro
    "10000000": "13515271", # 10.000.000 = 3.515.271 passages zéro
    "100000000": "138667981", # 100.000.000 = 38.667.981 passages zéro
    "1000000000": "1436458891", # 1.000.000.000 = 436.458.891 passages zéro
    "10000000000": "14812158911", # 10.000.000.000 = 4.812.158.911 passages zéro
    "100000000000": "153933759121", # 100.000.000.000 = 53.933.759.121 passages zéro
    "1000000000000": "1594372461331", # 1.000.000.000.000 = 594.372.461.331 passages zéro
    "10000000000000": "16648197174641", # 10.000.000.000.000 = 6.648.197.174.641 passages zéro
    "100000000000000": "174241278932151", # 100.000.000.000.000 = 74.241.278.932.151 passages zéro
    "1000000000000000": "1826654179353661", # 1.000.000.000.000.000 = 826.654.179.353.661 passages zéro
    "10000000000000000": "19194295983891371", # 10.000.000.000.000.000 = 9.194.295.983.891.371 passages zéro
    "100000000000000000": "212247366933915181", # 100.000.000.000.000.000 = 112.247.366.933.915.181 passages zéro
    "1000000000000000000": "2234732147374166991", # 1.000.000.000.000.000.000 = 1.234.732.147.374.166.991 passages zéro
    "10000000000000000000": "23583153632226848111", # 10.000.000.000.000.000.000 = 13.583.153.632.226.848.111 passages zéro
    "100000000000000000000": "249524689954496439221", # 100.000.000.000.000.000.000 = 149.524.689.954.496.439.221 passages zéro
    "1000000000000000000000": "2655772711549571852431" # 1.000.000.000.000.000.000.000 = 1.655.772.711.549.571.852.431 passages zéro
}

# ==============================================================================
# MOTEUR 1 : MULTIPLICATION PURE EN BASE 9 BIJECTIVE
# ==============================================================================
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

# ==============================================================================
# MOTEUR 2 : ADDITION PURE EN BASE 9 (AVEC SUPPORT DU 0 DE DÉPART)
# ==============================================================================
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

# ==============================================================================
# CONVERSION DIRECTE ENTIÈREMENT EN BASE 9 (CORRIGÉE ET FIABILISÉE)
# ==============================================================================
def convertisseur_par_segments(montant_str):
    # Nettoyage rigoureux des espaces insérés automatiquement par Streamlit
    montant_str = str(montant_str).strip().replace(" ", "").replace(",", "").replace(".", "")
    
    if not montant_str.isdigit():
        return "ERREUR : Saisie non numérique"
        
    if montant_str == "0" or not montant_str.lstrip("0"):
        return "0"
        
    premier_chiffre = int(montant_str[0])
    longueur = len(montant_str)
    
    str_palier = "1" + "0" * (longueur - 1)
    
    if str_palier in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[str_palier]
        
        # CAS 1 : Puissance de 10 PURE (Ex: 1000... sans autre chiffre à droite)
        if premier_chiffre == 1 and montant_str == str_palier:
            # Correction majeure : Plus d'addition parasite, on applique seulement la multiplication
            return multiplier_b9_bijective(sequence_b9, premier_chiffre)
            
        # CAS 2 : Nombre COMPOSITE (Ex: 15000... ou 3000...)
        else:
            produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
            
            # Isolement du reste numérique pour la récursion
            reste_montant = str(int(montant_str) - (premier_chiffre * int(str_palier)))
            
            # S'il reste une valeur à calculer à droite, on l'ajoute bijectivement
            if int(reste_montant) > 0:
                return additionner_b9(produit_b9, convertisseur_par_segments(reste_montant))
            return produit_b9
            
    return "PALIER NON PARAMÉTRÉ (Limite maximale de la grille atteinte)"

# ==============================================================================
# INTERFACE GRAPHIQUE STREAMLIT UNIFIÉE
# ==============================================================================
st.set_page_config(page_title="Projet 9 - Chagnon Julien", page_icon="🔢", layout="centered")

st.title("🔢 Architecture Mathématique - Projet 9")
st.subheader("Calculs 100% Base 9 par Chagnon Julien Christian Robert")

st.markdown("""
Cette application applique les tables de correspondances géométriques de la base 9 bijective rectifiée.
Entrez un montant en Base 10 pour extraire sa composante continue, dense et sans aucun zéro de valeur.
""")

st.write("---")

# Zone de saisie unique
montant_saisi = st.text_input(
    "Entrez le montant en Base 10 à convertir (Jusqu'à 22 chiffres) :",
    value="100000000000000000", # Valeur par défaut à 18 chiffres (10¹⁷)
    max_chars=22
)

if st.button("Lancer la conversion bijective ➔", type="primary"):
    with st.spinner("Calcul des décalages matriciels..."):
        # Appel du moteur corrigé
        resultat = convertisseur_par_segments(montant_saisi)
        
    if "ERREUR" in resultat or "PALIER" in resultat:
        st.error(resultat)
    else:
        st.success("Conversion réussie avec succès !")
        st.markdown("### 🔴 COMPOSANTE BASE 9 PLEINE :")
        st.code(resultat, language="text")
        st.caption(f"Longueur du résultat : {len(resultat)} chiffres actifs (de 1 à 9). Aucun déchet numérique.")
