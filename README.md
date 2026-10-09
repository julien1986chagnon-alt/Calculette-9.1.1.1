# Calculette 9.1.1.1

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Interface-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-00A4EF?logo=python&logoColor=white" alt="Tkinter" />
  <img src="https://img.shields.io/badge/Status-Experimental-orange" alt="Experimental" />
</p>

Une collection de scripts Python conçus pour explorer une numération alternative basée sur la base 9, sans utiliser le chiffre 0. Le projet combine conversions, calculs arithmétiques, encodage texte, et interfaces utilisateur simples.

## Sommaire

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Structure du dépôt](#structure-du-dépôt)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Principe de fonctionnement](#principe-de-fonctionnement)
- [Exemples](#exemples)
- [Licence](#licence)

## Présentation

Ce dépôt regroupe plusieurs versions d'un même concept : la manipulation de nombres dans un système de numération non standard, où les chiffres autorisés sont 1 à 9.

L'objectif est de tester des méthodes de :

- conversion entre base décimale et base 9 sans zéro
- calcul arithmétique personnalisé
- division avancée basée sur des règles spécifiques
- encodage et décodage de texte
- démonstration visuelle via interface web ou GUI

## Fonctionnalités

- Conversion décimale → base 9 sans zéro
- Conversion base 9 sans zéro → décimale
- Calculs d'addition, soustraction et multiplication
- Logique de division expérimentale
- Encodage de caractères en chaînes de chiffres
- Interfaces Streamlit et Tkinter
- Versions multi-variantes de la calculatrice et du convertisseur

## Structure du dépôt

```text
Calculette-9.1.1.1/
├── Calculette 9.1.1.1.py
├── Calculette 9.1.1.1 streamlit.app.py
├── Programme d'encodage base 9.py
├── Programme d'encodage base 9 streamlit.app.py
├── Convertisseur base 10 à base 9 streamlit.app.py
├── Convertisseur de base 9 et 10 streamlit.app.py
├── Calculatrice amélioré de divivision base 9, dépends de vos limites machine , ne soyer pas gourmands.py
├── Licence
└── README.md
```

## Détail des fichiers

### Calculette 9.1.1.1.py
Script principal de la calculatrice. Il contient les routines de conversion et les fonctionnalités de calcul dans un environnement Streamlit.

### Calculette 9.1.1.1 streamlit.app.py
Version web de la calculatrice, pensée pour être utilisée dans votre navigateur avec Streamlit.

### Programme d'encodage base 9.py
Application Tkinter permettant d'encoder et de décoder du texte à partir d'une suite de chiffres en base 9 sans zéro.

### Convertisseurs et variantes
Plusieurs fichiers complémentaires servent à démontrer des cas d'usage spécifiques :

- conversion base 10 ↔ base 9
- division avancée
- tests de logique numérique particulière
- démonstrations visuelles

## Installation

### Prérequis

- Python 3.x
- pip

### Dépendances

```bash
pip install streamlit
```

## Utilisation

### 1. Interface Streamlit

```bash
streamlit run "Calculette 9.1.1.1 streamlit.app.py"
```

Puis ouvrez l'URL locale affichée dans le terminal.

### 2. Interface Tkinter

```bash
python "Programme d'encodage base 9.py"
```

### 3. Scripts de conversion

Vous pouvez également exécuter directement les scripts spécialisés selon votre besoin.

## Principe de fonctionnement

### Base 9 sans zéro

Le système utilise uniquement les chiffres :

`1, 2, 3, 4, 5, 6, 7, 8, 9`

Le zéro est volontairement exclu, ce qui impose des règles de conversion spécifiques.

### Conversion

Les fonctions du projet calculent en interne la valeur décimale du nombre puis reconstruisent l'équivalent dans le système sans zéro. Les nombres décimaux et négatifs sont également gérés selon les besoins du projet.

### Calculs

Les opérations sont effectuées selon une logique qui :

1. nettoie la saisie
2. convertit les nombres dans un format interne
3. réalise le calcul
4. rétablit la virgule et le format visuel final

### Division évolutive

La division est la partie la plus avancée et la plus expérimentale du projet. Elle cherche à obtenir un quotient cohérent dans le système de numération sans zéro, en explorant des séquences de chiffres et en vérifiant les résultats.

## Exemples

### Exemple de calcul

```text
Entrée : 123.45 + 78.91
Sortie : résultat calculé selon la logique de conversion personnalisée
```

### Exemple d'encodage texte

```text
Entrée : HELIOS
Sortie : suite de chiffres encodés en base 9 sans zéro
```

Le flux généré peut ensuite être décodé pour retrouver le texte original.

## Cas d'usage

Ce projet est particulièrement adapté à :

- l'expérimentation mathématique
- l'apprentissage des systèmes de numération non standard
- la démonstration de conversions personnalisées
- la création d'outils de calcul spéciaux
- la recherche autour de représentations numériques alternatives

## Limites

Ce projet est expérimental et non standard. Il a pour vocation de démontrer des principes et des algorithmes plutôt que de fournir une solution de calcul industrielle classique.

Certaines fonctionnalités peuvent dépendre de :

- la taille des nombres
- la gestion des décimales
- la logique de conversion utilisée
- la complexité de la division

## Licence

Ce projet est distribué sous la licence indiquée dans le fichier `Licence`.

---

Développé par Chagnon Julien Christian Robert.

