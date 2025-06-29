# 🌐 DST Project – Web Application Infrastructure (WordPress & PrestaShop)

Ce projet vise à construire une infrastructure DevOps moderne, modulaire et scalable pour héberger deux CMS open-source (WordPress et PrestaShop), avec un Load Balancer en frontal. 

L'objectif est d'évoluer progressivement d'un environnement local Dockerisé vers une orchestration complète sur Kubernetes (K3s, puis EKS).

---

## 📦 Objectifs du projet

- Décomposer chaque composant applicatif en microservices (Nginx, PHP-FPM, DB, Redis…)
- Construire des Dockerfiles spécifiques pour chaque composant
- Tester l’infrastructure en local (Docker Compose)
- Déployer sur Kubernetes local (K3s)
- Déployer sur AWS via EKS avec CI/CD
- Gérer les secrets de manière sécurisée avec Sealed Secrets
- Automatiser les déploiements via GitHub Actions ou Gitlab

---

## 🛠️ Utilisation des scripts

### 📦 WordPress – Environnement `dev`

Les scripts suivants permettent de lancer, inspecter ou nettoyer l’environnement de développement WordPress (`dev`), accessible en HTTPS sur `https://localhost:8443` :
```bash
| Script                        | Description                                         |
|-------------------------------|-----------------------------------------------------|
| `run-wp-dev.sh`               | Lance l’environnement WP docker-compose             |
| `run-wp-dev-logs.sh`          | Affiche les logs temps réel de tous les services WP |
| `clean-wp-dev.sh`             | Supprime les volumes, containers et images WP       |
| `status-wp-dev.sh`            | Affiche l’état des containers WP                    |
```
---

### 🛍️ PrestaShop – Environnement `dev`

Même logique que pour WordPress, en HTTPS via `https://localhost:8444` :
```bash
| Script                        | Description                                          |
|-------------------------------|------------------------------------------------------|
| `run-pts-dev.sh`              | Lance l’environnement PrestaShop docker-compose      |
| `run-pts-dev-logs.sh`         | Affiche les logs temps réel des services PrestaShop  |
| `clean-pts-dev.sh`            | Supprime les volumes, containers et images PTS       |
| `status-pts-dev.sh`           | Affiche l’état des containers PTS                    |
```
> 💡 Les ports et volumes sont isolés pour chaque stack.

---

### 🔁 Scripts communs (WP + PTS)

Pour tout gérer en une seule commande :
```bash
| Script                 | Description                                                    |
|------------------------|----------------------------------------------------------------|
| `run-all-dev.sh`       | Lance les environnements WordPress + PrestaShop                |
| `run-all-dev-logs.sh`  | Regroupe et affiche les logs des deux environnements           |
| `clean-all-dev.sh`     | Nettoie tous les volumes, containers, images des deux stacks   |
```
---

## 🔐 Gestion des variables d’environnement

Le projet utilise un fichier `.env` à la racine, **non versionné dans Git**, qui contient tous les secrets, mots de passe, hôtes, etc.

### ✅ Exemple fourni

Un fichier **`.env.example`** est fourni avec les variables attendues.

💡 Ne modifiez jamais .env.example directement. C’est un fichier de référence à garder propre.

### 🔑 Variables typiques attendues
```bash
# WordPress
WORDPRESS_DB_NAME=wordpress
WORDPRESS_DB_USER=wpuser
WORDPRESS_DB_PASSWORD=wppass
WORDPRESS_DB_HOST=wp-mariadb

# PrestaShop
PRESTASHOP_DB_NAME=prestashop
PRESTASHOP_DB_USER=ptsuser
PRESTASHOP_DB_PASSWORD=ptspass
PRESTASHOP_DB_HOST=pts-mariadb

# Redis (WordPress)
WP_REDIS_HOST=wp-redis
WP_CACHE=true

# Redis (Prestashop)
WP_REDIS_HOST=pts-redis
WP_CACHE=true
```
---

## 👥 Auteurs

Patrick Miviere

Collaboration étudiante – Projet académique DevOps

---

