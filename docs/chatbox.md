# ChatBox

Il ChatBox riconosce in maniera autonoma le lingue dei messaggi, ed è in grado di
rispondere se trova una corrispondenza tra il messaggio analizzato e delle frasi che
gli vengono fornite manualmente e categorizzate in "label".

## Token GitLab (installazione)

Per configurare il token di GitLab per l'account del ChatBox, è necessario creare
un nuovo utente su GitLab e ottenere un token di accesso con il seguente procedimento:

1. Accedere con l'utente del ChatBox (tramite "_Impersonate_" o log-in regolare).
2. Visitare la pagina [`/profile/personal_access_tokens`](https://support.banana.ch/profile/personal_access_tokens)
3. Creare un nuovo token con le seguenti impostazioni :
    - api: on
    - read_user: off
    - read_api: off
    - read_repository: off
    - write_repository: off
    - sudo: off
4. Copiare il token nel file `chatbox/variables.env` e assegnarlo alla variabile `CHATBOX_GITLAB_TOKEN`

## Aggiunta nuove frasi riconosciute

Per riconoscere frasi, il ChatBox utilizza i file presenti nella cartella `chatbox/nlp/data/`:
i file con nome `CODICE_LINGUA.txt` sono compilati nel seguente formato:

```
__label__NOME  Frase di esempio
```

Il prefisso `__label__` indica che la stringa di caratteri che lo seguono fino al primo
carattere di spazio incontrato costituisce il nome del label (esempio: `__label__pizza` ->
label=`pizza`).

La frase che segue il nome del label fino alla fine della riga viene utilizzata per apprendere
come riconoscere un label.

Le frasi che vengono inserite vanno scritte in maniera attenta per evitare che il ChatBox non
riconosca falsi positivi, pertanto, dato il numero limitato di frasi a disposizione è stata
adottata una tecnica che consiste nell'insegnare al ChatBox delle parole chiave specifiche per
ogni label.

Ad esempio, per insegnare a riconoscere il concetto / frase
"_How can I quit my paid plan of Banana 9?_" per il label "_quit_", sono
state scritte alcune varianti della frase in forma sintetica, come ad esempio:

```
__label__quit quit paid plan?
__label__quit quit paid plan that subscribed?
__label__quit close plan paid?
__label__quit stop paying plan chosen?
```

È importante rimuovere tutte le "stopwords" e utilizzare "stem" dei nomi e verbi.

### Risposte

**Attenzione: le risposte sono state disattivate. Per ripristinarle, consultare
la git history**.

Dopo aver fornito le frasi d'esempio nei vari file di lingue in `chatbox/nlp/data/`,
è necessario aggiungere una risposta nei file json presenti in `chatbox/gitlab/data/`,
che definiscono le risposte automatiche del ChatBox nella piattaforma GitLab.
Aggiungere una nuova _key_ con il nome del label (senza il prefisso `__label__`,
esempio: `__label__quit` -> `quit`), e come _value_ la frase di risposta.
Tenere in considerazione che la risposta sarà sempre aperta con la frase definita
in `__begin` e terminerà con la frase definita in `__end`.

Dopo ogni modifica a questa configurazione, è necessario ricompilare.

## Aggiunta lingue nuove

Per aggiungere una nuova lingua riconosciuta, aggiungere un file `.txt` con nome il
codice ISO della lingua (esempio: inglese -> `en`, italiano -> `it`) nella cartella
`chatbox/nlp/data/`. Inserire all'interno di questo file le frasi di esempio mantenendo
i nomi dei label definiti nelle altre lingue (eventualmente utilizzare `en.txt` o
`de.txt` come riferimento). Questo file consentirà al ChatBox di riconoscere l'argomento
di cui parla un messaggio ed assegnare correttamente i label ai vari ticket.
I label assegnati ai ticket su gitlab sono i label che vengono definiti nel file txt
(esempio: `__label_quit` -> `quit`).

Dopodichè, aggiungere un file `.json` con lo stesso nome del file txt creato nella
cartella `chatbox/gitlab/data/` e compilarlo con le frasi delle risposte.
Se le frasi non vengono compilate, il ChatBox non risponderà alle domande su GitLab.
Utilizzare `chatbox/gitlab/data/en.json` come base.
Tenere in considerazione che la risposta sarà sempre aperta con la frase definita
in `__begin` e terminerà con la frase definita in `__end`.

Dopo ogni modifica a questa configurazione, è necessario ricompilare.

## _Redirect_ di ticket con assegnazione label d'origine

Per far in modo che alle mail inviate ad un particolare indirizzo venga associato un
determinato label è necessario creare un nuovo progetto in GitLab nel gruppo
[`inbox`](https://support.banana.ch/inbox).

Dopo aver creato un nuovo progetto, aggiungere l'utente ChatBox al progetto con permessi
`Developer` o superiori. Copiare l'id del progetto (accessibile dalle impostazioni dello
stesso), e modificare il seguente file: `chatbox/gitlab/data/inbox_map.json`.

Questo file presenta la seguente struttura:

```json
{
    "id": "label",
    "43": "africa",
    ...
}
```

La key rappresenta l'id del progetto, mentre la value è il label che verrà associato a tutti i
ticket che verranno inviati all'indirizzo mail del progetto designato dall'id della key.

I ticket di questi progetti verranno periodicamente spostati nel progetto corrispondente all'id
contenuto nella variabile d'ambiente `CHATBOX_GITLAB_MAIN_PROJECT`. Esempio:

```
CHATBOX_GITLAB_MAIN_PROJECT=41
```

Dopo ogni modifica a questa configurazione, è necessario ricompilare.

## Compilazione

Il file `docker-compose.yml` per il progetto di GitLab e il ChatBox si trova nel
seguente percorso del server: `/home/ticketingsystem/conf/dockerfile/docker-compose.yml`.

Per compilare i cambiamenti fatti al ChatBox, utilizzare il seguente comando
dalla cartella dove si trova il file `docker-compose.yml`:

```bash
cd /home/ticketingsystem/conf/dockerfile
docker-compose build
```

## Aggiunta a nuovi progetti

Per aggiungere il ChatBox ad un nuovo progetto è necessario andare nelle impostazioni
del progetto (accessibili tramite la pagina
[/NOME_GRUPPO/NOME_PROGETTO/edit](https://support.banana.ch/ticketing/en_support/edit)),
e copiare l'id del progetto (visualizzato nella parte alta vicino al nome; non modificabile).
Sempre dalle impostazioni, aggiungere un nuovo membro e selezionare l'account del ChatBox
(dovrebbe essere `@chatbox` con permessi "Reporter" o superiori).

Inserire questo id nel file `chatbox/variables.env` aggiungendolo alla stringa della variabile
`CHATBOX_GITLAB_PROJECTS`. Ad esempio, se vogliamo aggiungere il progetto 84:
`CHATBOX_GITLAB_PROJECTS="2,3,4,5,6,41"` -> `CHATBOX_GITLAB_PROJECTS="2,3,4,5,6,41,84"`.


## Cronjob

Lo script python viene eseguito ogni secondo minuto di ogni ora dalle 5:00 alle 21:00
ogni giorno della settimana tra il lunedí e il venerdí (compresi).

Per modificare i valori del cronjob, modificate il file `chatbox/crontab.txt` con la
configurazione di vostro gradimento. [Questo sito](https://crontab.guru/#*/2_5-21_*_*_1-5)
può aiutare nel formulare correttamente la sintassi per la configurazione desiderata.
