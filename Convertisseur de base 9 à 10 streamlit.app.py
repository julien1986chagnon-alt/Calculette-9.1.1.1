import streamlit as st

# ==========================================================================
# CONFIGURATION DÉFINITIVE : LE MOTEUR DOUBLE DE STRUCTURE RECTIFIÉE
# NOM DU PROJET : ARCHITECTURE MATHÉMATIQUE PAR CHAGNON JULIEN
# ==========================================================================

# --------------------------------------------------------------------------
# MOTEUR 1 : CONVERSION LOGIQUE ALLER (BASE 10 => BIJECTIVE BASE 9)
# --------------------------------------------------------------------------
def convertisseur_base10_vers_base9(montant_str):
    montant_str = str(montant_str).strip().replace(" ", "").replace(",", "").replace(".", "")
    
    if not montant_str.isdigit():
        return "ERREUR : Saisie non numérique"
        
    n = int(montant_str)
    if n == 0:
        return "0"
        
    resultat = []
    while n > 0:
        reste = n % 9
        if reste == 0:
            resultat.append("9")
            n = (n // 9) - 1
        else:
            resultat.append(str(reste))
            n = n // 9
            
    return "".join(reversed(resultat))

# --------------------------------------------------------------------------
# MOTEUR 2 : CONVERSION LOGIQUE RETOUR (BIJECTIVE BASE 9 => BASE 10)
# --------------------------------------------------------------------------
def convertisseur_base9_vers_base10(chaine_b9_cible):
    chaine_b9_cible = str(chaine_b9_cible).strip().replace(" ", "")
    
    if chaine_b9_cible == "0":
        return "0"
        
    if not all(c in "123456789" for c in chaine_b9_cible):
        return "ERREUR : La chaîne contient un '0' ou un caractère invalide"
        
    valeur_base10 = 0
    puissance = 1
    
    for chiffre in reversed(chaine_b9_cible):
        valeur_base10 += int(chiffre) * puissance
        puissance *= 9
        
    return str(valeur_base10)

# ==========================================================================
# INTERFACE GRAPHIQUE STREAMLIT
# ==========================================================================

st.set_page_config(
    page_title="Architecture Mathématique - Base 9",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Architecture Mathématique")
st.subheader("Par Chagnon Julien Christian Robert")
st.markdown("### *Moteur Double : Base 10 ⇔ Bijective Base 9*")
st.divider()

# Création des onglets
onglet1, onglet2 = st.tabs([
    "📥 (1) Base 10 ➔ Base 9 Bijective", 
    "📤 (2) Base 9 Bijective ➔ Base 10"
])

# --- ONGLET 1 : BASE 10 VERS BASE 9 ---
with onglet1:
    st.markdown("#### Convertir un montant depuis la Base 10")
    
    # L'argument max_chars=18 bloque physiquement le clavier à 18 chiffres maximum
    saisie_b10 = st.text_input(
        "Entrez le montant en Base 10 (18 chiffres maximum) :", 
        key="input_b10",
        placeholder="Exemple: 1234554321",
        max_chars=18
    ).strip()
    
    if saisie_b10:
        resultat_b9 = convertisseur_base10_vers_base9(saisie_b10)
        
        if "ERREUR" in resultat_b9:
            st.error(f"❌ {resultat_b9}")
        else:
            st.success("✅ Conversion réussie !")
            st.text_area(
                "[+] COMPOSANTE BASE 9 PLEINE :", 
                value=resultat_b9, 
                height=70
            )
            st.caption(f"📏 Longueur du résultat : **{len(resultat_b9)}** chiffres")

# --- ONGLET 2 : BASE 9 VERS BASE 10 ---
with onglet2:
    st.markdown("#### Convertir un nombre depuis la Base 9 Bijective")
    
    # L'argument max_chars=18 bloque également le clavier ici
    saisie_b9 = st.text_input(
        "Entrez le nombre en Base 9 (Chiffres de 1 à 9 uniquement, 18 maximum) :", 
        key="input_b9",
        placeholder="Exemple: 6175521322",
        max_chars=18
    ).strip()
    
    if saisie_b9:
        resultat_b10 = convertisseur_base9_vers_base10(saisie_b9)
        
        if "ERREUR" in resultat_b10:
            st.error(f"❌ {resultat_b10}")
        else:
            st.success("✅ Conversion réciproque réussie !")
            st.text_area(
                "[+] EQUIVALENT BASE 10 ENTIER :", 
                value=resultat_b10, 
                height=70
            )
            st.caption(f"📏 Longueur du résultat : **{len(resultat_b10)}** chiffres")

st.divider()
st.info("💡 La saisie dans les cases est limitée physiquement à 18 caractères maximum pour protéger l'architecture de calcul.")
