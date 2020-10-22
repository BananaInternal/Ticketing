from langdetect import detect_langs
from langdetect.language import Language


def get_language(text):
    """
    Obtain the iso language code of which the given
    text is written in if there's a certain certainty.
    :param text: The string to analyze
    :return: The iso language code (2 chars string)
    """
    language_probabilities = detect_langs(text)
    best_lang = Language(
        None,
        0.8  # Minimum probability
    )
    for item in language_probabilities:
        if item.prob > best_lang.prob:
            best_lang = item
    return best_lang.lang
