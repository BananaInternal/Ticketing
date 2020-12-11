

abilitare gli script sieve nei filtri (impostazioni della mail)

require ["editheader", "copy"];
deleteheader "To";
addheader "To" "ticketing+ticketing-direct-mail-41-issue-@banana.ch";
redirect :copy "ticketing@banana.ch";