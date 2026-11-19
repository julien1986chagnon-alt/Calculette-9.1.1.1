import streamlit as st
import sys

# Augmentation de la limite pour les nombres gigantesques (comme dans votre code original)
sys.set_int_max_str_digits(10000)

# ==========================================================
# 1. VOS FONCTIONS DE CONVERSION DE BASE (Stricte sans zéro)
# ==========================================================

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


# ==========================================================
# 2. MOTEUR A : ALIGNEMENT TEXTUEL DES VIRGULES (+ , - , *)
# ==========================================================

def executer_calcul_alignement_textuel(a_saisie_brut, b_saisie_brut, operation):
    # Nettoyage des espaces
    a_nettoye = a_saisie_brut.strip().replace(" ", "")
    b_nettoye = b_saisie_brut.strip().replace(" ", "")

    # Calcul du décalage des décimales
    dec_a = len(a_nettoye.split(".")[1]) if "." in a_nettoye else 0
    dec_b = len(b_nettoye.split(".")[1]) if "." in b_nettoye else 0

    # Nettoyage pour obtenir les nombres sans virgule
    a_saisi = a_nettoye.replace(".", "")
    b_saisi = b_nettoye.replace(".", "")

    # Conversions
    a_decimal = logique_sans_zero_a_decimal(a_saisi)
    b_decimal = logique_sans_zero_a_decimal(b_saisi)

    if a_decimal is None or b_decimal is None:
        return "Erreur : Saisie invalide (Chiffres 1 à 9 uniquement)", "--"

    # Choix de l'opération et de sa preuve inverse
    if operation == "+":
        res_decimal = a_decimal + b_decimal
        op_inverse = "-"
        res_inverso_decimal = res_decimal - b_decimal
        total_dec = max(dec_a, dec_b)
    elif operation == "-":
        res_decimal = a_decimal - b_decimal
        op_inverse = "+"
        res_inverso_decimal = res_decimal + b_decimal
        total_dec = max(dec_a, dec_b)
    elif operation == "*":
        res_decimal = a_decimal * b_decimal
        op_inverse = "/"
        res_inverso_decimal = res_decimal // b_decimal if b_decimal != 0 else 0
        total_dec = dec_a + dec_b

    # Traductions brutes en logique sans zéro
    res_propre_brut = decimal_a_logique_sans_zero(res_decimal)
    res_inverso_propre_brut = decimal_a_logique_sans_zero(res_inverso_decimal)

    # Replacement de la virgule par décalage textuel
    def replacer_virgule(chaine, nb_dec):
        if nb_dec > 0 and len(chaine) > nb_dec:
            pos = len(chaine) - nb_dec
            return chaine[:pos] + "." + chaine[pos:]
        elif nb_dec > 0:
            return "0." + chaine.zfill(nb_dec)
        return chaine

    res_propre = replacer_virgule(res_propre_brut, total_dec)

    # Preuve inverse pour l'affichage
    if operation == "*":
        res_inverso_propre = replacer_virgule(res_inverso_propre_brut, dec_a)
    else:
        res_inverso_propre = replacer_virgule(res_inverso_propre_brut, total_dec)

    phrase_preuve = f"L'INVERSION INVERSE : ({res_propre}) {op_inverse} ({b_nettoye}) = {res_inverso_propre}"
    return res_propre, phrase_preuve


# ==========================================================
# 3. MOTEUR B : DIVISION ARITHMÉTIQUE DIRECTE SANS LIMITE ( / )
# ==========================================================

def chercher_extension_sans_abandon(num_str, den_str, limite_max=500):
    num_str = num_str.replace(".", "").replace(",", "")
    den_str = den_str.replace(".", "").replace(",", "")

    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)

    if num_dec_origine is None or den_dec is None:
        return "Erreur", "Invalide", "Saisie invalide"

    if den_dec == 0:
        return "Erreur", "Invalide", "Division par zéro impossible"

    if num_dec_origine % den_dec == 0:
        q_brut = decimal_a_logique_sans_zero(num_dec_origine // den_dec)
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        return q_visuel, "Aucune (Tombe juste)", "Chemin direct"

    L = 1
    puissance_9 = 9
    min_val_ext = 1
    max_val_ext = 9

    trouve = False
    ext = ""
    q_brut = ""

    while L <= limite_max:
        base_dec = num_dec_origine * puissance_9
        reste = (base_dec + min_val_ext) % den_dec
        ajout_necessaire = min_val_ext if reste == 0 else min_val_ext + (den_dec - reste)

        if ajout_necessaire <= max_val_ext:
            dec_total = base_dec + ajout_necessaire
            ext = decimal_a_logique_sans_zero(ajout_necessaire)
            q_brut = decimal_a_logique_sans_zero(dec_total // den_dec)
            trouve = True
            break

        L += 1
        puissance_9 *= 9
        min_val_ext = min_val_ext * 9 + 1
        max_val_ext = max_val_ext * 9 + 9

    if trouve:
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        longueur_ext = len(ext)

        if len(q_visuel) > longueur_ext:
            res_final = f"{q_visuel[:-longueur_ext]},({q_visuel[-longueur_ext:]})"
        else:
            res_final = f"0,({q_visuel.zfill(longueur_ext)})"

        return res_final, f"0,{ext}", f"Fermeture réussie avec un segment de {longueur_ext} chiffre(s)"

    return "Calcul incomplet", "Recherche...", "Aucune fermeture trouvée avant 500 chiffres."


# ==========================================================
# 4. INTERFACE GRAPHIQUE WEB (Streamlit)
# ==========================================================

st.set_page_config(page_title="Calculatrice Totale Base 9", page_icon="🧮")

st.title("🧮 Calculatrice Évolutive Totale - Base 9 Bijective")
st.subheader("Moteurs Intégrés : Alignement Textuel & Résolution Directe")
st.caption("Développé par Chagnon Julien Christian Robert - Tous droits réservés.")

st.markdown("---")

# Menu de sélection des moteurs
choix_op = st.selectbox(
    "Sélectionnez l'opération mathématique :",
    [
        "➕ Addition (Moteur Alignement)",
        "➖ Soustraction (Moteur Alignement)",
        "✖️ Multiplication (Moteur Alignement)",
        "➗ Division (Moteur Fermeture Directe Sans Limite)"
    ]
)

st.markdown("### 📏 Saisie des dimensions")

# Configuration dynamique des règles de saisie selon le choix
if "Division" in choix_op:
    consigne_b = "Deuxième nombre (Dénominateur - Longueur illimitée sans virgule) :"
    max_c = None
    placeholder_a = "Ex: 123456789987654321 (Sans virgule)"
    placeholder_b = "Ex: 987654321123456789"
else:
    consigne_b = "Deuxième nombre (Longueur illimitée - Virgule autorisée) :"
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
                    st.info(f"➕ **RÉSULTAT DE L'ADDITION :** `{res}`")
                    st.success(preuve)

                elif "Soustraction" in choix_op:
                    res, preuve = executer_calcul_alignement_textuel(a_input, b_input, "-")
                    st.info(f"➖ **RÉSULTAT DE LA SOUSTRACTION :** `{res}`")
                    st.success(preuve)

                elif "Multiplication" in choix_op:
                    res, preuve = executer_calcul_alignement_textuel(a_input, b_input, "*")
                    st.info(f"✖️ **RÉSULTAT DE LA MULTIPLICATION :** `{res}`")
                    st.success(preuve)

                elif "Division" in choix_op:
                    res, ext, details = chercher_extension_sans_abandon(a_input, b_input)
                    st.info(f"➗ **RÉSULTAT DE LA DIVISION :** `{res}`")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.warning(f"➕ **CHIFFRES INJECTÉS :**\n`{ext}`")
                    with col2:
                        st.metric(label="🚀 CHEMIN DE FERMETURE", value=details)

