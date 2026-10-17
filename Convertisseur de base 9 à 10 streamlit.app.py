# Convertisseur base 10 à base 9.py - C:\Users\julie\Documents\Projet 9\Convertisseur base 10 à base 9.py (3.14.7)
# File Edit Format Run Options Window Help
#
# CONFIGURATION DEFINITIVE : LA PYRAMIDE RECTIFIEE DE CHAGNON JULIEN
#

TABLE_DES_ZEROS_PURS = {
    "10": "11",
    "100": "111",
    "1000": "1221",
    "10000": "12541",
    "100000": "127951",
    "1000000": "1318561",
    "10000000": "13512271",
    "100000000": "138667981",
    "1000000000": "1436458381",
    "10000000000": "14812158911",
    "100000000000": "153833759121",
    "1000000000000": "1594372461321",
    "10000000000000": "16548187174641",
    "100000000000000": "172141278522151",
    "1000000000000000": "182654179353661",
    "10000000000000000": "1919429558388137",
    "100000000000000000": "212241366911915181",
    "1000000000000000000": "2234732747374166991",
    "10000000000000000000": "2358915363222681811",
    "100000000000000000000": "2495244995464539221"
}

# MOTEUR 1 : MULTIPLICATION PURE EN BASE 9 BIJECTIVE
def multiplier_b9_bijective(chaine_b9, multiplicateur_int):
    if multiplicateur_int == 0:
        return "0"
        
    resultat = []
    retenue = 0
    
    for chiffre in reversed(chaine_b9):
        produit = int(chiffre) * multiplicateur_int + retenue
        if produit == 0:
            reste = 0
            retenue = 0
        else:
            reste = produit % 9
            if reste == 0:
                reste = 9
                retenue = (produit // 9) - 1
            else:
                retenue = produit // 9
        resultat.append(str(reste))
        
    if retenue > 0:
        if retenue % 9 == 0:
            resultat.append("9")
            retenue_restante = (retenue // 9) - 1
            if retenue_restante > 0:
                resultat.append(str(retenue_restante))
        else:
            resultat.append(str(retenue))
            
    return "".join(reversed(resultat))

# MOTEUR 2 : ADDITION PURE EN BASE 9 (AVEC SUPPORT DU 0 DE DEPART)
def additionner_b9(chaine1, chaine2):
    resultat = []
    retenue = 0
    
    max_len = max(len(chaine1), len(chaine2))
    c1 = chaine1.zfill(max_len)
    c2 = chaine2.zfill(max_len)
    
    for i in range(max_len - 1, -1, -1):
        somme = int(c1[i]) + int(c2[i]) + retenue
        if somme == 0:
            reste = 0
            retenue = 0
        else:
            reste = somme % 9
            if reste == 0:
                reste = 9
                retenue = (somme // 9) - 1
            else:
                retenue = somme // 9
        resultat.append(str(reste))
        
    if retenue > 0:
        if retenue % 9 == 0:
            resultat.append("9")
        resultat.append(str(retenue))
            
    return "".join(reversed(resultat))

# CONVERSION DIRECTE ENTIÈREMENT EN BASE 9 CONFORME À VOS IMAGES
def convertisseur_par_segments(montant_str):
    montant_str = str(montant_str).strip().replace(" ", "").replace(",", "").replace(".", "").replace("'", "")
    
    if not montant_str.isdigit():
        return "ERREUR : Saisie non numérique"
        
    if montant_str == "0" or not montant_str.lstrip("0"):
        return "0"
        
    if len(montant_str) == 1:
        return montant_str
        
    premier_chiffre = int(montant_str[0])
    longueur = len(montant_str)
    
    str_palier = "1" + "0" * (longueur - 1)
    
    if str_palier in TABLE_DES_ZEROS_PURS:
        sequence_b9 = TABLE_DES_ZEROS_PURS[str_palier]
        
        if premier_chiffre == 1 and montant_str == str_palier:
            return multiplier_b9_bijective(sequence_b9, premier_chiffre)
        else:
            produit_b9 = multiplier_b9_bijective(sequence_b9, premier_chiffre)
            
            # Extraction purement textuelle du reste pour éviter les approximations sur les grands nombres
            reste_montant = montant_str[1:].lstrip("0")
            if not reste_montant:
                reste_montant = "0"
            
            if reste_montant != "0":
                return additionner_b9(produit_b9, convertisseur_par_segments(reste_montant))
            else:
                return produit_b9
    else:
        return "PALIER NON PARAMETRE (Limite maximale de la grille atteinte)"

# BOUCLE INTERACTIVE CONSOLE INITIALE RESTAURÉE
if __name__ == "__main__":
    print("=================================================================")
    print(" ARCHITECTURE MATHEMATIQUE PAR CHAGNON JULIEN CHRISTIAN ROBERT ")
    print(" MOTEUR DE CONVERSION : BASE 10 ==> BIJECTIVE BASE 9 ")
    print(" Tapez 'quitter' pour fermer la console.\n")
    
    while True:
        montant_saisi = input("Entrez le montant en Base 10 à convertir : ")
        if montant_saisi.lower().strip() == "quitter":
            print("Fermeture du programme.")
            break
            
        resultat = convertisseur_par_segments(montant_saisi)
        
        if "ERREUR" in resultat or "PALIER" in resultat:
            print("X", resultat, "\n")
        else:
            print("[*] COMPOSANTE BASE 9 PLEINE :")
            print(resultat)
            print("[*] Longueur du résultat :", len(resultat), "chiffres (Aucun zéro).\n")

