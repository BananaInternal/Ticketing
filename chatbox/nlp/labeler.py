import fasttext as ft
import os


class NlpLabeler(object):
    def __init__(self, work_dir):
        """
        Object that can be used to label strings

        :param work_dir: The base directory in which labeler data is stored
        """
        self.__work_dir = work_dir
        self.__models = {}

    def label(self, text, language):
        """
        Label a string written in a given language

        :param text: The string to label
        :param language: The language (in iso two-chars code)
        :return:
        """
        labels, confidence = self.__get_model(language).predict(text, 3)
        results = []
        for i in range(0, len(labels)):
            if confidence[i] > 0.5:
                results.append(labels[i].replace("__label__", ""))
        return results

    def __get_model(self, language):
        try:
            model = self.__models[language]
        except KeyError:
            train_path = os.path.join(self.__work_dir, "{}.txt".format(language))
            if not os.path.exists(train_path):
                raise UnsupportedLanguageError(
                    "Missing train file for language {} at {}".format(language, train_path)
                )
            # Train the model
            model = ft.train_supervised(input=train_path,
                                        epoch=50)

            self.__models[language] = model
        return model


class UnsupportedLanguageError(Exception):
    pass
