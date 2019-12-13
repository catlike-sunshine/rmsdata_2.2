# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 18:48:16 2019

@author: yuliqun
"""

import jieba 
from gensim import corpora,models,similarities
import xlrd
import heapq

#读入源数据表格
file_path='ARJ事件和问题清单_input.xls'
event_info=xlrd.open_workbook(file_path)
event=event_info.sheet_by_name('事件和问题清单')
row=event.nrows

def recommandation(input_event,row):
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
    re1 = map(sims_list.index, heapq.nlargest(3, sims_list)) #求最大的三个索引，索引加2为excel行数
    max_three_index=list(re1)
    #sim_list_sort=sims_list.sort()#降序排序
    #print(max(sims_list))
    sim_one=max_three_index[0]#找出与输入事件相似度最高的事件的序号
    sim_two=max_three_index[1]
    sim_three=max_three_index[2]
    #print(sim_max)
    #str_link=''
    #output=str_link.join(event_list[sim_max])#将相似度最高的事件连接起来输出
    # print(event_list)
    unicode={}#描述-唯一编号字典
    num=[]#唯一编号
    for i in range(1,row):
        unicode[tuple(event_list[i-1])]=event.cell_value(i,30)
        num.append(event.cell_value(i,30))
    #print(output)
    num_one=unicode[tuple(event_list[sim_one])]#相似度最高的唯一编码
    num_two=unicode[tuple(event_list[sim_two])]
    num_three=unicode[tuple(event_list[sim_three])]
    #print(num_max)
    row_one=num.index(num_one)+1#excel表中的行数
    row_two=num.index(num_two)+1
    row_three=num.index(num_three)+1
    print('问题描述:'+event.cell_value(row_one,8))
    print('ATA:'+event.cell_value(row_one,6))
    print('纠正措施：'+event.cell_value(row_one,12))
    print('排故措施：'+event.cell_value(row_one,13)+'\n')
    
    print('问题描述:'+event.cell_value(row_two,8))
    print('ATA:'+event.cell_value(row_two,6))
    print('纠正措施：'+event.cell_value(row_two,12))
    print('排故措施：'+event.cell_value(row_two,13)+'\n')
    
    print('问题描述:'+event.cell_value(row_three,8))
    print('ATA:'+event.cell_value(row_three,6))
    print('纠正措施：'+event.cell_value(row_three,12))
    print('排故措施：'+event.cell_value(row_three,13))
    #print(output)


#模拟新事件的输入
flag = True
while (flag):
    input_event=input('请输入事件描述：')
    if input_event == 'False':
        flag = False
        break
    recommandation(input_event,row)
