###
# Mastosdict, bot que gestiona uno o más diccionarios. 
# Publica una palabra aleatoria una vez l dia y responde a diferentes kewwords
# Fork (cada vez más lejano) del bot "info" original de @spla@mastodont.cat
# En https://git.mastodont.cat/spla/info
###  

from mastobot import Mastobot
from pybot.programmer import Programmer
from pybot.config import Config
from pybot.translator import Translator
from pybot.logger import Logger

import random
import datetime

BOT_NAME = "Lambebot"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)

        self.init_replay_bot()
        self.init_publish_bot()
        self.init_translator()
        self.init_programmer()


    def run(self, botname: str = BOT_NAME) -> None:

        action   = self._actions["post"]   
        if self.check_programmer(action["hours"], True):

            for i in range(29):
                word, language = self.find_random_word(self._actions["data"]["dictionaries"])
                print ("word: " + word["word"])

            #self.post_toot (self.find_text(None, word), "en", 0)
     
        #action   = self._actions["replay_status"]   
        #notifications = self.mastodon.notifications()
        #for notif in notifications:
        #    replay, dismiss = self.process_notif(notif, "mention", action["keyword"])
        #    if replay:
        #        self.replay_toot(self.find_text(notif, action), notif)
        #    if dismiss:
        #        self.mastodon.notifications_dismiss(notif.id)

        super().run(botname = botname)


    def find_random_word(self, dictionaries):

        language   = random.choice(list(dictionaries.keys()))
        dictionary = dictionaries[language] 
        word_list  = random.choice(list(dictionary.values()))

        # en este punto tenemos un diccionario con un lenguage y un valor
        if isinstance(word_list, list):
            word = random.choice(word_list) 
        else: 
            word = word_list

        return word, language


    def find_text(self, notif, word):        

        self._logger.debug("notif language: " + language)                    

        if notif == None:
            language = "en" 
            post_text  = ""
        else:
            language = notif.status.language
            post_text  = "@" + notif.account.acct + ":\n\n"
                
        self._translator.fix_language (language)
        _text     = self._translator.get_text
        
        print ("word: " + word )


        #post_text += _text("registrados") + ": " + registers + "\n"
        #post_text += _text("activos") + ": " + mau + "\n"
        # post_text = (post_text[:400] + '... ') if len(post_text) > 400 else post_text

        self._logger.debug ("answer text\n" + post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
