"""
@author Wanying Ding
@email wd78@drexel.edu
@description:
    This module generate the topic links over years. The data in use will be the direct_citation.txt data
"""

import json

#loads topic distribution for each document

document_topic = dict()
document_time = dict()
document_list = list()

topic_file = "../data/hdp_document_topic.txt"
citation_file = "../data/direct_citations.txt"


topic_time = dict()
# years = ['2003-2004','2003-2005','2003-2006','2003-2007','2003-2008','2003-2009','2003-2010',
#          '2004-2005','2004-2006','2004-2007','2004-2008','2004-2009','2004-2010',
#          '2005-2006','2005-2007','2005-2008','2005-2009','2005-2010',
#          '2006-2007', '2006-2008', '2006-2009', '2006-2010',
#          '2007-2008', '2007-2009', '2007-2010',
#          '2008-2009', '2008-2010',
#          '2009-2010']

years = ['2003-2004','2004-2005','2005-2006','2006-2007','2007-2008','2008-2009','2009-2010']

for year in years:
    topic_time[year]=dict()

topic_reader = file(topic_file,'r')
for line in topic_reader.readlines():
    data = json.loads(line)
    topic= sorted(data["topic"],key=lambda x:x[1],reverse=True)
    major_topic = [t for t in topic if t[1]>0.1]
    time = data["time"]
    id = data["id"]
    document_list.append(id)

    document_topic[id]=major_topic
    document_time[id]=time

citation_reader = file(citation_file,'r')
lines =citation_reader.readlines()

for i in range(1,len(lines)):
    line = lines[i].strip()
    pairs = line.split("\t")
    citing_topics= document_topic[pairs[0]]
    citing_time = document_time[pairs[0]]
    cited_topics = document_topic[pairs[1]]
    cited_time =document_time[pairs[1]]

    time_pairs = str(cited_time)+"-"+str(citing_time)
    if time_pairs not in topic_time:
        continue
    #topic_pairs = dict()
    for citing_topic in citing_topics:
        for cited_topic in cited_topics:
            topics = str(cited_topic[0])+"-"+str(citing_topic[0])
            score= float(cited_topic[1])+float(citing_topic[1])/2
            #score =float(citing_topic[1])
            if topics in topic_time[time_pairs]:
                topic_time[time_pairs][topics].append(score)
            else:
                topic_time[time_pairs][topics]=list()
                topic_time[time_pairs][topics].append(score)


link_dict=dict()
for time_pairs,topic_pair_list in topic_time.iteritems():
    topic_list=dict()
    for topics,score_list in topic_pair_list.iteritems():
        num = len(score_list)
        score_sum = sum(score_list)
        score_ave = score_sum/num
        topic_list[topics]=score_sum
    scored_topic_list = sorted(topic_list.items(),key=lambda (k,v):v,reverse=True)[0:10]
    print scored_topic_list
    link_dict[time_pairs] = scored_topic_list

topic_link_file = file("../data/hdp_topic_link.txt",'w')
topic_link_file.write(json.dumps(link_dict))
topic_link_file.flush()
topic_link_file.close()














