from collections import Counter
from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
from wordcloud import wordcloud
import matplotlib.pyplot as plt


def counter():
    readData = open("C:\\users\\user\Downloads\크롤링Data_돌마갤.txt", 'r', encoding = 'utf8').read()
    okt = Okt()
    keywordNoun = okt.nouns(readData)
    cnt = Counter(keywordNoun)
    top = cnt.most_common(50)   
    print(top)
    return top

def main():
    top = counter()
    wordcloud = WordCloud().generate(top)
    plt.figure(figsize = (12,12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
     
