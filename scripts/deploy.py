import yaml
import os
import subprocess
import sys

# --- CONFIGURATION ---
CLIENTS_FILE = "configs/clients.yaml"
TEMPLATE_DIR = "k8s-templates"

# Récupération de la branche (fournie par GitHub Actions)
CURRENT_BRANCH = os.getenv("GITHUB_REF_NAME", "unknown")

print(f"🚀 Démarrage du déploiement depuis la branche : {CURRENT_BRANCH}")

# --- LOGIQUE DE SELECTION DU CLUSTER ET DU DOMAINE ---
if CURRENT_BRANCH == "main":
    print("💎 MODE PRODUCTION DETECTÉ (Cible: Gravelines)")
    TARGET_ENV = "prod"
    KUBE_SECRET = os.getenv("KUBECONFIG_PROD")
    VPS_IP = os.getenv("VPS_IP_PROD")
    DOMAIN_SUFFIX = "pmi.ovh"       # Domaine Propre
else:
    print("🛠 MODE DEVELOPPEMENT DETECTÉ (Cible: Strasbourg)")
    TARGET_ENV = "dev"
    KUBE_SECRET = os.getenv("KUBECONFIG_DEV")
    VPS_IP = os.getenv("VPS_IP_DEV")
    DOMAIN_SUFFIX = "dev.pmi.ovh"   # Sous-domaine de dev

# Sécurité : Vérification des secrets
if not KUBE_SECRET:
    print(f"❌ Erreur: Le secret KUBECONFIG_{TARGET_ENV.upper()} est vide ou introuvable.")
    sys.exit(1)
if not VPS_IP:
    print(f"❌ Erreur: L'IP du VPS ({TARGET_ENV.upper()}) est introuvable.")
    sys.exit(1)

# Configuration de kubectl
KUBECONFIG_PATH = f"{os.environ['HOME']}/.kube/config"
os.makedirs(os.path.dirname(KUBECONFIG_PATH), exist_ok=True)
with open(KUBECONFIG_PATH, "w") as f:
    f.write(KUBE_SECRET)
os.environ["KUBECONFIG"] = KUBECONFIG_PATH

print(f"✅ Cluster {TARGET_ENV.upper()} configuré (IP: {VPS_IP} | Domaine: *.{DOMAIN_SUFFIX})")

def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def apply_k8s_template(template_name, context):
    with open(f"{TEMPLATE_DIR}/{template_name}", 'r') as f:
        content = f.read()
    
    # Remplacement des variables
    for key, value in context.items():
        content = content.replace(f"${{{key}}}", str(value))
    
    # Application via kubectl
    process = subprocess.Popen(['kubectl', 'apply', '-f', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=content)
    
    if process.returncode != 0:
        print(f"❌ Erreur sur {template_name}: {stderr}")
        sys.exit(1)
    else:
        print(f"   [OK] {template_name} appliqué.")

def create_namespace_if_not_exists(namespace):
    subprocess.run(f"kubectl create namespace {namespace} --dry-run=client -o yaml | kubectl apply -f -", shell=True, check=True, stdout=subprocess.DEVNULL)

def deploy_system_apps(context):
    print(f"\n--- Déploiement Infrastructure (Monitoring) ---")
    apply_k8s_template("middleware.yaml", context)
    print(f" > Configuration Ingress Grafana (URL: monit.{context['DOMAIN_SUFFIX']})")
    # On force l'application du template
    apply_k8s_template("monitoring.yaml", context)

def main():
    config = load_yaml(CLIENTS_FILE)
    
    system_context = {
        "DOMAIN_SUFFIX": DOMAIN_SUFFIX,
        "VPS_IP": VPS_IP,
        # On ajoute ces variables même si monitoring.yaml n'en a pas besoin, pour éviter les erreurs
        "APP_NAME": "grafana",
        "NAMESPACE": "monitoring" 
    }
    deploy_system_apps(system_context)
    
    for client in config['clients']:
        client_name = client['name']
        
        # Filtre par environnement (Dev ou Prod)
        if TARGET_ENV not in client['environments']:
            continue

        print(f"\n--- Client: {client_name} | Env: {TARGET_ENV} ---")
        namespace = f"{client_name}-{TARGET_ENV}"
        create_namespace_if_not_exists(namespace)
        
        # Contexte global pour les templates
        context = {
            "APP_NAME": "", 
            "CLIENT_NAME": client_name,
            "ENV": TARGET_ENV,
            "NAMESPACE": namespace,
            "VPS_IP": VPS_IP,
            "DOMAIN_SUFFIX": DOMAIN_SUFFIX
        }

        # Création du secret DB
        db_secret_cmd = f"kubectl create secret generic {client_name}-db-secret --from-literal=password=rootroot --dry-run=client -o yaml | kubectl apply -n {namespace} -f -"
        subprocess.run(db_secret_cmd, shell=True, stdout=subprocess.DEVNULL)

        # Force le redirect https
        print(f" > Configuration Middleware HTTPS pour {namespace}")
        apply_k8s_template("middleware.yaml", context)

        for app in client['apps']:
            context["APP_NAME"] = app
            
            url_slug = f"{app}-{client_name}"
            context["URL_SLUG"] = url_slug
            full_url = f"{url_slug}.{DOMAIN_SUFFIX}"
            print(f" > Traitement de {app} (URL: {full_url})")
            
            apply_k8s_template(f"{app}.yaml", context)
            apply_k8s_template("mariadb.yaml", context)
            
            print(f" > Ajout FileBrowser")
            apply_k8s_template("filebrowser.yaml", context)

    print(f"\n✅ Déploiement {TARGET_ENV.upper()} terminé avec succès.")

if __name__ == "__main__":
    main()