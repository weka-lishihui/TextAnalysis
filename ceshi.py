# -*- coding:utf-8 -*-
import sys
from AutoSummary import SentenceRank
from AutoKeyWords import WordRank
reload(sys)
sys.setdefaultencoding('utf-8')


# 提取短文的关键词
text=(open('../jianzhu.txt','r').read())
wr = WordRank()
wr.analyze(text=text)
print wr.getWordRank(num=8)

'''
# 提取短文的摘要
sr = SentenceRank()
sr.analyze(text=text, lower=True, source = 'AllFilters')
print 'Summ：'
# for item in sr.getKeySentences(num=2):
#     print item.weight, item.sentence
print sr.getSummary(num=1)
'''