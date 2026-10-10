import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Décodeur", page_icon="🔓")

st.title("🔓 Décodeur Mystère")
st.write("Entrez les indices pour révéler le message.")

# Formulaire de saisie
with st.form(key="mon_formulaire"):
    nombre_saisi = st.number_input("1. Le Nombre Secret :", step=1, value=0)
    mot_saisi = st.text_input("2. Le Mot Secret :")
    bouton = st.form_submit_button(label="🔓 Valider")

# Logique de vérification
if bouton:
    if nombre_saisi == 42 and mot_saisi.strip().lower() == "secret":
        st.success("🎉 Bravo ! Voici le message secret.")
        st.balloons()
    elif nombre_saisi == 0 or mot_saisi.strip() == "":
        st.warning("⚠️ Veuillez remplir les deux champs.")
    else:
        st.error("❌ Clés incorrectes. Réessayez !")
