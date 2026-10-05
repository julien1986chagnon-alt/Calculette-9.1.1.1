import sys
import time

# Augmentation de la sécurité pour la manipulation de grands nombres textuels
sys.set_int_max_str_digits(100000)

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
    """ Règle de fermeture structurelle en fin de bloc (39 -> 40) """
    if quotient_b9_brut.endswith("39"):
        return quotient_b9_brut[:-2] + "40"
    return quotient_b9_brut

# ==============================================================================
# 2. LE MOTEUR QUANTIQUE PROTOCOLLÉ (Sécurité proportionnelle et RAM protégée)
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
        return q_visuel, "Aucune (Tombe juste directement)", "Fermeture directe"

    # LOI DE PROPORTIONNALITÉ : La virgule fait au maximum la taille du dénominateur + 2 chiffres
    limite_harmonique = len(den_str.strip().replace(" ", "")) + 2
    partie_entiere_dec = num_dec_origine // den_dec

    resultat_trouve = None

    # Exploration par vagues en profondeur (DFS) avec nettoyage en direct de la RAM
    def explorer(chaine_actuelle, dec_actuel):
        nonlocal resultat_trouve
        
        if resultat_trouve is not None:
            return
            
        if len(chaine_actuelle) >= limite_harmonique:
            return

        for chiffre in "123456789":
            nouvelle_chaine = chaine_actuelle + chiffre
            nouveau_dec_actuel = dec_actuel * 9 + int(chiffre)

            # Raccordement exact trouvé !
            if nouveau_dec_actuel % den_dec == 0:
                q_brut = decimal_a_logique_sans_zero(nouveau_dec_actuel // den_dec)
                q_visuel = traduire_en_votre_reponse_papier(q_brut)
                
                longueur_ext = len(nouvelle_chaine)
                if len(q_visuel) >= longueur_ext:
                    res_final = f"{q_visuel[:-longueur_ext]}.{q_visuel[-longueur_ext:]}"
                else:
                    res_final = f"0.{q_visuel.zfill(longueur_ext)}"
                
                resultat_trouve = (res_final, nouvelle_chaine, f"Fermeture quantique réussie avec un segment de {longueur_ext} chiffres.")
                return

            # Continuer l'exploration sous le seuil harmonique
            if len(nouvelle_chaine) < limite_harmonique:
                explorer(nouvelle_chaine, nouveau_dec_actuel)

    # Lancement du scan sécurisé
    explorer("", num_dec_origine)

    if resultat_trouve is not None:
        return resultat_trouve
        
    return "Calcul restreint", "Limite harmonique atteinte", f"Aucun raccord court trouvé sous le seuil de {limite_harmonique} chiffres."

# ==============================================================================
# 3. INTERFACE CONSOLE STRICTEMENT LIMITÉE À 6 CHIFFRES AU DÉNOMINATEUR
# ==============================================================================

if __name__ == "__main__":
    while True:
        try:
            print("-" * 75)
            print("CALCULATRICE CONSOLE BASE 9 — VERSION SÉCURISÉE 6 CHIFFRES")
            print("Sécurité matérielle : Dénominateur STRICTEMENT limité à 6 chiffres max")
            print("-" * 75)
            print("(Écrivez 'quitter' pour fermer)\n")
            
            num_input = input("Entrez le Numérateur (Longueur libre) : ").strip().replace(" ", "")
            if num_input.lower() == "quitter":
                break
            den_input = input("Entrez le Dénominateur (Maximum 6 chiffres) : ").strip().replace(" ", "")
            if den_input.lower() == "quitter":
                break
                
            if not num_input or not den_input:
                continue
                
            # 🛡️ LE VERROU MATÉRIEL SÉCURISÉ : Blocage immédiat sur le clavier si > 6 chiffres
            taille_den = len(den_input.replace(".", "").replace("-", ""))
            if taille_den > 6:
                print(f"\n[!] ERREUR SÉCURITÉ : Votre dénominateur fait {taille_den} chiffres.")
                print("[!] Ce fichier est configuré pour bloquer strictement à 6 chiffres MAXIMUM.\n")
                continue
                
            print("\n[i] Analyse du raccordement et lancement du chronomètre...")
            
            # ⏱️ DEBUT DU CHRONOMÈTRE
            temps_debut = time.time()
            
            reponse, extension, details = chercher_extension_sans_abandon(num_input, den_input)
            
            # ⏱️ FIN DU CHRONOMÈTRE
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut
            
            print("\n" + "=" * 70)
            print(f"📥 RÉSULTAT OBTENU : {reponse}")
            print(f"⚡ SÉQUENCE DANS LA VIRGULE : {extension if extension else 'Aucune'}")
            print(f"🔮 STATUT DE LA STRUCTURE : {details}")
            print(f"⏱️ TEMPS DE CALCUL MACHINE : {temps_ecoule:.6f} secondes")
            print("=" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n[!] Calcul arrêté proprement par l'utilisateur.")
        except Exception as e:
            print(f"\n[!] Une interruption est survenue : {e}\n")
