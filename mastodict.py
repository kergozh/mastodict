###
# Mastosdict, bot que gestiona uno o más diccionarios. 
# Publica una palabra aleatoria una vez l dia y responde a diferentes kewwords
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

import random
import re
import xmlrpc.client

from pybot.mastobot import Mastobot

BOT_NAME = "Lambebot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_publish_bot()
        self.init_translator()
        self.init_programmer()
        self.init_input_data()

        if self._config.get ("app.remote_calls"):
            self._proxy = xmlrpc.client.ServerProxy('http://localhost:8002')


    def run(self, botname: str = BOT_NAME) -> None:

        if self.check_programmer(self._actions.get("post.hours"), True):
            self.post_toot (self.find_random_text(None), "en")
     
        notifications = self.mastodon.notifications()
        for notif in notifications:
            content = self.check_notif(notif, "mention")

            if content != "":
                if re.search(self._actions.get("help.regex"), content) != None: 
                    self.replay_toot (self.find_help_text(notif), notif)
        
                elif re.search(self._actions.get("languages.regex"), content) != None:
                    self.replay_toot (self.find_languages_text(notif), notif)

                elif re.search(self._actions.get("random.regex"), content) != None:
                    self.replay_toot (self.find_random_text(notif), notif)

                elif re.search(self._actions.get("search.regex"), content) != None:
                    self.replay_toot (self.find_search_text(notif, content), notif)

                elif re.search(self._actions.get("marks.regex"), content) != None:
                    self.replay_toot (self.find_marks_text(notif), notif)

                elif re.search(self._actions.get("bibliografy.regex"), content) != None:
                    self.replay_toot (self.find_biblio_text(notif), notif)

                elif re.search(self._actions.get("filtered_random.regex"), content) != None:
                    self.replay_toot (self.find_filtered_random_text(notif, content), notif)

                elif re.search(self._actions.get("filtered_search.regex"), content) != None:
                    self.replay_toot (self.find_filtered_search_text(notif, content), notif)
    
                else: 
                    self.replay_toot (self.find_error_text(notif), notif)
    
        super().run(botname = botname)


    def find_error_text(self, notif):
            
        language = notif.status.language
        username = notif.account.acct
        post_texts = []
        
        self._logger.debug("notif language: %s", language)
        
        self._translator.fix_language (language)
        _text     = self._translator.get_text

        post_text  = "@" + username + ", " + _text("error")
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)
        
        return post_texts


    def find_help_text(self, notif):
            
        username = notif.account.acct
        language = notif.status.language
        post_texts = []
        
        self._logger.debug("notif language: %s", language)
        
        self._translator.fix_language (language)
        _text     = self._translator.get_text

        post_text  = "@" + username + ":\n\n" + _text("intro") + _text("opcions1")
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        post_text  = "@" + username + ":\n\n" + _text("opcions2")
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        post_text  = "@" + username + ":\n\n" + _text("opcions3")
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        return post_texts


    def find_languages_text(self, notif):
            
        post_texts = []    
        language  = notif.status.language

        self._logger.debug("notif language: %s", language)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        post_text = "@" + notif.account.acct + ":\n\n" 

        for lang in self._data.get("languages"):
            post_text += _text("idioma") + ": " + self._data.get("languages")[lang] + ", " + _text("codigo") + ": " + lang + "\n" 
            
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        return post_texts


    def find_marks_text(self, notif):
            
        post_texts = []    
        language  = notif.status.language

        self._logger.debug("notif language: %s", language)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n" 
        post_text = init_text

        for mark in self._data.get("word_marks"):
            post_text += "\"" + mark + "\": " + self._data.get("word_marks")[mark] + "\n" 
            if len(post_text) > 350:
                post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                self._logger.debug ("answer text\n" + post_text)
                post_texts.append(post_text)
                post_text = init_text
            
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        return post_texts


    def find_biblio_text(self, notif):
            
        post_texts = []    
        language  = notif.status.language

        self._logger.debug("notif language: %s", language)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n" 
        post_text = init_text

        for biblio in self._data.get("sources"):
            post_text += biblio + "\n" 
            if len(post_text) > 350:
                post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                self._logger.debug ("answer text\n" + post_text)
                post_texts.append(post_text)
                post_text = init_text
            
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        return post_texts


    def find_random_text(self, notif):

        post_texts = []    
        word_tuple, word_lang = self.find_random_word()

        if notif == None:
            post_text = ""        
        else:
            post_text  = "@" + notif.account.acct + ":\n\n" 
        
        post_text += self.find_word_text(word_tuple, word_lang)
             
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)
        
        return post_texts


    def find_search_text(self, notif, content):

        post_texts = []
        language   = notif.status.language
        word_query = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        word_query = self.clean_word(word_query).strip()

        self._logger.debug("notif language: %s", language)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n" 

        found, lang_dict = self.find_word(word_query)

        if found:
            # en este punto tenemos un diccionario de lenguages
            for word_lang in lang_dict:
                word_aux = lang_dict[word_lang]     
                # en este punto tenemos una lista de accepciones
                for word_tuple in word_aux:
                    post_text = init_text + self.find_word_text(word_tuple, word_lang)
                    post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                    self._logger.debug ("answer text\n" + post_text)
                    post_texts.append(post_text)
 
        else:
            post_text = init_text + _text("not_found")
            post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
            self._logger.debug ("answer text\n" + post_text)
            post_texts.append(post_text)
        
        return post_texts


    def clean_word(self, word_query):

        self._logger.debug("word query antes: %s", word_query)

        word_query = word_query.lower()
        word_query = re.sub(r'[^a-záéíóúàèìòùâêîôûäëïöüāēīōūýŷ]', '', word_query)
        word_query = word_query.lower()

        word_tuple  = word_query.maketrans("áéíóúàèìòùâêîôûäëïöüāēīōūýŷ", "aeiouaeiouaeiouaeiouaeiouyy")
        word_query = word_query.translate(word_tuple)

        self._logger.debug("word query cleaned: %s", word_query)

        return word_query


    def find_filtered_random_text(self, notif, content):

        post_texts = []
        language   = notif.status.language
        word_lang  = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()

        self._logger.debug("notif language: %s", language)
        self._logger.debug("word language : %s", word_lang)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        if notif == None:
            post_text = ""        
        else:
            post_text  = "@" + notif.account.acct + ":\n\n" 

        if word_lang in self._data.get("languages"):
            word_tuple = self.find_filtered_random_word(word_lang)
            post_text += self.find_word_text(word_tuple, word_lang)
        else:
            post_text += _text("error_idioma")

        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)
        
        return post_texts


    def find_filtered_search_text(self, notif, content):

        post_texts   = []
        language     = notif.status.language
        content      = (re.sub(r'((-|--)\s*\w+)', '', content)).strip()
        content_list = content.split()

        word_query   = self.clean_word(content_list[0]).strip()
        word_lang    = (content_list[1]).strip()
        
        self._logger.debug("notif language: %s", language)
        self._logger.debug("word language : %s", word_lang)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        init_text = "@" + notif.account.acct + ":\n\n" 

        found, word_list = self.find_filtered_word(word_query, word_lang)

        if found:
            # en este punto tenemos una lista de accepciones
            for word_tuple in word_list:
                post_text = init_text + self.find_word_text(word_tuple, word_lang)
                post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                self._logger.debug ("answer text\n" + post_text)
                post_texts.append(post_text)
        else:
            post_text = init_text + _text("not_found")
            post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
            self._logger.debug ("answer text\n" + post_text)
            post_texts.append(post_text)
        
        return post_texts


    def find_word_text(self, word_tuple, language):

        """
        La tuple de palabra de diccionario tiene este aspecto:
              line = '         - !!python/tuple [' 
        0-    line = line + '\"' + item3[str_word] + '\", ' 
        1-    line = line + '\"' + item3[str_grammar] + '\", ' 
        2-    line = line + '\"' + item3[str_gloss] + '\", ' 
              #line = line + '\"' + item3[str_category] + '\", ' 
        3-    line = line + '\"' + item3[str_mark] + '\", ' 
        4-    line = line + '\"' + str(item3[str_deprecated]) + '\"' + ', ' 
        5-    line = line + '\"' + item3[str_page] + '\", '
        6-    line = line + item3[str_ref]  
            line = line + ']' 
        """
        word = 0
        grammar = 1
        gloss = 2
        mark = 3
        deprecated = 4
        page = 5
        referencies = 6

        if word_tuple[mark] == "": 
            post_text = "\"" + word_tuple[word] + "\", "
        else:
            post_text = "\"" + word_tuple[mark] + " " + word_tuple[word] + "\", "

        post_text += self._data.get("languages")[language] + " " + word_tuple[grammar] + "\n"
        post_text += "\"" + word_tuple[gloss] + "\"\n"
        
        """
        de mmomento hemos eliminado las categorias porque no apostan mucho y ocupan memoria...
        if word_tuple[category] != "":
            post_text += " (category: " +  self._data.get("word_categories")[word_tuple[category]]  + ")"
        post_text += "\n\n"
        """

        for i in word_tuple[mark]:
            post_text += self._data.get("word_marks")[i] + "\n"

        if word_tuple[deprecated]:
            post_text += "Most likely it is a deprecated word" + "\n"

        if len(word_tuple[referencies]) > 0:
            post_text += "Referencies:\n"
            for ref in word_tuple[referencies]:
                if len(post_text) < 350:
                    post_text += "- " + ref + "\n"
            
        if word_tuple[page] == "":
            post_text += "https://eldamo.org/content/words/word-" + word_tuple[page] +".html"
             
        return post_text


    def find_random_word(self):
            
        if self._config.get("app.remote_calls"):
            word_tuple, word_lang = self._proxy.find_random_word()
        
        else:
            word_lang = random.choice(list(self._data.get("dictionaries").keys()))
            self._logger.debug("word language : %s", word_lang)

            word_tuple = self.find_filtered_random_word(word_lang)

        return word_tuple, word_lang


    def find_filtered_random_word(self, word_lang):

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
            
        found      = False
        lang_dict  = {}
        
        if self._config.get("app.remote_calls"):
            found, lang_dict = self._proxy.find_word(self, word_query)

        else:
            for word_lang in self._data.get("dictionaries").keys():

                self._logger.debug("word language : %s", word_lang)

                found_aux, word_tuple = self.find_filtered_word(word_query, word_lang)

                if found_aux:
                    lang_dict[word_lang] = word_tuple
                    found = found_aux

            if len(lang_dict) == 0:
                lang_dict["error"] = "not found"

        return found, lang_dict


    def find_filtered_word(self, word_query, word_lang):
            
        found     = False
        
        if self._config.get("app.remote_calls"):
            found, word_tuple = self._proxy.find_filtered_word(word_query, word_lang)

        else:
            if word_query in self._data.get("dictionaries")[word_lang]: 
                found    = True
                word_tuple = self._data.get("dictionaries")[word_lang][word_query]
                # en este punto tenemos una tuple de acepciones  

        if not found:
            word_tuple = ("error", "not found")

        return found, word_tuple


# main

if __name__ == '__main__':
    Bot().run()
