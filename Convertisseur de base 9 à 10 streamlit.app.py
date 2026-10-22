import streamlit as st

# Configuration graphique de la page
st.set_page_config(page_title="Calculateur Disjoint", page_icon="🔢", layout="centered")

# ==========================================
# 1. VOTRE TABLEUR DES PASSAGES ZÉRO (L'ARBRE)
# ==========================================
TABLEUR_PASSAGES_ZERO = {
    10: "1",
    100: "11",
    1000: "221",
    10000: "2541",
    100000: "27951",
    1000000: "318561",
    10000000: "3515271",
    100000000: "38667981",
    1000000000: "436456891",
    10000000000: "4812158911",
    100000000000: "53933759121",
    1000000000000: "594372461331",
    10000000000000: "66481971724641",
    100000000000000: "74241278932151",
    1000000000000000: "826654179353661",
    10000000000000000: "9194295983891371",
    100000000000000000: "112247366933915181",
    1000000000000000000: "1234732147374166991",
    10000000000000000000: "1358315363226848111",
    100000000000000000000: "14952469554496435221",
    1000000000000000000000: "165572711549571852431",
    10000000000000000000000: "183245988277116391476741",
    100000000000000000000000: "212571719215881416355251"
}

# Mémoire dynamique de l'application (Session State)
if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}

# ==========================================
# 2. VOS FONCTIONS DE CALCUL COMPTABLE (STR)
# ==========================================
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

# ==========================================
# 3. VOS FONCTIONS D'EXPLORATION DE L'ARBRE
# ==========================================
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
    return lignes_zeros_seules

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
                lignes_details.append(f"Rang 10^{nb_zeros_droite} -> ({chiffre})")
                
    somme_zeros_brute = somme_verticale_multi_lignes_b9(lignes_zeros_seules)
    resultat_final_b9 = addition_comptable_verticale_b9(saisie, somme_zeros_brute)
    return lignes_details, somme_zeros_brute, resultat_final_b9

def executer_etape_2(chaine_b9_str):
    saisie = chaine_b9_str.strip()
    solution_trouvee = []
    
    def explore_arbre(prefixe_actuel):
        if len(prefixe_actuel) == len(saisie):
            somme_brute = simuler_etape_1_pure(prefixe_actuel)
            somme_totale_b9 = somme_verticale_multi_lignes_b9(somme_brute)
            solution_trouvee_b9 = addition_comptable_verticale_b9(prefixe_actuel, somme_totale_b9)
            if solution_trouvee_b9 == saisie:
                solution_trouvee.append(prefixe_actuel)
                return True
            return False
            
        taille_restante = len(saisie) - len(prefixe_actuel)
        lim_basse_somme = simuler_etape_1_pure(prefixe_actuel + "0" * taille_restante)
        limite_basse = addition_comptable_verticale_b9(prefixe_actuel + "1", somme_verticale_multi_lignes_b9(lim_basse_somme))
        
        lim_haute_somme = simuler_etape_1_pure(prefixe_actuel + "9" * taille_restante)
        limite_haute = addition_comptable_verticale_b9(prefixe_actuel + "9", somme_verticale_multi_lignes_b9(lim_haute_somme))
        
        if comparaison_chaines_numeriques(saisie, limite_basse) >= 0 and comparaison_chaines_numeriques(saisie, limite_haute) <= 0:
            debut_range = 1 if prefixe_actuel == "" else 0
            for chiffre_choisi in range(debut_range, 10):
                if explore_arbre(prefixe_actuel + str(chiffre_choisi)):
                    return True
        return False

    explore_arbre("")
    return solution_trouvee if solution_trouvee else "ERREUR"

# ==========================================
# 4. INTERFACE APPLICATIVE GRAPHIQUE
# ==========================================
st.title("👑 Convertisseur base 9 bijective et 10 ")
st.caption("Calculateur Disjoint - Alignement des structures de bases numériques")

# Système d'onglets pour naviguer facilement
onglet_direct, onglet_inverse = st.tabs(["➡️ ÉTAPE 1 : Base 10 -> Base 9", "⬅️ ÉTAPE 2 : Base 9 -> Base 10"])

# --- CONVERTISSEUR DIRECT (BASE 10 -> BASE 9) ---
with onglet_direct:
    st.markdown("#### Génération Mathématique")
    # Sécurité max_chars=20 : impossible d'écrire plus de 20 chiffres dans la zone
    saisie_b10 = st.text_input("Saisissez le montant décimal (Base 10) :", max_chars=20, key="txt_b10")
    
    if st.button("Calculer le format Bijectif", key="btn_direct"):
        saisie_clean = saisie_b10.strip().replace(" ", "")
        if not saisie_clean.isdigit():
            st.error("⚠️ Saisie invalide. Veuillez n'entrer que des chiffres.")
        else:
            lignes, type_calcul, res_final = executer_etape_1(saisie_clean)
            st.session_state.memoire_session[res_final] = saisie_clean
            
            st.success(f"🎯 **RÉSULTAT BASE 9 BIJECTIVE :** `{res_final}`")

# --- CONVERTISSEUR INVERSE (BASE 9 -> BASE 10) ---
with onglet_inverse:
    st.markdown("#### Restauration d'Anatomie (3 Phases)")
    # Sécurité max_chars=20 : blocage matériel au clavier à 20 caractères
    saisie_b9 = st.text_input("Saisissez le nombre bijectif (Base 9) :", max_chars=20, key="txt_b9")
    
    if st.button("Lancer l'Exception de Secours", key="btn_inverse"):
        saisie_clean = saisie_b9.strip().replace(" ", "")
        if not saisie_clean.isdigit():
            st.error("⚠️ Saisie invalide. Veuillez n'entrer que des chiffres.")
        else:
            # PHASE 1 : Recherche en mémoire immédiate
            if saisie_clean in st.session_state.memoire_session:
                resultat = st.session_state.memoire_session[saisie_clean]
                st.success(f"🎯 **[PHASE 1] IDENTIFIÉ DANS LA SESSION :** `{resultat}`")
                
            else:
                # PHASE 2 : Recherche stricte via la cartographie de l'arbre
                res_strict = executer_etape_2(saisie_clean)
                
                if isinstance(res_strict, list) and len(res_strict) > 0 and res_strict != "ERREUR":
                    st.success(f"✨ **[PHASE 2] SÉQUENCE TROUVÉE DANS L'ARBRE :** `{res_strict}`")
                
                # PHASE 3 : Exception du vrai x 9 Bijectif (Pour les segments hors-arbre)
                else:
                    valeur_base10 = 0
                    for symbole in saisie_clean:
                        valeur_base10 = (valeur_base10 * 9) + int(symbole)
                    
                    st.warning(f"💎 **[PHASE 3] EXCEPTION DE CALCUL ACTIVÉE (Vrai x 9) :** `{valeur_base10}`")
