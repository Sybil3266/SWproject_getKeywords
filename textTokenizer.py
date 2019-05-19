from soynlp.utils import DoublespaceLineCorpus
import time
from soynlp.tokenizer import LTokenizer

import re
import sys
from soynlp.noun import LRNounExtractor_v2
from gensim.models import Word2Vec

from soynlp.normalizer import *
from soynlp.vectorizer import *
from soykeyword.lasso import LassoKeywordExtractor

start_time = time.time()
        
fp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\CrawlingData_pebble.txt", "r", encoding = "utf-8")

corpus_path = "C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\CrawlingData_pebble.txt"
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

for noun in nouns:
    nounScore[noun] = nouns[noun].score
    dictionary[noun] = index
    index += 1

del index

nounData = list(dictionary.keys())


'''
writefp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\WordScore_pebble.txt", "w", encoding = "utf-8")


writefp.write(str(nounScore))
writefp.close()
'''
    

tokenizer = LTokenizer(scores = nounScore)
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

#sents.iter_sent = False
#x = vectorizer.fit_transform(sents)

#lassobased_extractor = LassoKeywordExtractor(min_tf=1, min_df=1)
#lassobased_extractor.train(x, nounData) # x: sparse matrix, index2word가 뭐지?

'''
tokenfp = open("C:\\users\\user\Desktop\SWProject\SWproject_getKeywords\Tokenized_Labeled_Data_pebble.txt","w", encoding = "utf-8")

for i in tokenized_text:
    if len(i) == 0 or i == '\',' or i == '\'':
        continue
    i = '__label__' + i + ' '
    tokenfp.write(str(i))

tokenfp.close()
'''        

'''
word_extractor = WordExtractor(
     min_frequency=30,
#    min_cohesion_forward=0.05, 
#    min_right_branching_entropy=0.0
)
word_extractor.train(text) # list of str or like
words = word_extractor.extract()
#print(words)
'''
#embedding_model = Word2Vec(tokenized_text, size = 10, window = 2, min_count = 10, workers = 4, iter = 100, sg = 1)
#print(embedding_model.most_similar(positive=["라스타칸"], topn=100))


print("time : %s second" %(time.time() - start_time))
