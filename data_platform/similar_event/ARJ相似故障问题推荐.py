# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 18:48:16 2019

@author: yuliqun
"""

import jieba 
from gensim import corpora,models,similarities

def recommandation(input_event):
    input_cut=[]
    jieba.load_userdict(r'四性术语词典.txt')
    input_cut=jieba.cut(input_event)
    input_list=[]
    for word in input_cut:
        input_list.append(word)
    
    #从本地读取分完词的txt
    event_list=[]
    fileObject=open('wordcut.txt','r', encoding='utf-8',errors='ignore')
    for line in fileObject:
        line=line.rstrip('\n')
        event_list_tem=line.split(' ')
        event_list.append(event_list_tem)
        #event_list.insert(2,line)
        #print(event_list)
        #for word in line:
            #print(word)
    
    dictionary= corpora.Dictionary(event_list)#数据源生成词典
    corpus = [dictionary.doc2bow(item) for item in event_list]#通过doc2bow稀疏向量生成语料库
    tf = models.TfidfModel(corpus)#通过TF模型算法，计算出tf值
    num_features = len(dictionary.token2id.keys())#通过token2id得到特征数（字典里面的键的个数）
    index = similarities.MatrixSimilarity(tf[corpus], num_features=num_features)#计算稀疏矩阵相似度，建立一个索引
    
    new_vec = dictionary.doc2bow(input_list)#新的稀疏向量
    sims = index[tf[new_vec]]#算出相似度
    sims_list=list(sims)
    #print(max(sims_list))
    sim_max=sims_list.index(max(sims_list))#找出与输入事件相似度最高的事件的序号
    print(sim_max)
    str_link=''
    output=str_link.join(event_list[sim_max])#将相似度最高的事件连接起来输出
    #print(event_list)
    print(output)

#模拟新事件的输入
input_event=input('请输入事件描述：')
recommandation(input_event)
