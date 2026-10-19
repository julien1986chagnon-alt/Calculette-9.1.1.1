# =============================================================================
# APPLICATION STREAMLIT : ARCHITECTURE MATHÉMATIQUE (VERSION DÉCIMALE NEUTRE)
# LOGIQUE SANS INTERFÉRENCE DE ZÉROS - PRÉCISION ENTIÈRE COUPLÉE
# CONCEPTEUR : CHAGNON JULIEN CHRISTIAN ROBERT
# =============================================================================

import streamlit as st

# Configuration de la page internet
st.set_page_config(
    page_title="Architecture Mathématique",
    page_icon="🧮",
    layout="centered"
)

# --- MOTEUR DE CALCUL INTERNE (LOGIQUE BIJECTIVE NEUTRE SPATIAL) ---

def executer_etape_1(montant_b10_str):
    """
    Convertit la base 10 en base 9 bijective (alphabet 1 à 9).
    Traite la virgule comme un simple marqueur visuel sans calcul décimal.
    """
    saisie = montant_b10_str.strip().replace(" ", "").replace(".", ",")
    
    # Si c'est un nombre à virgule commençant par 0,
    if saisie.startswith("0,"):
        segment_chiffres = saisie[2:] # On isole les chiffres APRÈS le 0,
        if not segment_chiffres.isdigit():
            return "ERREUR : Saisie Invalide."
            
        nombre = int(segment_chiffres)
        if nombre == 0:
            return "0,0"
            
        digits = []
        while nombre > 0:
            reste = nombre % 9
            if reste == 0:
                digits.append('9')
                nombre = (nombre // 9) - 1
            else:
                digits.append(str(reste))
                nombre //= 9
        
        # On recolle le 0, visuel au tout début
        return "0密" + "".join(reversed(digits))
        
    else:
        # --- MONDE DES ENTIERS STANDARDS ---
        saisie_nettoye = saisie.replace(",", "")
        if not saisie_nettoye.isdigit():
            return "ERREUR : Saisie Invalide."
        nombre = int(saisie_nettoye)
        if nombre == 0:
            return "0"
        digits = []
        while nombre > 0:
            reste = nombre % 9
            if reste == 0:
                digits.append('9')
                nombre = (nombre // 9) - 1
            else:
                digits.append(str(reste))
                nombre //= 9
        return "".join(reversed(digits))


def executer_etape_2(chaine_b9_str):
    """
    Restaure l'anatomie en base 10 à partir de la base 9 bijective.
    Retire le 0, visuel pour calculer l'entier pur, puis le remet à la fin.
    """
    saisie = chaine_b9_str.strip().replace(" ", "").replace(".", ",")
    
    if saisie.startswith("0,"):
        segment_chiffres = saisie[2:] # On isole les chiffres de 1 à 9
        if not segment_chiffres.isdigit() or '0' in segment_chiffres:
            return "ERREUR : Le chiffre 0 est interdit dans l'alphabet bijective."
            
        total_base10 = 0
        for caractere in segment_chiffres:
            total_base10 = total_base10 * 9 + int(caractere)
            
        # On réinjecte le 0, visuel devant la réponse restaurée
        return "0," + str(total_base10)
        
    else:
        # --- MONDE DES ENTIERS STANDARDS ---
        if not saisie.isdigit() or '0' in saisie:
            return "ERREUR : Saisie Invalide ou présence de 0."
        total_base10 = 0
        for caractere in saisie:
            total_base10 = total_base10 * 9 + int(caractere)
        return str(total_base10)


# --- INTERFACE GRAPHIQUE STREAMLIT ---

st.title("Architecture Mathématique")
st.subheader("Calculateur Disjoint Évolué — Par Chagnon Julien Christian Robert")
st.markdown("---")

st.markdown("""
Ce système utilise une **arithmétique positionnelle bijective de base 9**. 
L'alphabet numérique y est exclusivement composé des symboles pleins de **1 à 9**, le chiffre 0 y est totalement exclu des calculs entiers et fractionnaires.
""")

# Création des onglets pour séparer proprement l'Étape 1 et l'Étape 2
onglet1, onglet2 = st.tabs([
    "1️⃣ ÉTAPE 1 : Base 10 ➔ Base 9 Bijective", 
    "2️⃣ ÉTAPE 2 : Base 9 Bijective ➔ Base 10"
])

# --- ONGLET 1 : DE LA BASE 10 À LA BASE 9 ---
with onglet1:
    st.header("Comptabilité en Base 9")
    
    saisie_b10 = st.text_input(
        "Saisissez le montant initial (Ex: 5847 ou 0,123456789) :",
        key="input_b10",
        placeholder="Entrez votre nombre ici..."
    )
    
    if saisie_b10:
        resultat_b9 = executer_etape_1(saisie_b10)
        
        st.info(f"**Longueur saisie :** {len(saisie_b10.strip().replace(' ', ''))} caractères")
        
        if "ERREUR" in resultat_b9:
            st.error(resultat_b9)
        else:
            st.success("### Résultat Calculé")
            st.code(resultat_b9, language="text")
            st.markdown(f"**Longueur en Base 9 :** {len(resultat_b9)} caractères")

# --- ONGLET 2 : DE LA BASE 9 À LA BASE 10 ---
with onglet2:
    st.header("Anatomie Restaurée en Base 10")
    
    saisie_b9 = st.text_input(
        "Saisissez le nombre à traiter (Ex: 4857 ou 0,123456789) :",
        key="input_b9",
        placeholder="Chiffres de 1 à 9 uniquement après la virgule..."
    )
    
    if saisie_b9:
        resultat_b10 = executer_etape_2(saisie_b9)
        
        st.info(f"**Longueur saisie :** {len(saisie_b9.strip().replace(' ', ''))} caractères")
        
        if "ERREUR" in resultat_b10:
            st.error(resultat_b10)
        else:
            st.success("### Anatomie Restaurée")
            st.code(resultat_b10, language="text")
            st.markdown(f"**Longueur Restaurée :** {len(resultat_b10)} caractères")

# Pied de page de l'application
st.markdown("---")
st.caption("© Architecture Mathématique Appliquée — Tous droits réservés.")
