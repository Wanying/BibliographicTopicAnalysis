"""
@author Wanying Ding
@email: wd78@drexel.edu
@description:
    This module reads document-topic distribution, and calculate topic distribution over years
    In this data set, there are 150 topics
    Time Span is 2003-2010
"""
import numpy as np
import json
import operator

years = [2003,2004,2005,2006,2007,2008,2009,2010]
topic_per_year = dict()

#initiate dictionary
for year in years:
    topic_per_year[year] = np.zeros(150)
#loads data
topic_file = "../data/hdp_document_topic.txt"
topic_reader = file(topic_file,'r')
for line in topic_reader.readlines():
    jsonObj = json.loads(line)
    time = jsonObj["time"]
    topics = jsonObj["topic"]
    for topic in topics:
        topic_id =int(topic[0])
        topic_score = float(topic[1])
        topic_per_year[time][topic_id]+=topic_score

#save topic node, according to the document numbers per year, we calculate the average
#  2003  2004  2005  2006  2007  2008  2009  2010
# 12982 13904 13371 13815 13586 14307 14697 14954

topic_per_year[2003]/=12982
topic_per_year[2004]/=13904
topic_per_year[2005]/=13371
topic_per_year[2006]/=13815
topic_per_year[2007]/=13586
topic_per_year[2008]/=14307
topic_per_year[2009]/=14697
topic_per_year[2010]/=14954

#save topic node information

topic_node_file ="../data/hdp_topic_node.txt"
writer = file(topic_node_file,'w')

for k,v in topic_per_year.iteritems():
    #v=v.to_list()
    topic_dict = dict()
    for i in range(150):
        topic_dict[i]=v[i]
    sorted_list = sorted(topic_dict.items(),key=lambda(k,v):v,reverse=True)
    print sorted_list
    topic_per_year[k]=sorted_list[0:10]
writer.write(json.dumps(topic_per_year))
writer.flush()
writer.close()





