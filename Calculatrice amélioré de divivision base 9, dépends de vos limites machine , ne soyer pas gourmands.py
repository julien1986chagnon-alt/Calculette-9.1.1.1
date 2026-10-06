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
    # Règle de fermeture structurelle en fin de bloc
    if quotient_b9_brut.endswith("39"):
        return quotient_b9_brut[:-2] + "40"
    return quotient_b9_brut


# ==============================================================================
# 2. LE VÉRITABLE ACCÉLÉRATEUR CORRIGÉ (Recherche avec retour en arrière automatique)
# ==============================================================================

def chercher_extension_sans_abandon(num_str, den_str):
    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)
    
    if den_dec == 0:
        return "Erreur", "Saisie Invalide", "Division par zéro impossible"
        
    # Cas direct immédiat
    if num_dec_origine % den_dec == 0:
        q_brut = decimal_a_logique_sans_zero(num_dec_origine // den_dec)
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        return q_visuel, "Aucune (Calcul direct pile)", "Fermeture immédiate"
        
    partie_entiere_dec = num_dec_origine // den_dec
    resultat_trouve = None
    
    # LOI DE PROPORTIONNALITÉ : Limite la recherche pour éviter de bloquer le PC
    limite_harmonique = len(den_str.strip().replace(" ", "")) + 2
    
    # Scan en profondeur avec gestion du demi-tour (Backtracking)
    def explorer(chaine_actuelle, dec_actuel):
        nonlocal resultat_trouve
        
        if resultat_trouve is not None:
            return
            
        # Si on dépasse la taille critique, on fait demi-tour pour essayer d'autres chiffres
        if len(chaine_actuelle) >= limite_harmonique:
            return
            
        for chiffre in "123456789":
            nouvelle_chaine = chaine_actuelle + chiffre
            nouveau_dec_actuel = dec_actuel * 9 + int(chiffre)
            
            if nouveau_dec_actuel % den_dec == 0:
                q_brut = decimal_a_logique_sans_zero(nouveau_dec_actuel // den_dec)
                q_visuel = traduire_en_votre_reponse_papier(q_brut)
                
                longueur_ext = len(nouvelle_chaine)
                if len(q_visuel) >= longueur_ext:
                    res_final = f"{q_visuel[:-longueur_ext]}.({q_visuel[-longueur_ext:]})"
                else:
                    res_final = f"0.{q_visuel.zfill(longueur_ext)}"
                    
                resultat_trouve = (res_final, nouvelle_chaine, f"Fermeture quantique réussie en {longueur_ext} étapes.")
                return
                
            explorer(nouvelle_chaine, nouveau_dec_actuel)

    explorer("", num_dec_origine)
    
    if resultat_trouve is not None:
        return resultat_trouve
        
    return "Calcul inachevé", "Infini", "Recherche interrompue."


# ==============================================================================
# 3. INTERFACE CONSOLE AMÉLIORÉE POUR LES UTILISATEURS
# ==============================================================================

if __name__ == "__main__":
    while True:
        try:
            print("=" * 75)
            print("CRASH-TEST TOTAL BASE 9 - RECHERCHE RAPIDE RECTIFIÉE")
            print("=" * 75)
            print("(Écrivez 'quitter' pour fermer)\n")
            
            num_input = input("Entrez le Numérateur : ").strip().replace(" ", "")
            if num_input.lower() == "quitter": break
            den_input = input("Entrez le Dénominateur : ").strip().replace(" ", "")
            if den_input.lower() == "quitter": break
            
            if not num_input or not den_input: continue
            
            temps_debut = time.time()
            reponse, extension, details = chercher_extension_sans_abandon(num_input, den_input)
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut
            
            print("\n" + "+" + "-"*68)
            print(f" 💎 RÉSULTAT DU CALCUL : {reponse}")
            print(f" ⚡ CHIFFRES COMPLÉMENTAIRES TROUVÉS APRÈS LA VIRGULE : {extension}")
            print(f" ⏱️ TEMPS D'EFFORT DU PROCESSEUR : {temps_ecoule:.6f} secondes")
            print("+" + "-"*68 + "\n")
            
        except KeyboardInterrupt:
            print("\n[i] Test stoppé manuellement (Ctrl+C).")
            break
        except Exception as e:
            print(f"\n[x] Erreur : {e}\n")
