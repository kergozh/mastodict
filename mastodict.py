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


    def find_random_text(self, notif):

        post_texts = []    
        word_dict, word_lang = self.find_random_word()

        if notif == None:
            post_text = ""        
        else:
            post_text  = "@" + notif.account.acct + ":\n\n" 
        
        post_text += self.find_word_text(word_dict, word_lang)
             
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
                # en este punto tenemos un diccionario o una lista de accepciones
                if isinstance(word_aux, list):                
                    for word_dict in word_aux:
                        post_text = init_text + self.find_word_text(word_dict, word_lang)
                        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                        self._logger.debug ("answer text\n" + post_text)
                        post_texts.append(post_text)
                else: 
                    word_dict = word_aux
                    post_text = init_text + self.find_word_text(word_dict, word_lang)
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

        word_dict  = word_query.maketrans("áéíóúàèìòùâêîôûäëïöüāēīōūýŷ", "aeiouaeiouaeiouaeiouaeiouyy")
        word_query = word_query.translate(word_dict)

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
            word_dict = self.find_filtered_random_word(word_lang)
            post_text += self.find_word_text(word_dict, word_lang)
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
            for word_dict in word_list:
                post_text = init_text + self.find_word_text(word_dict, word_lang)
                post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
                self._logger.debug ("answer text\n" + post_text)
                post_texts.append(post_text)
        else:
            post_text = init_text + _text("not_found")
            post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
            self._logger.debug ("answer text\n" + post_text)
            post_texts.append(post_text)
        
        return post_texts


    def find_word_text(self, word_dict, language):

        if word_dict["mark"] == "": 
            post_text = "\"" + word_dict["word"] + "\", "
        else:
            post_text = "\"" + word_dict["mark"] + " " + word_dict["word"] + "\", "

        post_text += self._data.get("languages")[language] + " " + word_dict["grammar"] + "\n"
        post_text += "\"" + word_dict["gloss"] + "\""
        if word_dict["category"] != "":
            post_text += " (category: " +  self._data.get("word_categories")[word_dict["category"]]  + ")"
        post_text += "\n\n"

        for i in word_dict["mark"]:
            post_text += self._data.get("word_marks")[i] + "\n"

        if word_dict["deprecated"]:
            post_text += "Most likely it is a deprecated word" + "\n"

        if "referencies" in word_dict:
            if len(word_dict["referencies"]) > 0:
                post_text += "Referencies:\n"
                for ref in word_dict["referencies"]:
                    if len(post_text) < 300:
                        if "." in ref["source"]:
                            ref_text = ref["source"][:ref["source"].index(".")]
                        else:
                            ref_text = ref["source"]
                        post_text += "- " + ref_text
                        if "word" in ref:
                            post_text += ": \"" + ref["word"] + "\"\n"
                        else:
                            post_text += "\n"
            post_text += "\n"
            
        if "page" in word_dict:
            post_text += "https://eldamo.org/content/words/word-" + word_dict["page"] +".html"
             
        return post_text


    def find_random_word(self):
            
        if self._config.get("app.remote_calls"):
            word_dict, word_lang = self._proxy.find_random_word()
        
        else:
            words     = self._data.get("words")
            lang_dict = random.choice(list(words.values()))
            word_lang  = random.choice(list(lang_dict.keys()))
            word_aux  = lang_dict[word_lang]

            # en este punto tenemos una lista de acepciones o un diccionario 
            if isinstance(word_aux, list):
                word_dict = random.choice(word_aux) 
            else: 
                word_dict = word_aux

        return word_dict, word_lang


    def find_filtered_random_word(self, word_lang):

        if self._config.get("app.remote_calls"):
            word_dict = self._proxy.find_filtered_random_word(word_lang)

        else:
            words     = self._data.get("dictionaries")[word_lang]
            word_aux  = random.choice(list(words.values()))

            # en este punto tenemos una lista de acepciones o un diccionario 
            if isinstance(word_aux, list):
                word_dict = random.choice(word_aux) 
            else: 
                word_dict = word_aux

        return word_dict


    def find_word(self, word_query):
            
        found     = False
        lang_dict = None
        
        if self._config.get("app.remote_calls"):
            found, lang_dict = self._proxy.find_word(word_query)

        else:
            if word_query in self._data.get("words"):
                found    = True
                lang_dict = self._data.get("words")[word_query]

        return found, lang_dict


    def find_filtered_word(self, word_query, word_lang):
            
        found     = False
        word_list = [] 
        
        if self._config.get("app.remote_calls"):
            found, word_list = self._proxy.find_filtered_word(word_query, word_lang)

        else:
            words     = self._data.get("dictionaries")[word_lang]
            if word_query in words: 
                found    = True
                word_aux = words[word_query]
                # en este punto tenemos una lista de acepciones o un diccionario 
                if isinstance(word_aux, list):
                    word_list = word_aux 
                else: 
                    word_list.append(word_aux)

        return found, word_list


# main

if __name__ == '__main__':
    Bot().run()
