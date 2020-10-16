from langdetect import detect_langs
from langdetect.language import Language


def get_language(text):
    language_probabilities = detect_langs(text)
    best_lang = Language(
        None,
        0.8  # Minimum probability
    )
    for item in language_probabilities:
        print(item.lang, end=" ")
        if item.prob > best_lang.prob:
            best_lang = item
    print("")
    return best_lang.lang
