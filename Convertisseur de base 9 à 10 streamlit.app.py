# =============================================================================
# VERSION STREAMLIT - INTERFACE INTÉGRALE ET 100% AUTONOME (SANS TRICHE)
# NOM DU PROJET : ARCHITECTURE MATHÉMATIQUE PAR CHAGNON JULIEN CHRISTIAN ROBERT
# =============================================================================

import streamlit as st

st.set_page_config(page_title="Architecture Mathématique", page_icon="🔢", layout="centered")

# Le tableur officiel strictement complet (Lignes 1 à 21 de votre écran)
TABLEUR_PASSAGES_ZERO = {
    10: 1,                       
    100: 11,                     
    1000: 221,                   
    10000: 2541,                 
    100000: 27951,               
    1000000: 318561,             
    10000000: 3515271,           
    100000000: 38667981,         
    1000000000: 436458891,       
    10000000000: 4812158911,     
    100000000000: 53933759121,   
    1000000000000: 594372461331, 
    10000000000000: 6648197174641, 
    100000000000000: 74241278932151, 
    1000000000000000: 826654179353661, 
    10000000000000000: 9194295983891371, 
    100000000000000000: 112247366933915181, 
    1000000000000000000: 1234732147374166991, 
    10000000000000000000: 13583153632226848111, 
    100000000000000000000: 149524689954496439221, 
    1000000000000000000000: 1655772711549571852431
}

def addition_comptable_base9(str_n1, str_n2):
    val1 = 0
    for c in str_n1: val1 = val1 * 9 + int(c)
    val2 = 0
    for c in str_n2: val2 = val2 * 9 + int(c)
    somme = val1 + val2
    if somme == 0: return "0"
    digits = []
    while somme > 0:
        reste = somme % 9
        if reste == 0: digits.append('9'); somme = (somme // 9) - 1
        else: digits.append(str(reste)); somme //= 9
    return "".join(reversed(digits))

def executer_etape_1(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "").replace(".", "")
    longueur = len(saisie)
    somme_zeros_brute = 0
    lignes_detail = []
    
    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        if chiffre > 0:
            p10 = 10 ** (longueur - 1 - i)
            if p10 in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[p10]
                partiel = chiffre * ref_tableur
                somme_zeros_brute += partiel
                
                val1 = 0
                for c in str(partiel): val1 = val1 * 9 + int(c)
                digits_p = []
                while val1 > 0:
                    r = val1 % 9
                    if r == 0: digits_p.append('9'); val1 = (val1 // 9) - 1
                    else: digits_p.append(str(r)); val1 //= 9
                partiel_b9 = "".join(reversed(digits_p)) if partiel > 0 else "0"
                lignes_detail.append(f"Rang {p10:,} ➔ {chiffre} x {ref_tableur:,} = {partiel_b9} zéros (en Base 9)")
            else:
                if p10 == 1:
                    lignes_detail.append(f"Rang 1 ➔ {chiffre} x 0 = 0 zéro")
    
    str_zeros_b9 = addition_comptable_base9(str(somme_zeros_brute), "0")
    str_montant_b9 = addition_comptable_base9(saisie, "0")
    resultat_final_b9 = addition_comptable_base9(str_montant_b9, str_zeros_b9)
    return str_zeros_b9, resultat_final_b9, lignes_detail

def b9_bijective_vers_quantite(chaine_b9):
    total = 0
    for c in chaine_b9: total = total * 9 + int(c)
    return total

def calculer_zeros_pour_base10(montant_b10_str):
    longueur = len(montant_b10_str)
    total_zeros = 0
    for i, chiffre_str in enumerate(montant_b10_str):
        chiffre = int(chiffre_str)
        if chiffre > 0:
            p10 = 10 ** (longueur - 1 - i)
            if p10 in TABLEUR_PASSAGES_ZERO: total_zeros += chiffre * TABLEUR_PASSAGES_ZERO[p10]
    return total_zeros

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip().replace(" ", "").replace(".", "")
    val_cible = b9_bijective_vers_quantite(saisie)
    
    bas, haut, solution = 1, 9999999999999999999999, None
    while bas <= haut:
        milieu = (bas + haut) // 2
        str_milieu = str(milieu)
        longueur = len(str_milieu)
        sz = 0
        for i, cs in enumerate(str_milieu):
            ch = int(cs)
            if ch > 0:
                p10 = 10 ** (longueur - 1 - i)
                if p10 in TABLEUR_PASSAGES_ZERO: sz += ch * TABLEUR_PASSAGES_ZERO[p10]
        candidat_b9 = addition_comptable_base9(str_milieu, addition_comptable_base9(str(sz), "0"))
        if candidat_b9 == saisie: solution = milieu; break
        val_cand = 0
        for c in candidat_b9: val_cand = val_cand * 9 + int(c)
        if val_cand < val_cible: bas = milieu + 1
        else: haut = milieu - 1
    return solution

st.title("🔢 Architecture Mathématique")
st.caption("Par Chagnon Julien Christian Robert")
st.markdown("---")

mode = st.radio("Action :", ("ÉTAPES 1 : Calcul de Base 10 vers Base 9", "ÉTAPES 2 : Calcul de Base 9 vers Base 10"))
st.markdown("---")

if "ÉTAPES 1" in mode:
    saisie_b10 = st.text_input("Montant Base 10 :", placeholder="Exemple : 1444444")
    saisie_propre = saisie_b10.strip().replace(" ", "").replace(".", "")
    if saisie_propre:
        if len(saisie_propre) > 18: st.error("⚠️ Max 18 chiffres.")
        elif not saisie_propre.isdigit(): st.error("❌ Entrez des chiffres.")
        else:
            zeros, res, details = executer_etape_1(saisie_propre)
            for l in details: st.text(l)
            st.markdown("---")
            st.success(f"📈 **Passages zéro extraits :** {zeros}")
            st.info(f"✅ **RÉSULTAT COMPTABILISÉ :** {res}")
else:
    saisie_b9 = st.text_input("Nombre Base 9 :", placeholder="Exemple : 1912723")
    saisie_propre = saisie_b9.strip().replace(" ", "").replace(".", "")
    if saisie_propre:
        if len(saisie_propre) > 18: st.error("⚠️ Max 18 chiffres.")
        elif '0' in saisie_propre: st.error("❌ Le 0 est interdit.")
        else:
            st.success(f"✅ **ANATOMIE RESTAURÉE BASE 10 :** {executer_etape_2(saisie_propre)}")

