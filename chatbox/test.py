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
        "Mi povas paroli Esperanton"
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
