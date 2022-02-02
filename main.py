from utils import *
import sys
collections = [file.split("_")[0] for file in os.listdir("collections")]

print(f"### We have {len(collections)} collections available: {collections}")

try:
    collection = sys.argv[1]
    if collection in collections:
        with open(f"collections/{collection}_texts.json") as f:
            texts = json.load(f)
    else:
        sys.exit(f"sys.argv[1] must be in {collections}")
except IndexError:
    sys.exit(f"Add from {collections} in sys.argv[1]")


print(f"### For corpus {collection}, we have data for {len(texts)} languages")


results = eval_on_texts(texts)

df = pd.DataFrame.from_dict(results)
#print(df.head())
df.drop(["Sentence", 'Language'], axis=1, inplace=True)
#print(df.head())

not_tested = set(EU_LANGUAGES) - set(texts.keys())
print(f'\n### Language(s) not tested: {not_tested}')

cols = df.columns
plot_perf(df, cols, collection, not_tested)