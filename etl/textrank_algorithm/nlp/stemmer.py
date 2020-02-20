# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import nltk.stem.snowball as nltk_stemmers_module

class Stemmer(object):

    def __init__(self, language):
        stemmer_classname = language.capitalize() + 'Stemmer'
        try:
            stemmer_class = getattr(nltk_stemmers_module, stemmer_classname)
        except AttributeError:
            raise LookupError("Stemmer is not available for language %s." % language)
        self._stemmer = stemmer_class().stem

    def __call__(self, word):
        return self._stemmer(word)
