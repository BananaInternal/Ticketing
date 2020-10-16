from nlp.labeler import NlpLabeler
from nlp.labeler import UnsupportedLanguageError
from nlp.polyglot import get_language

if __name__ == '__main__':
    nlp_labeler = NlpLabeler("nlp/data")

    tests = [
        "Il vostro programmma e supportato su Windows?",
        "E disponibile il programma per Mac?",
        "Posso installarlo su Android?",
        "Posso gestire le fatture con QR Code?",
        "Fatture con QR Code?",
        "Ci sono le fatture con QR Code?",
        "Banana e disponibile per Linux?",
        "Accettate pagamenti con VISA?",
        "Can I install Banana on Windows?",
        "Can the program run on Mac?",
        "Can we use the software on Android?",
        "Can I manage QR Code invoices?",
        "Does Banana handle QR Code invoices?",
        "Can I install banana on Ubuntu?",
        "Are the new invoices with qr code available?",
        "Can I pay with credit card?",
        "Mi povas paroli Esperanton",
        "E supportato Windows?",
        "E disponibile il programma per Mac?",
        "Posso installarlo su Android?",
        "Posso gestire le fatture con QR Code?",
        "Fatture con QR Code?",
        "Ci sono le fatture con QR Code?",
        "Banana e disponibile per Linux?",
        "Accettate pagamenti con VISA?",
        "Posso annullare il piano acquistato?",
        "Vorrei cancellare il piano da me sottoscritto",
        "Posso passare a un piano annuale?",
        "Can I install Banana on Windows?",
        "Can the program run on Mac?",
        "Can we use the software on Android?",
        "Can I manage QR Code invoices?",
        "I want to stop the subscription to the plan.",
        "Does Banana handle QR Code invoices?",
        "Can I install banana on Ubuntu?",
        "Are the new invoices with qr code available?",
        "Can I pay with credit card?",
        "Can I cancel my subscription to the paid plan?",
        "I want to delete my subscription to the paid plan.",
        "Can I switch to an annual subscription?",
        "What if I want to switch to an annual subscription?",
        "Pouis-je telecharger Banana sur Mac OS?",
        "Pouis-je telecharger Banana sur mon Android telephone intelligent?",
        "Pouis-je travailler avec QR Code factures?",
        "Les factures supportent QR Codes?",
        "Pouis-je installer Banana sur Ubuntu?",
        "Pouis-je utiliser votre programme sur Windows?",
        "Pouis-je acheter votre produits avec ma carte de credit?",
        "Pouis-je acheter votre produits de un Etat etrangere?",
        "Puedo instalar Banana en Mac OS?",
        "Puedo instalar el software en un iPhone?",
        "Puedo escargar el programa en un Android smarphone?",
        "La factura con QR Code esta soportada?",
        "Puedo instalar Banana Accounting en Linux Ubuntu?",
        "Puedo usar mia Visa tarjeta de credito para comprar Banana?",
        "Puedo trabajar con el nuevo modelo de factura con QR Code?",
        "Puedo pagar desde Estados Unitos?",
        "Ist es von Windows unterstuzt?",
        "Gibt es das Software auch fur Mac?",
        "Kann ich es auf Android installieren?",
        "Kann ich meine Rechnungen mit dem QR code machen?",
        "Rechnungen mit QR Code?",
        "Gibt es Rechnungen mit QR Code?",
        "Gibt es Banana auch fur Linux?",
        "Akzeptiert ihr bezahlungen via VISA?"
    ]

    print("-- Test --")

    for s in tests:
        lang = get_language(s)
        print(s)
        if lang is None:
            print("- error: failed to recognize language\n")
            continue
        try:
            labels = nlp_labeler.label(s, lang)
            print("- labels: {}\n".format(labels))
        except UnsupportedLanguageError:
            print("- error: unsupported language: {}".format(lang))
