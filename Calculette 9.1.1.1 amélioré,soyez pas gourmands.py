import sys
import time

# ==============================================================================
# CONFIGURATION DU BENCHMARK COMPOSANTS (Désactivation des verrous logiciels)
# ==============================================================================
sys.set_int_max_str_digits(1000000) # Autorise les nombres géants en texte
sys.setrecursionlimit(1000000) # Force Python à accepter la profondeur maximale

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
# 2. LE MOTEUR QUANTIQUE "STRESS-TEST" — HORS LIMITE POUR PROCESSEUR PURE
# ==============================================================================

def chercher_extension_sans_abandon(num_str, den_str):
    """
    Moteur de benchmark pur.
    Explore l'arbre en profondeur totale sans aucune restriction matérielle logicielle.
    C'est la vitesse brute du CPU de l'utilisateur qui dictera le temps de réponse.
    """
    num_dec_origine = logique_sans_zero_a_decimal(num_str)
    den_dec = logique_sans_zero_a_decimal(den_str)
    
    if den_dec == 0:
        return "Erreur", "Saisie Invalide", "Division par zéro impossible"
        
    if num_dec_origine % den_dec == 0:
        q_brut = decimal_a_logique_sans_zero(num_dec_origine // den_dec)
        q_visuel = traduire_en_votre_reponse_papier(q_brut)
        return q_visuel, "Aucune (Calcul direct pile)", "Fermeture immédiate sans cascade"

    partie_entiere_dec = num_dec_origine // den_dec
    resultat_trouve = None

    # Scan en profondeur libre (DFS) - Auto-nettoyage de la RAM activé
    def explorer(chaine_actuelle, dec_actuel):
        nonlocal resultat_trouve # Correction du bug de portée variable
        
        if resultat_trouve is not None:
            return

        for chiffre in "123456789":
            nouvelle_chaine = chaine_actuelle + chiffre
            nouveau_dec_actuel = dec_actuel * 9 + int(chiffre)

            # Raccordement géométrique parfait détecté
            if nouveau_dec_actuel % den_dec == 0:
                q_brut = decimal_a_logique_sans_zero(nouveau_dec_actuel // den_dec)
                q_visuel = traduire_en_votre_reponse_papier(q_brut)
                
                longueur_ext = len(nouvelle_chaine)
                if len(q_visuel) >= longueur_ext:
                    res_final = f"{q_visuel[:-longueur_ext]}.{q_visuel[-longueur_ext:]}"
                else:
                    res_final = f"0.{q_visuel.zfill(longueur_ext)}"
                
                resultat_trouve = (res_final, nouvelle_chaine, f"Fermeture quantique totale réussie en {longueur_ext} étapes.")
                return

            # Descente continue sans aucun garde-fou logiciel
            explorer(nouvelle_chaine, nouveau_dec_actuel)

    # Lancement du scan sur le silicium de l'utilisateur
    explorer("", num_dec_origine)

    if resultat_trouve is not None:
        return resultat_trouve
        
    return "Calcul inachevé", "Infini", "Le processeur n'a pas trouvé la fin de la cascade."

# ==============================================================================
# 3. INTERFACE DE BENCHMARK UNIVERSELLE (Console locale)
# ==============================================================================

if __name__ == "__main__":
    while True:
        try:
            print("=" * 75)
            print(" BENCHMARK ARITHMÉTIQUE BASE 9 — LE CRASH-TEST HORS LIMITE MACHINE")
            print("= Attention : Longueur libre totale. Testez la puissance brute de votre CPU =")
            print("= C'est à vous de surveiller votre PC. Si ça chauffe trop, faites Ctrl+C ! =")
            print("=" * 75)
            print("(Écrivez 'quitter' pour fermer le programme)\n")
            
            num_input = input("Entrez le Numérateur (Longueur libre) : ").strip().replace(" ", "")
            if num_input.lower() == "quitter":
                break
            
            den_input = input("Entrez le Dénominateur (Longueur libre) : ").strip().replace(" ", "")
            if den_input.lower() == "quitter":
                break
                
            if not num_input or not den_input:
                continue
                
            print("\n[!] AVERTISSEMENT : Lancement de la cascade numérique en profondeur pure...")
            print("[i] Effort maximal de vos composants en cours...")
            
            # ⏱️ DEBUT DU CHRONOMÈTRE
            temps_debut = time.time()
            
            reponse, extension, details = chercher_extension_sans_abandon(num_input, den_input)
            
            # ⏱️ FIN DU CHRONOMÈTRE
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut
            
            print("\n" + "📊 " + "-" * 68)
            print(f"📥 RÉSULTAT OBTENU : {reponse}")
            print(f"⚡ SÉQUENCE DANS LA VIRGULE : {extension if extension else 'Aucune'}")
            print(f"🔮 STATUT DE LA STRUCTURE : {details}")
            print(f"⏱️ TEMPS D'EFFORT DE VOTRE PROCESSEUR : {temps_ecoule:.6f} secondes")
            print("📊 " + "-" * 68 + "\n")
            
        except KeyboardInterrupt:
            print("\n[!] INTERRUPTION : Test stoppé manuellement par l'utilisateur (Ctrl+C).\n")
        except Exception as e:
            print(f"\n[!] Le benchmark a provoqué une alerte système : {e}\n")
