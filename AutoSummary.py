# -*- coding:utf-8 -*-
from SplitTools import Segmentation
from Util import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SentenceRank(object):

    def __init__(self, stop_words_file = None,
                 allowSpeechTags = allow_speech_tags,
                 delimiters = delimiters):

        self.seg = Segmentation(stopWordsFile=stop_words_file,
                                allow_speech_tags=allowSpeechTags,
                                delimiters=delimiters)

        self.sentences = None
        self.wordsNoFilter = None     # 2维列表
        self.wordsNoStopWords = None
        self.wordsAllFilters = None

        self.key_sentences = None

    def analyze(self, text, lower = False,
              source = 'NoStopWords',
              sim_func = getSimilarity,
              pagerank_config = {'alpha': 0.85,}):

        self.key_sentences = []

        result = self.seg.segment(text=text, lower=lower)
        self.sentences = result.sentences
        self.wordsNoFilter = result.wordsNoFilter
        self.wordsNoStopWords = result.wordsNoStopWords
        self.wordsAllFilters   = result.wordsAllFilters

        options = ['NoFilter', 'NoStopWords', 'AllFilters']
        if source in options:
            _source = result['words'+source]
        else:
            _source = result['wordsNoFilter']

        self.key_sentences = sortSentences(sentences = self.sentences,
                                                 words     = _source,
                                                 sim_func  = sim_func,
                                                 pagerank_config = pagerank_config)

    def getKeySentences(self, num = 6, sentence_min_len = 6):
        result = []
        count = 0
        for item in self.key_sentences:
            if count >= num:
                break
            if len(item['sentence']) >= sentence_min_len:
                result.append(item)
                count += 1
        return result

    def getSummary(self,num=5,sentence_min_len = 8):
        result=self.getKeySentences(num=num,sentence_min_len=sentence_min_len)
        temp=""
        for item in result:
            temp=temp+item.sentence+"。"
        return temp