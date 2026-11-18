import streamlit as st

# Configuration graphique de la page
st.set_page_config(page_title="Calculateur Disjoint", page_icon="🔢", layout="centered")

# ==========================================
# 1. VOTRE TABLEUR DES PASSAGES ZÉRO (L'ARBRE)
# ==========================================
TABLEUR_PASSAGES_ZERO = {
    1: ("0", "1"),
    10: ("1","11"),
    100: ("11","111"), 
    1000: ("221","1221"),
    10000: ("2531","12531"),
    100000: ("27841","127841"),
    1000000: ("317351","1317351"),
    10000000: ("3491861","13491861"),
    100000000: ("38521571","138521571"),
    1000000000: ("434737381","1434737381"),
    10000000000: ("4783222291","14783222291"),
    100000000000: ("53725445311","153725445311"),
    1000000000000: ("591979898421","1591979898421"),
    10000000000000: ("6622889993631","16622889993631"),
    100000000000000: ("73853112139941","173853112139941"),
    1000000000000000: ("823484233551451","1823484233551451"),
    10000000000000000: ("9158437569165961","19158437569165961"),
    100000000000000000: ("111753824371836671","211753824371836671"),
    1000000000000000000: ("1229393168191314481","2229393168191314481"),
    10000000000000000000: ("13534434861214459391","23534434861214459391"),
    100000000000000000000: ("148878784573359164411","248878784573359164411"),
    1000000000000000000000: ("1648777741416961818521","2648777741416961818521"),
    10000000000000000000000: ("18247666255587681114731","28247666255587681114731"),
    100000000000000000000000: ("211735438822575592263141","311735438822575592263141"),
    1000000000000000000000000: ("2329189838148442624894551","3329189838148442624894551"),
    10000000000000000000000000: ("25632199329643868874951161","35632199329643868874951161"),
    100000000000000000000000000: ("282954313637183668735562771","382954313637183668735562771"),
}


# Mémoire dynamique de l'application (Session State)
if "memoire_session" not in st.session_state:
    st.session_state.memoire_session = {}
# =====================================================================
# 2. FONCTIONS DE CALCUL VERTICAL EN BASE 9 BIJECTIVE
# =====================================================================

def addition_comptable_verticale_b9(str_n1, str_n2):
    n1, n2 = str_n1.strip(), str_n2.strip()
    if n1 == "0": return n2
    if n2 == "0": return n1
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

def soustraction_comptable_verticale_b9(str_grand, str_petit):
    """Soustrait un palier du reste en respectant les règles de votre addition sans zéro."""
    if str_grand == str_petit:
        return "0"
    max_len = max(len(str_grand), len(str_petit))
    n_grand = str_grand.strip().zfill(max_len)
    n_petit = str_petit.strip().zfill(max_len)
    resultat, emprunt = [], 0

    for i in range(max_len - 1, -1, -1):
        d_grand = int(n_grand[i])
        d_petit = int(n_petit[i]) + emprunt

        if d_grand <= d_petit and i > 0:
            diff = (d_grand + 9) - d_petit
            emprunt = 1
        else:
            diff = d_grand - d_petit
            emprunt = 0

        if diff == 0 and i > 0:
            diff = 9
            emprunt = 1

        resultat.append(str(diff))

    res_final = "".join(reversed(resultat)).lstrip('0')
    return res_final if res_final != "" else "0"

def somme_verticale_multi_lignes_b9(liste_chaines):
    total = "0"
    for chaine in liste_chaines:
        total = addition_comptable_verticale_b9(total, chaine)
    return total

def multiplication_comptable_unitaire_b9(str_b9, chiffre_int):
    resultat = "0"
    for _ in range(chiffre_int):
        resultat = addition_comptable_verticale_b9(resultat, str_b9)
    return resultat

def est_superieur_ou_egal_b9(str_a, str_b):
    """Compare deux nombres en Base 9 (sans zéro) par longueur puis chiffre par chiffre."""
    a = str_a.lstrip('0')
    b = str_b.lstrip('0')
    if len(a) != len(b):
        return len(a) > len(b)
    return a >= b

# =====================================================================
# 3. FONCTIONS ALLER ET RETOUR (DÉCOMPTE DU PLUS GRAND AU PLUS PETIT)
# =====================================================================

def executer_etape_1(montant_b10_str):
    """Aller : Utilise directement le total cumulé de votre tableau."""
    saisie = montant_b10_str.strip().replace(" ", "")
    if not saisie.isdigit() or int(saisie) <= 0:
        return None

    longueur = len(saisie)
    lignes_totaux = []

    for i, chiffre_str in enumerate(saisie):
        chiffre = int(chiffre_str)
        nb_zeros_droite = longueur - 1 - i
        if chiffre > 0:
            puissance_dix = 10 ** nb_zeros_droite
            if puissance_dix in TABLEUR_PASSAGES_ZERO:
                # Lit la 2e valeur du tuple : le total cumulé (index 1)
                total_unitaire_b9 = TABLEUR_PASSAGES_ZERO[puissance_dix][1]
                partiel_b9 = multiplication_comptable_unitaire_b9(total_unitaire_b9, chiffre)
                lignes_totaux.append(partiel_b9)

    return somme_verticale_multi_lignes_b9(lignes_totaux)

def executer_etape_2(chaine_b9_str):
    """Retour : Repère le plus grand multiple dans votre tableau et descend sur le reste."""
    saisie = chaine_b9_str.strip().replace(" ", "")
    if not saisie.isdigit() or "0" in saisie:
        return None

    reste_b9 = saisie
    total_base10 = 0
    
    # On trie vos paliers du plus grand (10^26) jusqu'au plus petit (1)
    paliers_descendants = sorted(TABLEUR_PASSAGES_ZERO.keys(), reverse=True)
    
    for cle_b10 in paliers_descendants:
        if reste_b9 == "0":
            break
            
        passage, total_palier_b9 = TABLEUR_PASSAGES_ZERO[cle_b10]
        
        # On cherche le plus grand multiple (de 9 à 1) qui rentre dans le reste actuel
        for multiple in range(9, 0, -1):
            valeur_multiple_b9 = multiplication_comptable_unitaire_b9(total_palier_b9, multiple)
            
            if est_superieur_ou_egal_b9(reste_b9, valeur_multiple_b9):
                # On ajoute ce palier à la réponse finale en Base 10
                total_base10 += cle_b10 * multiple
                # On soustrait ce bloc pour continuer sur ce qu'il reste
                reste_b9 = soustraction_comptable_verticale_b9(reste_b9, valeur_multiple_b9)
                break

    return str(total_base10) if total_base10 > 0 else "1"

# =====================================================================
# 4. INTERFACE APPLICATIVE GRAPHIQUE
# =====================================================================

st.title("🔢 Convertisseur base 9 bijective et 10")
st.caption("Calculateur Disjoint - Alignement des structures de bases numériques")

onglet_direct, onglet_inverse = st.tabs(["➡️ ÉTAPE 1 : Base 10 -> Base 9", "⬅️ ÉTAPE 2 : Base 9 -> Base 10"])

with onglet_direct:
    st.markdown("#### Génération Mathématique")
    saisie_b10 = st.text_input("Saisissez le montant décimal (Base 10) :", max_chars=26, key="txt_b10")
    
    if st.button("Calculer le format Bijectif", key="btn_direct"):
        res_final = executer_etape_1(saisie_b10)
        if res_final is None:
            st.error("⚠️ Saisie invalide. Entrez un nombre entier supérieur à 0.")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 9 BIJECTIVE :** `{res_final}`")

with onglet_inverse:
    st.markdown("#### Décompte par Paliers Descendants")
    saisie_b9 = st.text_input("Saisissez le nombre bijectif (Base 9) :", max_chars=27, key="txt_b9")
    
    if st.button("Décompter vers Base 10", key="btn_inverse"):
        res_b10 = executer_etape_2(saisie_b9)
        if res_b10 is None:
            st.error("⚠️ Saisie invalide. Utilisez uniquement les chiffres de 1 à 9 (sans zéro).")
        else:
            st.success(f"🟢 **RÉSULTAT BASE 10 :** `{res_b10}`")

