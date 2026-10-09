import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. FONCTIONS DE CONVERSION & ENCODAGE
# ==========================================

def decimal_a_base9_bijective(n):
    if n == 0:
        return ""
    restes = []
    while n > 0:
        reste = n % 9
        quotient = n // 9
        if reste == 0:
            reste = 9
            quotient -= 1
        restes.append(str(reste))
        n = quotient
    return "".join(reversed(restes))

def base9_bijective_a_decimal(nombre_str):
    valeur = 0
    for caractere in nombre_str:
        valeur = valeur * 9 + int(caractere)
    return valeur

def encoder_message_sans_zero(texte):
    blocs_encodes = []
    for caractere in texte:
        code_decimal = ord(caractere)
        code_bijectif = decimal_a_base9_bijective(code_decimal)
        blocs_encodes.append(code_bijectif)
    return " ".join(blocs_encodes)

def decoder_message_sans_zero(flux_b9):
    blocs = flux_b9.strip().split(" ")
    caracteres_decoles = []
    for bloc in blocs:
        if not bloc:
            continue
        try:
            code_decimal = base9_bijective_a_decimal(bloc)
            caracteres_decoles.append(chr(code_decimal))
        except ValueError:
            # Ignore les caractères invalides (comme les lettres dans le flux de chiffres)
            continue
    return "".join(caracteres_decoles)

# ==========================================
# 2. LOGIQUE TRADUCTION DOUBLE SENS (TEMPS RÉEL)
# ==========================================

def actualiser_depuis_texte(event=None):
    """Quand l'utilisateur écrit du texte en haut -> On génère le flux au milieu"""
    texte_saisi = zone_saisie.get("1.0", tk.END).strip("\n")
    flux_b9 = encoder_message_sans_zero(texte_saisi)
    
    # Met à jour la zone Flux sans bloquer l'écriture
    affichage_encode.delete("1.0", tk.END)
    affichage_encode.insert(tk.END, flux_b9)

def actualiser_depuis_flux(event=None):
    """Quand l'utilisateur colle des chiffres au milieu -> On décode le texte en haut"""
    flux_saisi = affichage_encode.get("1.0", tk.END).strip("\n")
    texte_decode = decoder_message_sans_zero(flux_saisi)
    
    # Met à jour la zone Texte Source
    zone_saisie.delete("1.0", tk.END)
    zone_saisie.insert(tk.END, texte_decode)

# ==========================================
# 3. CRÉATION DE L'INTERFACE GRAPHIQUE
# ==========================================

root = tk.Tk()
root.title("Console de Routage Bijectif Bilatéral")
root.geometry("600x450")
root.configure(padx=15, pady=15)

# Style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50")

# En-tête
titre1 = ttk.Label(root, text="Console de Routage Bijectif Bilatéral", style="Title.TLabel")
titre1.pack(anchor=tk.W, pady=(0, 2))
consigne = ttk.Label(root, text="Écrivez du texte en haut pour l'encoder, OU collez des chiffres au milieu pour les décoder !", font=("Arial", 9, "italic"), foreground="#7f8c8d")
consigne.pack(anchor=tk.W, pady=(0, 15))

# --- Zone 1 : Texte Source ---
lbl_saisie = ttk.Label(root, text="Texte Source (Lettres) :")
lbl_saisie.pack(anchor=tk.W)
zone_saisie = tk.Text(root, height=5, font=("Courier", 10))
zone_saisie.insert(tk.END, "HELIOS Base 9")
zone_saisie.pack(fill=tk.X, pady=(0, 15))

# Si on écrit ici, ça encode vers le bas
zone_saisie.bind("<KeyRelease>", actualiser_depuis_texte)


# --- Zone 2 : Flux Encodé (MAINTEANT MODIFIABLE !) ---
lbl_encode = ttk.Label(root, text="Flux Encodé (Chiffres de 1 à 9 séparés par des espaces) :")
lbl_encode.pack(anchor=tk.W)
affichage_encode = tk.Text(root, height=5, font=("Courier", 10), bg="#fcfcfc")
affichage_encode.pack(fill=tk.X, pady=(0, 15))

# Si on écrit ou colle des chiffres ici, ça décode vers le haut !
affichage_encode.bind("<KeyRelease>", actualiser_depuis_flux)


# Lancement initial pour afficher le texte par défaut
actualiser_depuis_texte()

root.mainloop()
