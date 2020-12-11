# Configurazione sul server mail

## Mail forwarding con script sieve

Accedere alla webmail di Infomaniak, andare nei settings della mail.

Nel menu di sinistra cliccare su Filters.

Aggiungere uno script.

```sieve
require ["editheader", "copy"];

# modifica indirizzo To in modo da rispecchiare il progetto
if address :is "To" "support_it@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto italiano>@banana.ch";
} else if address :is "To" "support_de@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto tedesco>@banana.ch";
} else if address :is "To" "support_fr@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto francese>@banana.ch";
} else if address :is "To" "support_en@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto inglese>@banana.ch";
} else if address :is "To" "africa@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto africa>@banana.ch";
} else if address :is "To" "cns@banana.ch"{
    deleteheader "To";
    addheader "To" "ticketing+<progetto cinese>@banana.ch";
} else {
    deleteheader "To";
    addheader "To" "ticketing+ticketing-direct-mail-41-issue-@banana.ch";
}
# invia una copia a ticketing@banana.ch
redirect :copy "ticketing@banana.ch";
```

