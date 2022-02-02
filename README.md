# language-identification-benchmark
Repo to test several language ID tools on several types of texts. See https://github.com/ec-doris/drivein-cdk/issues/269.

SOTA and survey for language identification is available in these [PhD thesis](https://helda.helsinki.fi/handle/10138/301459) and [survey paper](https://doi.org/10.1613/jair.1.11675).

## Current tools

- langid.py, https://aclanthology.org/P12-3005/ **\*currently in drive-in\***
- glcd3, https://github.com/google/cld3 latest google thingy
- transliterate, https://github.com/barseghyanartur/transliterate only works on some non-Latin scripts
- whatthelang, https://github.com/indix/whatthelang
- langdetect, https://github.com/Mimino666/langdetect earlier google thingy

Not considered for now:

- whatlang, because in rust (https://github.com/greyblake/whatlang-rs)
- YALI, because in perl (https://github.com/martin-majlis/YALI)
- LDIG, because only 17 languages (https://github.com/shuyo/ldigpip)

## Use
`python main.py $COLLECTION`

where `$COLLECTION` is currently `kohesio`, `emea`, `eubooks`, `europarl`, `subs`, `wikimatrix`

Results will be plotted in `results`

## Data

- `kohesio` contains very small texts -- beneficiaries from [Kohesio](https://kohesio.eu/). We only find 2 beneficiaries in Maltese in Kohesio, so `mt` is not included in this collection. Only 5 texts are included for any language in `kohesio`.
- Other corpora were downloaded from Jörg Tiedemann's https://opus.nlpl.eu/ :
    - `subs` is OpenSubtitles: https://opus.nlpl.eu/OpenSubtitles-v2018.php, with permission from http://www.opensubtitles.org/ 
    - `eubooks` is EUbookshop: https://opus.nlpl.eu/EUbookshop.php
    - `europarl` is Europarl: https://opus.nlpl.eu/Europarl.php
    - `emea` is EMEA: https://opus.nlpl.eu/EMEA.php
    - `wikimatrix` is WikiMatrix: https://opus.nlpl.eu/WikiMatrix.php

Data can be downloaded with `python download.py`, although it is included in the repo. The script will shuffle sentences so results will probably vary. 

## References

- J. Tiedemann, 2012, _[Parallel Data, Tools and Interfaces in OPUS](http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf)_. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)
- Holger Schwenk, Vishrav Chaudhary, Shuo Sun, Hongyu Gong and Paco Guzman, [WikiMatrix: Mining 135M Parallel Sentences in 1620 Language Pairs from Wikipedia](https://arxiv.org/abs/1907.05791), arXiv, July 11 2019.
- Jauhiainen, T., Lui, M., Zampieri, M., Baldwin, T. and Lindén, K., 2019. [Automatic language identification in texts: A survey.](https://doi.org/10.1613/jair.1.11675) Journal of Artificial Intelligence Research, 65, pp.675-782.
- Tommi Jauhiainen. 2019. [Language identification in texts.](https://helda.helsinki.fi/handle/10138/301459) Ph.D. thesis, University of Helsinki, Finland.