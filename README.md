# 📌 Projet Fil Rouge - Analyse des locations Airbnb à Paris 🏡

## 📖 Description

Ce projet consiste à analyser les données des locations Airbnb à Paris en utilisant **PostgreSQL** pour le stockage des données et **Python (Pandas, Matplotlib, Seaborn)** pour l'analyse et la visualisation.

## 📂 Structure du Projet

- **Base de données PostgreSQL** : Stockage des tables `listings` et `reviews`.
- **DataFrame Pandas** : Chargement, filtrage et transformation des données.
- **Analyse de données** : Calculs statistiques et exploration des tendances.
- **Visualisation des données** : Graphiques pour illustrer les résultats.

## 🚀 Objectifs du Projet

### 📊 Pré-traitement des Données :

1. Charger depuis la base de données **PostgreSQL** les tables **listings** et **reviews**.
2. Afficher le schéma des **DataFrames**.
3. Filtrer les listings avec **disponibilité > 30 jours** sur 365 jours.
4. Calculer la **moyenne des prix des listings** par type de chambre.
5. Extraire le **mois** à partir de la date dans les **reviews**.
6. Ajouter une colonne **Year** à partir de `date_review`.
7. Filtrer les listings avec **disponibilité > 30 jours et prix < 100 euros**.
8. Ajouter une colonne **price\_per\_room** dans `listings`.
9. Remplacer les valeurs manquantes dans **reviews\_per\_month** par **0**.
10. Remplacer les valeurs nulles de **review\_scores\_rating** par la moyenne calculée.

### 📊 Analyse et Statistiques :

11. Calculer la moyenne de **review\_scores\_rating**.
12. Calculer la **moyenne des prix** pour chaque type de logement.
13. Trouver le **nombre total de types de chambres** dans chaque quartier.
14. Calculer la **corrélation** entre **nombre de nuits disponibles** et **prix**.
15. Identifier les **5 quartiers avec le plus grand nombre de listings**.

### 🗄️ PostgreSQL - Requêtes SQL :

16. Compter le **nombre total d'annonces** par ville.
17. Calculer la **disponibilité et les prix moyens** par quartier.
18. Obtenir le **nombre total d’avis** dans la table `reviews`.
19. Trouver la **date du dernier avis**.
20. Identifier les **5 utilisateurs ayant publié le plus d’avis**.
21. Compter le **nombre d’hôtes uniques** dans la table `listings`.
22. Ajouter une colonne `premium_listing` et stocker les résultats dans une **nouvelle table**.
23. Calculer la **moyenne des nuits disponibles** par hôte et stocker les résultats.

## 📊 Visualisation des Données

1. **Graphique en barres** : Prix moyen par type de chambre.

   - Axe X : Types de chambre (`Private Room`, `Entire Home/Apartment`, etc.).
   - Axe Y : Prix moyen (€).
   - 📷&#x20;

2. **Graphique en ligne** : Nombre de commentaires par mois.

   - Axe X : Mois de l'année.
   - Axe Y : Nombre total de commentaires.
   - 📷&#x20;

## 🛠️ Technologies Utilisées

- **Python** : Pandas, Matplotlib, Seaborn pour l'analyse et la visualisation.
- **PostgreSQL** : Base de données relationnelle pour stocker les données.
- **pgAdmin** : Interface de gestion PostgreSQL.
- **Jupyter Notebook** : Exécution des scripts d'analyse.
- **Git & GitHub** : Versionning et partage du code.

## 🔧 Installation et Exécution

1️⃣ **Cloner le projet** :

```bash
git clone https://github.com/LamyaaER/Projet-Fil-Rouge-Airbnb.git
cd Projet-Fil-Rouge-Airbnb
```

2️⃣ **Installation des dépendances** :

```bash
pip install -r requirements.txt
```

3️⃣ **Lancer l'analyse des données** :

```bash
python filRouge.py
```

## 📜 Licence

Ce projet est sous **licence MIT**.

👤 **Auteur** : [Lamyaa ER-RECHAKI](https://github.com/LamyaaER)

