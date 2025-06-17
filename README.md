# 🌐 DST Project – Web Application Infrastructure (WordPress & PrestaShop)

Ce projet vise à construire une infrastructure DevOps moderne, modulaire et scalable pour héberger deux CMS open-source (WordPress et PrestaShop), avec un Load Balancer en frontal. L'objectif est d'évoluer progressivement d'un environnement local Dockerisé vers une orchestration complète sur Kubernetes (K3s, puis EKS).

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

## 🧱 Architecture technique

              [ Users ]
                  |
          +----------------+
          | Load Balancer  |
          |    (NGINX)     |
          +----------------+
              /         \
 +----------------+   +----------------+
 | WordPress Stack|   | PrestaShop Stack|
 +----------------+   +----------------+
    | PHP-FPM           | PHP-FPM
    | Redis (cache)     | Redis (sessions)
    | PostgreSQL        | PostgreSQL

---

## 📁 Structure du projet

```bash
├── docker/                  # Dockerfiles par composant
│   ├── nginx/
│   ├── wordpress-php/
│   ├── prestashop-php/
│   ├── redis/
│   └── postgres/
│
├── compose/                 # Docker Compose pour dev/prod
│   ├── docker-compose.base.yml
│   ├── dev/
│   └── prod/
│
├── k8s/                     # Manifests Kubernetes
│   ├── base/
│   └── overlays/
│       ├── dev/
│       └── prod/
│
├── tools/                   # Scripts et setup local
│   ├── k3s-local-env.md
│   └── sealed-secrets/
│
├── scripts/                 # SQL init, healthchecks, etc.
├── .env.dev / .env.prod     # Fichiers d'environnement (non commités)
├── .github/workflows/       # GitHub Actions (CI/CD)
└── README.md
```

---

## 🚀 Lancer l’environnement de dev

Pré-requis : Docker et Docker Compose
cd compose/
docker-compose -f docker-compose.base.yml -f dev/docker-compose.override.yml up --build
Pour la production :
docker-compose -f docker-compose.base.yml -f prod/docker-compose.override.yml up -d

---

## ☸️ Déploiement Kubernetes

🧪 En local avec K3s
kubectl apply -k k8s/overlays/dev
☁️ En production sur EKS (à venir)
Le projet sera porté vers Amazon EKS avec :

Manifests Kubernetes adaptés
Secrets sécurisés via Sealed Secrets
Déploiement automatisé par GitHub Actions
Infrastructure provisionnée via CloudFormation

---

## 🔐 Gestion des secrets

Le projet utilise Bitnami Sealed Secrets :

Les secrets sont chiffrés et versionnés en toute sécurité
Les secrets scellés sont différents selon l’environnement (dev, prod)
Voir k8s/overlays/*/sealed-secrets/ pour les exemples

---

## ✨ En cours...

 Dockerfiles de chaque composant
 Setup Sealed Secrets dans K3s
 Scripts CI/CD (GitHub Actions)
 Manifests Kubernetes complets
 Helm chart optionnel pour packaging

---

## 👥 Auteurs

Patrick Miviere
Collaboration étudiante – Projet académique DevOps

---

