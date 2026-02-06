import yaml
import os
import requests
import time
import sys

# CONFIGURATION
CLIENTS_FILE = "configs/clients.yaml"
VPS_IP = os.getenv("VPS_IP", "152.228.130.213") # Ton IP
MAX_RETRIES = 10  # On essaie 10 fois
DELAY = 10        # On attend 10s entre chaque essai (Total ~1min30 de patience)

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def check_url(url):
    print(f"   🔎 Test de {url}...", end="", flush=True)
    for i in range(MAX_RETRIES):
        try:
            # On met un timeout de 5s pour ne pas bloquer indéfiniment
            response = requests.get(f"http://{url}", timeout=5)
            
            # Si le code est inférieur à 500 (200 OK, 301 Redirect, 401 Auth...), c'est que le serveur répond.
            # Si c'est 502/503/504, c'est que le pod ou l'ingress est KO.
            if response.status_code < 500:
                print(f" ✅ (Status: {response.status_code})")
                return True
            else:
                print(f".", end="", flush=True) # Petit point pour dire "j'attends"
        except requests.exceptions.ConnectionError:
            print(f".", end="", flush=True)
        except Exception as e:
            print(f"!")
        
        # On attend avant de réessayer
        time.sleep(DELAY)
    
    print(f" ❌ ECHEC après {MAX_RETRIES} tentatives.")
    return False

def main():
    print("🚑 Démarrage des Smoke Tests...")
    
    if not os.path.exists(CLIENTS_FILE):
        print(f"Erreur: {CLIENTS_FILE} introuvable.")
        sys.exit(1)

    config = load_yaml(CLIENTS_FILE)
    errors = 0
    
    for client in config['clients']:
        client_name = client['name']
        for env in client['environments']:
            print(f"\n--- Client: {client_name} [{env}] ---")
            
            for app in client['apps']:
                # 1. Test de l'URL principale
                url = f"{app}-{client_name}-{env}.{VPS_IP}.nip.io"
                if not check_url(url):
                    errors += 1

                # 2. Test de l'URL FileBrowser (Bonus)
                fb_url = f"files-{app}-{client_name}-{env}.{VPS_IP}.nip.io"
                if not check_url(fb_url):
                    errors += 1

    if errors > 0:
        print(f"\n🔥 {errors} tests ont échoué ! La pipeline est marquée comme FAILED.")
        sys.exit(1) # Ça fait échouer la pipeline GitHub
    else:
        print("\n✨ Tous les systèmes sont opérationnels !")
        sys.exit(0)

if __name__ == "__main__":
    main()