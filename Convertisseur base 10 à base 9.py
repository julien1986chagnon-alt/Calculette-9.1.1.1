import streamlit as st

# =====================================================================
# LA GRILLE DES ZÉROS PURS DE TES PALIERS (ISSUE DE TON ÉCRAN)
# =====================================================================
TABLE_DES_ZEROS_PURS = {
    10: "1",
    100: "11",
    1000: "212",
    10000: "2332",
    100000: "25652",
    1000000: "283272",
    10000000: "3954679",
    100000000: "44612579",
    1000000000: "491738479",
    10000000000: "5519234379",
    100000000000: "61722578279",
    1000000000000: "678948472179",
    10000000000000: "7579544293979",
    100000000000000: "84485587344879",
    1000000000000000: "9345137789853679",
    10000000000000000: "113796526799491579",
    100000000000000000: "1252872795914417479",
    1000000000000000000: "13782711866165193379",
    10000000000000000000: "152719831637827237279" # Ligne 20 de ton tableau
}

def addition_bijective_base9(a_str, b_str):
    """Effectue l'addition en colonne pure en base 9 bijective (chiffres de 1 à 9)."""
    i, j = len(a_str) - 1, len(b_str) - 1
    retenue = 0
    resultat = []
    while i >= 0 or j >= 0 or retenue > 0:
        chiffre_a = int(a_str[i]) if i >= 0 else 0
        chiffre_b = int(b_str[j]) if j >= 0 else 0
        somme = chiffre_a + chiffre_b + retenue
        if somme == 0 and i < 0 and j < 0:
            break
        reste = somme % 9
        if reste == 0:
            chiffre_final = 9
            retenue = (somme - 1) // 9
        else:
            chiffre_final = reste
            retenue = somme // 9
        resultat.append(str(chiffre_final))
        i -= 1
        j -= 1
    return "".join(reversed(resultat))

def convertisseur_par_segments(nombre_depart_str):
    nombre_depart_str = nombre_depart_str.replace(" ", "")
    
    if not nombre_depart_str.isdigit():
        return "ERREUR_SAISIE", "Erreur : Tu devez taper uniquement des chiffres !"
        
    valeur_entiere = int(nombre_depart_str)
    limite_strict_superieure = 1000000000000000000000 # 1 000 milliards de milliards
    
    if valeur_entiere >= limite_strict_superieure:
        return "ERREUR_LIMITE", "🚫 Impossible d'aller au-delà ! Ce montant dépasse la limite de 999 milliards de milliards."

    somme_zeros_b9 = "0"
    longueur = len(nombre_depart_str)
    
    for idx, chiffre_char in enumerate(nombre_depart_str):
        chiffre = int(chiffre_char)
        if chiffre == 0:
            continue
            
        exposant = longueur - 1 - idx
        if exposant > 0:
            valeur_palier = 10 ** exposant
            if valeur_palier in TABLE_DES_ZEROS_PURS:
                zeros_du_palier = TABLE_DES_ZEROS_PURS[valeur_palier]
                for _ in range(chiffre):
                    somme_zeros_b9 = addition_bijective_base9(somme_zeros_b9, zeros_du_palier)
                    
    # L'addition finale se fait ENTIÈREMENT avec ta fonction bijective base 9
    montant_final_b9 = addition_bijective_base9(nombre_depart_str, somme_zeros_b9)
    
    return somme_zeros_b9, montant_final_b9

# =====================================================================
# CODE DE L'INTERFACE WEB STREAMLIT
# =====================================================================
st.set_page_config(page_title="Convertisseur Base 9 Bijective", page_icon="🧮")

st.title("🧮 Mon Convertisseur Base 10 vers Base 9 Bijective")
st.write("Ce système analyse vos nombres par segments et calcule les zéros cumulés sans utiliser le chiffre 0.")

# La boîte de saisie blanche sur le site web
montant_saisi = st.text_input("Entrez le montant de ton choix :", value="17545")

# Le bouton cliquable
if st.button("Lancer le calcul"):
    zeros_comptabilises, resultat_total = convertisseur_par_segments(montant_saisi)
    
    if zeros_comptabilises in ["ERREUR_LIMITE", "ERREUR_SAISIE"]:
        st.error(resultat_total)
    else:
        st.subheader("📊 Résultats :")
        st.info(f"**Montant que TU as mis :** {montant_saisi}")
        st.success(f"**Segment des zéros accumulés :** {zeros_comptabilises}")
        st.metric(label="Montant final de ta grille", value=resultat_total)
