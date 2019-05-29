from soynlp.utils import DoublespaceLineCorpus
from soynlp.tokenizer import LTokenizer
from soynlp.noun import LRNounExtractor_v2
from soykeyword.lasso import LassoKeywordExtractor
import time
from soynlp.vectorizer import *
from soynlp.normalizer import *
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
text = only_hangle_number(text)
text = emoticon_normalize(text, num_repeats = 3)
text = repeat_normalize(text, num_repeats = 3)

noun_extractor = LRNounExtractor_v2(verbose=True, extract_compound=True)
nouns = noun_extractor.train_extract(sents)
nounScore = {}
dictionary = {}
index = 0
idx2word = {}
for noun in nouns:
    nounScore[noun] = nouns[noun].score
    dictionary[noun] = index
    idx2word[index] = noun
    index += 1

del index


nounData = list(dictionary.keys())

tokenizer = LTokenizer(scores=nounScore)
tokenized_text = tokenizer.tokenize(text)

vectorizer = BaseVectorizer(
    tokenizer=tokenizer,
    min_tf=0,
    max_tf=10000,
    min_df=0,
    max_df=1.0,
    stopwords=None,
    lowercase=True,
    verbose=True
)


vector_path = "./vectorizedPebble.mtx"
vec = my_read(vector_path)

from sklearn.feature_extraction.text import CountVectorizer
vectorizer2 = CountVectorizer(min_df=0.001)
x = vectorizer.fit_transform(tokenized_text)
print(x.shape)

w2i = vectorizer.vocabulary_
index2word = sorted(
    vectorizer.vocabulary_,
    key=lambda x:vectorizer.vocabulary_[x]
)
'''
벡터부분 코드. 
vectorizer = BaseVectorizer(
    tokenizer=tokenizer,
    min_tf=0,
    max_tf=10000,
    min_df=0,
    max_df=1.0,
    stopwords=None,
    lowercase=True,
    verbose=True
)

sents.iter_sent = False
#x = vectorizer.fit_transform(sents)
import tensorflow as tf


vectorPath = "./vectorizedHSInvenNews.txt"
with tf.device('/gpu:0'):
    vectorizer.fit_to_file(sents, vectorPath)
    
'''
lassobased_extractor = LassoKeywordExtractor(min_tf=1, min_df=1)
#train 대상을 vec으로 하면 문제없음, x와의 차이가 뭐지? corpus인거 아닌거 차이?
lassobased_extractor.train(vec) # vec: sparse matrix, index2word가 뭐지?

print("extractor load completed")
print("time : %s second" %(time.time() - start_time))

testkeyword = '가로쉬'
#idx자체에서 찾는것은 문제 x, docs에서 사용되는 index2word자체가 문제인듯
#x로 학습된 벡터에서도 오류가 남.
kwindex = w2i[testkeyword]
keywords = lassobased_extractor.extract_from_word(kwindex, min_num_of_keywords=50)
for i in keywords[:10]:
    print("관련 단어 : " + index2word[i.word] + " // 등장 횟수 : " + str(i.frequency) + " // 유사도 : " + str(i.coefficient))