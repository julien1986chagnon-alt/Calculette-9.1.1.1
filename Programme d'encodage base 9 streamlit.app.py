import streamlit as st

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================
st.set_page_config(
    page_title="Décodeur LinkedIn 🔓",
    page_icon="🔓",
    layout="centered"
)

# Style CSS pour rendre l'interface plus sympa
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; background-color: #0077B5; color: white; }
    </style>
""", unsafe_allowed_html=True)

st.title("🔓 Le Décodeur Mystère LinkedIn")
st.write("Trouvez les indices sur mon post LinkedIn, entrez-les ci-dessous et révélez le message secret !")

st.divider()

# ==============================================================================
# PARTIE 1 : VOTRE LOGIQUE DE CALCUL / VOS RÉPONSES
# ==============================================================================
def decoder_mon_message(nombre, mot):
    """
    Cette fonction prend le nombre et le mot saisis par l'utilisateur,
    et applique votre logique pour retourner le message secret.
    """
    # 📝 MODIFIEZ LES VALEURS CI-DESSOUS AVEC VOS VRAIS SECRETS :
    NOMBRE_CORRECT = 42 # Remplacez par votre nombre secret
    MOT_CORRECT = "secret" # Remplacez par votre mot secret (en minuscules)
    
    # Nettoyage de la saisie utilisateur (enlève les espaces et met en minuscules)
    mot_nettoye = mot.strip().lower()
    
    # Vérification des clés
    if nombre == NOMBRE_CORRECT and mot_nettoye == MOT_CORRECT:
        # 📝 REMPLACEZ PAR VOTRE VRAI MESSAGE FINAL ICI :
        message_final = "🎉 Bravo ! Vous avez décodé le message. Voici l'annonce exclusive : [Votre message secret ici]"
        return message_final
    else:
        # Si les clés sont fausses, on ne renvoie rien
        return None

# ==============================================================================
# PARTIE 2 : INTERFACE GRAPHIQUE (WIDGETS)
# ==============================================================================
# Formulaire pour regrouper les entrées et éviter que la page se recharge à chaque frappe
with st.form(key="formulaire_decodage"):
    st.write("### 🔑 Entrez vos clés de décodage")
    
    # Champ pour le nombre secret
    nombre_saisi = st.number_input(
        "1. Le Nombre Secret :", 
        step=1, 
        value=0,
        help="Entrez le nombre trouvé grâce à l'énigme LinkedIn"
    )
    
    # Champ pour le mot secret
    mot_saisi = st.text_input(
        "2. Le Mot Secret :", 
        value="",
        placeholder="Écrivez le mot ici...",
        help="Entrez le mot clé trouvé dans le post"
    )
    
    # Bouton de validation à l'intérieur du formulaire
    bouton_valider = st.form_submit_button(label="🔓 Tenter le décodage")

# ==============================================================================
# PARTIE 3 : LE DÉCLENCHEMENT DU CALCUL
# ==============================================================================
if bouton_valider:
    # On vérifie d'abord que l'utilisateur a bien rempli les deux champs
    if nombre_saisi == 0 or mot_saisi.strip() == "":
        st.warning("⚠️ Veuillez remplir le nombre ET le mot secret pour lancer le décodage.")
    else:
        # Appel de la fonction de décodage avec les saisies de l'utilisateur
        resultat = decoder_mon_message(nombre_saisi, mot_saisi)
        
        if resultat:
            # Succès ! On affiche le message de manière très visuelle
            st.success("🔓 CLÉS CORRECTES ! Le message a été déchiffré avec succès :")
            st.info(resultat)
            st.balloons() # Animation de ballons de célébration !
        else:
            # Échec
            st.error("❌ Clés incorrectes. Le message reste crypté ! Vérifiez vos indices et réessayez.")
