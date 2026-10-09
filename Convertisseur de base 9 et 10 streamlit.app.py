# =====================================================================
# CONFIGURATION DE LA PAGE STREAMLIT
# =====================================================================
st.set_page_config(
    page_title="Convertisseur Bijectif",
    page_icon="🔢",
    layout="centered"
)

# =====================================================================
# CONFIGURATION : LA GRILLE DES ZÉROS PURS
# =====================================================================
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

# =====================================================================
# LENGAGE METIER / LOGIQUE DE CALCUL
# =====================================================================
def convertisseur_par_segments(montant_depart_str):
    montant_depart_str = montant_depart_str.replace(" ", "")
    if not montant_depart_str.isdigit():
        return "ERREUR SAISIE"
        
    valeur_entiere = int(montant_depart_str)
    somme_zeros = 0
    longueur = len(montant_depart_str)
    
    for idx, chiffre_char in enumerate(montant_depart_str):
        chiffre = int(chiffre_char)
        exposant = longueur - 1 - idx
        if exposant > 0:
            valeur_palier = 10 ** exposant
            if str(valeur_palier) in TABLE_DES_ZEROS_PURS:
                valeur_zeros = int(TABLE_DES_ZEROS_PURS[str(valeur_palier)])
                somme_zeros += valeur_zeros * chiffre
                
    montant_final = valeur_entiere + somme_zeros
    return str(montant_final)

def convertisseur_inverse_par_segments(montant_b9_str):
    montant_b9_str = montant_b9_str.replace(" ", "")
    if not montant_b9_str.isdigit():
        return "ERREUR SAISIE"
        
    cible = int(montant_b9_str)
    bas = 0
    haut = cible
    resultat_b10 = None
    
    while bas <= haut:
        milieu = (bas + haut) // 2
        test_str = convertisseur_par_segments(str(milieu))
        
        if test_str in ["ERREUR SAISIE", "ERREUR LIMITE"]:
            haut = milieu - 1
            continue
            
        test_valeur = int(test_str)
        
        if test_valeur == cible:
            resultat_b10 = milieu
            break
        elif test_valeur < cible:
            bas = milieu + 1
        else:
            haut = milieu - 1
            
    if resultat_b10 is not None:
        return str(resultat_b10)
    else:
        return "Aucune correspondance exacte trouvée"

# =====================================================================
# INTERFACE UTILISATEUR (STREAMLIT)
# =====================================================================
st.title("🔢 Convertisseur Bijectif par Segments")
st.write("Interface graphique pour la conversion directe et inverse avec gestion des grands nombres.")

st.markdown("---")

# Boutons radio pour sélectionner le mode
mode = st.radio(
    "**Choisissez le sens de conversion :**",
    ("Base 10 ➔ Ajouter les décalages", "Retrouver le nombre d'origine (Inverse)")
)

# Champ de saisie du montant
montant_saisi = st.text_input("**Entrez le montant :**", placeholder="Ex: 1000 ou 1221")

st.markdown("###")

# Bouton d'action
if st.button("Calculer le résultat", type="primary"):
    if not montant_saisi.strip():
        st.warning("⚠️ Veuillez saisir un montant avant de lancer le calcul.")
    else:
        if mode == "Base 10 ➔ Ajouter les décalages":
            resultat = convertisseur_par_segments(montant_saisi)
            if "ERREUR" in resultat:
                st.error(f"❌ {resultat} : Veuillez entrer un nombre entier valide.")
            else:
                st.success(f"📈 **Résultat obtenu :** {resultat}")
        else:
            resultat = convertisseur_inverse_par_segments(montant_saisi)
            if "ERREUR" in resultat or "Aucune" in resultat:
                st.error(f"❌ {resultat}")
            else:
                st.info(f"📉 **Retour Base 10 d'origine :** {resultat}")
