import streamlit as st

# ==========================================
# 1. FONCTIONS DE CONVERSION & ENCODAGE
# ==========================================

def decimal_a_base9_bijective(n):
    if n == 0:
        return ""
    restes = []
    while n > 0:
        reste = n % 9
        quotient = n // 9
        if reste == 0:
            reste = 9
            quotient -= 1
        restes.append(str(reste))
        n = quotient
    return "".join(reversed(restes))

def base9_bijective_a_decimal(nombre_str):
    valeur = 0
    for caractere in nombre_str:
        valeur = valeur * 9 + int(caractere)
    return valeur

def encoder_message_sans_zero(texte):
    if not texte:
        return ""
    blocs_encodes = []
    for caractere in texte:
        code_decimal = ord(caractere)
        code_bijectif = decimal_a_base9_bijective(code_decimal)
        blocs_encodes.append(code_bijectif)
    return " ".join(blocs_encodes)

def decoder_message_sans_zero(flux_b9):
    if not flux_b9:
        return ""
    blocs = flux_b9.strip().split(" ")
    caracteres_decoles = []
    for bloc in blocs:
        if not bloc:
            continue
        try:
            code_decimal = base9_bijective_a_decimal(bloc)
            caracteres_decoles.append(chr(code_decimal))
        except ValueError:
            # Ignore les blocs invalides
            continue
    return "".join(caracteres_decoles)


# ==========================================
# 2. INTERFACE GRAPHIQUE LINÉAIRE & ROBUSTE
# ==========================================

# Configuration minimale de la page
st.set_page_config(page_title="Console de Routage")

st.title("🔐 Console de Routage Bijectif Bilatéral")
st.write("---")

# --- SECTION 1 : ENCODAGE ---
st.header("✍️ Encodage de message")
texte_source = st.text_area(
    "Écrivez votre texte en lettres ci-dessous :", 
    value="HELIOS base 9",
    key="zone_saisie_lettres"
)

# On calcule le flux de chiffres
flux_chiffre = encoder_message_sans_zero(texte_source)

st.write("✨ **Résultat chiffré à copier :**")
# Utilisation d'un affichage textuel basique pour éviter les erreurs de composants
st.text(flux_chiffre)

st.write("---")

# --- SECTION 2 : DÉCODAGE ---
st.header("🔓 Décodage de flux")
flux_saisi = st.text_area(
    "Collez vos chiffres (séparés par des espaces) ci-dessous :", 
    value="",
    placeholder="Exemple: 12 45 78...",
    key="zone_saisie_chiffres"
)

# On calcule le texte décodé
texte_decode = decoder_message_sans_zero(flux_saisi)

st.write("📝 **Résultat décodé :**")
if flux_saisi:
    st.text(texte_decode)
else:
    st.text("En attente de chiffres...")

