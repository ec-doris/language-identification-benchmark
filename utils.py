import json

import langid
EU_LANGUAGES = ['bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr',
                'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv']
langid.set_languages(EU_LANGUAGES)


import gcld3
detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)

from transliterate import detect_language

from whatthelang import WhatTheLang
wtl = WhatTheLang()

from langdetect import detect as lang_detect

