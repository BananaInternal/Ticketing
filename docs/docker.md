# Docker

## Inizio esecuzione

Per far partire i servizi di GitLab, è necessario utilizzare Docker Compose
nella cartella dove si trova il file `docker-compose.yml` che definisce
i container di GitLab (`ticketingsystem_gitlab`) e del ChatBox (`ticketingsystem_chatbox`):

```bash
docker-compose up
```

Oppure

```bash
docker-compose up -d
```

Per farlo eseguire in detached mode.

## Termine esecuzione

Per fermare i servizi di GitLab e del ChatBox, utilizzare il seguente comando
dalla cartella dove si trova il file `docker-compose.yml` che definisce
i container di GitLab (`ticketingsystem_gitlab`) e del ChatBox (`ticketingsystem_chatbox`):

```bash
docker-compose stop
```

## Riavvio esecuzione

Per riavviare i servizi di GitLab e del ChatBox, utilizzare il seguente comando
dalla cartella dove si trova il file `docker-compose.yml` che definisce
i container di GitLab (`ticketingsystem_gitlab`) e del ChatBox (`ticketingsystem_chatbox`):

```bash
docker-compose restart
```
