""" 
Dictionaries server
"""

import random
from xmlrpc.server import SimpleXMLRPCServer

from pybot.config import Config
from pybot.logger import Logger

PGM_NAME = "Lambeserver"


config     = Config("confserver.yaml")
logger     = Logger(config).getLogger()

logger.info("init " + PGM_NAME)

data       = Config(config.get("app.data_file_name"))

logger.info("ready " + PGM_NAME)

with SimpleXMLRPCServer(('localhost', 8002), logRequests=True, allow_none=True) as server:

    server.register_introspection_functions()

    @server.register_function
    def find_random_word():
            
        words     = data.get("words")
        lang_dict = random.choice(list(words.values()))
        word_lang = random.choice(list(lang_dict.keys()))
        word_aux  = lang_dict[word_lang]

        # en este punto tenemos una lista de acepciones o un diccionario 
        if isinstance(word_aux, list):
            word_dict = random.choice(word_aux) 
        else: 
            word_dict = word_aux

        return word_dict, word_lang


    @server.register_function
    def find_filtered_random_word(word_lang):
            
        words     = data.get("dictionaries")[word_lang]
        word_aux  = random.choice(list(words.values()))

        # en este punto tenemos una lista de acepciones o un diccionario 
        if isinstance(word_aux, list):
            word_dict = random.choice(word_aux) 
        else: 
            word_dict = word_aux

        return word_dict

    @server.register_function
    def find_word(word_query):
            
        found     = False
        lang_dict = {}
        
        if word_query in data.get("words"):
            found    = True
            lang_dict = data.get("words")[word_query]

        return found, lang_dict

    @server.register_function
    def find_filtered_word(word_query, word_lang):
            
        found     = False
        word_list = [] 
        
        words     = data.get("dictionaries")[word_lang]
        if word_query in words: 
            found    = True
            word_aux = words[word_query]
            # en este punto tenemos una lista de acepciones o un diccionario 
            if isinstance(word_aux, list):
                word_list = word_aux 
            else: 
                word_list.append(word_aux)

        return found, word_list

    # Run the server's main loop
    server.serve_forever()

logger.info("end " + PGM_NAME)

