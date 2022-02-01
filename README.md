# language-identification-benchmark
Repo to test several language ID tools on several types of texts. See https://github.com/ec-doris/drivein-cdk/issues/269

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

## Data

- `kohesio` contains very small texts -- beneficiaries from Kohesio. We only find 2 beneficiaries in Maltese in Kohesio, so `mt` is not included in this collection. 
- Other corpora were downloaded from https://opus.nlpl.eu/

Data can be downloaded with `python download.py`, although it is included in the repo

## TODO

Proper evaluation pipeline