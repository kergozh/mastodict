"""
Mastosdict, bot que gestiona uno o más diccionarios.
Publica una palabra aleatoria una vez l dia y responde a diferentes kewwords
Basado (pero cada vez más lejano) en el bot "info" original de @spla@mastodont.cat
https://git.mastodont.cat/spla/info
"""

import random
import re
import xmlrpc.client

from pybot.mastobot import Mastobot

BOT_NAME = "Lambebot"
MAX_LENGTH = 490

class Bot(Mastobot):
    """ Clase que implementa el bot heredando del genérico Mastobot """

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_publish_bot()
        self.init_translator()
        self.init_programmer()
        self.init_input_data()

        if self._config.get ("app.remote_calls"):
            self._proxy = xmlrpc.client.ServerProxy('http://localhost:8002')

        self._hashtag = "\n#Tolkien #Tolkiendili"


    def run(self, botname: str = BOT_NAME) -> None:

        if self.check_programmer(self._actions.get("post.hours"), True):
            self.post_toot (self.find_random_text(None), "en")

        notifications = self.get_notifications()
        for notif in notifications:
            content = self.check_notif(notif, "mention")

            if content != "":
                if re.search(self._actions.get("help.regex"), content) is not None:
                    self.replay_toot (self.find_help_text(notif), notif)

                elif re.search(self._actions.get("languages.regex"), content) is not None:
                    self.replay_toot (self.find_languages_text(notif), notif)

                elif re.search(self._actions.get("random.regex"), content) is not None:
                    self.replay_toot (self.find_random_text(notif), notif)

                elif re.search(self._actions.get("search.regex"), content) is not None:
                    self.replay_toot (self.find_search_text(notif, content), notif)

                elif re.search(self._actions.get("gloss.regex"), content) is not None:
                    self.replay_toot (self.find_gloss_text(notif, content), notif)

                elif re.search(self._actions.get("marks.regex"), content) is not None:
                    self.replay_toot (self.find_marks_text(notif), notif)

                elif re.search(self._actions.get("bibliografy.regex"), content) is not None:
                    self.replay_toot (self.find_biblio_text(notif), notif)

                elif re.search(self._actions.get("filtered_random.regex"), content) is not None:
                    self.replay_toot (self.find_filtered_random_text(notif, content), notif)

                elif re.search(self._actions.get("filtered_search.regex"), content) is not None:
                    self.replay_toot (self.find_filtered_search_text(notif, content), notif)

                elif re.search(self._actions.get("filtered_gloss.regex"), content) is not None:
                    self.replay_toot (self.find_filtered_gloss_text(notif, content), notif)

                else:
                    self.replay_toot (self.find_error_text(notif), notif)

        super().run(botname = botname)


    def find_error_text(self, notif):
        """ Rellenar la salida en caso de error """

        language = notif.status.language
        username = notif.account.acct
        p_txts = []

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        p_txt  = "@" + username + ", " + _text("error")
        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_help_text(self, notif):
        """ Rellenar la salida en caso de pedir help """

        username = notif.account.acct
        language = notif.status.language
        p_txts = []

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        p_txt  = "@" + username + ":\n\n" + _text("intro") + _text("opcions1")
        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        p_txt  = "@" + username + ":\n\n" + _text("opcions2")
        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        p_txt  = "@" + username + ":\n\n" + _text("opcions3")
        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        p_txt  = "@" + username + ":\n\n" + _text("opcions4")
        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_languages_text(self, notif):
        """ Rellenar la salida en caso de pedir la lista de idiomas """

        p_txts = []
        language  = notif.status.language

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n"
        p_txt = init_text

        for lang in self._data.get("languages"):
            lang_text = _text("idioma") + ": " + self._data.get("languages")[lang] + \
                ", " + _text("codigo") + ": " + lang + "\n"
            if len(p_txt) + len(lang_text) > (MAX_LENGTH):
                p_txt= (p_txt[:MAX_LENGTH] + '...') if len(p_txt) > MAX_LENGTH else p_txt
                self._logger.debug ("answer text\n%s", p_txt)
                p_txts.append(p_txt)
                p_txt = init_text + lang_text
            else:
                p_txt += lang_text

        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_marks_text(self, notif):
        """ Rellenar la salida en caso de pedir la lista de marcas """

        p_txts = []
        language  = notif.status.language

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n"
        p_txt = init_text

        for mark in self._data.get("word_marks"):
            mark_text = "\"" + mark + "\": " + self._data.get("word_marks")[mark] + "\n"
            if len(p_txt) + len(mark_text) > (MAX_LENGTH):
                p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                self._logger.debug ("answer text\n%s", p_txt)
                p_txts.append(p_txt)
                p_txt = init_text + mark_text
            else:
                p_txt += mark_text

        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_biblio_text(self, notif):
        """ Rellenar la salida en caso de pedir la lista de bibliografía """

        p_txts = []
        language  = notif.status.language

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n"
        p_txt = init_text

        for biblio in self._data.get("sources"):
            biblio_text = biblio + "\n"
            if len(p_txt) + len(biblio_text) > (MAX_LENGTH):
                p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                self._logger.debug ("answer text\n%s", p_txt)
                p_txts.append(p_txt)
                p_txt = init_text + biblio_text
            else:
                p_txt += biblio_text

        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_random_text(self, notif):
        """ Rellenar la salida en caso de pedir una palabra aleatoria """

        p_txts = []
        word_tuple, word_lang = self.find_random_word()

        if notif is None:
            init_text = ""
        else:
            init_text  = "@" + notif.account.acct + ":\n\n"

        p_txt = init_text + \
            self.find_word_text(word_tuple, word_lang, len(init_text) + len(self._hashtag), True)

        if len(p_txt) + len(self._hashtag) < (MAX_LENGTH):
            p_txt += self._hashtag

        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_search_text(self, notif, content):
        """ Rellenar la salida en caso de pedir buscar una palabra """

        p_txts = []
        language   = notif.status.language
        word_query = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        word_query = self.clean_word(word_query).strip()

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        found, lang_dict = self.find_word(word_query)

        if found:
            init_text = "@" + notif.account.acct + ":\n\n"
            # en este punto tenemos un diccionario de lenguages
            for word_lang in lang_dict:
                word_aux = lang_dict[word_lang]
                # en este punto tenemos una lista de accepciones
                for word_tuple in word_aux:
                    p_txt = init_text + \
                        self.find_word_text(word_tuple, word_lang, len(init_text), True)
                    p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                    self._logger.debug ("answer text\n%s", p_txt)
                    p_txts.append(p_txt)

        else:
            init_text = "@" + notif.account.acct + ": "
            p_txt = init_text + _text("not_found")
            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)

        return p_txts


    def find_gloss_text(self, notif, content):
        """ Rellenar la salida en caso de pedir buscar una búsqueda inversa """

        p_txts = []
        language   = notif.status.language
        word_query = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        word_query = self.clean_word(word_query).strip()

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        found, lang_dict = self.find_gloss(word_query)

        if found:
            init_text = "@" + notif.account.acct + ":\n\n"
            # en este punto tenemos un diccionario de lenguages
            p_txt = init_text
            for word_lang in lang_dict:
                word_aux = lang_dict[word_lang]
                # en este punto tenemos una lista de accepciones
                for word_tuple in word_aux:
                    word_text = self.find_word_text(word_tuple, word_lang, 0, False)
                    if len(p_txt) + len (word_text) > MAX_LENGTH:
                        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                        self._logger.debug ("answer text\n%s", p_txt)
                        p_txts.append(p_txt)
                        p_txt = init_text + word_text
                    else:
                        p_txt += word_text

            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)
        else:
            init_text = "@" + notif.account.acct + ": "
            p_txt = init_text + _text("not_found")
            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)

        return p_txts


    def clean_word(self, word_query):
        """ Eliminar caracteres "extraños" para hacer la búsquesa en los diccionarios """

        self._logger.debug("word: %s", word_query)

        word_query = word_query.lower()
        word_query = re.sub(r'[^a-záéíóúàèìòùâêîôûäëïöüāēīōūýŷ]', '', word_query)
        word_query = word_query.lower()

        word_tuple  = \
          word_query.maketrans("áéíóúàèìòùâêîôûäëïöüāēīōūýŷ", "aeiouaeiouaeiouaeiouaeiouyy")
        word_query = word_query.translate(word_tuple)

        self._logger.debug("cleaned word: %s", word_query)

        return word_query


    def find_filtered_random_text(self, notif, content):
        """ Rellenar la salida en caso de pedir una palabra aleatoria filtrada """

        p_txts = []
        language   = notif.status.language
        word_lang  = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()

        self._logger.debug("word language : %s", word_lang)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text  = "@" + notif.account.acct + ":\n\n"
        p_txt = init_text

        if word_lang in self._data.get("languages"):
            word_tuple = self.find_filtered_random_word(word_lang)
            p_txt += self.find_word_text(word_tuple, word_lang, len(init_text), True)
        else:
            p_txt += _text("error_idioma")

        p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
        self._logger.debug ("answer text\n%s", p_txt)
        p_txts.append(p_txt)

        return p_txts


    def find_filtered_search_text(self, notif, content):
        """ Rellenar la salida en caso de pedir buscar una palabra filtrada """

        p_txts   = []
        language     = notif.status.language
        content      = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        content_list = content.split()

        word_query   = self.clean_word(content_list[0]).strip()
        word_lang    = (content_list[1]).strip()

        self._logger.debug("word language : %s", word_lang)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        found, word_tuples = self.find_filtered_word(word_query, word_lang)

        if found:
            init_text = "@" + notif.account.acct + ":\n\n"
            # en este punto tenemos una lista de accepciones
            for word_tuple in word_tuples:
                p_txt = init_text + self.find_word_text(word_tuple, word_lang, len(init_text), True)
                p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                self._logger.debug ("answer text\n%s", p_txt)
                p_txts.append(p_txt)

        else:
            init_text = "@" + notif.account.acct + ": "
            p_txt = init_text + _text("not_found")
            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)

        return p_txts


    def find_filtered_gloss_text(self, notif, content):
        """ Rellenar la salida en caso de pedir buscar una búsqueda inversa filtrada """

        p_txts   = []
        language     = notif.status.language
        content      = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        content_list = content.split()

        word_query   = self.clean_word(content_list[0]).strip()
        word_lang    = (content_list[1]).strip()

        self._logger.debug("word language : %s", word_lang)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        found, word_tuples = self.find_filtered_gloss(word_query, word_lang)

        if found:
            init_text = "@" + notif.account.acct + ":\n\n"
            p_txt = init_text
            # en este punto tenemos una lista de accepciones
            for word_tuple in word_tuples:
                word_text = self.find_word_text(word_tuple, word_lang, 0, False)
                if len(p_txt) + len (word_text) > MAX_LENGTH:
                    p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
                    self._logger.debug ("answer text\n%s", p_txt)
                    p_txts.append(p_txt)
                    p_txt = init_text + word_text
                else:
                    p_txt += word_text

            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)

        else:
            init_text = "@" + notif.account.acct + ": "
            p_txt = init_text + _text("not_found")
            p_txt = (p_txt[:MAX_LENGTH] + '... ') if len(p_txt) > MAX_LENGTH else p_txt
            self._logger.debug ("answer text\n%s", p_txt)
            p_txts.append(p_txt)

        return p_txts


    def find_word_text(self, word_tuple, language, init_lenght, all_text):
        """ Dar formato a una palabra de un diccionario
         La tuple de palabra de diccionario tiene este aspecto:
              line = '         - !!python/tuple ['
        0-    line = line + '\"' + item3[str_word] + '\", '
        1-    line = line + '\"' + item3[str_grammar] + '\", '
        2-    line = line + '\"' + item3[str_gloss] + '\", '
        3-    line = line + '\"' + item3[str_mark] + '\", '
        4-    line = line + '\"' + str(item3[str_deprecated]) + '\"' + ', '
        5-    line = line + '\"' + item3[str_page] + '\", '
        6-    line = line + item3[str_element]  + ', '
        7-    line = line + item3[str_ref]
            line = line + ']'
        """

        word = 0
        grammar = 1
        gloss = 2
        mark = 3
        deprecated = 4
        page = 5
        elements = 6
        referencies = 7

        if word_tuple[mark] == "":
            p_txt = "\"" + word_tuple[word] + "\", "
        else:
            p_txt = "\"" + word_tuple[mark] + " " + word_tuple[word] + "\", "

        if all_text:
            p_txt += self._data.get("languages")[language] + " " + word_tuple[grammar] + ": "
        else:
            p_txt += language + " " + word_tuple[grammar] + ": "

        p_txt += "\"" + word_tuple[gloss] + "\"\n"

        if all_text:
            for i in word_tuple[mark]:
                p_txt += self._data.get("word_marks")[i] + "\n"

            #if word_tuple[deprecated]:
            #    p_txt += "Most likely it is a deprecated word" + "\n"

            if len(word_tuple[elements]) > 0:
                p_txt += "Elements: "
                for element in word_tuple[elements]:
                    p_txt += "\"" + element + "\", "
                p_txt = p_txt[:len(p_txt)-2] + "\n"

            if word_tuple[page] != "":
                last_text = "https://eldamo.org/content/words/word-" + word_tuple[page] +".html\n"
            else:
                last_text = ""

            if len(word_tuple[referencies]) > 0:
                p_txt += "References:\n"
                for ref in word_tuple[referencies]:
                    ref_text = "- " + ref + "\n"
                    if (init_lenght + len(p_txt) + len(ref_text) + len(last_text)) < MAX_LENGTH:
                        p_txt += ref_text

            if last_text != "":
                p_txt += last_text

        return p_txt


    def find_random_word(self):
        """ Buscar una palabra aleatoria en el diccionario """

        if self._config.get("app.remote_calls"):
            word_tuple, word_lang = self._proxy.find_random_word()

        else:
            word_lang = random.choice(list(self._data.get("dictionaries").keys()))
            self._logger.debug("word language : %s", word_lang)

            word_tuple = self.find_filtered_random_word(word_lang)

        return word_tuple, word_lang


    def find_filtered_random_word(self, word_lang):
        """ Buscar una palabra aleatoria filtrada en el diccionario """

        if self._config.get("app.remote_calls"):
            word_tuple = self._proxy.find_filtered_random_word(word_lang)

        else:
            word_aux  = random.choice(list(self._data.get("dictionaries")[word_lang].values()))

            # en este punto tenemos una tuple de acepciones o una tuple-paraula
            if isinstance(word_aux[0], tuple):
                word_tuple = random.choice(word_aux)
            else:
                word_tuple = word_aux

        return word_tuple


    def find_word(self, word_query):
        """ Buscar una palabra en el diccionario """

        found      = False
        lang_dict  = {}

        if self._config.get("app.remote_calls"):
            found, lang_dict = self._proxy.find_word(word_query)

        else:
            for word_lang in self._data.get("dictionaries").keys():

                self._logger.debug("word language : %s", word_lang)
                found_aux, word_tuple = self.find_filtered_word(word_query, word_lang)

                if found_aux:
                    lang_dict[word_lang] = word_tuple
                    found = found_aux

            if not found:
                lang_dict["error"] = "not found"

        return found, lang_dict


    def find_filtered_word(self, word_query, word_lang):
        """ Buscar una palabra filtrada en el diccionario """

        found     = False

        if self._config.get("app.remote_calls"):
            found, word_tuples = self._proxy.find_filtered_word(word_query, word_lang)

        else:
            if word_query in self._data.get("dictionaries")[word_lang]:
                found    = True
                word_tuples = self._data.get("dictionaries")[word_lang][word_query]
                # en este punto tenemos una tuple de acepciones

        if not found:
            word_tuples = ("error", "not found")

        return found, word_tuples


    def find_gloss(self, word_query):
        """ Hacer una búsqueda inversa en el diccionario """

        found      = False
        lang_dict  = {}

        if self._config.get("app.remote_calls"):
            found, lang_dict = self._proxy.find_gloss(word_query)

        else:
            if word_query in self._data.get("english"):
                found = True
                lang_dict = self._data.get("english")[word_query]
            else:
                lang_dict["error"] = "not found"

        return found, lang_dict


    def find_filtered_gloss(self, word_query, word_lang):
        """ Hacer una búsqueda inversa filtrada en el diccionario """

        found     = False

        if self._config.get("app.remote_calls"):
            found, word_tuples = self._proxy.find_filtered_gloss(word_query, word_lang)

        else:
            if word_query in self._data.get("english"):
                if word_lang in self._data.get("english")[word_query]:
                    found    = True
                    word_tuples = self._data.get("english")[word_query][word_lang]
                    # en este punto tenemos una tuple de acepciones

            if not found:
                word_tuples = ("error", "not found")

        return found, word_tuples


# main

if __name__ == '__main__':
    Bot().run()
