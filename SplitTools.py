# -*- coding:utf-8 -*-
import jieba.posseg as pseg
import codecs
import os
from Util import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getDefaultStopWordsFile():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')

class WordSegmentation(object):
    '''
    提取满足条件的分词结果，即是否去除停用词、是否去除指定词性的词语
    '''
    def __init__(self, stopWordsFile = None, allowSpeechTags = allow_speech_tags):
        '''
        :param stopWordsFile: 初始化时是否需要指定过滤停用词的文件名
        :param allowSpeechTags:指定需要保留的词性名称
        :return:
        '''
        allowSpeechTags = [as_text(item) for item in allowSpeechTags]

        self.defaultSpeechTagFilter = allowSpeechTags
        self.stopWords = set()
        self.stopWordsFile = getDefaultStopWordsFile()
        if type(stopWordsFile) is str:
            self.stopWordsFile = stopWordsFile
        for word in codecs.open(self.stopWordsFile, 'r', 'utf-8', 'ignore'):
            self.stopWords.add(word.strip())

    def segmentSentence(self,sentence , lower = True, useStopWords = True, useSpeechTagsFilter = False):
        sentence = as_text(sentence)
        # 利用jieba分词器按照词性来进行分词
        jiebaResult = pseg.cut(sentence)
        if useSpeechTagsFilter == True:
            jiebaResult = [w for w in jiebaResult if w.flag in self.defaultSpeechTagFilter]
        else:
            jiebaResult = [w for w in jiebaResult]
        # 去除特殊符号
        wordList = [w.word.strip() for w in jiebaResult if w.flag!='x']
        wordList = [word for word in wordList if len(word)>0]
        if lower:
            wordList = [word.lower() for word in wordList]
        if useStopWords:
            wordList = [word.strip() for word in wordList if word.strip() not in self.stopWords]
        return wordList

    def segmentSentences(self, sentences, lower=True, useStopWords=True, useSpeechTagsFilter=False):
        res = []
        for sentence in sentences:
            res.append(self.segmentSentence(sentence=sentence,
                                    lower=lower,
                                    useStopWords=useStopWords,
                                    useSpeechTagsFilter=useSpeechTagsFilter))
        return res


class SentenceSegmentation(object):
    '''
    将短文按照指定的分隔符进行分隔，返回List型结果
    '''
    def __init__(self, delimiters=delimiters):
        self.delimiters = set([as_text(item) for item in delimiters])
    def segment(self, text):
        res = [as_text(text)]
        for sep in self.delimiters:
            text, res = res, []
            for seq in text:
                res += seq.split(sep)
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res


class Segmentation(object):

    def __init__(self, stopWordsFile = None,
                    allow_speech_tags = allow_speech_tags,
                    delimiters = delimiters):
        self.ws = WordSegmentation(stopWordsFile=stopWordsFile, allowSpeechTags=allow_speech_tags)
        self.ss = SentenceSegmentation(delimiters=delimiters)

    def segment(self, text, lower = False):
        text = as_text(text)
        sentences = self.ss.segment(text)
        words_no_filter = self.ws.segmentSentences(sentences=sentences,
                                                    lower = lower,
                                                    useStopWords = False,
                                                    useSpeechTagsFilter = False)
        words_no_stop_words = self.ws.segmentSentences(sentences=sentences,
                                                    lower = lower,
                                                    useStopWords = True,
                                                    useSpeechTagsFilter = False)

        words_all_filters = self.ws.segmentSentences(sentences=sentences,
                                                    lower = lower,
                                                    useStopWords = True,
                                                    useSpeechTagsFilter = True)

        return AttrDict(
                    sentences           = sentences,
                    wordsNoFilter     = words_no_filter,
                    wordsNoStopWords = words_no_stop_words,
                    wordsAllFilters   = words_all_filters
                )