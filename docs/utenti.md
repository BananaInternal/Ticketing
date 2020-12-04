# Utenti

La gestione degli utenti va eseguita con l'account `root` / amministratore di GitLab.

Il pannello di controllo degli utenti è accessibile al percorso
[/admin/users](https://support.banana.ch/admin/users).

## Creazione di un nuovo utente

Per creare un nuovo utente, visitare la pagina
[/admin/users/new](https://support.banana.ch/admin/users/new) con un account amministratore.

Inserite le informazioni nei campi (è obbligatorio fornire almeno un username e indirizzo email).

Il supporto al log-in tramite Active Directory sarà fattibile in maniera automatica se
in Active Directory esiste un account con la stessa email ed è stato eseguito almeno un accesso
tramite password normale.

## Gestione infromazioni ed eliminazione di un utente

Per gestire le informazioni relative ad un utente, login associati (ad esempio Active Directory)
o eliminare un utente, è necessario visitare la pagina [/admin/users](https://support.banana.ch/admin/users).

Da quella pagina è necessario selezionare l'utente e poi "Edit". Per eliminare l'utente è necessario
premere il tasto "Delete" in rosso in basso. Per confermare l'eliminazione dell'utente è necessario
digitare il nome come richiesto.

## Gestione permessi

In maniera predefinita, gli account appena creati non hanno accesso ai progetti di ticketing,
è necessario dunque aggiungerli manualmente.

È possibile garantire l'accesso ad un gruppo (che contiene più progetti) oppure ad un progetto
specifico.

### Gestione permessi per gruppo

Per gestire i permessi dei membri di un gruppo (o aggiungere nuovi membri), è necessario visitare
la pagina [/groups/NOME_GRUPPO/-/group_members](https://support.banana.ch/groups/ticketing/-/group_members).

Da questa schermata sarà possibile aggiungere uno o più nuovi utenti compilando l'apposito form, oppure
gestire gli utenti attuali.

### Gestione permessi per progetto

Per gestire i permessi dei membri di un gruppo (o aggiungere nuovi membri), è necessario visitare
la pagina [/NOME_GRUPPO/NOME_PROGETTO/-/project_members](https://support.banana.ch/ticketing/en_support/-/project_members).

Da questa schermata sarà possibile aggiungere uno o più nuovi utenti compilando l'apposito form, oppure
gestire gli utenti attuali.

### Gestione livelli di permessi

Gli utenti sono organizzati in vari livelli, come descritto nella
[documentazione ufficiale](https://docs.gitlab.com/ce/user/permissions.html).

Generalmente, viene assegnato il livello "_Developer_" agli utenti di "_livello 2_" e
"_Reporter_" agli utenti di "_livello 1_".

È possibile anche fornire accesso temporaneo ad un progetto / gruppo selezionando la
data di revoca del permesso al momento della creazione o revocando manualmente un permesso
dall'interfaccia di amministrazione.

## Ulteriori informazioni

Per ulteriori informazioni, consultare la
[documentazione ufficiale](https://docs.gitlab.com/ce/raketasks/user_management.html).
