
# 🌐 InfluenceHub - Plateforme de Collecte et Classement d’Influenceurs

## 📖 Contexte
MVP d’une plateforme permettant de :
- Répertorier les influenceurs
- Collecter leurs informations (nom, réseau social, nombre d’abonnés…)
- Visualiser et filtrer les profils
- Classer les influenceurs selon différents critères

Ce projet a pour but de fournir une **base technique** simple mais extensible.

---

## ⚙️ Stack Technique
- **Backend** : Django 5 / Django REST Framework
- **Frontend (templates)** : Django Templates (Bootstrap intégré)
- **Base de données** : PostgreSQL (ou SQLite par défaut)
- **Authentification** : Django auth (login / register)
- **Gestion statique & médias** : Django staticfiles + dossier `media/`

---

## 📂 Structure du projet
```

influencehub/
├── influencehub/        # Configuration principale Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/  # Gestion des utilisateurs
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   └── influencer/      # Gestion des influenceurs
│       ├── management/commands/populate\_data.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── forms.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── influencers/
│       ├── list.html
│       ├── detail.html
│       ├── register.html
│       └── success.html
├── static/              # Fichiers CSS/JS/images
├── media/               # Uploads des utilisateurs
├── requirements.txt
└── manage.py

````

---

## 🚀 Installation & Lancement

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/votre-user/influencehub.git
cd influencehub
````

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 5️⃣ Charger les données d’exemple

```bash
python manage.py populate_data
```

### 6️⃣ Lancer le serveur

```bash
python manage.py runserver
```

---

## 🧑‍💻 Fonctionnalités principales

* ✅ Authentification (inscription, login)
* ✅ CRUD Influenceurs (ajout, édition, suppression, liste, détail)
* ✅ Recherche & filtres par nom, réseau social, nombre d’abonnés
* ✅ Classement des influenceurs
* ✅ Page d’accueil et interface utilisateur simple
* ✅ Commande custom `populate_data` pour injecter des données fictives

---

## 📸 Captures d’écran

<img width="1221" height="622" alt="image" src="https://github.com/user-attachments/assets/f54498c9-ea9e-41bd-96fb-c1677ec6c353" />
<img width="1213" height="654" alt="image" src="https://github.com/user-attachments/assets/f1145106-047b-45e4-b9d1-1aab84452372" />
<img width="1204" height="624" alt="image" src="https://github.com/user-attachments/assets/f03a2642-c582-4614-95ce-a69708f29bb2" />



---

## 📊 Exemple API (Influenceurs)

### Liste des influenceurs

```http
GET /api/influencers/
```

**Réponse**

```json
[
  {
    "id": 1,
    "name": "Alice Doe",
    "platform": "Instagram",
    "followers": 125000,
    "category": "Fashion"
  },
  {
    "id": 2,
    "name": "John Smith",
    "platform": "YouTube",
    "followers": 98000,
    "category": "Tech"
  }
]
```

---

## 📌 Livrables

* **Application Web** fonctionnelle avec interface utilisateur
* **Dépôt GitHub** public avec ce README
* **Présentation PowerPoint** pour résumer :

  * Le contexte
  * La stack choisie
  * Les fonctionnalités
  * Démo et prochaines évolutions

---

👨‍💻 *Développé dans le cadre du test technique InfluenceHub.*

```

---
