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
            # Ignore les caractères invalides pendant la saisie
            continue
    return "".join(caracteres_decoles)

# ==========================================
# 2. LOGIQUE DE MISE À JOUR EN TEMPS RÉEL
# ==========================================

def actualiser_traduction(event=None):
    # Récupérer le texte saisi par l'utilisateur
    texte_saisi = zone_saisie.get("1.0", tk.END).strip("\n")
    
    # Encodage
    flux_b9 = encoder_message_sans_zero(texte_saisi)
    # Mise à jour de la zone "Flux Encodé"
    affichage_encode.config(state=tk.NORMAL)
    affichage_encode.delete("1.0", tk.END)
    affichage_encode.insert(tk.END, flux_b9)
    affichage_encode.config(state=tk.DISABLED)
    
    # Décodage en temps réel
    affichage_decode.config(state=tk.NORMAL)
    affichage_decode.delete("1.0", tk.END)
    affichage_decode.insert(tk.END, texte_saisi) # Le décodage réaffirme le texte initial
    affichage_decode.config(state=tk.DISABLED)

# ==========================================
# 3. CRÉATION DE L'INTERFACE GRAPHIQUE (Tkinter)
# ==========================================

# Fenêtre principale
root = tk.Tk()
root.title("Console de Routage Bijectif Bilatéral")
root.geometry("600x550")
root.configure(padx=15, pady=15)

# Style général
style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50")

# Titres d'en-tête
titre1 = ttk.Label(root, text="Console de Routage Bijectif Bilatéral", style="Title.TLabel")
titre1.pack(anchor=tk.W, pady=(0, 2))
consigne = ttk.Label(root, text="Modifiez le champ ci-dessous, le décodage s'opère instantanément à partir du flux converti.", font=("Arial", 9, "italic"), foreground="#7f8c8d")
consigne.pack(anchor=tk.W, pady=(0, 15))

# --- Zone de saisie (Texte Source) ---
lbl_saisie = ttk.Label(root, text="Texte Source :")
lbl_saisie.pack(anchor=tk.W)
zone_saisie = tk.Text(root, height=5, font=("Courier", 10))
zone_saisie.insert(tk.END, "HELIOS Base 9")
zone_saisie.pack(fill=tk.X, pady=(0, 15))
# Déclencher la fonction dès qu'une touche est relâchée
zone_saisie.bind("<KeyRelease>", actualiser_traduction)

# --- Zone d'affichage (Flux Encodé) ---
lbl_encode = ttk.Label(root, text="Flux Encodé (Base 9) :")
lbl_encode.pack(anchor=tk.W)
affichage_encode = tk.Text(root, height=5, font=("Courier", 10), bg="#f8f9fa", state=tk.DISABLED)
affichage_encode.pack(fill=tk.X, pady=(0, 15))

# --- Zone d'affichage (Message Décodé) ---
lbl_decode = ttk.Label(root, text="Message Décodé :")
lbl_decode.pack(anchor=tk.W)
affichage_decode = tk.Text(root, height=5, font=("Courier", 10), bg="#f8f9fa", state=tk.DISABLED)
affichage_decode.pack(fill=tk.X, pady=(0, 15))

# Lancer la première traduction pour le texte par défaut
actualiser_traduction()

# Lancement de la boucle d'affichage Windows
root.mainloop()
