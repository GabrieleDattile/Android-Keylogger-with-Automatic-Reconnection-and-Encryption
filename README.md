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
    git clone https://github.com/tuo-username/Android-Keylogger.git
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

