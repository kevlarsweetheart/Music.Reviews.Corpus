from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from nltk.stem import WordNetLemmatizer
from copy import deepcopy
from whoosh.analysis import Composable, Filter, StopFilter, RegexTokenizer, LowercaseFilter
from whoosh.searching import Hit

class LemmaFilter(Filter):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, tokens):
        for token in tokens:
            lemma = self.lemmatizer.lemmatize(token.text)
            lemma_token = deepcopy(token)
            lemma_token.text = lemma
            yield token
            yield lemma_token

index = open_dir("../Index")

print("Type your search request")
request = input()

fields = set()
terms = request.split()
for term in terms:
    if ':' in term:
        fields.add(term.split(':')[0])
if not bool(fields):
    fields.add('text')

searcher = index.searcher()
qp = MultifieldParser(list(fields), schema=index.schema)
q = qp.parse(request)

with searcher as s:
    results = s.search(q, limit=None, terms=True)
    for i, item in enumerate(results):
        print('Terms', ' '.join(map(str, item.matched_terms())), 'were found in text', item.values()[0])
        if i > 19:
            break