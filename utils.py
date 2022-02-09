import json
import os
import langid
import sys
import random

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
from langdetect.lang_detect_exception import LangDetectException

import subprocess
from iso639 import Lang
# taken from accompanying python code by Tommi Jauhiainen
# and adapted for ISO 639-3 to ISO 639-1 conv
# source: https://zenodo.org/record/5890998/
def run_heli(text):
    p = subprocess.run(['java', '-jar', 'HeLI.jar', '-c'], stdout=subprocess.PIPE, input=text, encoding='UTF-8')
    iso_639_3 = p.stdout.split("\t")[0]
    iso_639_1 = Lang(iso_639_3).pt1

    return iso_639_1

################################### 
####     Evaluation stuff      ####
###################################

def eval_on_texts(texts):
    results = {
    "Sentence": [],
    "Language": [],
    "langid": [],
    "glcd3": [],
    "transliterate": [],
    "whatthelang": [],
    "langdetect": [],
    "heli": [],
        }

    for lang, li in texts.items():
        
        for ph in li:
            results['Language'].append(lang)
            results['Sentence'].append(ph)
            
            
            guessed = langid.classify(ph)[0]
            if guessed == lang:
                results['langid'].append(True)
            else:
                results['langid'].append(False)

            guessed = detector.FindLanguage(text=ph).language        
            if guessed == lang:
                results['glcd3'].append(True)
            else:
                results['glcd3'].append(False)
            
            guessed = detect_language(ph)
            if guessed == lang:
                results['transliterate'].append(True)
            else:
                results['transliterate'].append(False)
            
            try:
            # There apparently is a prepro step
            # where they remove digits and punct
            # leaving absolutely nothing in some very small string
            # which then throws ValueError: Not enough text to predict language
                guessed = wtl.predict_lang(ph)     
                if guessed == lang:
                    results['whatthelang'].append(True)
                else:
                    results['whatthelang'].append(False)
            except ValueError:
                results['whatthelang'].append(False)
            
            try:
            # There apparently is a prepro step
            # where they remove digits and punct
            # leaving absolutely nothing in some very small string
            # which then throws langdetect.lang_detect_exception.LangDetectException: No features in text.
                guessed = lang_detect(ph)
                if guessed == lang:
                    results['langdetect'].append(True)
                else:
                    results['langdetect'].append(False)
            except LangDetectException:
                results['langdetect'].append(False) 

            
            guessed = run_heli(ph)        
            if guessed == lang:
                results['heli'].append(True)
            else:
                results['heli'].append(False)
            

    return results

################################### 
####  Downloading files  stuff ####
###################################
from urllib.request import urlopen
from urllib.error import HTTPError
from io import BytesIO
from zipfile import ZipFile
import pandas as pd

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
                sentences = [line.rstrip() for line in f]
                random.shuffle(sentences)
                sentences = sentences[:num_sentences]

            dictionary[lang] = sentences
        except IndexError:
            continue
    
    with open(f"collections/{corpus}_texts.json", "w") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


################################### 
####       Plotting stuff      ####
###################################

import plotly.graph_objects as go
from plotly.subplots import make_subplots

if not os.path.exists("results"):
    os.mkdir("results")

def plot_perf(df, cols, collection, not_tested, open_window=False):
    fig = make_subplots(rows=1, cols=5, subplot_titles=('langid', 'glcd3', 'transliterate', 'whatthelang', 'langdetect'), shared_yaxes="all")
    L= len(df)

    cnames = list(df.columns)
    for k, name in enumerate(cnames):
        n_true = df[name].sum()
        fig.add_trace(go.Bar(x=['True', 'False'], y=[n_true, L-n_true], name=name ), 1,k+1)
    fig.update_layout(barmode='relative',  bargap=0.05, width=1200, height=800,  title=f"Performance across all languages for corpus {collection}. Untested language(s): {not_tested}")
    
    if open_window:
        fig.write_html(f'results/perf_{collection}.html', auto_open=True)
    else:
        fig.write_html(f'results/perf_{collection}.html')#, auto_open=True)
