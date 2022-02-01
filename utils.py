import json
import os
import langid

################################### 
####  Language detection stuff ####
###################################
EU_LANGUAGES = ['bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'ga', 'hr',
                'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv']
langid.set_languages(EU_LANGUAGES)


import gcld3
detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)

from transliterate import detect_language

from whatthelang import WhatTheLang
wtl = WhatTheLang()

from langdetect import detect as lang_detect



################################### 
####  Language detection stuff ####
###################################
from urllib.request import urlopen
from urllib.error import HTTPError
from io import BytesIO
from zipfile import ZipFile

corpus_url = {
    "subs": "https://opus.nlpl.eu/download.php?f=OpenSubtitles/v1/moses/bg-€OTHERLANG€.txt.zip",
    "europarl": "https://opus.nlpl.eu/download.php?f=Europarl/v8/moses/bg-€OTHERLANG€.txt.zip",
    "eubooks": "https://opus.nlpl.eu/download.php?f=EUbookshop/v2/moses/bg-€OTHERLANG€.txt.zip",
    "wikimatrix": "https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/moses/bg-€OTHERLANG€.txt.zip",
    "emea": "https://opus.nlpl.eu/download.php?f=EMEA/v3/moses/bg-€OTHERLANG€.txt.zip"
}

def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

def OPUS_downloader(corpus, num_sentences = 100):
    # Basically we download LANG-LANG pairs but with BG as one
    # Then we parse everything to get a sample amount of sentences in each languages

    if corpus not in corpus_url.keys():
        sys.exit(f"### Error: {corpus} is not in {list(corpus_url.keys())}")

    print(f"### Downloading files for {corpus}")
    BASE_URL = corpus_url[corpus]
    output_dir = f"data/{corpus}"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for lang in EU_LANGUAGES:
        URL = BASE_URL.replace("€OTHERLANG€",lang)
        if lang != "bg":
            #print(URL)
            try:
                download_and_unzip(URL, output_dir)
            except HTTPError:
                print(f"Could not download {corpus} for language {lang}")

    dictionary = {}
    files = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file[-2:] in EU_LANGUAGES] 
    for lang in EU_LANGUAGES:
        try:
            file = [f for f in files if lang in f[-2:]][0] # we take whatever first ".lang" file
            with open(file) as f:
                sentences = [line.rstrip() for line in f][:num_sentences]

            dictionary[lang] = sentences
        except IndexError:
            continue
    
    with open(f"collections/{corpus}_texts.json", "w") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)




        