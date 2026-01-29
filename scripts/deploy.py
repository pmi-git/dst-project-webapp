import yaml
import os
import subprocess
import sys

# --- CONFIGURATION ---
CLIENTS_FILE = "configs/clients.yaml"
TEMPLATE_DIR = "k8s-templates"

# On essaie de récupérer l'IP depuis les variables d'env, sinon on met une valeur par défaut
# Pour que ça marche sur GitHub, il faudra peut-être ajouter une variable d'env VPS_IP dans le workflow

VPS_IP = os.getenv("VPS_IP", "152.228.130.213") 

def load_yaml(filepath):
    if not os.path.exists(filepath):
        print(f"Erreur: {filepath} introuvable.")
        sys.exit(1)
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

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
    print(f"🚀 Déploiement Multi-Apps sur {VPS_IP}...")
    
    try:
        config = load_yaml(CLIENTS_FILE)
    except Exception as e:
        print(f"Erreur lecture YAML: {e}")
        sys.exit(1)
    
    for client in config['clients']:
        client_name = client['name']
        
        for env in client['environments']:
            namespace = f"{client_name}-{env}"
            print(f"\n--- Client: {client_name} | Env: {env} ---")
            
            # 1. Création du Namespace
            create_namespace(namespace)
            
            # 2. Boucle sur les Apps (Wordpress / Prestashop)
            for app in client['apps']:
                # Génération de l'URL : ex: prestashop-garage-moto-dev.152.X.X.X.nip.io
                url = f"{app}-{client_name}-{env}.{VPS_IP}.nip.io"
                print(f" > Traitement de {app} (URL: {url})")
                
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
                    apply_k8s_manifest(
                        app_tpl.replace('${NAMESPACE}', namespace)
                               .replace('${APP_NAME}', app)
                    )
                else:
                    print(f"   [!] Attention: Template {app}.yaml introuvable.")

                # C. L'Ingress
                with open(f"{TEMPLATE_DIR}/ingress.yaml", 'r') as f:
                    ing_tpl = f.read()
                apply_k8s_manifest(
                    ing_tpl.replace('${NAMESPACE}', namespace)
                           .replace('${APP_NAME}', app)
                           .replace('${URL}', url)
                )

    print("\n✅ Déploiement terminé.")

if __name__ == "__main__":
    main()