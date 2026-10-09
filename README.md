# Calculette 9.1.1.1

Ce dépôt regroupe plusieurs projets Python autour du même concept : manipuler des nombres en base 9, sans utiliser le chiffre 0, et explorer des méthodes de conversion, de calcul et d'encodage.

Les scripts ont été créés pour tester des idées mathématiques, des conversions entre bases, et des interfaces utilisateur simples avec Python.

## 1. Présentation générale

Le principe central de ce projet est d'utiliser une numération en base 9 où les chiffres autorisés sont :

1, 2, 3, 4, 5, 6, 7, 8, 9

Le chiffre 0 n'est pas utilisé. Cela impose des règles de conversion particulières et un comportement mathématique original, notamment pour :

- la conversion décimal -> base 9 sans zéro
- la conversion base 9 sans zéro -> décimal
- les opérations arithmétiques
- la division avec recherche de motifs numériques
- l'encodage de texte sous forme de suite de chiffres

## 2. Fichiers présents

### `Calculette 9.1.1.1.py`

C'est le cœur de la calculatrice. Il contient :

- la logique de conversion entre nombre décimal et base 9 sans zéro
- les fonctions de calcul pour l'addition, la soustraction et la multiplication
- la logique de division "évolutive" ou "quantique"
- une interface Streamlit qui permet à l'utilisateur d'entrer des nombres et d'obtenir des résultats

Le script fonctionne avec des nombres pouvant contenir des virgules décimales et utilise une logique spéciale pour aligner les chiffres selon la position de la virgule.

### `Calculette 9.1.1.1 streamlit.app.py`

C'est une version web de la calculatrice, destinée à être utilisée avec Streamlit.

Elle propose :

- un formulaire de saisie de deux nombres
- la sélection de l'opération : addition, soustraction, multiplication ou division
- le calcul directement dans le navigateur
- un affichage plus lisible des résultats

Cette version est probablement la plus pratique pour un usage visuel et rapide.

### `Programme d'encodage base 9.py`

Ce script est un outil d'encodage/decodage de texte en base 9.

Son fonctionnement est le suivant :

1. chaque lettre est convertie en son code ASCII
2. ce nombre est ensuite transformé en base 9 sans zéro
3. le résultat est affiché sous forme d'une suite de chiffres séparés par des espaces
4. réciproquement, il est possible de recopier cette suite pour reconstituer le texte original

C'est un système de codage bijectif, dans le sens où un message texte peut être transformé puis reconstruit sans perte.

### Autres fichiers de conversion et de calcul

Le dépôt contient aussi plusieurs versions plus spécialisées, notamment :

- `Calculatrice amélioré de divivision base 9...py`
- `Convertisseur base 10 à base 9 streamlit.app.py`
- `Convertisseur de base 9 et 10 streamlit.app.py`
- `Programme d'encodage base 9 streamlit.app.py`

Ces fichiers proposent des variantes de conversion ou des interfaces plus ciblées sur des tâches précises comme :

- conversion entre base 10 et base 9
- affichage en interface web
- division avancée en base 9
- encodage de texte

## 3. Comment fonctionne la base 9 sans zéro

En base 10, on utilise les chiffres 0 à 9.

En base 9 sans zéro, on utilise seulement 1 à 9.

Exemple :

- 1 en base 10 = 1 en base 9
- 9 en base 10 = 10 en base 9, mais comme 0 est interdit, le système est réécrit de manière spécifique selon la logique du projet, ce qui explique l'algorithme particulier

La conversion repose sur :

- division successive par 9
- stockage des restes
- remplacement des 0 par 9 dans certaines phases
- reconstruction du nombre dans le bon ordre

C'est ce mécanisme qu'on retrouve dans les fonctions `decimal_a_logique_sans_zero()` et `logique_sans_zero_a_decimal()`.

## 4. Fonctionnement des calculs

### Addition, soustraction et multiplication

Les opérations de base utilisent :

1. la conversion du nombre saisi en valeur décimale
2. le calcul décimal classique
3. reconversion du résultat dans le système sans zéro
4. réinsertion de la virgule au bon endroit

La partie la plus délicate est la gestion des décimales : le programme doit conserver la bonne position de la virgule et réaligner les chiffres correctement.

### Division

La division est la partie la plus avancée du projet.

Le script tente de trouver une séquence de chiffres qui permet de trouver un quotient exact ou un quotient approché en respectant les règles de base 9 sans zéro.

L'algorithme :

- nettoie la saisie
- transforme les nombres en décimal
- vérifie s'il n'y a pas de reste
- sinon explore des suites de chiffres pour chercher un quotient compatible
- retourne le résultat sous forme de valeur lisible et exploitable

Cette logique est décrite dans la fonction `chercher_extension_sans_abandon()`.

## 5. Interface utilisateur

Le dépôt contient à la fois :

- des scripts en ligne de commande / console
- des versions Streamlit pour navigateur
- une interface Tkinter pour le codage texte / décodage chiffre

### Streamlit

La version web se lance avec :

```bash
pip install streamlit
streamlit run "Calculette 9.1.1.1 streamlit.app.py"
```

### Tkinter

Le script Python standard avec interface graphique peut être exécuté directement :

```bash
python "Programme d'encodage base 9.py"
```

## 6. Exemple d'utilisation

### Exemple de calcul

- saisie : `123.45`
- opération : addition ou multiplication
- résultat : affiché selon la méthode de conversion base 9 sans zéro

### Exemple d'encodage texte

Entrée :

```text
HELIOS
```

Sortie :

```text
... suite de chiffres en base 9 sans zéro ...
```

Puis, en décodant, le texte original est retrouvé.

## 7. Dépendances

Les projets Python utilisent principalement :

- Python 3
- `streamlit` pour les interfaces web
- `tkinter` pour l'interface graphique standard

## 8. Objectif du projet

Ce dépôt est avant tout une expérimentation mathématique et algorithmique.

Il vise à :

- tester une base numérique non conventionnelle
- développer des méthodes de conversion personnalisées
- explorer des calculs sans le chiffre 0
- créer des outils visuels pour comprendre le système

## 9. Conclusion

Ce projet est un mélange entre :

- calcul mathématique
- base numérique personnalisée
- conversion de nombres
- encodage de texte
- visualisation Web

Il peut être vu comme une mini-plateforme de démonstration de logique numérique alternative.

---

Si tu veux, je peux aussi créer un README encore plus avancé avec :

- une section "installation"
- une section "exemples de calculs"
- une section "capture d'écran / interface"
- une version plus professionnelle pour GitHub
- une version plus courte et plus esthétique

Je peux le faire directement dans le dépôt.
