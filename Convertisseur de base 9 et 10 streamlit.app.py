import streamlit as st

# =================================================================
# METADONNÉES DE LA PAGE & DROITS RÉSERVÉS DANS L'ONGLET
# =================================================================
st.set_page_config(
    page_title="Architecture Mathématique - J.C.R. Chagnon",
    page_icon="🔢",
    layout="centered"
)

# TABLE DES ZEROS PURS STRICTEMENT CONFORME
TABLE_DES_ZEROS_PURS = {
    "10": "11",
    "100": "111",
    "1000": "1221",
    "10000": "12541",
    "100000": "127951",
    "1000000": "1318561",
    "10000000": "13512271",
    "100000000": "138667981",
    "1000000000": "1436458381",
    "10000000000": "14812158911",
    "100000000000": "153833759121",
    "1000000000000": "1594372461321",
    "10000000000000": "16548187174641",
    "100000000000000": "172141278522151",
    "1000000000000000": "182654179353661",
    "10000000000000000": "1919429558388137",
    "100000000000000000": "212241366911915181",
    "1000000000000000000": "2234732747374166991",
    "10000000000000000000": "2358915363222681811",
    "100000000000000000000": "2495244995464539221"
}

# =================================================================
# ALGORITHMES ET MOTEURS LOGIQUES ORIGINAUX
# =================================================================

def multiplier_b9_bijective(chaine_b9, multiplicateur_int):
    if multiplicateur_int == 0:
        return "0"
    resultat = []
    retenue = 0
    for chiffre in reversed(chaine_b9):
        produit = int(chiffre) * multiplicateur_int + retenue
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
        resultat.append(str(retenue))
    return "".join(reversed(resultat))

def convertisseur_par_segments(montant_str):
    montant_str = str(montant_str).strip().replace(" ", "").replace(",", "").replace(".", "").replace("'", "")
    if not montant_str.isdigit():
        return "ERREUR : Saisie non numérique"
    if montant_str == "0" or not montant_str.lstrip("0"):
        return "0"
    if len(montant_str) == 1:
        return montant_str
        
    premier_chiffre = int(montant_str[0])
    longueur = len(montant_str)
    str_palier = "1" + "0" * (longueur - 1)
    
    if str_palier in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[str_palier]
        if premier_chiffre == 1 and montant_str == str_palier:
            return multiplier_b9_bijective(sequence_b9, premier_chiffre)
        else:
            produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
            reste_montant = str(int(montant_str) - (premier_chiffre * int(str_palier)))
            if int(reste_montant) > 0:
                return additionner_b9(produit_b9, convertisseur_par_segments(reste_montant))
            else:
                return produit_b9
    else:
        return "PALIER NON PARAMETRE (Limite maximale de la grille atteinte)"

def est_inferieur_ou_egal_b9(chaine1, chaine2):
    if len(chaine1) != len(chaine2):
        return len(chaine1) < len(chaine2)
    return chaine1 <= chaine2

def convertisseur_base9_vers_base10(chaine_b9_cible):
    chaine_b9_cible = str(chaine_b9_cible).strip().replace(" ", "")
    if not chaine_b9_cible:
        return "0"
    if not all(c in "123456789" for c in chaine_b9_cible):
        return "ERREUR : La chaîne contient un '0' ou un caractère invalide"
    if len(chaine_b9_cible) == 1:
        return chaine_b9_cible

    paliers_decimaux = sorted([int(k) for k in TABLE_DES_ZEROS_PURS.keys()], reverse=True)
    montant_decimale_cumul = 0
    
    for palier in paliers_decimaux:
        for chiffre_test in range(9, -1, -1):
            test_valeur_decimale = montant_decimale_cumul + (chiffre_test * palier)
            if test_valeur_decimale == 0:
                continue
            resultat_b9_test = convertisseur_par_segments(str(test_valeur_decimale))
            if est_inferieur_ou_egal_b9(resultat_b9_test, chaine_b9_cible):
                montant_decimale_cumul = test_valeur_decimale
                break
                
    for unite_test in range(9, -1, -1):
        test_valeur_decimale = montant_decimale_cumul + unite_test
        resultat_b9_test = convertisseur_par_segments(str(test_valeur_decimale))
        if resultat_b9_test == chaine_b9_cible:
            return str(test_valeur_decimale)
            
    return str(montant_decimale_cumul)

# =================================================================
# INTERFACE GRAPHIQUE STREAMLIT
# =================================================================

st.title("🔢 Architecture Mathématique")
st.subheader("Moteur Double : Base 10 <=> Base 9 Bijective")
st.caption("Par Chagnon Julien Christian Robert")

st.divider()

# Sélection du sens de conversion via des boutons radio
sens = st.radio(
    "Choisissez le sens de la conversion :",
    ("Base 10 ➔ Base 9 bijective", "Base 9 bijective ➔ Base 10")
)

# Utilisation d'un formulaire pour capturer la validation
with st.form(key="conversion_form"):
    if sens == "Base 10 ➔ Base 9 bijective":
        valeur_saisie = st.text_input("Entrez le montant en Base 10 :", placeholder="Ex: 100020003000")
    else:
        valeur_saisi = st.text_input("Entrez le nombre en Base 9 (chiffres de 1 à 9 uniquement) :", placeholder="Ex: 153861888446")
        
    bouton_valider = st.form_submit_button(label="Calculer la conversion")

# Traitement du calcul lors de l'appui sur le bouton
if bouton_valider and valeur_saisie:
    if sens == "Base 10 ➔ Base 9 bijective":
        resultat = convertisseur_par_segments(valeur_saisie)
        
        if "ERREUR" in resultat or "PALIER" in resultat:
            st.error(f"❌ {resultat}")
        else:
            st.success("### 💎 Composante Base 9 Pleine :")
            st.code(resultat, language="text")
            st.info(f"📏 **Longueur du résultat :** {len(resultat)} chiffres (Aucun zéro).")
            
    else:
        resultat = convertisseur_base9_vers_base10(valeur_saisie)
        
        if "ERREUR" in resultat:
            st.error(f"❌ {resultat}")
        else:
            st.success("### 💎 Équivalent Base 10 Entier :")
            st.code(resultat, language="text")

st.divider()

# =================================================================
# SECTION MENTION LEGALE - DROITS RESERVES
# =================================================================
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.85em; margin-top: 50px;">
        © Tous droits réservés à <b>Julien Christian Robert Chagnon</b>. 
        <br><i>Configuration Définitive : La Pyramide Rectifiée.</i>
    </div>
    """, 
    unsafe_allow_html=True
)
