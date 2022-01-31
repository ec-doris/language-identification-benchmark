from utils import *
import sys
collections = ["kohesio", "normal"]

try:
    collection = sys.argv[1]
    if collection in collections:
        with open(f"collections/{collection}_texts.json") as f:
            texts = json.load(f)
    else:
        sys.exit(f"sys.argv[1] must be in {collections}")
except IndexError:
    sys.exit(f"Add from {collections} in sys.argv[1]")


scores = {}
scores["langid"] = []
scores["glcd3"] = []
scores["transliterate"] = []
scores["whatthelang"] = []


print(f"### We have data for {len(texts)} languages")

for lang, li in texts.items():
    correct = 0

    for ph in li:
        guessed = langid.classify(ph)[0]
        if guessed == lang:
            correct += 1
    scores["langid"].append(correct)
    

    correct = 0
    for ph in li:
        guessed = detector.FindLanguage(text=ph).language
        if guessed == lang:
            correct += 1
    scores["glcd3"].append(correct)

    correct = 0
    for ph in li:
        guessed = detect_language(ph)
        if guessed == lang:
                correct += 1
    scores["transliterate"].append(correct)


    correct = 0
    for ph in li:
        guessed = wtl.predict_lang(ph)
        if guessed == lang:
                correct += 1
    scores["whatthelang"].append(correct)


for tool in scores:
    avg = round(sum(scores[tool])/len(scores[tool]), 1)
    print(f"{tool}: average of  {avg} out of 5 across {len(texts)} langs, distrib: {scores[tool]} ")    


not_tested = set(EU_LANGUAGES) - set(texts.keys())
print(f'\n### Language(s) not tested: {not_tested}')