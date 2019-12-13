# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:41:12 2019

@author: yuliqun
"""

original_info=[['ROLL CONTROLS DISCO','驾驶盘脱开','WARNING','正副驾驶驾驶盘脱开' ,'27-11-00-810-806','27-11-14-710-801'],
['ELEV SPLIT','左右升降舵偏度不一致','WARNING','左右升降舵偏度不一致超过限制值，可能引起飞机结构损坏','27-91-04-810-801','27-91-04-000-801'],
['ELEV SPLIT','左右升降舵偏度不一致','WARNING','左右升降舵偏度不一致超过限制值，可能引起飞机结构损坏','27-91-04-810-801','27-91-04-400-801'],
['PITCH CONTROLS DISCO','驾驶杆脱开','WARNING','正副驾驶驾驶杆脱开','27-31-00-810-801','27-31-14-710-801'],
['SINGLE AIL INOP','单个副翼不工作', 'CAUTION','左侧或右侧副翼漂浮或卡阻','27-91-21-810-801','27-91-21-000-801'],
['SINGLE AIL INOP','单个副翼不工作', 'CAUTION','左侧或右侧副翼漂浮或卡阻','27-91-21-810-801','27-91-21-400-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-804','27-22-01-000-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-804','27-22-01-400-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-803','27-22-01-000-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-803','27-22-01-400-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-801','27-22-01-000-801'],
['RUDDER JAM','方向舵卡阻','CAUTION','方向舵卡阻或漂浮','27-22-00-810-801','27-22-01-400-801'],
['副翼驾驶盘：操作不灵活,卡阻/过松-正驾驶员','','观察到的故障','','27-11-00-810-803','27-11-00-710-801']]

def display(input_info,original_info):
    input_info=input_info.upper()
    a=0
    for line in original_info:
        if input_info==line[0]:
            print('定义：'+line[1],'等级分类:'+line[2],'中文（失效）条件:'+line[3],'FIM对应任务号'+line[4],'AMM对应任务号:'+line[5])
            a=a+1
    if a==0:
        print('本条EICAS信息尚未记录，请检查输入是否有误')
input_info=input('请输入EICAS信息：')
display(input_info,original_info)           
                
        