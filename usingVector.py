from soynlp.utils import DoublespaceLineCorpus
from soynlp.tokenizer import LTokenizer
from soynlp.noun import LRNounExtractor_v2
from soykeyword.lasso import LassoKeywordExtractor
import time
from scipy.sparse import csr_matrix

start_time = time.time()


def my_read(path):
    with open(path) as f:
        # skip head
        for _ in range(3):
            next(f)
        rows = []
        cols = []
        data = []
        for line in f:
            elements = line.split()
            i = int(elements[0])
            j = int(elements[1])
            d = float(elements[2])
            rows.append(i)
            cols.append(j)
            data.append(d)
    return csr_matrix((data, (rows, cols)))


fp = open("C:\\Users\sybil\OneDrive\Documents\GitHub\SWproject_getKeywords\hsinvennews.txt", "r", encoding="utf-8")

corpus_path = "C:\\Users\sybil\OneDrive\Documents\GitHub\SWproject_getKeywords\hsinvennews.txt"
sents = DoublespaceLineCorpus(corpus_path, iter_sent=True)

text = []
while True:
    line = fp.readline()
    if not line: break
    text.append(line)

fp.close()
text = str(text)

noun_extractor = LRNounExtractor_v2(verbose=True, extract_compound=True)
nouns = noun_extractor.train_extract(sents)
nounScore = {}
dictionary = {}
index = 0

for noun in nouns:
    nounScore[noun] = nouns[noun].score
    dictionary[noun] = index
    index += 1

del index

nounData = list(dictionary.keys())

tokenizer = LTokenizer(scores=nounScore)
tokenized_text = tokenizer.tokenize(text)

vector_path = "./vectorizedHSInvenNews.mtx"
vec = my_read(vector_path)

lassobased_extractor = LassoKeywordExtractor(min_tf=1, min_df=1)
lassobased_extractor.train(vec, nounData) # vec: sparse matrix, index2word가 뭐지?

print("time : %s second" %(time.time() - start_time))