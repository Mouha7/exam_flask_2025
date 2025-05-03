# 🍳 Cuisine Collective

![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## 📖 À propos

Cuisine Collective est une plateforme web interactive permettant aux passionnés de cuisine de partager leurs recettes, de découvrir celles des autres et d'observer en temps réel qui cuisine quoi. Cette application utilise les technologies Flask, Tailwind CSS et Socket.IO pour offrir une expérience utilisateur fluide et moderne.

![Aperçu de l'application](https://via.placeholder.com/800x400?text=Cuisine+Collective)

## ✨ Fonctionnalités principales

### 🧭 Navigation générale
- **Page d'accueil** : Découvrez les recettes les plus récentes
- **Liste des recettes** : Explorez toutes les recettes partagées
- **Cuisine en direct** : Observez qui cuisine quoi en temps réel

### 👨‍🍳 Pour les utilisateurs connectés
- **Partager une recette** : Créez et publiez vos propres recettes
- **Modifier vos recettes** : Mettez à jour vos publications
- **Cuisiner une recette** : Indiquez aux autres lorsque vous cuisinez une recette
- **Noter les recettes** : Donnez votre appréciation des recettes des autres

### ⚡ Fonctionnalités en temps réel
- **Notifications** : Recevez des alertes lorsque quelqu'un commence ou arrête de cuisiner
- **Mise à jour de la liste de cuisine en direct** : Visualisez immédiatement les changements

## 🚀 Installation

### Prérequis
- Python 3.8+
- Node.js et npm
- Base de données SQLite (incluse)

### Étapes d'installation

1. Clonez le répertoire du projet :
```bash
git https://github.com/Mouha7/exam_flask_2025.git
cd exam_flask_2025-main
```

2. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

3. Installez les dépendances pour Tailwind CSS :
```bash
npm install
npm install @tailwindcss/forms
```

4. Générez le CSS :
```bash
npx tailwindcss -i ./static/css/style.css -o ./static/css/output.css
```

5. Lancez l'application :
```bash
flask run
```

6. Accédez à l'application dans votre navigateur :
```
http://localhost:5000
```

## 👥 Comptes utilisateurs prédéfinis

Pour tester l'application, vous pouvez utiliser les comptes suivants :

| Utilisateur | Mot de passe |
|------------|------------|
| mouhamed   | mouhamed   |
| rassoul    | rassoul    |

## 📝 Guide d'utilisation

### Création de compte
1. Cliquez sur "Inscription" dans la barre de navigation
2. Remplissez le formulaire avec vos informations
3. Validez votre inscription

### Connexion
1. Cliquez sur "Connexion" dans la barre de navigation
2. Entrez votre nom d'utilisateur et mot de passe
3. Cochez "Se souvenir de moi" (optionnel)
4. Connectez-vous

### Partager une recette
1. Connectez-vous à votre compte
2. Cliquez sur "Nouvelle recette"
3. Remplissez tous les champs du formulaire :
   - Titre de la recette
   - Description
   - Temps de préparation
   - Niveau de difficulté
   - Liste des ingrédients (un par ligne)
   - Instructions détaillées (une étape par ligne)
   - Image (optionnelle)
4. Cliquez sur "Publier la recette"

### Cuisiner une recette
1. Naviguez vers la recette que vous souhaitez cuisiner
2. Cliquez sur "Je cuisine cette recette!"
3. Tous les utilisateurs connectés recevront une notification
4. Vous apparaîtrez dans la section "Cuisine en direct"
5. Pour terminer, cliquez sur "Arrêter de cuisiner"

### Rechercher des recettes
1. Utilisez la barre de recherche sur la page des recettes
2. Entrez un mot-clé (nom de recette, ingrédient, etc.)
3. Explorez les résultats

## 🏗️ Architecture du projet

```
cuisine-collective/
├── app.py              # Point d'entrée de l'application
├── models/             # Modèles de données
├── routes/             # Routes Flask
├── services/           # Services métier
├── static/             # Ressources statiques
│   ├── css/            # Fichiers CSS (Tailwind)
│   ├── js/             # Scripts JavaScript
│   ├── images/         # Images téléchargées
│   └── sounds/         # Sons de notification
├── templates/          # Templates HTML
│   ├── auth/           # Pages d'authentification
│   └── recipes/        # Pages de recettes
└── requirements.txt    # Dépendances Python
```

Le projet est organisé selon une architecture MVC :
- **Models** : Définition des structures de données
- **Views** : Templates HTML avec Tailwind CSS
- **Controllers** : Routes Flask et logique d'application
- **Services** : Logique métier séparée des contrôleurs

## 🔧 Résolution des problèmes courants

| Problème | Solution |
|----------|----------|
| **Styles CSS incorrects** | Régénérez le CSS avec `npx tailwindcss -i ./static/css/style.css -o ./static/css/output.css` |
| **Notifications manquantes** | Vérifiez que JavaScript est activé dans votre navigateur |
| **Problèmes de son** | Assurez-vous que votre navigateur autorise la lecture automatique de l'audio |
| **Erreur Module not found** | Exécutez `npm install @tailwindcss/forms` pour installer le plugin manquant |

## 🤝 Contribuer au projet

Pour contribuer :
1. Créez une branche pour votre fonctionnalité
2. Développez et testez vos modifications
3. Soumettez une pull request avec une description détaillée

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

Développé avec ❤️ pour l'examen de Flask 2025.