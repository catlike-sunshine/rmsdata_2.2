# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:23:22 2019

@author: zylzlh
"""

import jieba
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


risk= {'0':'无风险','1':'有风险','2':'存在重大风险','3':'存在重大风险'}

def riskidentification(event_input):
    xpre=pd.DataFrame()
    #停用词读入列表
    stopwords_list=[]
    for word in open(r"stopwords.txt", encoding='utf-8',errors='ignore'):
        stopwords_list.append(word.strip()) 

    jieba.load_userdict(r'四性术语词典.txt')
    seg_list=jieba.cut(event_input)
    event_cut=[]
    for word in seg_list:
        if word not in stopwords_list:
            event_cut.append(word)
    eventdevide = ' '.join(event_cut)
    xpre['text'] = eventdevide

    trainDF = pd.read_excel('data.xlsx', index=False)
    tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2, 3), max_features=500)
    #tfidf_vect_ngram.fit(df['问题描述'])
    tfidf_vect_ngram.fit(trainDF['text'])

    xpre_tfidf_ngram = tfidf_vect_ngram.transform(xpre)


    clf = joblib.load("train_model.m")
    prediction=clf.predict(xpre_tfidf_ngram)
    print(risk[str(int(prediction))])


event_input = input()
riskidentification(event_input)