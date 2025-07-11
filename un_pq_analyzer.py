"""
filename: palestext.py
description: An extensible reusable library for text analysis and comparison of
country positions on palestine
"""

from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import random as rnd
import un_parsers as sp
import pprint as pp
from nltk.corpus import stopwords
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import json
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn
import pandas as pd
import matplotlib
from wordcloud import WordCloud
matplotlib.use('TkAgg')

class Sentiment:

    def __init__(self):
        # string  --> {filename/label --> statistics}
        # "wordcounts" --> {"A": wc_A, "B": wc_B, ....}
        self.data = defaultdict(dict)

    def _save_results(self, label, results):
        for key, value in results.items():
            self.data[key][label] = value

    @staticmethod
    def _default_parser(self, filename):
        f = open(filename)
        raw = json.load(f)
        text = raw['text']
        words = text.split(" ")
        wc = Counter(words)
        num = len(wc)
        f.close()
        return {'wordcount': wc, 'numwords':num}

    def load_stop_words(self):
        # remove stop words
        # load the stopwords
        with open("stopwords.txt", "r") as stopwords:
            lines = stopwords.readlines()
            # put the stopwords to a list
            stop_words_list = []
            # remove commas and \n s from the stopwords.txt file
            for l in lines:
                as_list = l.split(", ")
                stop_words_list.append(as_list[0].replace("\n", ""))
        # return the list (will be used in the parser
        return stop_words_list

    def load_text(self, filename, label=None, parser=None):
        """ Registers a text document with the framework
        Extracts and stores data to be used in later
        visualizations. """

        if parser is None:
            results = Sentiment._default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        # store the results of processing one file
        # in the internal state (data)
        self._save_results(label, results)

    def tester(self):
        # simply for testing purposes as I figure out the code
        # figuring out the links for the sankey diagram
        wordcount_test = self.data['wordcount']
        #print(wordcount_test)
        links = [{'source': key, 'target': item[0], 'value': item[1]} for key in wordcount_test for item in wordcount_test[key]]
        #print(links)
        # source - the filenames
        source = []
        # target - the words
        target = []
        # value - the count
        value = []
        paragraphs = self.data['paragraph']
        print(paragraphs)

        """
        for key, value in self.data['wordcount'].items():
            # key is the filenames/source
            source.append(key)
            print(value)
            for pairing in value:
                for key, item in pairing:
                    print(item)
        """










    def make_sankey_un(self, labels=None):
        """ make a sankey diagram for the entire compiled data"""
        wordcount = self.data['top5']

        # compile the data into lists that can be used to make the sankey
        nodes = list(set([item[0] for sublist in wordcount.values() for item in sublist] + list(wordcount.keys())))
        links = [{'source': key, 'target': item[0], 'value': item[1]} for key in wordcount for item in wordcount[key]]

        # Create the Sankey diagram
        sankey_un = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=nodes
            ),
            link=dict(
                source=[nodes.index(link['source']) for link in links],
                target=[nodes.index(link['target']) for link in links],
                value=[link['value'] for link in links]
            )
        )])
        return sankey_un.show()

    def un_wordcloud(self):
        """ create a wordcloud for every word in the speech """
        data = self.data['paragraph'].items()

        #these two lines of code (alphabetical and num rows) was generated by chatpgt
        # Sort keys alphabetically
        sorted_keys = sorted(self.data['paragraph'].keys())
        # Calculate the number of rows needed
        num_rows = len(sorted_keys) // 2 + len(sorted_keys) % 2

        # Create subplots for each key in the dictionary
        fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(15, 6 * num_rows))

        # Flatten the data and generate word cloud for each key
        for i, (key, text) in enumerate(data):
            #text = ' '.join([' '.join([word[0]] * word[1]) for word in values])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

            #adjusting the rows and columns to fit in a 2x5 pattern (comparing same nation with each other over time)
            row = i // 2
            col = i % 2

            # Plot word cloud in the corresponding subplot
            axes[row, col].imshow(wordcloud, interpolation='bilinear')
            axes[row, col].set_title(key, fontsize=16)
            axes[row, col].axis('off')

        plt.tight_layout()
        return plt.show()



    # calculating a sentiment score that will be used in other graphs
    def un_calc_sentiment(self):
        """ the majority of this process is written from ideas on this github page:
        https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/04-Sentiment-Analysis.html#:~:text=Calculate%20Sentiment%20Scores&text=polarity_scores()%20and%20input%20a,score%20between%20%2D1%2D1."""
        # init tool
        sia = SentimentIntensityAnalyzer()
        # create a dict for scores to go into
        sentiment_scores = {}

        # finding the sentiment for each
        for key, paragraph in self.data['paragraph'].items():
            # from the ntlk sentiment tool, apply for each word in the text
            sentiment = sia.polarity_scores(paragraph)
            sentiment_scores[key] = sentiment['compound']

        return sentiment_scores

    def sentiment_score_bar(self, sentiment_scores):
        """ plots the sentiment score of each document on one bar graph """


        keys = list(sentiment_scores.keys())
        values = list(sentiment_scores.values())

        # determining the colors
        # create a color list that chooses either green or red if the score is pos or neg
        color= []
        for rating in values:
            if rating >= 0:
                color.append('green')
            else:
                color.append('red')


        plt.bar(keys, values, color=color)
        plt.tick_params(rotation=30)
        plt.title('How Positively or Negatively Polarized are Countries on the Palestine Question?')
        plt.xlabel('Speech')
        plt.ylabel('Sentiment Score')
        plt.tight_layout()
        #plt.get_xticklabels(self.data['shortlabel'])
        plt.figure(figsize=(15, 10))

        return plt.show()


    # heatmap! cosine heatmap of differences in speeches
    # negativity or positivity scores?
    # the idea for a cosine heatmap is to see which speeches are similar in opinion

    # first, must establish the cosine similarity scores (that will be used to plot in the heatmap function)
    def calc_cosine_sim(self):
        """ calculates the cosine similarity matrix of the self.data """
        keys = list(self.data['wordcount'].keys())
        #print(keys)
        texts = [' '.join([word for word in values]) for values in self.data['wordcount'].values()]

        # this suggestion was found in a chatgpt search on building a cosine similarity matrix
        # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        #print(similarity_matrix)
        return similarity_matrix, keys


    def un_heatmap(self, similarity_matrix, keys):
        """ creates a heatmap of similarities between speeches using seaborn """
        # according to the sns.heatmap documentation, (https://seaborn.pydata.org/generated/seaborn.heatmap.html)
        # sns.heatmap takes in one data variable, must be a 2d dataset ie a pd.dataframe
        # set the dataframe from the data returned by the calc_cosine_sim funtion
        heat_df = pd.DataFrame(similarity_matrix, keys, columns=keys)

        # Plot the heatmap
        # set fig size
        plt.figure(figsize=(10, 8))
        # create the heatmap
        sns.heatmap(heat_df, annot=True, cmap='plasma', vmin=0, vmax=1)
        plt.tick_params(rotation=30)
        plt.title('Cosine Similarity Heatmap')
        plt.tight_layout()
        return plt.show()

