import wikipedia as wiki
import wikipediaapi as wiki1
import pandas
import nltk
# nltk.download('stopwords')
import re
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
from nltk import tokenize
from sklearn.feature_extraction.text import TfidfTransformer
# nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer


def pre_process(summary):
    corpus = []

    # Creating a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))

    # Creating a list of custom stopwords
    new_words = ["using", "aired", "shows", "show", "season", "result", "actor", "large", "also", "iv", "one", "two",
                 "previously", "shown", "series", "award", "awards", "television", "starring", "critics", "among","received","critically"]
    stop_words = stop_words.union(new_words)

    for i in range(len(summary)):
        text = summary[i]
        # print(text)
        # lowercase
        text = text.lower()

        #     remove tags
        text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)

        ##Convert to list from string
        text = text.split()

        # Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in stop_words]
        text = " ".join(text)
        corpus.append(text)


    # print(doc)
    cv = CountVectorizer(max_df=0.85, stop_words=stop_words, max_features=10000)
    X = cv.fit_transform(corpus)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    # get feature names
    feature_names = cv.get_feature_names()

    # fetch document for which keywords needs to be extracted
    doc = corpus[-1]

    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))






    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)

    # now print the results
    print("\nAbstract:")
    print(doc)
    print("\nKeywords:")
    for k in keywords:
        print(k, keywords[k])

    # print(list(cv.vocabulary_.keys()))

    # print(summary)
    # print(" ==============")

    # print(summary)

    # freq = pandas.Series(summary.split()).value_counts()[:30]
    # print(freq)
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results
summary = []
def print_sections(sections, level=0):

    for s in sections:
        # print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
        if s.text:
            # print(s.title," TEXT ====  ",s.text[:40])
            summary.append(s.text)
        print_sections(s.sections, level + 1)
    return summary

def main():
    # print(wiki.search("breaking bad show"))

    # keywordList = wiki.search("new girl show")
    keywordList = wiki.search("breaking bad show")
    wiki_wiki = wiki1.Wikipedia('en')
    page = wiki_wiki.page(keywordList[0])
    print("name of the page = ", keywordList[0])
    # print(page.sections)
    # summary = wiki.page(keywordList[0]).content
    summary = print_sections(page.sections)

    summary.append(wiki.summary(keywordList[0]))

    # print(len(summary))
    # for i in summary:
    #     print(i)
    #     print(" =========== end ================== ")
    # summary = wiki.summary(keywordList[0])
    # summary = "these Breaking Bad is  an American neo-Western crime drama television series created and produced by Vince Gilligan. " \
    #           "The show originally aired on AMC for five seasons, from January 20, 2008, to September 29, 2013. Set and filmed in Albuquerque, New Mexico, the series tells the story of Walter White (Bryan Cranston), a struggling and depressed high school chemistry teacher who is diagnosed with stage-3 lung cancer. " \
    #           "Together with his former student Jesse Pinkman (Aaron Paul), White turns to a life of crime by producing and selling crystallized methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld. " \
    #           "The title comes from the Southern colloquialism breaking bad which means to raise hell or turn to a life of crime. " \
    #           "Gilligan characterized the series as showing Walter's transformation from a soft-spoken Mr. Chips into Scarface." \
    #           " Among the shows co-stars are Anna Gunn and RJ Mitte as Walter's wife Skyler and son Walter, Jr., and Betsy Brandt and Dean Norris as Skyler's sister Marie Schrader and her husband Hank, a DEA agent. " \
    #           "Others include Bob Odenkirk as the sleazy lawyer Saul Goodman, Jonathan Banks as private investigator and fixer Mike Ehrmantraut, and Giancarlo Esposito as the drug kingpin Gus Fring. " \
    #           "The final season introduces Jesse Plemons as the criminally-ambitious Todd Alquist, and Laura Fraser as Lydia Rodarte-Quayle, a business executive secretly managing Walter's global meth sales for her company." \
    #           " Breaking Bad is widely regarded as one of the greatest television series of all time. By the time the series finale aired, it was among the most-watched cable shows on American television. " \
    #           "The show received numerous awards, including 16 Primetime Emmy Awards, eight Satellite Awards, two Golden Globe Awards, two Peabody Awards, two Critics' Choice Awards and four Television Critics Association Awards. " \
    #           "For his leading performance, Cranston won the Primetime Emmy Award for Outstanding Lead Actor in a Drama Series four times, while Aaron Paul won the Primetime Emmy Award for Outstanding Supporting Actor in a Drama Series three times; Anna Gunn won the Primetime Emmy Award for Outstanding Supporting Actress in a Drama Series twice. In 2013, Breaking Bad entered the Guinness World Records as the most critically acclaimed show of all time. A spin-off prequel series, Better Call Saul, starring Bob Odenkirk and Jonathan Banks, debuted on February 8, 2015, on AMC. A sequel film, El Camino: A Breaking Bad Movie, starring Aaron Paul will be released on Netflix on October 11, 2019."

    # count of all words
    # freq = pandas.Series(summary.split()).value_counts()[:30]
    # print(freq)


    # sentences = []
    # sentences = tokenize.sent_tokenize(summary)
    pre_process(summary)

    # print(corpus)




if __name__ =='__main__':
    main()



    # print(wiki.search("new girl"))
    # print(wiki.search("breaking bad show"))

    # keywordList = wiki.search("breaking bad show")
    # print("name of the page = ",keywordList[0])
    # summary = wiki.summary(keywordList[0])
    # print(summary)

# print(wiki.search("limitless movie"))
# print(wiki.search("limitless show"))
# print(wiki.suggest("limitless"))
# print(wiki.search("Bill cliton"))
# print(wiki.suggest("Bill cliton"))

# Abstract:
# breaking bad american neo western crime drama created produced vince gilligan
#
# Keywords:
# created 0.338
# vince 0.338
# western 0.338
# neo 0.338
# produced 0.338
