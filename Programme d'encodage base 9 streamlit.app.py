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
# 2. INTERFACE GRAPHIQUE (TEMPS RÉEL STABLE)
# ==========================================

# Configuration de la page web
st.set_page_config(page_title="Console de Routage Bijectif Bilatéral", page_icon="🔐")

st.title("🔐 Console de Routage Bijectif Bilatéral")
st.markdown("---")

# Création de deux colonnes pour l'affichage côte à côte
col1, col2 = st.columns(2)

with col1:
    st.subheader("✍️ Section Encodage")
    # Zone de saisie du texte brut
    texte_source = st.text_area(
        "Texte Source (Lettres) :", 
        value="HELIOS base 9", 
        height=150,
        key="txt_source"
    )
    
    st.write("✨ **Message encodé :**")
    # Le conteneur de code est généré une seule fois à l'écran pour éviter le bug visuel
    zone_code = st.code("", language="text")
    
    # Mise à jour du texte à l'intérieur du conteneur fixe
    if texte_source:
        flux_chiffre = encoder_message_sans_zero(texte_source)
        zone_code.code(flux_chiffre, language="text")

with col2:
    st.subheader("🔓 Section Décodage")
    # Zone de saisie des chiffres
    flux_saisi = st.text_area(
        "Flux Encodé (Chiffres de 1 à 9 séparés par des espaces) :", 
        value="", 
        placeholder="Collez les chiffres ici...",
        height=150,
        key="flx_saisi"
    )
    
    st.write("📝 **Message décodé :**")
    # La zone de texte décodée reste fixe elle aussi
    zone_texte = st.empty()
    
    # Mise à jour en temps réel
    if flux_saisi:
        texte_decode = decoder_message_sans_zero(flux_saisi)
        zone_texte.text(texte_decode)
    else:
        zone_texte.text("En attente de données...")
