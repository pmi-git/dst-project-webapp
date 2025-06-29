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

## 👥 Auteurs

Patrick Miviere

Collaboration étudiante – Projet académique DevOps

---

