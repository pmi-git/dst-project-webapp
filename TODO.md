# ✅ Projet WordPress - Roadmap Technique

## ⚠️ Environnement
Les environnements `intg` et `prod` doivent être techniquement identiques.  
Seules les valeurs dynamiques (FQDN, secrets) sont autorisées à différer.

---

## 🏁 Objectifs atteints

- [x] Architecture multi-conteneurs : PHP-FPM, NGINX, MariaDB
- [x] Configuration complète de `wp-config.php` (env vars, debug, prefix, etc.)
- [x] Stack Docker opérationnelle (`docker-compose.base.yml`)
- [x] Fichier `Dockerfile` optimisé (`mysqli`, `zip`, etc.)
- [x] Scripts de build (`rebuild.sh`) et de veille (`pause-stack.sh`)
- [x] Readme clair et documenté sur GitHub
- [x] Page d'installation WordPress atteinte (`/wp-admin/install.php`)

---

## 🧪 Environnement `dev` (local Docker/K3s)

- [ ] Générer certificat SSL auto-signé (`generate-cert.sh`)
- [ ] Ajouter `docker-compose.dev.yml`
  - [ ] Activer SSL (`https://localhost:8443`)
  - [ ] Monter config en volume
  - [ ] Variables `WP_DEBUG`, `WP_CACHE`, etc.
  - [ ] Mount des logs pour inspection locale
- [ ] Définir un domaine local (`wordpress.local` ou autre)
- [ ] Créer script d’initialisation `setup-dev.sh`

---

## 🚧 Environnement `intg` (K3s ou EKS avec IP publique)

- [ ] `docker-compose.intg.yml` ou Helm chart
- [ ] Intégration Let's Encrypt via NGINX/Traefik/certbot
- [ ] Déploiement avec noms de domaine `dev.wordpress.pmi.ip-ddns.com`
- [ ] Ajout des Sealed Secrets (`kustomize` ou `kubeseal`)
- [ ] Script de déploiement `deploy-intg.sh`

---

## 🚀 Environnement `prod` (EKS)

- [ ] Copier strictement la config `intg`
- [ ] Déploiement sur `wordpress.pmi.ip-ddns.com`
- [ ] Activation monitoring (prometheus, logging)
- [ ] Déploiement avec `deploy-prod.sh`

---

## 🔐 Secrets & Sécurité

- [ ] Générer et intégrer Sealed Secrets (avec clé publique du cluster)
- [ ] Synchroniser secrets `intg` et `prod` sans fuite de credentials
- [ ] Ajouter vérification dans pipeline (ex : check des variables)

---

## 🔧 Outils & automatisation

- [ ] Ajout de `Makefile` ou `run.sh` (build, test, deploy, logs)
- [ ] Ajouter `wp-cli` (via alias Docker ou container dédié)
- [ ] Ajouter script `docker logs -f` automatique
- [ ] Pipeline GitHub Actions (à venir dans CI/CD)

---

## 🧪 Qualité & tests

- [ ] Ajouter `/ping.php` ou `healthcheck.php` pour supervision
- [ ] Activer `healthcheck:` dans `docker-compose`
- [ ] Tests fonctionnels simples (ping DB, index.php, etc.)

---

## 📦 Application (facultatif)

- [ ] Installer un thème WordPress (TwentyTwentyX ou Astra)
- [ ] Activer un plugin utile (`WP Super Cache`, `Query Monitor`, etc.)
- [ ] Créer une page et un article de test
