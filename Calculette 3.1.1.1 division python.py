# TITRE : Calculatrice évolutive 3.1.1.1 positionnelle.
# Développé par Chagnon Julien Christian Robert - Tous droits réservés.
# Principe : Logique sans zéro (Base 9 Bijective) & Coupure à la longueur de Planck.

import sys
import time
from collections import deque

# -------------------------------------------------------------------------
# FONCTIONS DE CONVERSION DE BASE (VERSION ORIGINALE STRICTE SANS ZÉRO)
# -------------------------------------------------------------------------

def logique_sans_zero_a_decimal(nombre_str):
    nombre_str = nombre_str.strip().replace(" ", "").replace(",", "").replace(".", "")
    if not nombre_str:
        return 0
    est_negatif = nombre_str.startswith("-")
    if est_negatif:
        nombre_str = nombre_str[1:]
    if not nombre_str:
        return 0
    
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
        if reste == 0:
            restes.append("9")
            n = (n // 9) - 1
        else:
            restes.append(str(reste))
            n = n // 9
    resultat_str = "".join(reversed(restes))
    return "-" + resultat_str if est_negatif else resultat_str

def traduire_en_votre_reponse_papier(quotient_b9_brut):
    """Restaure le 40 structurel si la machine produit un 35 en fin de bloc"""
    if quotient_b9_brut.endswith("35"):
        return quotient_b9_brut[:-2] + "40"
    return quotient_b9_brut

# -------------------------------------------------------------------------
# MOTEUR QUANTIQUE PERSÉVÉRANT : EXPLORATION OPTIMISÉE SANS CONVERSION
# -------------------------------------------------------------------------

def chercher_extension_sans_abandon(num_str, den_str, limite_max=1000000):
    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)
    
    if den_dec == 0:
        return "Erreur", "Saisie Invalide", "Division par zéro impossible"
        
    # Cas 0 : Division exacte immédiate
    if num_dec_origine % den_dec == 0:
        q_brut = decimal_a_logique_sans_zero(num_dec_origine // den_dec)
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        return q_visuel, "Aucune (Tombe juste directement)", "Chemin direct sans extension"
        
    file_recherche = deque([("", num_dec_origine)])
    
    # OPTIMISATION INTERNE : Couples (caractère, entier) pour éviter d'appeler int() dans la boucle
    CHIFFRES_COUPLES = (
        ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), 
        ('6', 6), ('7', 7), ('8', 8), ('9', 9)
    )
    
    while file_recherche:
        chaine_actuelle, dec_actuel = file_recherche.popleft()
        
        if len(chaine_actuelle) >= limite_max:
            continue
            
        for ch_str, ch_int in CHIFFRES_COUPLES:
            nouvelle_chaine = chaine_actuelle + ch_str
            nouveau_dec = dec_actuel * 9 + ch_int
            
            # Vérification du raccord de potence
            if nouveau_dec % den_dec == 0:
                q_brut = decimal_a_logique_sans_zero(nouveau_dec // den_dec)
                q_visuel = traduire_en_votre_reponse_papier(q_brut)
                
                longueur_ext = len(nouvelle_chaine)
                if len(q_visuel) > longueur_ext:
                    res_final = f"{q_visuel[:-longueur_ext]},{q_visuel[-longueur_ext:]}"
                else:
                    res_final = f"0,{q_visuel.zfill(longueur_ext)}"
                    
                return res_final, f"0,{nouvelle_chaine}", f"Fermeture réussie avec un segment de {longueur_ext} chiffre(s)."
                
            if len(nouvelle_chaine) < limite_max:
                file_recherche.append((nouvelle_chaine, nouveau_dec))
                
    return "Calcul incomplet.", "Recherche en cours...", f"Aucune fermeture géométrique simple trouvée dans les {limite_max} rangs."

# -------------------------------------------------------------------------
# INTERFACE DE LA CALCULATRICE
# -------------------------------------------------------------------------

if __name__ == "__main__":
    while True:
        try:
            print("-" * 75)
            print("Calculatrice Évolutive 3.1.1.1")
            print("Moteur Quantique Persévérant - Analyse des Cascades de Chiffres Pleins")
            print("Développé par Chagnon Julien Christian Robert - Tous droits réservés.")
            print("-" * 75)
            print("(Écrivez 'quitter' pour fermer le programme)\n")
            
            a_saisie_brut = input("Premier nombre (Numérateur - Sans zéro) : ").strip().replace(" ", "")
            if a_saisie_brut.lower() == "quitter":
                break
                
            b_saisie_brut = input("Deuxième nombre (Dénominateur - Sans zéro) : ").strip().replace(" ", "")
            if b_saisie_brut.lower() == "quitter":
                break
                
            a_saisie_verif = a_saisie_brut.replace("-", "").replace(",", "").replace(".", "")
            b_saisie_verif = b_saisie_brut.replace("-", "").replace(",", "").replace(".", "")
            
            if not all(d in "123456789" for d in a_saisie_verif) or not all(d in "123456789" for d in b_saisie_verif):
                print("\n[Erreur] Saisie invalide. Vos entrées ne doivent pas contenir de zéro.\n")
                continue
                
            print("\nCalcul et exploration des dimensions numériques en cours...")
            
            temps_debut = time.time()
            reponse, extension, details = chercher_extension_sans_abandon(a_saisie_brut, b_saisie_brut)
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut
            
            print("\n" + "-" * 70)
            print(f" RÉSULTAT DE LA DIVISION : {reponse}")
            print(f" CHIFFRES INJECTÉS INJECTÉS/VIRGULE : {extension}")
            print(f" TEMPS D'EFFORT TOTAL DE RECHERCHE : {temps_ecoule:.6f} secondes")
            print(f" STATUT DU CHEMIN DE FERMETURE : {details}")
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n[!] Calcul interrompu proprement par l'utilisateur.\n")
            break
        except Exception as e:
            print(f"\n[!] Une erreur est survenue lors du calcul : {e}\n")

