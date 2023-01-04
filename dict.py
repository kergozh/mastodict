###
# Mastosdict, bot que gestiona uno o más diccionarios. 
# Publica una palabra aleatoria una vez l dia y responde a diferentes kewwords
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

import random
import re

from mastobot import Mastobot

BOT_NAME = "Lambebot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_publish_bot()
        self.init_translator()
        self.init_programmer()
        self.init_input_data()


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
                    self.replay_toot (self.find_search_text(notif), notif)

                elif re.search(self._actions.get("filtered_random.regex"), content) != None:
                    self.replay_toot (self.find_filtered_random_text(notif), notif)

                elif re.search(self._actions.get("filtered_search.regex"), content) != None:
                    self.replay_toot (self.find_filtered_search_text(notif), notif)
    
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

        return post_texts


    def find_languages_text(self, notif):
            
        post_texts = []    
        language  = notif.status.language

        self._logger.debug("notif language: %s", language)

        self._translator.fix_language (language)
        _text     = self._translator.get_text

        post_text = "@" + notif.account.acct + ":\n\n" 

        for lang in self._data.get("languages"):
            post_text += _text("idioma") + ": " + self._data.get("languages")[lang] + ", " + _text("codi") + ": " + lang + "\n" 
            
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)

        return post_texts


    def find_random_text(self, notif):

        post_texts = []    
        word_dict, language = self.find_random_word()

        if notif == None:
            post_text = ""        
        else:
            post_text  = "@" + notif.account.acct + ":\n\n" 
        
        post_text += "\"" + word_dict["mark"] + word_dict["word"] + "\", "
        post_text += self._data.get("languages")[language] + " " + word_dict["grammar"] + "\n"
        post_text += "\"" + word_dict["gloss"] + "\""
        if word_dict["category"] != "":
            post_text += " (category: " +  self._data.get("word_categories")[word_dict["category"]]  + ")"
        post_text += "\n\n"

        for i in word_dict["mark"]:
            post_text += self._data.get("word_marks")[i] + "\n"

        if word_dict["deprecated"]:
            post_text += "Most likely it is a deprecated word" + "\n"

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
        
        if "page" in word_dict:
            post_text += "\nhttps://eldamo.org/content/words/word-" + word_dict["page"] +".html"
             
        post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text
        self._logger.debug ("answer text\n" + post_text)
        post_texts.append(post_text)
        
        return post_texts


    def find_random_word(self):
            
        words     = self._data.get("words")
        lang_aux  = random.choice(list(words.values()))

        # en este punto tenemos una lista de lenguajes o un diccionario 
        if isinstance(lang_aux, list):
            lang_dict = random.choice(lang_aux) 
        else: 
            lang_dict = lang_aux

        language = random.choice(list(lang_dict.keys()))
        word_aux = lang_dict[language]

        # en este punto tenemos una lista de lenguajes o un diccionario 
        if isinstance(word_aux, list):
            word_dict = random.choice(word_aux) 
        else: 
            word_dict = word_aux

        return word_dict, language

# main

if __name__ == '__main__':
    Bot().run()
