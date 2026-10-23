import streamlit as st

# =====================================================================
# CONFIGURATION DE LA PAGE STREAMLIT
# =====================================================================
st.set_page_config(
    page_title="Convertisseur Base 9 Bijective",
    page_icon="🔢",
    layout="centered"
)

# =====================================================================
# CONFIGURATION : LA GRILLE DES ZÉROS PURS (STRICTEMENT INTACTE)
# =====================================================================
TABLE_DES_ZEROS_PURS = {
    10: "1",
    100: "11",
    1000: "221",
    10000: "2541",
    100000: "27951",
    1000000: "318561",
    10000000: "3515271",
    100000000: "38667981",
    1000000000: "436456891",
    10000000000: "4812158911",
    100000000000: "53933759121",
    1000000000000: "594372461331",
    10000000000000: "6648197174641",
    100000000000000: "74241278932151",
    1000000000000000: "826654179353661",
    10000000000000000: "9194295983891371",
    100000000000000000: "112247366933915181",
    1000000000000000000: "1234732147374166991",
    10000000000000000000: "1358315363226848111",
    100000000000000000000: "14952469554496435221",
    1000000000000000000000: "165572711549571852431",
    10000000000000000000000: "18324599827716391476741",
    100000000000000000000000: "212571719215881416355251"
}


# Mémoire dynamique de l'application (Session State)
if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}

# =====================================================================
# MOTEUR 1 : MULTIPLICATION PURE EN BASE 9 BIJECTIVE
# =====================================================================
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

# =====================================================================
# MOTEUR 2 : ADDITION PURE EN BASE 9 (AVEC SUPPORT DU 0 DE DÉPART)
# =====================================================================
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

# =====================================================================
# PARTIE 1 : LA CONVERSION DIRECTE ENTIÈREMENT EN BASE 9 (CORRIGÉE)
# =====================================================================
def convertisseur_par_segments(montant_str):
    montant_str = montant_str.strip().replace(" ", "")
    if not montant_str.isdigit():
        return "ERREUR SAISIE"
        
    # CORRECTION ICI : On prend uniquement le tout premier caractère pour le multiplicateur
    premier_chiffre = int(montant_str[0])
    longueur = len(montant_str)
    
    str_palier = "1" + "0" * (longueur - 1)
    
    if int(str_palier) in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[int(str_palier)]
        produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
        resultat_final = additionner_b9(montant_str, produit_b9)
        return resultat_final
        
    return "PALIER NON PARAMÉTRÉ"

# =====================================================================
# PARTIE 2 : LA CONVERSION INVERSE (BASE 9 -> BASE 10)
# =====================================================================
def convertisseur_inverse_par_segments(montant_b9_str):
    montant_b9_str = montant_b9_str.strip().replace(" ", "")
    if not montant_b9_str.isdigit() or "0" in montant_b9_str:
        return "ERREUR SAISIE"
        
    cible_b9 = int(montant_b9_str)
    bas = 0
    haut = 10000000000000000000000
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

# =====================================================================
# INTERFACE GRAPHIQUE STREAMLIT
# =====================================================================
st.title("👑 Convertisseur base 9 bijective et 10")
st.caption("Calculateur Disjoint - Alignement des structures de bases numériques")
st.write("---")

choix = st.selectbox(
    "Choisissez le sens de conversion :",
    [
        "1 : Base 10 ➡️ Ajouter les décalages (Calculs 100% Base 9)",
        "2 : Retrouver le nombre d'origine (Inverse en Base 10)"
    ]
)

montant_saisi = st.text_input("Tapez le montant à évaluer :", placeholder="Exemple: 5000")

if st.button("LANCER LE CALCUL", type="primary"):
    if montant_saisi.strip() == "":
        st.warning("Veuillez entrer une valeur.")
    else:
        if choix.startswith("1"):
            resultat = convertisseur_par_segments(montant_saisi)
            if "PALIER" in resultat or "ERREUR" in resultat:
                st.error(f"❌ {resultat}")
            else:
                st.success(f"🏁 **RÉSULTAT EN BASE 9 :**")
                st.code(resultat, language="text")
                st.session_state.memoire_session[resultat] = montant_saisi
        else:
            # --- MODIFICATION APPORTÉE UNIQUEMENT SUR L'AFFICHAGE DU ZÉRO EN BASE 9 ---
            if "0" in montant_saisi.strip().replace(" ", ""):
                st.error("⚠️ Erreur Pureté Bijective : Le chiffre 0 n'existe pas en Base 9 Bijective ! Saisie refusée.")
            else:
                resultat_inverse = convertisseur_inverse_par_segments(montant_saisi)
                if "ERREUR" in resultat_inverse or "Aucune" in resultat_inverse:
                    st.error(f"❌ {resultat_inverse}")
                else:
                    st.success(f"🏁 **RETOUR EN BASE 10 D'ORIGINE :**")
                    st.code(resultat_inverse, language="text")
