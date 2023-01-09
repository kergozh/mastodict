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
            
        word_lang = random.choice(list(data.get("dictionaries").keys()))
        logger.debug("word language : %s", word_lang)

        word_tuple = find_filtered_random_word(word_lang)

        return word_tuple, word_lang

    @server.register_function
    def find_filtered_random_word(word_lang):

        word_aux  = random.choice(list(data.get("dictionaries")[word_lang].values()))

        # en este punto tenemos una tuple de acepciones o una tuple-paraula  
        if isinstance(word_aux[0], tuple):
            word_tuple = random.choice(word_aux) 
        else: 
            word_tuple = word_aux

        return word_tuple

    @server.register_function
    def find_word(word_query):
            
        found     = False
        lang_dict = {}
        
        for word_lang in data.get("dictionaries").keys():

            logger.debug("word language : %s", word_lang)

            found_aux, word_tuple = find_filtered_word(word_query, word_lang)

            if found_aux:
                lang_dict[word_lang] = word_tuple
                found = found_aux

        #al xml-rpc no le gustan los objetos nulos
        if not found:
            lang_dict["error"] = "not found"

        return found, lang_dict


    @server.register_function
    def find_filtered_word(word_query, word_lang):
            
        found     = False
        
        if word_query in data.get("dictionaries")[word_lang]: 
            found    = True
            word_tuple = data.get("dictionaries")[word_lang][word_query]
            # en este punto tenemos una tuple de acepciones  

        if not found:
            word_tuple = ("error", "not found")

        return found, word_tuple


    @server.register_function
    def find_gloss(word_query):
            
        found      = False
        lang_dict  = {}
        
        if word_query in data.get("english"):
            found = True
            lang_dict = data.get("english")[word_query]
        else:
            lang_dict["error"] = "not found"

        return found, lang_dict

    @server.register_function
    def find_filtered_gloss(word_query, word_lang):
            
        found     = False
        
        if word_query in data.get("english"):
            if word_lang in data.get("english")[word_query]:
                found    = True
                word_tuple = data.get("english")[word_query][word_lang]
                # en este punto tenemos una tuple de acepciones  

        if not found:
            word_tuple = ("error", "not found")

        return found, word_tuple

    # Run the server's main loop
    server.serve_forever()

logger.info("end " + PGM_NAME)

