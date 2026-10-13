import streamlit as st

st.set_page_config(page_title="Calculatrice Division Verticale Base 9", page_icon="🧮")

# --- VOS FONCTIONS D'ORIGINE CONSERVÉES À 100% ---

def division_tableau_automatique(n, x):
    """Calcule dynamiquement la valeur de la table sans base de données."""
    if x == 1:
        return n
    if x < n:
        return n - x
    return 9 - x + n

def convertir_en_base_9_sans_zero(nombre_base_10):
    """Convertit un score total d'une colonne dans votre système sans zéro."""
    if nombre_base_10 == 0:
        return ""
    
    resultat = ""
    while nombre_base_10 > 0:
        reste = nombre_base_10 % 9
        if reste == 0:
            resultat = "9" + resultat
            nombre_base_10 = (nombre_base_10 // 9) - 1
        else:
            resultat = str(reste) + resultat
            nombre_base_10 = nombre_base_10 // 9
    return resultat

def addition_base_9_pure(blocs):
    """Effectue l'addition colonne par colonne selon vos règles."""
    max_len = max(len(b) for b in blocs)
    blocs_padded = [b.zfill(max_len) for b in blocs]
    
    resultat_final = ""
    retenue = 0
    
    # On progresse de droite à gauche
    for i in range(max_len - 1, -1, -1):
        somme_colonne_10 = retenue + sum(int(b[i]) for b in blocs_padded)
        
        if i == 0:
            conversion = convertir_en_base_9_sans_zero(somme_colonne_10)
            resultat_final = conversion + resultat_final
        else:
            conversion = convertir_en_base_9_sans_zero(somme_colonne_10)
            chiffre_unites = conversion[-1] if conversion else "9"
            chiffre_retenue = conversion[:-1] if conversion else ""
            
            resultat_final = chiffre_unites + resultat_final
            retenue = int(chiffre_retenue) if chiffre_retenue else 0
            
    return resultat_final

# --- INTERFACE GRAPHIQUE STREAMLIT ---

st.title("🧮 Calculatrice Division Verticale en Base 9")
st.write("Conçue par l'Architecte. Exécutée fidèlement selon vos algorithmes.")

# Entrées utilisateur (remplace les "input" du terminal)
col1, col2 = st.columns(2)
with col1:
    n1_input = st.text_input("Entrez le premier nombre (ex: 153) :", value="153").strip()
with col2:
    n2_input = st.text_input("Entrez le deuxième nombre (ex: 149) :", value="142").strip()

if st.button("🚀 Lancer le calcul vertical", type="primary"):
    # Validation des entrées selon vos critères exacts
    if not n1_input.isdigit() or not n2_input.isdigit() or '0' in n1_input or '0' in n2_input:
        st.error("Erreur : Veuillez entrer uniquement des nombres entiers sans le chiffre 0.")
    else:
        try:
            # Étape 1 : Division chiffre par chiffre avec explications
            N_str = str(n1_input)
            X_str = str(n2_input)
            blocs = []
            explications_globales = []
            
            for chiffre_N in N_str:
                bloc_actuel = ""
                explications = []
                for chiffre_X in X_str:
                    res = division_tableau_automatique(int(chiffre_N), int(chiffre_X))
                    bloc_actuel += str(res)
                    explications.append(f"{chiffre_N} / {chiffre_X} = {res}")
                
                explications_globales.append(f"Pour le chiffre {chiffre_N} : " + ", ".join(explications) + f" -> Bloc : {bloc_actuel}")
                blocs.append(bloc_actuel)
            
            # Affichage de la décomposition
            st.subheader("--- DECOMPOSITION DU CALCUL ---")
            st.code("\n".join(explications_globales))
            
            # Étape 2 & 3 : Présentation visuelle et résultat de l'addition
            st.subheader("--- ADDITION FINALE ---")
            
            max_len = max(len(b) for b in blocs)
            lignes_addition = [b.zfill(max_len) for b in blocs]
            lignes_addition.append("-" * max_len)
            
            # Calcul via votre fonction pure
            reponse = addition_base_9_pure(blocs)
            lignes_addition.append(f"= {reponse}")
            
            st.code("\n".join(lignes_addition))
            
        except Exception as e:
            st.error(f"Une erreur est survenue lors du calcul : {e}")

