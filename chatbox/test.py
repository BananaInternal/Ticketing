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
        "To whom it may concern. Good morning/afternoon/evening sir/madam, it depends on when you red that emmail. Me like to know if or whether or weter ai chen work with invoices that supports qr code. tykbye", "en",
        "Due to internal company restructuring, I would have to rely on installing banana accounting on another computer. So far the accounting has only been installed on one computer. However, my employee solved the mail with the license key! Can you send me my license key again?", "en",
        "306/5000 Dear Sir or Madam, I am looking for my license key. At arthur.grossen@bluewin.ch comes the message no key found. Is it possible that my Banana9 accounting for Fr. 129.00 has not yet been paid, although I have been working with it since April? Best regards Arthur Grossen", "en",
        "Hello Years ago we bought a Banana license for version 8 for the now dissolved company Mountainbike Parts Langer & Co in velotec.ch GmbH. Since then we have used the license for the successor company velotec.ch GmbH. Now we have changed the IT equipment and mail server and unfortunately I can no longer find the email with the license key to enter the license key for the new installation of Banana. Would you be so kind as to resend me the email with the license key? The email at that time was probably either info@mountainbike-parts.ch or info@velotec.ch (if already ordered with the successor company). You are welcome to send the license again to the same email at the time. Thanks for your efforts. Kind regards Andreas Langer", "en",
        "good day your support info says that you get telephone support if you are registered. should i know the phone number? my problem: i upgraded from banana 8 to banana 9 last year. now i want to install banana 9 on my new computer, but i can only find the license key for banana-8. can you tell me the license key for banana 9? many thanks and best regards manuela ryter", "en",
        "Sehr geehrte Damen und Herren Gerne möchten wir unser Banana-Programm auf die neuste Version updaten. Da ich erst ein Jahr damit arbeite, weiss ich nicht, wo ich den Lizenz-Schlüssel finden kann.   Im Anhang sende ich Ihnen ein Dokument, welches Angaben zur Registration beinhaltet. Die dort angegebene Mailadresse existiert aber schon lange nicht mehr. Auch die Postadresse stimmt nicht mehr. Neu lautet sie:  Elite Autocenter AG Kirchweg 5 3812 Wilderswil", "de",
        "Hallo, ich plane Banana fuer meine Buchhaltung einzusetzen (1Benutzer, 1 Lizenz) ich weiss aber bereits, dass ich in wenigen Monaten  meinen Laptop (wo ich die Software zunaechst installieren wuerde) durch eine PC ersetzen werde. Wie kann ich meinen Lizenzschluessel auf meinen neuen PC uebertragen? Wie kann ich meine Buchhaltungsdaten auf meinen neuen PC uebertragen? Mit freundlichem Gruss Benedikt Brenke", "de",
        "Guten Tag, ich wollte fragen, ob es möglich ist, banana auf einem weiteren Computer zu installieren, ohne eine weitere Lizenz kaufen zu müssen? Meine Mutter arbeitet teilweise an meiner Buchhaltung und vom Handling her wäre es einfacher, wenn sie dabei nicht auf meinen Comuputer angewiesen wäre.", "de"

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
