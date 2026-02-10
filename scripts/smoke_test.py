import yaml
import os
import requests
import time
import sys

# CONFIGURATION
CLIENTS_FILE = "configs/clients.yaml"
MAX_RETRIES = 10
DELAY = 10

# --- DETECTION DE L'ENVIRONNEMENT (Comme dans deploy.py) ---
CURRENT_BRANCH = os.getenv("GITHUB_REF_NAME", "unknown")

if CURRENT_BRANCH == "main":
    print("💎 MODE PRODUCTION (Smoke Test)")
    TARGET_ENV = "prod"
    VPS_IP = os.getenv("VPS_IP_PROD")
    DOMAIN_SUFFIX = "pmi.ovh"
else:
    print("🛠 MODE DEVELOPPEMENT (Smoke Test)")
    TARGET_ENV = "dev"
    VPS_IP = os.getenv("VPS_IP_DEV")
    DOMAIN_SUFFIX = "dev.pmi.ovh"

if not VPS_IP:
    print(f"❌ Erreur: L'IP du VPS ({TARGET_ENV.upper()}) est introuvable.")
    sys.exit(1)

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def check_url(url):
    print(f"   🔎 Test de {url}...", end="", flush=True)
    for i in range(MAX_RETRIES):
        try:
            # On suit les redirections (allow_redirects=True)
            response = requests.get(f"http://{url}", timeout=5, allow_redirects=True)
            
            # CRITERE DE REUSSITE : Code 200 uniquement
            if response.status_code == 200:
                print(f" ✅ (Status: {response.status_code})")
                return True
            else:
                # Si c'est 404, 503, 500, etc... on attend
                print(f" ⏳ ({response.status_code})", end="", flush=True)
        except requests.exceptions.ConnectionError:
            print(f".", end="", flush=True)
        except Exception as e:
            print(f"!", end="", flush=True)
        
        time.sleep(DELAY)
    
    print(f" ❌ ECHEC après {MAX_RETRIES} tentatives.")
    return False

def main():
    print(f"🚑 Démarrage des Smoke Tests sur {TARGET_ENV.upper()}...")
    
    if not os.path.exists(CLIENTS_FILE):
        print(f"Erreur: {CLIENTS_FILE} introuvable.")
        sys.exit(1)

    config = load_yaml(CLIENTS_FILE)
    errors = 0
    tests_run = 0
    
    for client in config['clients']:
        client_name = client['name']
        
        # FILTRE : On ne teste que l'environnement en cours
        if TARGET_ENV not in client['environments']:
            continue

        print(f"\n--- Client: {client_name} [{TARGET_ENV}] ---")
        namespace = f"{client_name}-{TARGET_ENV}"
            
        for app in client['apps']:
            # 1. Test de l'URL principale
            url = f"{app}-{client_name}.{DOMAIN_SUFFIX}"
            if not check_url(url):
                errors += 1
            tests_run += 1

            # 2. Test de l'URL FileBrowser
            fb_url = f"files-{app}-{client_name}.{DOMAIN_SUFFIX}"
            if not check_url(fb_url):
                errors += 1
            tests_run += 1

    print("-" * 30)
    if tests_run == 0:
        print("⚠️ Aucun test n'a été exécuté (vérifiez clients.yaml ou la branche).")
    elif errors > 0:
        print(f"🔥 {errors} tests ont échoué ! La pipeline est marquée comme FAILED.")
        sys.exit(1)
    else:
        print("\n✨ Tous les systèmes répondent 200 OK !")
        sys.exit(0)

if __name__ == "__main__":
    main()