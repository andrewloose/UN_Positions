from un_pq_analyzer import Sentiment
import pprint as pp
import un_parsers as sp

def main():
    # load the analyzer for un resolutions
    un = Sentiment()
    res_files_test = {'S_RES_1478(2003).json', 'S_RES_1553(2004).json'}
    pq_files = {'BrazilPQ2013.json', 'ChinaPQ2013.json', 'MoroccoPQ2013.json', 'RussiaPQ2013.json', 'USAPQ2013.json',
                'BrazilPQ2023.json', 'ChinaPQ2023.json', 'MoroccoPQ2023.json', 'RussiaPQ2023.json', 'USAPQ2023.json'}
    for file in pq_files:
        un.load_text(file, parser=sp.json_parser)

    # test function
    #un.tester()

    # prints the data output
    #pp.pprint(un.data)


    # sankey diagram top 5 words each file viz1
    #un.make_sankey_un()

    # wordcloud subplots graph
    un.un_wordcloud()

    # sentiment score bar graph viz2
    #scores = un.un_calc_sentiment()
    #un.sentiment_score_bar(scores)

    # heatmap viz 3
    #matrix, keys = un.calc_cosine_sim()
    #un.un_heatmap(matrix, keys)

if __name__ == '__main__':
    main()