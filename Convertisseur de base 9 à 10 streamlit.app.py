import streamlit as st

TABLEUR_PASSAGES_ZERO = {
    10: "1", 
    100: "11", 
    1000: "221", 
    10000: "2541", 
    100000: "27951",
    1000000: "318561", 
    10000000: "3515271", 
    100000000: "38667981",
    1000000000: "436458891", 
    10000000000: "4812158911",
    100000000000: "53933759121", 
    1000000000000: "594372461331",
    10000000000000: "66481971724641", 
    100000000000000: "74241278932151",
    1000000000000000: "826654179353661", 
    10000000000000000: "9194295983891371",
    100000000000000000: "112247366933915181", 
    1000000000000000000: "1234732147374166951",
    10000000000000000000: "1356315363226848111", 
    100000000000000000000: "149524689554496435221",
    1000000000000000000000: "165572711549571852431", 
    10000000000000000000000: "18324598827716391476741",
    100000000000000000000000: "212571719215881416355251"
}

if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}

def addition_comptable_verticale_b9(str_n1, str_n2):
    n1, n2 = str_n1.strip(), str_n2.strip()
    max_len = max(len(n1), len(n2))
    n1, n2 = n1.zfill(max_len), n2.zfill(max_len)
    resultat, retenue = [], 0
    for i in range(max_len - 1, -1, -1):
        d1 = int(n1[i]) if n1[i] != '0' else 0
        d2 = int(n2[i]) if n2[i] != '0' else 0
        somme_colonne = d1 + d2 + retenue
        if somme_colonne >= 9:
            reste = somme_colonne % 9
            chiffre_ici = 9 if reste == 0 else reste
            retenue = (somme_colonne // 9) - 1 if reste == 0 else somme_colonne // 9
        else:
            chiffre_ici = somme_colonne
            retenue = 0
        resultat.append(str(chiffre_ici))
    if retenue > 0:
        resultat.append(str(retenue))
    res_final = "".join(reversed(resultat)).lstrip('0')
    return res_final if res_final != "" else "0"

def somme_verticale_multi_lignes_b9(liste_chaines):
    total = "0"
    for chaine in liste_chaines:
        total = addition_comptable_verticale_b9(total, chaine)
    return total

def multiplication_comptable_unitaire_b9(str_b0, chiffre_int):
    resultat = "0"
    for _ in range(chiffre_int):
        resultat = addition_comptable_verticale_b9(resultat, str_b0)
    return resultat

def comparaison_chaines_numeriques(str_b9_1, str_b9_2):
    s1, s2 = str_b9_1.lstrip('0'), str_b9_2.lstrip('0')
    if s1 == "": s1 = "0"
    if s2 == "": s2 = "0"
    if len(s1) > len(s2): return 1
    if len(s1) < len(s2): return -1
    if s1 > s2: return 1
    if s1 < s2: return -1
    return 0

def simuler_etape_1_pure(saisie_b10):
    longueur = len(saisie_b10)
    lignes_zeros_seules = []
    for i, chiffre_str in enumerate(saisie_b10):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partial_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                lignes_zeros_seules.append(partial_b9)
    return lignes_zeros_seules, somme_verticale_multi_lignes_b9(lignes_zeros_seules)

def executer_etape_1(montant_b10_str):
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) == 0:
        return None, "ERREUR", "0"
    longueur = len(saisie)
    lignes_details, lignes_zeros_seules = [], []
    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partial_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                lignes_zeros_seules.append(partial_b9)
                lignes_details.append(f"Rang 10^{nb_zeros_droite} -> ({chiffre}) x ({ref_tableur}) = {partial_b9}")
    somme_zeros_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    resultat_final_b9 = addition_comptable_verticale_b9(saisie, somme_zeros_brute)
    return lignes_details, somme_zeros_brute, resultat_final_b9

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip()
    solution_trouvee = []
    def explore_arbre(prefixe_actuel):
        if len(prefixe_actuel) == length:
            _, somme_brute = simuler_etape_1_pure(prefixe_actuel)
            if addition_comptable_verticale_b9(prefixe_actuel, somme_brute) == saisie:
                solution_trouvee.append(prefixe_actuel)
            return False
        taille_restante = length - len(prefixe_actuel)
        _, lim_basse_somme = simuler_etape_1_pure(prefixe_actuel + "1" * taille_restante)
        limite_basse = addition_comptable_verticale_b9(prefixe_actuel + "1" * taille_restante, lim_basse_somme)
        _, lim_haute_somme = simuler_etape_1_pure(prefixe_actuel + "9" * taille_restante)
        limite_haute = addition_comptable_verticale_b9(prefixe_actuel + "9" * taille_restante, lim_haute_somme)
        if comparaison_chaines_numeriques(saisie, limite_basse) >= 0 and comparaison_chaines_numeriques(saisie, limite_haute) <= 0:
            for chiffre_choisi in range(1, 10):
                explore_arbre(prefixe_actuel + str(chiffre_choisi))
        return False
    for length in range(1, len(saisie) + 1):
        explore_arbre("")
    return solution_trouvee if solution_trouvee else "ERREUR"

def etape_1_logique_zero(saisie_b10):
    saisie = saisie_b10.strip().replace(" ", "")
    longueur = len(saisie)
    blocs_b9, lignes_details = [], []
    for i, chiffre_str in enumerate(saisie):
        if chiffre_str != '0':
            montant_positionnel = chiffre_str + '0' * (longueur - 1 - i)
            lignes, _, res_b9 = executer_etape_1(montant_positionnel)
            if lignes:
                blocs_b9.append(res_b9)
                lignes_details.extend(lignes)
    if not blocs_b9: return None, "ERREUR", "0"
    return lignes_details, "Calcul combiné", somme_verticale_multi_lignes_b9(blocs_b9)

def simuler_etape_1_logique_zero(saisie_b10):
    longueur = len(saisie_b10)
    blocs_b9 = []
    for i, chiffre_str in enumerate(saisie_b10):
        if chiffre_str != '0':
            chiffre = int(chiffre_str)
            puissance_dix = 10 ** (longueur - 1 - i)
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                ref_tableur = TABLEUR_PASSAGES_ZERO[puissance_dix]
                partial_b9 = multiplication_comptable_unitaire_b9(ref_tableur, chiffre)
                blocs_b9.append(addition_comptable_verticale_b9(chiffre_str + '0' * (longueur - 1 - i), partial_b9))
    return somme_verticale_multi_lignes_b9(blocs_b9) if blocs_b9 else "0"

def etape_2_logique_zero(saisie_b9):
    solution_trouvee = []
    def explore_arbre_zero(prefixe_actuel, length):
        if len(prefixe_actuel) == length:
            if simuler_etape_1_logique_zero(prefixe_actuel) == saisie_b9:
                solution_trouvee.append(prefixe_actuel)
            return False
        taille_restante = length - len(prefixe_actuel)
        limite_basse = simuler_etape_1_logique_zero(prefixe_actuel + "0" * taille_restante)
        limite_haute = simuler_etape_1_logique_zero(prefixe_actuel + "9" * taille_restante)
        if comparaison_chaines_numeriques(saisie_b9, limite_basse) >= 0 and comparaison_chaines_numeriques(saisie_b9, limite_haute) <= 0:
            debut_range = 1 if prefixe_actuel == "" else 0
            for chiffre_choisi in range(debut_range, 10):
                explore_arbre_zero(prefixe_actuel + str(chiffre_choisi), length)
        return False
    for length in range(1, len(saisie_b9) + 1):
        explore_arbre_zero("", length)
    return solution_trouvee if solution_trouvee else "ERREUR"

st.title("ARCHITECTURE MATHÉMATIQUE - CALCULATEUR DISJOINT")
st.write("ANALYSE EXTENSION THÈSE")

onglet1, onglet2 = st.tabs(["ÉTAPE 1 : Base 10 -> Base 9", "ÉTAPE 2 : Base 9 -> Base 10"])

with onglet1:
    st.header("Comptabilité en Base 9")
    # max_chars=20 bloque la saisie à 20 chiffres maximum
    saisie_brute = st.text_input("Saisissez le montant initial (Base 10) :", key="input_e1", max_chars=20)
    if st.button("Calculer l'Étape 1"):
        if saisie_brute:
            if len(saisie_brute) > 20:
                st.error("❌ La saisie dépasse la limite de 20 chiffres autorisée.")
            else:
                if '0' in saisie_brute:
                    st.info("💡 Détection de zéro mémoire. Traitement par décomposition.")
                    lignes, _, res_final = etape_1_logique_zero(saisie_brute)
                else:
                    lignes, _, res_final = executer_etape_1(saisie_brute)
                
                st.session_state.memoire_session[res_final] = saisie_brute
                st.success(f"🏆 RÉSULTAT BASE 9 PURE : {res_final}")

with onglet2:
    st.header("Anatomie Restaurée en Base 10")
    # max_chars=20 bloque la saisie à 20 chiffres maximum
    saisie_b9 = st.text_input("Saisissez le nombre à traiter (Base 9) :", key="input_e2", max_chars=20)
    if st.button("Calculer l'Étape 2"):
        if saisie_b9:
            if len(saisie_b9) > 20:
                st.error("❌ La saisie dépasse la limite de 20 chiffres autorisée.")
            else:
                if saisie_b9 in st.session_state.memoire_session:
                    resultat = st.session_state.memoire_session[saisie_b9]
                    st.success(f"👉 ANATOMIE RESTAURÉE (EXCEPTION MÉMOIRE) : {resultat}")
                else:
                    st.warning("⚠️ Valeur absente de l'exception mémoire. Lancement des arbres combinatoires...")
                    res_strict = executer_etape_2(saisie_b9)
                    res_zero = etape_2_logique_zero(saisie_b9)
                    toutes_solutions = []
                    if isinstance(res_strict, list): toutes_solutions.extend(res_strict)

