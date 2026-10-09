import gradio as gr

# ==========================================
# 1. FONCTIONS DE CONVERSION & ENCODAGE (VOTRE LOGIQUE)
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
    if not texte:
        return ""
    blocs_encodes = []
    for caractere in texte:
        code_decimal = ord(caractere)
        code_bijectif = decimal_a_base9_bijective(code_decimal)
        blocs_encodes.append(code_bijectif)
    return " ".join(blocs_encodes)

def decoder_message_sans_zero(flux_b9):
    if not flux_b9:
        return ""
    blocs = flux_b9.strip().split(" ")
    caracteres_decoles = []
    for bloc in blocs:
        if not bloc:
            continue
        try:
            code_decimal = base9_bijective_a_decimal(bloc)
            caracteres_decoles.append(chr(code_decimal))
        except ValueError:
            continue
    return "".join(caracteres_decoles)


# ==========================================
# 2. INTERFACE GRAPHIQUE ULTRA-STABLE (GRADIO)
# ==========================================

with gr.Blocks(title="Console de Routage Bijectif Bilatéral") as app:
    gr.Markdown("# 🔐 Console de Routage Bijectif Bilatéral")
    gr.Markdown("---")
    
    with gr.Row():
        # Colonne de gauche : Encodage
        with gr.Column():
            gr.Markdown("### ✍️ Section Encodage")
            texte_source = gr.Textbox(
                label="Texte Source (Lettres)", 
                value="HELIOS base 9", 
                lines=5
            )
            flux_chiffre = gr.Textbox(
                label="✨ Message encodé (En temps réel)", 
                interactive=False, 
                lines=5
            )
            # Liaison temps réel pour l'encodage
            texte_source.change(
                fn=encoder_message_sans_zero, 
                inputs=texte_source, 
                outputs=flux_chiffre
            )
            
        # Colonne de droite : Décodage
        with gr.Column():
            gr.Markdown("### 🔓 Section Décodage")
            flux_saisi = gr.Textbox(
                label="Flux Encodé (Chiffres de 1 à 9 séparés par des espaces)", 
                placeholder="Collez les chiffres ici...", 
                lines=5
            )
            texte_decode = gr.Textbox(
                label="📝 Message décodé (En temps réel)", 
                interactive=False, 
                lines=5
            )
            # Liaison temps réel pour le décodage
            flux_saisi.change(
                fn=decoder_message_sans_zero, 
                inputs=flux_saisi, 
                outputs=texte_decode
            )

# Lancement de l'application
if __name__ == "__main__":
    app.launch()
