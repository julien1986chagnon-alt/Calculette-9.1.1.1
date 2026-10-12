import streamlit as st

# ==============================================================================
# CONFIGURATION DE LA PAGE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Convertisseur Base 9 Bijective",
    page_icon="💎",
    layout="centered"
)

# ==============================================================================
# CONFIGURATION : LA GRILLE DES ZÉROS PURS (STRICTEMENT INTACTE)
# ==============================================================================
TABLE_DES_ZEROS_PURS = {
    "10": "1",
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
    "100000000000000": "69968133228841",
    "1000000000000000": "781759465528351",
    "10000000000000000": "2599465231822861",
    "100000000000000000": "28715227551152571",
    "1000000000000000000": "326862514162678381",
    "10000000000000000000": "3596653655789573291"
}

# ==============================================================================
# MOTEURS DE CALCUL (STRICTEMENT INTACTS ET SÉCURISÉS)
# ==============================================================================
def b9_bijective_vers_valeur_base10(chaine_b9):
    valeur = 0
    for idx, char in enumerate(reversed(chaine_b9)):
        valeur += int(char) * (9 ** idx)
    return valeur

def convertisseur_par_segments(montant_depart_str):
    montant_depart_str = montant_depart_str.replace(" ", "")
    if not montant_depart_str.isdigit():
        return "ERREUR SAISIE"
        
    valeur_entiere = int(montant_depart_str)
    somme_zeros_b10 = 0
    longueur = len(montant_depart_str)
    
    for idx, chiffre_char in enumerate(montant_depart_str):
        chiffre = int(chiffre_char)
        exposant = longueur - 1 - idx
        
        if chiffre == 0:
            valeur_palier = 10 ** exposant
            str_palier = str(valeur_palier)
            
            if str_palier in TABLE_DES_ZEROS_PURS:
                chaine_b9 = TABLE_DES_ZEROS_PURS[str_palier]
                somme_zeros_b10 += b9_bijective_vers_valeur_base10(chaine_b9)
                
    montant_final_b10 = valeur_entiere + somme_zeros_b10
    
    if montant_final_b10 == 0:
        return "0"
        
    res_b9 = ""
    n = montant_final_b10
    while n > 0:
        reste = n % 9
        if reste == 0:
            res_b9 = "9" + res_b9
            n = (n // 9) - 1
        else:
            res_b9 = str(reste) + res_b9
            n = n // 9
            
    return res_b9

def convertisseur_inverse_par_segments(montant_b9_str):
    montant_b9_str = montant_b9_str.replace(" ", "")
    if not montant_b9_str.isdigit() or "0" in montant_b9_str:
        return "ERREUR SAISIE"
        
    cible_b9 = int(montant_b9_str)
    bas = 0
    haut = 10000000000000000000
    resultat_b10 = None
    
    while bas <= haut:
        milieu = (bas + haut) // 2
        test_res = convertisseur_par_segments(str(milieu))
        
        if test_res.isdigit():
            test_b9 = int(test_res)
            if test_b9 == cible_b9:
                resultat_b10 = milieu
                break
            elif test_b9 < cible_b9:
                bas = milieu + 1
            else:
                haut = milieu - 1
        else:
            haut = milieu - 1
            
    if resultat_b10 is not None:
        return str(resultat_b10)
    else:
        return "Aucune correspondance exacte trouvée"

# ==============================================================================
# INTERFACE GRAPHIQUE STREAMLIT
# ==============================================================================
st.title("💎 Convertisseur Logique Bijective")
st.caption("Architecture mathématique par Chagnon Julien Christian Robert - Tous droits réservés.")
st.write("---")

# 1. Sélection du sens de calcul via un menu déroulant visuel
choix = st.selectbox(
    "Choisissez le sens de conversion :",
    [
        "1 : Base 10 ➔ Ajouter les décalages (Base 9 sans 0)",
        "2 : Retrouver le nombre d'origine (Inverse en Base 10)"
    ]
)

# 2. Zone de texte pour entrer le nombre
montant_saisi = st.text_input("Tapez le montant à convertir :", placeholder="Exemple: 1256302320")

# 3. Bouton d'action pour lancer le traitement
if st.button("ÉVALUER LA CONVERSION", type="primary"):
    if montant_saisi.strip() == "":
        st.warning("Veuillez saisir un nombre avant de cliquer.")
    else:
        # Nettoyage et routage vers la bonne fonction selon le choix du menu
        if choix.startswith("1"):
            resultat = convertisseur_par_segments(montant_saisi)
            if "ERREUR" in resultat:
                st.error(f"❌ {resultat} : Veuillez entrer uniquement des chiffres.")
            else:
                st.success(f"📈 **RÉSULTAT EN BASE 9 BIJECTIVE :**")
                st.code(resultat, language="text")
        else:
            resultat_inverse = convertisseur_inverse_par_segments(montant_saisi)
            if "ERREUR" in resultat_inverse or "Aucune" in resultat_inverse:
                st.error(f"❌ {resultat_inverse}")
            else:
                st.success(f"🔄 **RETOUR EN BASE 10 D'ORIGINE :**")
                st.code(resultat_inverse, language="text")

# Petit rappel sur la loi mathématique découverte sur LibreOffice
with st.expander("ℹ️ Note de l'architecte sur la structure géométrique"):
    st.write("""
    Chaque segment supérieur de notre grille des zéros purs est généré par l'application stricte du multiplicateur **11** :
    * **1 000** ➔ décalage de **221**
    * **10 000** ➔ \(221 \\times 11\) = **2 431**
    * **100 000** ➔ \(2 431 \\times 11\) = **26 741**
    """)
