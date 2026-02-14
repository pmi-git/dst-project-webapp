# Syntaxe : kubectl get secret -n <NAMESPACE> <NOM_SECRET> -o jsonpath="{.data.<CLE>}" | base64 -d

# Exemple concret pour le garage en dev :
kubectl get secret -n garage-moto-dev prestashop-admin-secret -o jsonpath="{.data.admin-password}" | base64 -d ; echo

# Exemple la db presta
kubectl get secret -n garage-moto-dev prestashop-db-secret -o jsonpath="{.data.db-password}" | base64 -d ; echo

#db wordpress boulangerie (apres modif password)
kdev get secret -n boulangerie-dev boulangerie-db-secret -o jsonpath="{.data.password}" | base64 -d ; echo 

# ------> script à faire !