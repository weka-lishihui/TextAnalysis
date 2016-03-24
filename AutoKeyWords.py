# -*- coding:utf-8 -*-
import sys
from Util import *
from SplitTools import Segmentation
reload(sys)
sys.setdefaultencoding("utf-8")

class WordRank(object):
    def __init__(self, stopWordsFile = None,
                 allowSpeechTags = allow_speech_tags,
                 delimiters = delimiters):

        self.text = ''
        self.keywords = None

        self.seg = Segmentation(stopWordsFile=stopWordsFile,
                                allow_speech_tags=allowSpeechTags,
                                delimiters=delimiters)

        self.sentences = None
        self.wordsNoFilter = None     # 2维列表
        self.wordsNoStopWords = None
        self.wordsAllFilters = None

    def analyze(self, text,
                window = 2,
                lower = False,
                vertex_source = 'AllFilters',
                edge_source = 'NoStopWords',
                pagerank_config = {'alpha': 0.85,}):

        self.text = text
        self.word_index = {}
        self.index_word = {}
        self.keywords = []
        self.graph = None

        result = self.seg.segment(text=text, lower=lower)
        self.sentences = result.sentences
        self.wordsNoFilter = result.wordsNoFilter
        self.wordsNoStopWords = result.wordsNoStopWords
        self.wordsAllFilters   = result.wordsAllFilters

        options = ['NoFilter', 'NoStopWords', 'AllFilters']

        if vertex_source in options:
            _vertex_source = result['words'+vertex_source]
        else:
            _vertex_source = result['wordsAllFilters']

        if edge_source in options:
            _edge_source   = result['words'+edge_source]
        else:
            _edge_source   = result['wordsNoStopWords']

        self.keywords = sortWords(_vertex_source, _edge_source, window = window, pagerank_config = pagerank_config)

    def getKeywords(self, num = 6, word_min_len = 2):
        result = []
        count = 0
        for item in self.keywords:
            if count >= num:
                break
            if len(item.word) >= word_min_len:
                result.append(item)
                count += 1
        return result

    def getWordRank(self,num=5,word_min_len=2):
        result=self.getKeywords(num=num,word_min_len=word_min_len)
        temp=""
        for item in result:
            temp=temp+item.word+","
        return temp






    def get_keyphrases(self, keywords_num = 12, min_occur_num = 2):
        keywords_set = set([ item.word for item in self.get_keywords(num=keywords_num, word_min_len = 1)])
        keyphrases = set()
        for sentence in self.words_no_filter:
            one = []
            for word in sentence:
                if word in keywords_set:
                    one.append(word)
                else:
                    if len(one) >  1:
                        keyphrases.add(''.join(one))
                    if len(one) == 0:
                        continue
                    else:
                        one = []
            # 兜底
            if len(one) >  1:
                keyphrases.add(''.join(one))

        return [phrase for phrase in keyphrases
                if self.text.count(phrase) >= min_occur_num]