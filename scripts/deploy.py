import yaml
import os
import subprocess
import sys

# Chemins des fichiers
CLIENTS_FILE = "configs/clients.yaml"
TEMPLATE_DIR = "k8s-templates"

def load_yaml(filepath):
    """Charge le fichier de configuration des clients"""
    if not os.path.exists(filepath):
        print(f"Erreur: Le fichier {filepath} n'existe pas.")
        sys.exit(1)
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def apply_k8s_manifest(manifest_content):
    """Envoie le contenu YAML directement à kubectl via stdin"""
    # L'équivalent de : echo "contenu" | kubectl apply -f -
    process = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=manifest_content.encode('utf-8'),
        capture_output=True
    )
    
    if process.returncode == 0:
        print("   [OK] Ressource appliquée.")
    else:
        print(f"   [ERREUR] {process.stderr.decode('utf-8')}")

def create_namespace_if_not_exists(namespace):
    """Crée le namespace s'il n'existe pas"""
    # cheats : --dry-run=client -o yaml | kubectl apply -f -
    # rend la commande idempotente
    cmd = f"kubectl create ns {namespace} --dry-run=client -o yaml | kubectl apply -f -"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    print(f" -> Namespace '{namespace}' vérifié/créé.")

def main():
    print("🚀 Démarrage du déploiement automatisé...")
    
    config = load_yaml(CLIENTS_FILE)
    
    for client in config['clients']:
        name = client['name']
        env = client['environment']
        app_type = client['app']
        url = client['url']
        
        # 1. Définition du Namespace (ex: boulangerie-dev)
        namespace = f"{name}-{env}"
        
        print(f"\nTraitement du client : {name} ({env})")
        print(f"App: {app_type} | URL: {url}")
        
        # 2. Création du Namespace
        create_namespace_if_not_exists(namespace)
        
        # 3. Liste des templates à déployer
        # On commence par la DB, puis l'App, puis l'Ingress
        templates_to_deploy = ["mariadb.yaml", "wordpress.yaml", "ingress.yaml"]
        
        for template_file in templates_to_deploy:
            template_path = os.path.join(TEMPLATE_DIR, template_file)
            
            with open(template_path, 'r') as f:
                content = f.read()
            
            # 4. TEMPLATISATION (Remplacement des variables)
            # C'est ici que la magie opère
            content = content.replace('${NAMESPACE}', namespace)
            content = content.replace('${APP_HOST}', url)
            
            # Si on avait d'autres variables (DB User, etc), on les ferait ici
            
            # 5. Application
            print(f"   Déploiement de {template_file}...")
            apply_k8s_manifest(content)

    print("\n✅ Déploiement terminé pour tous les clients !")

if __name__ == "__main__":
    main()