# =============================================================================
# APPLICATION STREAMLIT : ARCHITECTURE MATHÉMATIQUE (BASE 9 BIJECTIVE)
# LOGIQUE SANS TABLE NI PYRAMIDE - SANS AUCUNE INTERFÉRENCE DE ZÉROS
# CONCEPTRICE / CONCEPTEUR : CHAGNON JULIEN CHRISTIAN ROBERT
# =============================================================================

import streamlit as st

# Configuration de la page internet
st.set_page_config(
    page_title="Architecture Mathématique",
    page_icon="🧮",
    layout="centered"
)

# --- MOTEUR DE CALCUL INTERNE (LOGIQUE BIJECTIVE SIMPLIFIÉE) ---

def base10_vers_base9_bijective(montant_b10_str):
    """
    Convertit directement la base 10 en base 9 bijective (alphabet 1 à 9).
    Logique : Chaque fois qu'un reste vaut 0, on le remplace par 9 et on ajuste.
    """
    # Nettoyage complet des espaces ou points pour éviter les bugs
    saisie = montant_b10_str.strip().replace(" ", "").replace(".", "").replace(",", "")
    if not saisie.isdigit():
        return "ERREUR : Saisie Invalide (Entrez uniquement des chiffres)."
    
    nombre = int(saisie)
    if nombre == 0:
        return "0"
        
    digits = []
    while nombre > 0:
        reste = nombre % 9
        if reste == 0:
            digits.append('9')          # Règle bijective : le 0 devient un 9
            nombre = (nombre // 9) - 1  # Ajustement du quotient supérieur
        else:
            digits.append(str(reste))
            nombre //= 9
            
    return "".join(reversed(digits))


def base9_bijective_vers_base10(chaine_b9_str):
    """
    Restaure l'anatomie en base 10 de manière directe et instantanée.
    Logique : Évaluation polynomiale pure de l'alphabet de 1 à 9.
    """
    saisie = chaine_b9_str.strip().replace(" ", "").replace(".", "").replace(",", "")
    if not saisie.isdigit():
        return "ERREUR : Saisie Invalide."
    if '0' in saisie:
        return "ERREUR : Le chiffre 0 est strictement interdit en Base 9 Bijective."
        
    total_base10 = 0
    for caractere in saisie:
        # Évaluation cumulative de la position
        total_base10 = total_base10 * 9 + int(caractere)
        
    return str(total_base10)


# --- INTERFACE GRAPHIQUE STREAMLIT ---

st.title("Architecture Mathématique")
st.subheader("Calculateur Disjoint Évolué — Par Chagnon Julien Christian Robert")
st.markdown("---")

st.markdown("""
Ce système utilise une **arithmétique positionnelle bijective de base 9**. 
L'alphabet numérique y est exclusivement composé des symboles pleins de **1 à 9**, le chiffre 0 y est totalement exclu.
""")

# Création des onglets pour séparer proprement l'Étape 1 et l'Étape 2
onglet1, onglet2 = st.tabs([
    "1️⃣ ÉTAPE 1 : Base 10 ➔ Base 9 Bijective", 
    "2️⃣ ÉTAPE 2 : Base 9 Bijective ➔ Base 10"
])

# --- ONGLET 1 : DE LA BASE 10 À LA BASE 9 ---
with onglet1:
    st.header("Comptabilité en Base 9")
    
    # Utilisation stratégique de text_input pour briser la barrière de précision machine
    saisie_b10 = st.text_input(
        "Saisissez le montant initial (Base 10 standard) :",
        key="input_b10",
        placeholder="Ex: 987654321123456789987654321123456789"
    )
    
    if saisie_b10:
        resultat_b9 = base10_vers_base9_bijective(saisie_b10)
        
        st.info(f"**Longueur saisie :** {len(saisie_b10.strip().replace(' ', ''))} chiffres")
        
        if "ERREUR" in resultat_b9:
            st.error(resultat_b9)
        else:
            st.success("### Résultat Calculé")
            # Zone de texte sélectionnable pour copier facilement le résultat géant
            st.code(resultat_b9, language="text")
            st.markdown(f"**Longueur en Base 9 :** {len(resultat_b9)} chiffres (Alphabet de 1 à 9)")

# --- ONGLET 2 : DE LA BASE 9 À LA BASE 10 ---
with onglet2:
    st.header("Anatomie Restaurée en Base 10")
    
    saisie_b9 = st.text_input(
        "Saisissez le nombre à traiter (Chiffres de 1 à 9 uniquement) :",
        key="input_b9",
        placeholder="Ex: 47749584422891351794458265288476893719"
    )
    
    if saisie_b9:
        resultat_b10 = base9_bijective_vers_base10(saisie_b9)
        
        st.info(f"**Longueur saisie :** {len(saisie_b9.strip().replace(' ', ''))} caractères")
        
        if "ERREUR" in resultat_b10:
            st.error(resultat_b10)
        else:
            st.success("### Anatomie Restaurée")
            st.code(resultat_b10, language="text")
            st.markdown(f"**Longueur Restaurée :** {len(resultat_b10)} chiffres")

# Pied de page de l'application
st.markdown("---")
st.caption("© Architecture Mathématique Appliquée — Tous droits réservés.")
