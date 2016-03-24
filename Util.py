# -*- coding:utf-8 -*-
import networkx as nx
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 设置短文中的分隔符
delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']

# 利用词性标记来进行筛选
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']

text_type = unicode
string_types = (str, unicode)

def as_text(v):
    '''
    :param v: 输入需要进行编码转换的文本字符串
    :return:如果是unicode字符则直接返回，str类型则转换成UTF-8型的编码
    '''
    '''
    :param v:
    :return:
    '''
    if v is None:
        return None
    elif isinstance(v, unicode):
        return v
    elif isinstance(v, str):
        return v.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Invalid type %r' % type(v))

def is_text(v):
    '''
    :param v:
    :return:判断是否unicode字符串
    '''
    return isinstance(v, text_type)

def combine(wordList, window = 2):
    '''
    :param wordList: 单词列表
    :param window: 计算window个单词为一组，并安排每个单词的排列组合
    :return:返回每个两个词组成的元组
    '''
    if window < 2:
        window = 2
    for x in xrange(1, window):
        if x >= len(wordList):
            break
        wordList2 = wordList[x:]
        res = zip(wordList, wordList2)
        for r in res:
            yield r

def getSimilarity(wordList1, wordList2):
    '''
    参考TF-IDF中的定义来计算两个句子之间的相似度
    :param wordList1:
    :param wordList2:
    :return:
    '''
    words   = list(set(wordList1 + wordList2))
    x = [float(wordList1.count(word)) for word in words]
    y = [float(wordList2.count(word)) for word in words]

    x=np.array(x)
    y=np.array(y)

    Lx=np.sqrt(x.dot(x))
    Ly=np.sqrt(y.dot(y))

    return abs(x.dot(y) /(Lx*Ly))

class AttrDict(dict):
    '''
    创建满足自己要求的字典
    '''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def sortWords(vertex_source, edge_source, window = 2, pagerank_config = {'alpha': 0.85,}):
    '''
    :param vertex_source: 表示用于计算图中节点的数据源（并且按照出现的顺序来记录位置）
    :param edge_source: 表示用于计算图中边的权重
    :param window: 在计算边的时候设置的窗口长度，及多少个词可以在一组进行排列组合
    :param pagerank_config: 设置默认的阻尼系数
    :return:返回每个单词的得分权重和单词内容，类型为List但是元素为新定义的字典
    '''
    sortedWords   = []
    wordIndex     = {} #用于记录词第一次出现的位置
    indexWord     = {}#用于表示在某个位置上存储的具体是哪一个词
    _vertexSource = vertex_source
    _edgeSource   = edge_source
    wordsNum   = 0   #用于记录所构成的有向图中的节点的个数
    for wordLlist in _vertexSource:
        for word in wordLlist:
            if not word in wordIndex:
                wordIndex[word] = wordsNum
                indexWord[wordsNum] = word
                wordsNum += 1

    # 生成一个元素为0的方阵，阶数为词的个数
    graph = np.zeros((wordsNum, wordsNum))

    for wordList in _edgeSource:
        for w1, w2 in combine(wordList, window):
            if w1 in wordIndex and w2 in wordIndex:
                index1 = wordIndex[w1]
                index2 = wordIndex[w2]
                graph[index1][index2] = 1.0
                graph[index2][index1] = 1.0

    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, **pagerank_config)          # this is a dict
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)
    for index, score in sorted_scores:
        item = AttrDict(word=indexWord[index], weight=score)
        sortedWords.append(item)

    return sortedWords


def sortSentences(sentences, words, sim_func = getSimilarity, pagerank_config = {'alpha': 0.85,}):
    '''
    :param sentences: 用于计算权重的句子列表
    :param words: 与sentences相对应的每个句子的单词列表，该参数的类型为二维列表
    :param sim_func: 用于计算句子相似度的函数名
    :param pagerank_config:
    :return:
    '''
    sortedSentences = []
    _source = words
    sentencesNum = len(_source)   #获得图的大小
    graph = np.zeros((sentencesNum, sentencesNum))

    for x in xrange(sentencesNum):
        for y in xrange(x, sentencesNum):
            similarity = sim_func( _source[x], _source[y] )
            graph[x, y] = similarity
            graph[y, x] = similarity

    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, **pagerank_config)              # this is a dict
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)

    for index, score in sorted_scores:
        item = AttrDict(sentence=sentences[index], weight=score)
        sortedSentences.append(item)

    return sortedSentences
