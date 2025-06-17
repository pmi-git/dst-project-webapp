# Base officielle NGINX allégée
FROM nginx:stable-alpine

# Mainteneur
LABEL maintainer="Patrick Miviere <patrick.miviere@gmail.com>"

# Copie de la configuration custom
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Port exposé (80 par défaut)
EXPOSE 80

# Santé du conteneur
#HEALTHCHECK --interval=30s --timeout=5s \
#  CMD wget -q --spider http://localhost || exit 1
