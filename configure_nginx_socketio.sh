#!/bin/bash

# Richiedi informazioni all'utente
read -p "Inserisci il tuo dominio (es: tuodominio.com): " DOMAIN
read -p "Inserisci l'IP statico del server Socket.IO: " SOCKETIO_SERVER_IP
read -p "Inserisci la porta del server Socket.IO: " SOCKETIO_SERVER_PORT
read -p "Inserisci il percorso del certificato SSL (es: /etc/nginx/ssl/tuodominio.com.crt): " SSL_CERT_PATH
read -p "Inserisci il percorso della chiave SSL (es: /etc/nginx/ssl/tuodominio.com.key): " SSL_KEY_PATH

# Funzione per creare il file di configurazione Nginx
create_nginx_config() {
    cat <<EOL > /etc/nginx/sites-available/socketio_nginx_config
upstream socketio_servers {
    server $SOCKETIO_SERVER_IP:$SOCKETIO_SERVER_PORT;
    keepalive 64;
}

server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    # Configurazione del certificato SSL
    ssl_certificate $SSL_CERT_PATH;
    ssl_certificate_key $SSL_KEY_PATH;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';

    # Headers di sicurezza
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location /socket.io {
        proxy_pass http://socketio_servers/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Rate limiting
        limit_req zone=one burst=5 nodelay;
    }

    # Definire la zona di limitazione delle richieste
    limit_req_zone \$binary_remote_addr zone=one:10m rate=1r/s;

    # Firewall IP basato su elenco
    allow 192.168.1.0/24;
    deny all;
}

# Firewall di base
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # ...
    # Altre configurazioni

    server_tokens off;
}
EOL
}

# Funzione per abilitare la configurazione Nginx (solo per Debian/Ubuntu)
enable_nginx_config() {
    ln -s /etc/nginx/sites-available/socketio_nginx_config /etc/nginx/sites-enabled/
}

# Funzione per testare la configurazione Nginx
test_nginx_config() {
    nginx -t
}

# Funzione per ricaricare Nginx
reload_nginx() {
    systemctl reload nginx
}

# Esegui i passaggi
create_nginx_config
enable_nginx_config
if test_nginx_config; then
    reload_nginx
    echo "La configurazione Nginx è stata applicata con successo."
else
    echo "Errore nella configurazione di Nginx. Controlla il file di configurazione."
fi
