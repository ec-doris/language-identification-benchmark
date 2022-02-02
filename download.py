from utils import *

for corpus in corpus_url.keys():
    if not os.path.exists(f"collections/{corpus}_texts.json"):
        OPUS_downloader(corpus)
        print()

#OPUS_downloader("subs")