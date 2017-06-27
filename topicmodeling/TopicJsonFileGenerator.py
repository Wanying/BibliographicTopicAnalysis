"""
@author Wanying Ding
@email wd78@drexel.edu
@description:
    Used to generate the json file for the visualization
"""

import json


node_id2topic=dict()
node_id2score =dict()
node_id2content=dict()
year_topic2node_id=dict()
node_source_count=dict()
node_target_count=dict()
links=list()

topic_node_file ="../data/hdp_topic_node.txt"
topic_word_file ="../data/hdp_topic_word.txt"
topic_link_file="../data/hdp_topic_link.txt"

timelist=["2003","2004","2005","2006","2007","2008","2009","2010"]

#loads topic per year
topic_nodes=json.loads(file(topic_node_file,'r').read())
node_id=0
for i in range(len(timelist)):
    time = timelist[i]
    topiclist = topic_nodes[time]
    for topic in topiclist:
        topic_id = topic[0]
        topic_score=topic[1]
        node_id2topic[node_id]=topic_id
        node_id2score[node_id]=topic_score

        year_topic=time+"_"+str(topic_id)
        year_topic2node_id[year_topic]=node_id
        #print year_topic, node_id
        node_id+=1

#loads topic content
topic_contents = json.loads(file(topic_word_file,'r').read())
for node_id,topic_id in node_id2topic.iteritems():
    content = topic_contents[str(topic_id)]
    node_id2content[node_id]=content

#print year_topic2node_id
#load link information
links_content = json.loads(file(topic_link_file,'r').read())
for years, score_list in links_content.iteritems():
    #print years,score_list
    cited_year = years.split("-")[0]
    citing_year = years.split("-")[1]
    #print cited_year,citing_year
    for score_pair in score_list:
        cited_topic =score_pair[0].split("-")[0]
        citing_topic = score_pair[0].split("-")[1]
        try:
            cited_node_id = year_topic2node_id[str(cited_year)+"_"+str(cited_topic)]
            citing_node_id = year_topic2node_id[str(citing_year)+"_"+str(citing_topic)]
            link = str(cited_node_id) + ":" + str(citing_node_id)
            #print link
            #print link, cited_year,cited_topic, citing_year,citing_topic
            links.append(link)
            if cited_node_id in node_source_count:
                node_source_count[cited_node_id] += 1
            else:
                node_source_count[cited_node_id] = 1

            if citing_node_id in node_target_count:
                node_target_count[citing_node_id] += 1
            else:
                node_target_count[citing_node_id] = 1
        except:
            print cited_topic,citing_topic
            continue

#
#write json file
times = list()
for time in timelist:
    topiclist = topic_nodes[time]
    per_time =list()
    for topic in topiclist:
        node_map = dict()
        topic_id = topic[0]
        node_id = year_topic2node_id[str(time)+"_"+str(topic_id)]
        node_map["id"]=node_id
        node_map["topicid"]=topic_id
        node_map["topic"]=node_id2content[node_id]
        node_map["color"]=""
        node_map["size"]=node_id2score[node_id]
        node_map["x"]=0.0
        node_map["y"]=0.0
        if node_id in node_source_count:
            node_map["sourcecount"]=node_source_count[node_id]
        else:
            node_map["sourcecount"]=0
        if node_id in node_target_count:
            node_map["targetcount"] = node_target_count[node_id]
        else:
            node_map["targetcount"]=0

        node_map["sourceoff"]=0.0
        node_map["targetoff"]=0.0

        per_time.append(node_map)
    times.append(per_time)

link_pairs =list()
lid=0
for link in links:
    link_map=dict()
    link_map["id"]=lid
    lid+=1
    source = int(link.split(":")[0])
    target = int(link.split(":")[1])
    link_map["source"]=source
    link_map["target"]=target
    link_map["sourcex1"]=0.0
    link_map["sourcey1"]=0.0
    link_map["targetx1"]=0.0
    link_map["targety1"]=0.0
    link_map["sourcex2"] = 0.0
    link_map["sourcey2"] = 0.0
    link_map["targetx2"] = 0.0
    link_map["targety2"] = 0.0
    link_map["linksize"]=0.0
    #print link_map
    link_pairs.append(link_map)

jsonObj=dict()
jsonObj["times"]=times
jsonObj["links"]=link_pairs

jsonFile="../data/galaxy_hdp_model.json"
writer = file(jsonFile,'w')
writer.write(json.dumps(jsonObj,indent=2))
writer.flush()
writer.close()













