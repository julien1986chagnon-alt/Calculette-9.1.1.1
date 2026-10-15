import sys
import time

# Suppression absolue de TOUTES les sécurités logicielles internes
sys.set_int_max_str_digits(1000000)
sys.setrecursionlimit(1000000) # Brise la barrière de récursion !

# ==============================================================================
# 1. VOS FONCTIONS DE CONVERSION DE BASE (Version originale stricte sans zéro)
# ==============================================================================

def logique_sans_zero_a_decimal(nombre_str):
    nombre_str = nombre_str.strip().replace(" ", "").replace(",", "").replace(".", "")
    if not nombre_str:
        return 0
    est_negatif = nombre_str.startswith("-")
    if est_negatif:
        nombre_str = nombre_str[1:]
    if not nombre_str:
        return 0
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
        if reste == 0:
            restes.append("9")
            n = (n // 9) - 1
        else:
            restes.append(str(reste))
            n = n // 9
    resultat_str = "".join(reversed(restes))
    return "-" + resultat_str if est_negatif else resultat_str

# ==============================================================================
# 2. LE VÉRITABLE ACCÉLÉRATEUR CORRIGÉ (Recherche avec retour en arrière)
# ==============================================================================

def chercher_extension_sans_abandon(num_str, den_str):
    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)
    
    if den_dec == 0:
        return "Erreur", "Saisie Invalide", "Division par zéro impossible"
        
    if num_dec_origine % den_dec == 0:
        q_brut = num_dec_origine // den_dec
        q_visuel = decimal_a_logique_sans_zero(q_brut)
        return q_visuel, "Aucune", "Fermeture immédiate"
        
    partie_entiere_dec = num_dec_origine // den_dec
    resultat_trouve = None
    
    limite_harmonique = len(den_str.strip().replace(" ", "")) + 2
    
    def explorer(chaine_actuelle, dec_actuel):
        nonlocal resultat_trouve
        if resultat_trouve is not None:
            return
            
        if len(chaine_actuelle) >= limite_harmonique:
            return
            
        for chiffre in "123456789":
            nouvelle_chaine = chaine_actuelle + chiffre
            nouveau_dec_actuel = dec_actuel * 9 + int(chiffre)
            
            if nouveau_dec_actuel % den_dec == 0:
                q_brut = nouveau_dec_actuel // den_dec
                q_visuel = decimal_a_logique_sans_zero(q_brut)
                
                longueur_ext = len(nouvelle_chaine)
                if len(q_visuel) >= longueur_ext:
                    res_final = f".({q_visuel.zfill(longueur_ext)})"
                    resultat_trouve = (res_final, nouvelle_chaine, f"Fermeture quantique réussie en {longueur_ext} étapes.")
                    return
                    
            explorer(nouvelle_chaine, nouveau_dec_actuel)

    explorer("", num_dec_origine)
    
    if resultat_trouve is not None:
        return resultat_trouve
    return "Calcul inachevé", "Infini", "Recherche interrompue."

# ==============================================================================
# 3. INTERFACE CONSOLE REFORMATÉE ET NETTOYÉE
# ==============================================================================

if __name__ == "__main__":
    while True:
        try:
            print("-" * 75)
            print("CRASH-TEST TOTAL BASE 9 - RECHERCHE RAPIDE RECTIFIÉE")
            print("-" * 75)
            print("(Écrivez 'quitter' pour fermer)\n")
            
            num_input = input("Entrez le Numérateur : ").strip().replace(" ", "")
            if num_input.lower() == "quitter":
                break
            den_input = input("Entrez le Dénominateur : ").strip().replace(" ", "")
            if den_input.lower() == "quitter":
                break
                
            if not num_input or not den_input:
                continue
                
            temps_debut = time.time()
            reponse, extension, details = chercher_extension_sans_abandon(num_input, den_input)
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut
            
            # --- BLOC DE NETTOYAGE VISUEL REFORMATÉ ---
            # 1. Nettoyage de la réponse principale (Suppression des parenthèses et ajout du zéro initial)
            reponse_propre = reponse
            if reponse_propre.startswith(".("):
                # Enlève le point et les parenthèses, et ajoute le vrai zéro virgule initial
                contenu = reponse_propre.replace(".(", "").replace(")", "")
                reponse_propre = f"0,{contenu}"
            elif reponse_propre.startswith("."):
                reponse_propre = f"0,{reponse_propre[1:]}"
                
            # 2. Nettoyage de la séquence générée pour l'afficher sous forme décimale
            if extension.isdigit():
                extension_propre = f"0,{extension}"
            else:
                extension_propre = extension
            
            # --- AFFICHAGE FINAL ÉPURÉ ---
            print("\n" + "+" + "="*68 + "+")
            print(f" 💎 RÉSULTAT DU CALCUL : {reponse_propre}")
            print(f" ⚡ SÉQUENCE GÉNÉRÉE : {extension_propre}")
            print(f" ⏱️ TEMPS D'EFFORT : {temps_ecoule:.6f} secondes")
            print("+" + "="*68 + "+\n")
            
        except KeyboardInterrupt:
            print("\n[!] Test stoppé manuellement (Ctrl+C).")
            break
        except Exception as e:
            print(f"\n[!] Erreur : {e}\n")
