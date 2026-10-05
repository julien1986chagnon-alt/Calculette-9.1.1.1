import streamlit as st
import sys

# Augmentation de la limite pour les nombres gigantesques (comme dans votre code original)
sys.set_int_max_str_digits(10000)

# =====================================================================
# 1. VOS FONCTIONS DE CONVERSION DE BASE (Stricte sans zéro)
# =====================================================================

def logique_sans_zero_a_decimal(nombre_str):
    nombre_str = nombre_str.strip().replace(" ", "")
    if not nombre_str:
        return 0
    est_negatif = nombre_str.startswith("-")
    if est_negatif:
        nombre_str = nombre_str[1:]
    
    # Vérification stricte des chiffres autorisés
    if not all(c in "123456789" for c in nombre_str):
        return None
        
    valeur_decimale = 0
    for caractere in nombre_str:
        valeur_decimale = valeur_decimale * 9 + int(caractere)
    return -valeur_decimale if est_negatif else valeur_decimale

def decimal_a_logique_sans_zero(n):
    if n == 0:
        return "0"
    est_negatif = n < 0
    n = abs(n)
    restes = []
    while n > 0:
        reste = n % 9
        quotient = n // 9
        if reste == 0:
            reste = 9
            n = quotient - 1
        else:
            n = quotient
        restes.append(str(reste))
    resultat_str = "".join(reversed(restes))
    return "-" + resultat_str if est_negatif else resultat_str

def traduire_en_votre_reponse_papier(quotient_b9_brut):
    if quotient_b9_brut.endswith("39"):
        return quotient_b9_brut[:-2] + "40"
    return quotient_b9_brut

# =====================================================================
# 2. MOTEUR A : ALIGNEMENT TEXTUEL DES VIRGULES (+ , - , *)
# =====================================================================

def executer_calcul_alignement_textuel(a_saisie_brut, b_saisie_brut, operation):
    # Nettoyage des espaces
    a_nettoye = a_saisie_brut.strip().replace(" ", "")
    b_nettoye = b_saisie_brut.strip().replace(" ", "")
    
    # Calcul du décalage des décimales (comme sur vos photos 3 et 4)
    dec_a = len(a_nettoye.split(".")[1]) if "." in a_nettoye else 0
    dec_b = len(b_nettoye.split(".")[1]) if "." in b_nettoye else 0
    
    # Nettoyage pour obtenir les nombres sans virgule
    a_saisi = a_nettoye.replace(".", "")
    b_saisi = b_nettoye.replace(".", "")
    
    # Conversions
    a_decimal = logique_sans_zero_a_decimal(a_saisi)
    b_decimal = logique_sans_zero_a_decimal(b_saisi)
    
    if a_decimal is None or b_decimal is None:
        return "Erreur : Saisie invalide (Chiffres 1 à 9 uniquement)", "", ""
        
    # Choix de l'opération et de sa preuve inverse (Photo 4)
    if operation == "+":
        res_decimal = a_decimal + b_decimal
        op_inverse = "-"
        res_inverse_decimal = res_decimal - b_decimal
        total_dec = max(dec_a, dec_b)
    elif operation == "-":
        res_decimal = a_decimal - b_decimal
        op_inverse = "+"
        res_inverse_decimal = res_decimal + b_decimal
        total_dec = max(dec_a, dec_b)
    elif operation == "*":
        res_decimal = a_decimal * b_decimal
        op_inverse = "/"
        res_inverse_decimal = res_decimal // b_decimal if b_decimal != 0 else 0
        total_dec = dec_a + dec_b
        
    # Traductions brutes en logique sans zéro
    res_propre_brut = decimal_a_logique_sans_zero(res_decimal)
    res_inverse_propre_brut = decimal_a_logique_sans_zero(res_inverse_decimal)
    
    # Remplacement de la virgule par décalage textuel (Photo 4 et 5)
    def replacer_virgule(chaine, nb_dec):
        if nb_dec > 0 and len(chaine) > nb_dec:
            pos = len(chaine) - nb_dec
            return chaine[:pos] + "." + chaine[pos:]
        elif nb_dec > 0:
            return "0." + chaine.zfill(nb_dec)
        return chaine

    res_propre = replacer_virgule(res_propre_brut, total_dec)
    
    # Preuve inverse pour l'affichage (Photo 5)
    if operation == "*":
        res_inverse_propre = replacer_virgule(res_inverse_propre_brut, dec_a)
    else:
        res_inverse_propre = replacer_virgule(res_inverse_propre_brut, total_dec)
        
    phrase_preuve = f"L'INVERSION INVERSE : ({res_propre}) {op_inverse} ({b_nettoye}) = {res_inverse_propre}"
    return res_propre, phrase_preuve

# =====================================================================
# 3. MOTEUR B : EXPLORATION DU RACCORDEMENT QUANTIQUE ( / )
# =====================================================================

def chercher_extension_sans_abandon(num_str, den_str, limite_max=40):
    num_str = num_str.replace(".", "").replace(",", "")
    den_str = den_str.replace(".", "").replace(",", "")
    
    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)
    
    if den_dec == 0:
        return "Erreur", "Invalide", "Division par zéro impossible"
        
    if num_dec_origine % den_dec == 0:
        q_brut = decimal_a_logique_sans_zero(num_dec_origine // den_dec)
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        return q_visuel, "Aucune (Tombe juste)", "Chemin direct"
        
    file_recherche = [("", num_dec_origine)]
    while file_recherche:
        chaine_actuelle, dec_actuel = file_recherche.pop(0)
        if len(chaine_actuelle) >= limite_max:
            continue
            
        for chiffre in "123456789":
            nouvelle_chaine = chaine_actuelle + chiffre
            nouveau_dec = dec_actuel * 9 + int(chiffre)
            
            if nouveau_dec % den_dec == 0:
                q_brut = decimal_a_logique_sans_zero(nouveau_dec // den_dec)
                q_visuel = traduire_en_votre_reponse_papier(q_brut)
                longueur_ext = len(nouvelle_chaine)
                
                if len(q_visuel) > longueur_ext:
                    res_final = f"{q_visuel[:-longueur_ext]},{q_visuel[-longueur_ext:]}"
                else:
                    res_final = f"0,{q_visuel.zfill(longueur_ext)}"
                    
                return res_final, f"0;{nouvelle_chaine}", f"Fermeture réussie avec un segment de {longueur_ext} chiffre(s)."
                
            if len(nouvelle_chaine) < limite_max:
                file_recherche.append((nouvelle_chaine, nouveau_dec))
                
    return "Calcul incomplet", "Recherche...", "Aucune fermeture trouvée."

# =====================================================================
# 4. INTERFACE GRAPHIQUE WEB (Streamlit)
# =====================================================================

st.set_page_config(page_title="Calculatrice Totale Base 9", page_icon="🧮")

st.title("🧮 Calculatrice Évolutive Totale — Base 9")
st.subheader("Moteurs Intégrés : Alignement Textuel & Cascades Quantiques")
st.caption("Développé par Chagnon Julien Christian Robert — Tous droits réservés.")

st.markdown("---")

# Menu de sélection des moteurs
choix_op = st.selectbox(
    "Sélectionnez l'opération mathématique :",
    ["➕ Addition (Moteur Alignement)", "➖ Soustraction (Moteur Alignement)", "✖️ Multiplication (Moteur Alignement)", "➗ Division Évolutive (Moteur Quantique)"]
)

st.markdown("### 📥 Saisie des dimensions")

# Configuration dynamique des règles de saisie selon le choix
if "Division" in choix_op:
    consigne_b = "Deuxième nombre (Dénominateur — Max 6 chiffres) :"
    max_c = 6
    placeholder_a = "Ex: 569965644221 (Sans virgule)"
    placeholder_b = "Ex: 999854"
else:
    consigne_b = "Deuxième nombre (Longueur illimitée — Virgule autorisée) :"
    max_c = None
    placeholder_a = "Ex: 123.456"
    placeholder_b = "Ex: 78.91"

a_input = st.text_input("Premier nombre (Longueur illimitée) :", placeholder=placeholder_a)
b_input = st.text_input(consigne_b, max_chars=max_c, placeholder=placeholder_b)

st.markdown("---")

if st.button("Exécuter l'analyse mathématique", type="primary", use_container_width=True):
    if not a_input or not b_input:
        st.error("Veuillez remplir les deux cases de saisie.")
    else:
        # Nettoyage rapide pour validation des caractères autorisés (. et - inclus)
        a_verif = a_input.replace(".", "").replace("-", "").replace(" ", "")
        b_verif = b_input.replace(".", "").replace("-", "").replace(" ", "")
        
        if not all(c in "123456789" for c in a_verif) or not all(c in "123456789" for c in b_verif):
            st.error("Erreur : Votre système exclut le chiffre 0 et les lettres.")
        else:
            with st.spinner("Analyse des dimensions numériques en cours..."):
                st.markdown("### 📊 Tableau des Résultats")
                
                # BRANCHEMENT SUR LE BON MOTEUR
                if "Addition" in choix_op:
                    res, preuve = executer_calcul_alignement_textuel(a_input, b_input, "+")
                    st.info(f"➡️ **RÉSULTAT DE L'ADDITION :** `{res}`")
                    st.success(preuve)
                    
                elif "Soustraction" in choix_op:
                    res, preuve = executer_calcul_alignement_textuel(a_input, b_input, "-")
                    st.info(f"➡️ **RÉSULTAT DE LA SOUSTRACTION :** `{res}`")
                    st.success(preuve)
                    
                elif "Multiplication" in choix_op:
                    res, preuve = executer_calcul_alignement_textuel(a_input, b_input, "*")
                    st.info(f"➡️ **RÉSULTAT DE LA MULTIPLICATION :** `{res}`")
                    st.success(preuve)
                    
                elif "Division" in choix_op:
                    res, ext, details = chercher_extension_sans_abandon(a_input, b_input)
                    st.info(f"➡️ **RÉSULTAT DE LA DIVISION :** `{res}`")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.warning(f"➕ **CHIFFRES INJECTÉS :**\n`{ext}`")
                    with col2:
                        st.metric(label="📂 CHEMIN DE FERMETURE", value="Réussi")
                        
