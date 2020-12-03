# Backup

Il sistema come definito nel file `docker-compose.yml` effetua in maniera automatica
dei backup dal Martedí al Sabato alle ore 21:00 (orario locale del server).
I backup vengono caricati nella cartella `/var/opt/gitlab/backups/`, accessibile dal container
`ticketingsystem-backup`.

I dati dell'istanza GitLab sono salvati nei seguenti container, pertanto la loro eliminazione
comporta ad una perdita di dati e configurazione dell'istanza GitLab:

- `ticketingsystem-config`: File di configurazione di GitLab
- `ticketingsystem-logs`: File di log di GitLab
- `ticketingsystem-data`: File di dati dei progetti di GitLab

## Creazione di un backup (manualmente)

In questa repository viene fornito uno script in grado di collegarsi al
container docker (secondo la documentazione del file `docker-compose.yml`) e effetuare e scaricare
in locale un backup dell'instanza gitlab.

Lo script si trova nella cartella `backup` di questa repo, e ha nome `banana_backup.sh`.

È stato testato su MacOS e Ubuntu Linux. Necessita delle seguenti dipendenze:

- `docker`
- `sha512sum` (linux) / `shasum` (MacOS)
- `zip`

## Ripristino di un backup

Per ripristinare un backup di GitLab, copiare il file di backup nel container ed estrarlo.

Il file `$DATE_XX.Y.Z-ce_gitlab_backup.tar` contenuto nell'archivio di backup deve essere copiato
nella cartella `/var/opt/gitlab/backups/` e impostato come proprietà dell'utente (e gruppo) `git`.

Esempio:

```bash
sudo cp 11493107454_2018_04_25_10.6.4-ce_gitlab_backup.tar /var/opt/gitlab/backups/
sudo chown git.git /var/opt/gitlab/backups/11493107454_2018_04_25_10.6.4-ce_gitlab_backup.tar
```

Dopodiché eseguire i seguenti comandi, come riportato nella
[documentazione ufficiale](https://docs.gitlab.com/ce/raketasks/backup_restore.html#restore-for-omnibus-gitlab-installations):

```bash
# Fermare i servizi di GitLab
sudo gitlab-ctl stop unicorn
sudo gitlab-ctl stop puma
sudo gitlab-ctl stop sidekiq

# Verificare lo stato di GitLab
sudo gitlab-ctl status

# Ripristinare il backup
# NOTA: inserisci il nome del backup da ripristinare corretto, di seguito è riportato un esempio
sudo gitlab-backup restore BACKUP=11493107454_2018_04_25_10.6.4-ce
```

Ora, copiare i file `gitlab-secrets.json` e `gitlab.rb` in `/etc/gitlab/gitlab-secrets.json` e
`/etc/gitlab/gitlab.rb` rispettivamente. Questi file sono essenziali in quanto contengono configurazioni
per accedere ai dati presenti nel backup.

Esempio:

```bash
sudo cp gitlab-secrets.json /etc/gitlab/gitlab-secrets.json
sudo cp gitlab.rb /etc/gitlab/gitlab.rb
```

Infine, fate partire i servizi di GitLab nuovamente con i seguenti comandi:

```bash 
sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart
sudo gitlab-rake gitlab:check SANITIZE=true
```

## Ulteriori informazioni

Ulteriori informazioni sono disponibili nella
[documentazione ufficiale](https://docs.gitlab.com/ce/raketasks/backup_restore.html) di GitLab.

**Importante**: se la versione di GitLab in uso non corrisponde con la versione di GitLab con
la quale è stato creato il backup, non sarà possibile effetuare il ripristino di tale backup.
