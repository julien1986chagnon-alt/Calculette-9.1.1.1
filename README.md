# Calculette 9.1.1.1

Projet Python dédié à l'étude et à la démonstration de calculs numériques dans une base 9 sans zéro, avec des outils de conversion, d'encodage et d'interface utilisateur.

## Présentation

Ce dépôt rassemble plusieurs scripts et variantes expérimentales autour d'un même concept : manipuler des nombres dans un système de numération basé sur les chiffres 1 à 9, sans utiliser le chiffre 0.

L'objectif est de tester des méthodes originales de conversion, de calcul arithmétique et d'encodage de données, tout en proposant des interfaces simples à utiliser via Python standard, Tkinter ou Streamlit.

## Objectifs du projet

- convertir des nombres entre décimal et base 9 sans zéro
- effectuer des additions, soustractions et multiplications dans ce système
- explorer une logique de division avancée
- encoder et décoder du texte sous forme de suites de chiffres
- fournir des démonstrations visuelles via des interfaces graphiques

## Structure du dépôt

- `Calculette 9.1.1.1.py` : calculatrice principale avec logique de conversion et interface Streamlit
- `Calculette 9.1.1.1 streamlit.app.py` : version web de la calculatrice compatible Streamlit
- `Programme d'encodage base 9.py` : encodeur/décodeur de texte en base 9
- `Programme d'encodage base 9 streamlit.app.py` : version Streamlit de l'encodeur
- `Convertisseur base 10 à base 9 streamlit.app.py` : convertisseur dédié
- `Convertisseur de base 9 et 10 streamlit.app.py` : conversion bidirectionnelle
- `Calculatrice amélioré de divivision base 9...py` : version spécialisée pour la division
- `Licence` : licence du projet

## Fonctionnement général

### Système de numération sans zéro

Le projet utilise une base 9 spécifique où les chiffres valides sont :

`1, 2, 3, 4, 5, 6, 7, 8, 9`

Le zéro est exclu, ce qui impose des méthodes de conversion particulières.

Les fonctions principales de conversion incluent :

- conversion décimale vers base 9 adaptée
- conversion base 9 vers décimal
- traitement des nombres négatifs
- gestion des nombres décimaux et de la virgule

### Opérations arithmétiques

Les calculs sont réalisés en convertissant les nombres saisis vers une représentation exploitable en interne, puis en reconvertissant le résultat pour l'affichage.

Les opérations principales sont :

- addition
- soustraction
- multiplication
- division avancée

### Division évolutive

La division est la fonctionnalité la plus sophistiquée du projet. Elle tente de construire une séquence de chiffres compatible avec les règles de la base 9 sans zéro et de déterminer un quotient valide selon une logique mathématique particulière.

## Interfaces disponibles

### 1. Interface Streamlit

La version Streamlit permet d'utiliser le projet directement dans un navigateur web.

#### Prérequis

```bash
pip install streamlit
```

#### Lancement

```bash
streamlit run "Calculette 9.1.1.1 streamlit.app.py"
```

### 2. Interface Tkinter

Le script `Programme d'encodage base 9.py` utilise Tkinter pour offrir une interface graphique locale.

#### Lancement

```bash
python "Programme d'encodage base 9.py"
```

## Exemple d'utilisation

### Calcul d'addition

```text
Entrée : 123.45 + 78.91
Sortie : Résultat calculé selon la logique de conversion base 9 sans zéro
```

### Encodage de texte

```text
Entrée : HELIOS
Sortie : suite de chiffres encodés en base 9 sans zéro
```

Puis, en décodant cette suite, le texte original peut être reconstitué.

## Dépendances

Le projet repose principalement sur :

- Python 3
- `streamlit` pour les interfaces web
- `tkinter` pour les interfaces graphiques locales

## Cas d'usage

Ce dépôt est utile pour :

- expérimenter une base de numération alternative
- comprendre le fonctionnement des conversions non standard
- tester des algorithmes de calcul sans zéro
- construire des démonstrations pédagogiques autour des systèmes numériques

## Limitations

- le système repose sur une logique spécifique non standard
- la division peut devenir complexe en présence de grands nombres
- la lisibilité des résultats dépend fortement du modèle de conversion utilisé
- certains scripts sont expérimentalement orientés démonstration plutôt que production

## Licence

Ce projet est distribué sous la licence présente dans le fichier `Licence`.

## Conclusion

Ce dépôt représente une exploration mathématique et algorithmique autour d'une numération alternative en base 9. Il combine théorie, programmation, interfaces utilisateur et démonstration de calculs dans un cadre original et expérimental.

Il constitue une base solide pour des extensions futures, notamment :

- amélioration de la gestion des nombres décimaux
- optimisation de la division
- ajout de tests unitaires
- interface plus ergonomique
- documentation plus détaillée pour chaque script

---

Développé par Chagnon Julien Christian Robert.
