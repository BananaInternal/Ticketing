from nlp.labeler import NlpLabeler
from nlp.labeler import UnsupportedLanguageError
from nlp.polyglot import get_language

if __name__ == '__main__':
    nlp_labeler = NlpLabeler("nlp/data")

    tests = [
        "Il vostro programmma e supportato su Windows?", "it",
        "E disponibile il programma per Mac?", "it",
        "Posso installarlo su Android?", "it",
        "Posso gestire le fatture con QR Code?", "it",
        "Fatture con QR Code?", "it",
        "Ci sono le fatture con QR Code?", "it",
        "Banana e disponibile per Linux?", "it",
        "Accettate pagamenti con VISA?", "it",
        "Can I install Banana on Windows?", "en",
        "Can the program run on Mac?", "en",
        "Can we use the software on Android?", "en",
        "Can I manage QR Code invoices?", "en",
        "Does Banana handle QR Code invoices?", "en",
        "Can I install banana on Ubuntu?", "en",
        "Are the new invoices with qr code available?", "en",
        "Can I pay with credit card?", "en",
        "Mi povas paroli Esperanton", None,
        "E supportato Windows?", "it",
        "E disponibile il programma per Mac?", "it",
        "Posso installarlo su Android?", "it",
        "Posso gestire le fatture con QR Code?", "it",
        "Fatture con QR Code?", "it",
        "Ci sono le fatture con QR Code?", "it",
        "Banana e disponibile per Linux?", "it",
        "Accettate pagamenti con VISA?", "it",
        "Posso annullare il piano acquistato?", "it",
        "Vorrei cancellare il piano da me sottoscritto", "it",
        "Posso passare a un piano annuale?", "it",
        "Can I install Banana on Windows?", "en",
        "Can the program run on Mac?", "en",
        "Can we use the software on Android?", "en",
        "Can I manage QR Code invoices?", "en",
        "I want to stop the subscription to the plan.", "en",
        "Does Banana handle QR Code invoices?", "en",
        "Can I install banana on Ubuntu?", "en",
        "Are the new invoices with qr code available?", "en",
        "Can I pay with credit card?", "en",
        "Can I cancel my subscription to the paid plan?", "en",
        "I want to delete my subscription to the paid plan.", "en",
        "Can I switch to an annual subscription?", "en",
        "What if I want to switch to an annual subscription?", "en",
        "Pouis-je telecharger Banana sur Mac OS?", "fr",
        "Pouis-je telecharger Banana sur mon Android telephone intelligent?", "fr",
        "Pouis-je travailler avec QR Code factures?", "fr",
        "Les factures supportent QR Codes?", "fr",
        "Pouis-je installer Banana sur Ubuntu?", "fr",
        "Pouis-je utiliser votre programme sur Windows?", "fr",
        "Pouis-je acheter votre produits avec ma carte de credit?", "fr",
        "Pouis-je acheter votre produits de un Etat etrangere?", "fr",
        "Puedo instalar Banana en Mac OS?", "es",
        "Puedo instalar el software en un iPhone?", "es",
        "Puedo escargar el programa en un Android smarphone?", "es",
        "La factura con QR Code esta soportada?", "es",
        "Puedo instalar Banana Accounting en Linux Ubuntu?", "es",
        "Puedo usar mia Visa tarjeta de credito para comprar Banana?", "es",
        "Puedo trabajar con el nuevo modelo de factura con QR Code?", "es",
        "Puedo pagar desde Estados Unitos?", "es",
        "Ist es von Windows unterstuzt?", "de",
        "Gibt es das Software auch fur Mac?", "de",
        "Kann ich es auf Android installieren?", "de",
        "Kann ich meine Rechnungen mit dem QR code machen?", "de",
        "Rechnungen mit QR Code?", "de",
        "Gibt es Rechnungen mit QR Code?", "de",
        "Gibt es Banana auch fur Linux?", "de",
        "Akzeptiert ihr bezahlungen via VISA?", "de",
        "Angenommen ich installiere Banana nicht auf meinen PC sondern über meinen PC auf einem separaten Speicher und gebe den Lizenzschlüssel ein, funktioniert dann Banana auch noch wenn ich den separaten Speicher an einem anderen PC einstecke", "de",
        "Guten morgen, Ich musst mir einen neuen Computer zulegen. Ich kann aber auf meinem alten Laptop den Lizenzschlüssel nicht komplett lesen. Wie muss ich vorgehen, dass ich den Lizenzschlüssel auf dem neuen Laptop eingeben kann? ", "de",
        "Good morning, I would like to install Banana software on my iPad. Does this program run on iOS? Thank you, God bless you", "en",
        "To whom it may concern. Good morning/afternoon/evening sir/madam, it depends on when you red that emmail. Me like to know if or whether or weter ai chen work with invoices that supports qr code. tykbye", "en"

    ]

    print("-- Test --")

    i = 0
    while i < len(tests):
        s = tests[i]
        i += 1
        expected = tests[i]
        i += 1

        lang = get_language(s)
        if lang is None:
            if expected is not None:
                print("{}\n\terror: failed to recognize language".format(s))
            continue

        if lang != expected:
            print("{}\n\terror: expected {}, detected {}".format(s, expected, lang))
            continue
        try:
            labels = nlp_labeler.label(s, lang)
            print("{}\n\tlabels: {}".format(s, labels))
        except UnsupportedLanguageError:
            print("{}\n\terror: unsupported language: {}".format(s, lang))
