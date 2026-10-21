import streamlit as st

# =============================================================================
# MOTEUR DE CALCUL BIJECTIF ET CUMUL DES SÉQUENCES DE JULIEN CHAGNON
# =============================================================================

def addition_verticale_bijective(nb1_str, nb2_str):
    """
    Réalise l'addition en colonne directe selon vos tables.
    Calcule dynamiquement le multiple d'additions de zéros positionnels
    générés pour chaque bloc ou séquence de l'intervalle.
    """
    n1 = nb1_str.strip()
    n2 = nb2_str.strip()
    
    max_len = max(len(n1), len(n2))
    n1 = n1.zfill(max_len)
    n2 = n2.zfill(max_len)
    
    resultat = ""
    retenue = 0
    zeros_de_position_comptes = 0
    
    # Traitement vertical de droite à gauche (votre règle de calcul)
    for i in range(max_len - 1, -1, -1):
        d1 = int(n1[i]) if n1[i] != '0' else 0
        d2 = int(n2[i]) if n2[i] != '0' else 0
        
        somme_colonne = d1 + d2 + retenue
        
        if somme_colonne == 0:
            continue
            
        # Votre engrenage bijective : le passage au rang supérieur évacue le 0
        if somme_colonne >= 9:
            reste = somme_colonne % 9
            if reste == 0:
                chiffre_ici = 9
                retenue = (somme_colonne // 9) - 1
            else:
                chiffre_ici = reste
                retenue = somme_colonne // 9
            zeros_de_position_comptes += 1
        else:
            chiffre_ici = somme_colonne
            retenue = 0
            
        resultat = str(chiffre_ici) + resultat
        
    if retenue > 0:
        resultat = str(retenue) + resultat
        zeros_de_position_comptes += 1

    # Application de votre règle de cascade sur la longueur de la séquence
    total_zeros_cascades = zeros_de_position_comptes * max_len
    
    return resultat, total_zeros_cascades

def dec_vers_base9_bijective(n):
    """ Conversion anatomique respectant votre condition de reste 0 -> 9 """
    if n == 0:
        return ""
    resultat = ""
    while n > 0:
        reste = n % 9
        if reste == 0:
            reste = 9
            n = (n // 9) - 1
        else:
            n = n // 9
        resultat = str(reste) + resultat
    return resultat

def base9_bijective_vers_dec(chaine_b9):
    """ Décodage inverse pour la restauration de la matière numérique """
    if not chaine_b9 or not chaine_b9.isdigit():
        return 0
    n = 0
    for caractere in chaine_b9:
        n = n * 9 + int(caractere)
    return n

# =============================================================================
# INTERFACE EXCLUSIVE DE VOTRE CONVERTISSEUR STREAMLIT
# =============================================================================

st.set_page_config(page_title="Architecture Mathématique", page_icon="📊", layout="centered")

st.title("Calculateur Disjoint Bijectif Pur")
st.caption("Par Chagnon Julien Christian Robert")

st.header("Convertisseur Anatomique Réversible")
st.write("Analyse et décomposition des séquences numériques sans perte d'unité.")

# Zone d'entrée pour le grand nombre initial de départ
nombre_input = st.text_input("Entrez une valeur ou une séquence numérique (ex: 987654321123456789) :", key="conv_unitaire")

if nombre_input:
    if nombre_input.isdigit():
        valeur_dec = int(nombre_input)
        
        # 1. Extraction en Base 9 Bijective selon vos lois
        representation_b9 = dec_vers_base9_bijective(valeur_dec)
        
        # 2. Restauration pour prouver la symétrie parfaite
        restoration_dec = base9_bijective_vers_dec(representation_b9)
        
        # 3. Calcul automatique du cumul des zéros de position de votre pyramide
        # Le programme applique votre logique séquentielle sur la valeur
        _, total_zeros_grille = addition_verticale_bijective(representation_b9, "0")
        
        # Affichage des résultats
        st.success(f"**Anatomie extraite (Base 9 Bijective) :** `{representation_b9}`")
        st.info(f"**Anatomie Restaurée en Base 10 :** `{restoration_dec}`")
        
        # Affichage de votre compteur de zéros cumulés pour chaque bloc
        st.metric(label="Cumul des zéros de position (Loi des séquences)", value=f"{total_zeros_grille}")
        st.markdown("💡 *Ce montant comptabilise les passages de zéros calculés par le multiple de vos blocs de structure.*")
        
        if valeur_dec == restoration_dec:
            st.markdown("✨ **SYMÉTRIE PARFAITE :** Le retour à la valeur initiale est validé au chiffre près.")
    else:
        st.error("Veuillez n'entrer que des chiffres.")
