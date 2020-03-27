#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 00:46:15 2020

@author: vyvo
"""

import pandas as pd 
from bs4 import BeautifulSoup
from itertools import chain
from langdetect import detect

data = pd.read_csv('dsjob_final.csv')

#Split train & test data by title 
test_data = []
train_data = []
for desc in data.description: 
    parse = BeautifulSoup(desc,'lxml')
    extr = parse.find_all(['strong','p','li'])
    split_index = []
    for i, val in enumerate(extr):
         if '<strong>' in str(val):
             split_index.append(i)
    if len(split_index) == 0: 
        result = [t.get_text().lower() for t in extr]
        result = '. '.join(result)
        try:
            if len(extr) < 3 or result.isalpha() == False: 
                test_data.append(parse.get_text().lower())
            else:
                test_data.append(result)            
        except: pass 
    else: 
        result = [extr[k : j] for k, j in zip([0] + split_index, split_index + [None])] 
        train_data.append(result) 


#filter only elements with bold titles
title = []
for element in train_data: 
    l = list(chain(*element))#unnest the list
    l = list(filter(lambda x: '<strong>' in str(x),l)) 
    l = list(map(lambda x: x.get_text(),l))
    title.extend(l)


#label training data 

train_data = list(chain(*train_data)) #unnest the list
train_data = list(filter(lambda x: len(x) > 2 and '<strong>' in str(x[0]),train_data)) #filter data with bold title

def labeling(data,jd_kw,jr_kw): 
    #1: Job responsibility, 2: Requirements, 3: Others 
    # data is job description in html 
    d = {'Content':[],'Label':label} 
    for inst in data: 
        #get content in raw text 
        content = list(map(lambda x: x.get_text(),inst))
        content = '.'.join(content) #join all elements in the list
        d['Content'].append(content)
        
        #get labels
        txt = inst[0].get_text().lower() 
        i = 0
        j = 0
        result = False
        while result == False and j < len(jr_kw): 
            if i >= len(jd_kw):
                result = all(s in txt for s in jr_kw[j].split(' '))
                j +=1 
            else: 
                result = all(s in txt for s in jd_kw[i].split(' '))
                i+=1 
        if i < len(jd_kw): 
            d['Label'].append(1)
        elif i >= len(jd_kw) and j < len(jr_kw): 
            d['Label'].append(2)
        else: 
            d['Label'].append(3)
    return d



#Adjusted data
newdf = pd.read_csv('englabel_nodup.csv')
newdf.info()

