import streamlit as st

# =============================================================================
# 1. LOGIQUE BIJECTIVE INTERNE : LE CALCUL VERTICAL DE JULIEN CHAGNON
# =============================================================================

def addition_verticale_julien(nb1_str, nb2_str):
    """
    Réalise l'addition en colonne verticale directe (de droite à gauche).
    Conserve et comptabilise le multiple d'additions de zéros de position 
    générés par les décalages de blocs (1000, 2000, etc.) selon vos grilles.
    """
    # Nettoyage des entrées
    n1 = nb1_str.strip()
    n2 = nb2_str.strip()
    
    # Aligner les longueurs par la gauche pour poser le calcul en colonne
    max_len = max(len(n1), len(n2))
    n1 = n1.zfill(max_len)
    n2 = n2.zfill(max_len)
    
    resultat = ""
    retenue = 0
    zeros_de_position_comptes = 0
    
    # Parcours vertical colonne par colonne, de droite à gauche
    for i in range(max_len - 1, -1, -1):
        # On extrait la valeur pleine (de 1 à 9)
        d1 = int(n1[i]) if n1[i] != '0' else 0
        d2 = int(n2[i]) if n2[i] != '0' else 0
        
        # Somme de la colonne courante avec la retenue précédente
        somme_colonne = d1 + d2 + retenue
        
        if somme_colonne == 0:
            if i == max_len - 1: # Si l'utilisateur a entré 0
                continue
        
        # Règle d'engrenage bijective de Julien (quand on atteint ou dépasse le rang 9)
        if somme_colonne >= 9:
            reste = somme_colonne % 9
            if reste == 0:
                chiffre_ici = 9
                retenue = (somme_colonne // 9) - 1
            else:
                chiffre_ici = reste
                retenue = somme_colonne // 9
                
            # Accumulation des passages provoquant un décalage de rang
            zeros_de_position_comptes += 1
        else:
            chiffre_ici = somme_colonne
            retenue = 0
            
        resultat = str(chiffre_ici) + resultat
        
    # Si une retenue finale subsiste à l'extrémité gauche
    if retenue > 0:
        resultat = str(retenue) + resultat
        zeros_de_position_comptes += 1

    # Calcul du multiple d'additions de zéros en cascade par rapport à l'échelle du bloc
    # Plus le nombre est grand (centaines, milliers), plus l'effet de cascade se multiplie
    facteur_echelle = max_len
    total_zeros_cascades = zeros_de_position_comptes * facteur_echelle
    
    return resultat, total_zeros_cascades

# Fonctions de support pour la conversion anatomique
def dec_vers_base9_bijective(n):
    if n == 0: return ""
    res = ""
    while n > 0:
        reste = n % 9
        if reste == 0:
            reste = 9
            n = (n // 9) - 1
        else:
            n = n // 9
        res = str(reste) + res
    return res

def base9_bijective_vers_dec(chaine_b9):
    if not chaine_b9 or not chaine_b9.isdigit(): return 0
    n = 0
    for c in chaine_b9:
        n = n * 9 + int(c)
    return n

# =============================================================================
# 2. INTERFACE GRAPHIQUE STREAMLIT : VOTRE ARCHITECTURE
# =============================================================================

st.set_page_config(page_title="Architecture Mathématique", page_icon="🧮", layout="centered")

st.title("Calculateur Disjoint Bijectif Pur")
st.caption("Par Chagnon Julien Christian Robert")

# Vos différents onglets
onglet1, onglet2, onglet3 = st.tabs([
    "📊 Convertisseur Réversible", 
    "🧮 Calculatrice Verticale & Cumul", 
    "🔐 Encodeur Alphanumérique Base 35"
])

# --- ONGLET 1 : LE CONVERTISSEUR ---
with onglet1:
    st.header("Convertisseur Anatomique Réversible")
    st.write("Vérification de la réversibilité absolue de la matière numérique sur de grands entiers.")
    
    nombre_input = st.text_input("Entrez un grand nombre en Base 10 (ex: 987654321123456789) :", key="conv_b10")
    if nombre_input and nombre_input.isdigit():
        valeur_dec = int(nombre_input)
        representation_b9 = dec_vers_base9_bijective(valeur_dec)
        restoration_dec = base9_bijective_vers_dec(representation_b9)
        
        st.success(f"**Anatomie extraite (Base 9 Bijective) :** `{representation_b9}`")
        st.info(f"**Restauration en Base 10 :** `{restoration_dec}`")
        if int(nombre_input) == restoration_dec:
            st.markdown("✨ **SYMÉTRIE PARFAITE :** Aucune unité perdue en chemin.")

# --- ONGLET 2 : VOTRE CALCULATRICE AVEC COMPTEUR DE ZÉROS ---
with onglet2:
    st.header("Calculatrice Positionnelle Directe")
    st.write("Calcule verticalement de droite à gauche en comptabilisant le multiple d'additions de zéros.")
    
    col1, col2 = st.columns(2)
    with col1:
        nb1_input = st.text_input("Premier nombre (Base 9) :", value="121", key="julien_nb1")
    with col2:
        nb2_input = st.text_input("Second nombre (Base 9) :", value="99", key="julien_nb2")
        
    if nb1_input and nb2_input:
        if nb1_input.isdigit() and nb2_input.isdigit():
            # Exécution de votre algorithme d'addition en colonne
            resultat_calcul, zeros_generes = addition_verticale_julien(nb1_input, nb2_input)
            
            st.success(f"**Résultat de l'addition en colonne :** `{resultat_calcul}`")
            
            # Affichage de votre loi de proportionnalité des zéros positionnels
            st.info(f"🌟 **Analyse de la Grille :** Il y a un cumul de **{zeros_generes} zéros de position** comptabilisés pour ce bloc.")
            st.markdown("💡 *Ce multiple reflète la cascade d'additions de zéros de la dernière ligne observée sur votre tableur.*")
        else:
            st.error("Veuillez n'entrer que des chiffres.")

# --- ONGLET 3 : ENCODEUR BASE 35 ---
with onglet3:
    st.header("Encodeur Cryptographique Symétrique Base 35")
    st.write("Fusionne les 9 chiffres pleins et les 26 lettres de l'alphabet.")
    
    message = st.text_area("Votre message en clair :", value="MESSAGE SECRET")
    c1, c2 = st.columns(2)
    with c1:
        nombre_secret = st.number_input("Nombre secret (Clé 1) :", min_value=1, value=11)
    with c2:
        mot_secret = st.text_input("Mot secret (Clé 2) :", value="CLE")
        
    if st.button("Générer le flux encodé"):
        if message and mot_secret:
            alphabet_b35 = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            flux_liste = []
            cle_somme = nombre_secret + sum(ord(c) for c in mot_secret)
            
            for i, char in enumerate(message.upper()):
                if char in alphabet_b35:
                    idx_actuel = alphabet_b35.index(char)
                    nouvel_idx = (idx_actuel + cle_somme + i) % 35
                    flux_liste.append(alphabet_b35[nouvel_idx])
                elif char == " ":
                    flux_liste.append("-")
                else:
                    flux_liste.append(char)
            st.success(f"🔒 **FLUX ENCODÉ SÉCURISÉ :** `{''.join(flux_liste)}`")

