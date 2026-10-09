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
    blocs_encodes = []
    for caractere in texte:
        code_decimal = ord(caractere)
        code_bijectif = decimal_a_base9_bijective(code_decimal)
        blocs_encodes.append(code_bijectif)
    return " ".join(blocs_encodes)

def decoder_message_sans_zero(flux_b9):
    blocs = flux_b9.strip().split(" ")
    caracteres_decoles = []
    for bloc in blocs:
        if not bloc:
            continue
        try:
            code_decimal = base9_bijective_a_decimal(bloc)
            caracteres_decoles.append(chr(code_decimal))
        except ValueError:
            # Ignore les caractères invalides (comme les lettres dans le flux de chiffres)
            continue
    return "".join(caracteres_decoles)


# ==========================================
# 2. INTERFACE GRAPHIQUE COMPLÈTEMENT FIXE
# ==========================================

st.set_page_config(page_title="Console de Routage Bijectif Bilatéral", page_icon="🔐")

st.title("🔐 Console de Routage Bijectif Bilatéral")
st.markdown("---")

# Nous utilisons des blocs de saisie standards. Plus de st.code ni de st.empty.
col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ Section Encodage")
    texte_source = st.text_area(
        "Texte Source (Lettres) :", 
        value="HELIOS base 9", 
        height=150,
        key="txt_source"
    )
    
    # Calcul direct du message encodé
    flux_chiffre = encoder_message_sans_zero(texte_source) if texte_source else ""
    
    # Remplacement de st.code par un champ de texte standard en lecture seule (sécurisé)
    st.text_area(
        "✨ Message encodé (Copiez ce flux) :",
        value=flux_chiffre,
        height=150,
        disabled=True,
        key="res_encode"
    )

with col2:
    st.subheader("🔓 Section Décodage")
    flux_saisi = st.text_area(
        "Flux Encodé (Chiffres de 1 à 9 séparés par des espaces) :", 
        value="", 
        placeholder="Collez les chiffres ici...",
        height=150,
        key="flx_saisi"
    )
    
    # Calcul direct du message décodé
    texte_decode = decoder_message_sans_zero(flux_saisi) if flux_saisi else "En attente de données..."
    
    # Remplacement de st.info par un champ de texte standard en lecture seule (sécurisé)
    st.text_area(
        "📝 Message décodé :",
        value=texte_decode,
        height=150,
        disabled=True,
        key="res_decode"
    )
