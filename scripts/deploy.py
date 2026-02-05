import yaml
import os
import subprocess
import sys
import secrets
import string

# --- CONFIGURATION ---
CLIENTS_FILE = "configs/clients.yaml"
TEMPLATE_DIR = "k8s-templates"
VPS_IP = os.getenv("VPS_IP", "152.228.130.213") 

def load_yaml(filepath):
    if not os.path.exists(filepath):
        print(f"Erreur: {filepath} introuvable.")
        sys.exit(1)
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def generate_password(length=16):
    """Génère un mot de passe fort aléatoire"""
    alphabet = string.ascii_letters + string.digits # On évite les caractères spéciaux qui cassent parfois les URLs
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_secret_if_not_exists(namespace, secret_name, data_dict):
    """
    Crée un secret Kubernetes seulement s'il n'existe pas déjà.
    Garantit la persistance du mot de passe en cas de redéploiement.
    """
    # 1. Vérifier si le secret existe
    check = subprocess.run(
        ["kubectl", "get", "secret", secret_name, "-n", namespace],
        capture_output=True
    )
    
    if check.returncode == 0:
        print(f"   🔒 Secret '{secret_name}' existe déjà. On le conserve.")
        return

    # 2. Construire la commande de création
    # data_dict est sous la forme {'cle': 'valeur'}
    cmd = ["kubectl", "create", "secret", "generic", secret_name, "-n", namespace]
    for key, value in data_dict.items():
        cmd.append(f"--from-literal={key}={value}")
    
    # 3. Exécuter
    print(f"   ✨ Création du secret '{secret_name}'...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

def apply_k8s_manifest(manifest_content):
    process = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=manifest_content.encode('utf-8'),
        capture_output=True
    )
    if process.returncode != 0:
        print(f"   [ERREUR] {process.stderr.decode('utf-8')}")
    else:
        print("   [OK] Appliqué.")

def create_namespace(namespace):
    cmd = f"kubectl create ns {namespace} --dry-run=client -o yaml | kubectl apply -f -"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)

def main():
    print(f"🚀 Déploiement V2 (Secure) sur {VPS_IP}...")
    
    config = load_yaml(CLIENTS_FILE)
    
    for client in config['clients']:
        client_name = client['name']
        
        for env in client['environments']:
            namespace = f"{client_name}-{env}"
            print(f"\n--- Client: {client_name} | Env: {env} ---")
            
            create_namespace(namespace)
            
            for app in client['apps']:
                url = f"{app}-{client_name}-{env}.{VPS_IP}.nip.io"
                print(f" > Traitement de {app} (URL: {url})")
                print(f" > Traitement de {app}")

                # --- GESTION DES SECRETS (LA V2 EST ICI) ---
                
                # 1. Secret pour la Base de Données (Commun à WP et Presta)
                # On génère des passwords, mais ils ne seront utilisés que si le secret n'existe pas
                db_secret_name = f"{app}-db-secret"
                create_secret_if_not_exists(namespace, db_secret_name, {
                    "root-password": generate_password(),
                    "db-password": generate_password()
                })

                # 2. Secret pour l'Admin (Spécifique PrestaShop)
                if app == "prestashop":
                    admin_secret_name = f"{app}-admin-secret"
                    create_secret_if_not_exists(namespace, admin_secret_name, {
                        "admin-password": generate_password() # Ou mettre un fix si tu préfères : "Admin123!"
                    })

                # --- DEPLOIEMENT DES YAML ---

                # A. La Base de Données
                with open(f"{TEMPLATE_DIR}/mariadb.yaml", 'r') as f:
                    db_tpl = f.read()
                apply_k8s_manifest(
                    db_tpl.replace('${NAMESPACE}', namespace)
                          .replace('${APP_NAME}', app) 
                )
                
                # B. L'Application
                app_file = f"{TEMPLATE_DIR}/{app}.yaml"
                if os.path.exists(app_file):
                    with open(app_file, 'r') as f:
                        app_tpl = f.read()
                    
                    # On injecte juste l'URL et les Noms, plus de password en clair ici !
                    apply_k8s_manifest(
                        app_tpl.replace('${NAMESPACE}', namespace)
                               .replace('${APP_NAME}', app)
                               .replace('${URL}', url)
                    )
                else:
                    print(f"   [!] Template {app}.yaml introuvable.")

                # C. L'Ingress
                with open(f"{TEMPLATE_DIR}/ingress.yaml", 'r') as f:
                    ing_tpl = f.read()
                apply_k8s_manifest(
                    ing_tpl.replace('${NAMESPACE}', namespace)
                           .replace('${APP_NAME}', app)
                           .replace('${URL}', url)
                )

                # D. Le Gestionnaire de Fichiers (FileBrowser)
                # On génère une URL spécifique : files-app-client-env...
                fb_url = f"files-{app}-{client_name}-{env}.{VPS_IP}.nip.io"
                print(f" > Ajout FileBrowser (URL: {fb_url})")

                fb_file = f"{TEMPLATE_DIR}/filebrowser.yaml"
                if os.path.exists(fb_file):
                    with open(fb_file, 'r') as f:
                        fb_tpl = f.read()
                    
                    apply_k8s_manifest(
                        fb_tpl.replace('${NAMESPACE}', namespace)
                              .replace('${APP_NAME}', app)
                              .replace('${FILEBROWSER_URL}', fb_url)
                    )
                else:
                    print(f"   [!] Template filebrowser.yaml introuvable.")
                    
    print("\n✅ Déploiement sécurisé terminé.")

if __name__ == "__main__":
    main()