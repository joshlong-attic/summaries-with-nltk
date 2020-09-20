#!/usr/bin/env python


## todo it would be cool to use someting like newspaper3k to figure out the main
# body text for an article to help the process along
def get_article_text(url: str):
    import urllib.request
    try:
        return str(urllib.request.urlopen(url).read())
    except BaseException as e:
        print(e.__traceback__)


def summarize(article: str) -> str:
    import heapq
    import re

    import bs4 as bs
    import nltk

    import os

    nltk.download('stopwords')
    nltk.download('punkt')

    article = [a.strip() for a in article.split(os.linesep) if a.strip() != '']
    article = ['<P> %s </p> ' % a for a in article]
    article = os.linesep.join(article)

    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""

    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 0
            word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    top_ten_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)

    return ' '.join(top_ten_sentences)


if __name__ == '__main__':
    txt = get_article_text('https://www.infoq.com/news/2020/09/google-api-gateway/')
    print(summarize(txt))
