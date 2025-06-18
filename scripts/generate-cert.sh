#!/bin/bash

CERT_DIR="./ssl"
DOMAIN="localhost"

mkdir -p $CERT_DIR

echo "🔐 Génération du certificat auto-signé pour https://$DOMAIN..."

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout $CERT_DIR/self-signed.key \
  -out $CERT_DIR/self-signed.crt \
  -subj "/C=FR/ST=Local/L=DevCity/O=PMI/CN=$DOMAIN"

echo "Certificat généré dans $CERT_DIR/"
