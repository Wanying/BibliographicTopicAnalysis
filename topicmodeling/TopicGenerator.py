"""
@author: Wanying Ding
@email: alice.ding@viphshop.com
@description: This module is used to apply HDP to generate topic model
"""

from gensim import corpora, models,similarities
import gensim
import logging
import json

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#stoplist= set('a for the and to in at of'.split(' '))
stoplist= set()

stopreader = file("../data/stopwords.txt",'r').readlines()
for line in stopreader:
    stoplist.add(line.strip())

def data_process(document_addr):
    file_reader =file(document_addr,'r')
    dataList = list()
    #stopWords = get_stop_words("en").extend(stoplist)
    tokenizer = RegexpTokenizer(r'[\w_]+')
    for line in file_reader.readlines():
        jsonObj = json.loads(line)
        document = jsonObj["document"]
        tokens = tokenizer.tokenize(document)
        stopped_tokens =[i for i in tokens if not i in stoplist]
        jsonObj["pText"] = stopped_tokens
        dataList.append(jsonObj)
    return dataList


def trainHDPModel(dataList,save_model_address,save_dictionary_address):
    print "Train Hierarchical Dirichlet Process Models..."
    topicTextList = list()
    for data in dataList:
        text = data["pText"]
        topicTextList.append(text)
    dictionary=corpora.Dictionary(topicTextList)
    corpus = [dictionary.doc2bow(text) for text in topicTextList]

    hdpModel = gensim.models.HdpModel(corpus=corpus,id2word=dictionary,K=100,T=5,alpha=0.001,gamma=0.001,chunksize=100000)
    hdpModel.save(save_model_address)
    dictionary.save(save_dictionary_address)

    #print each document's topic distribution

def trainLDAModel(dataList,save_model_address,save_dictionary_address):
    print "Train Latent Dirichlet Allocation Models..."
    topicTextList = list()
    for data in dataList:
        text = data["pText"]
        topicTextList.append(text)
    dictionary = corpora.Dictionary(topicTextList)
    corpus = [dictionary.doc2bow(text) for text in topicTextList]

    ldaModel = gensim.models.LdaModel(corpus=corpus,id2word=dictionary,num_topics=20,iterations=1000)
    ldaModel.save(save_model_address)
    dictionary.save(save_dictionary_address)


def loadLDAModel(dataList,model_address,dictionary_address,doc_topic_distribution):
    ldaModel = gensim.models.LdaModel.load(model_address)
    dictionary = corpora.Dictionary.load(dictionary_address)
    # hdpModel.print_topics(num_topics=10,num_words=10)
    doc_topic_writer = file(doc_topic_distribution, 'w')
    for data in dataList:
        text = data["pText"]
        doc_hdp = ldaModel[dictionary.doc2bow(text)]
        doc_id = data["id"]
        doc = dict()
        doc["id"] = doc_id
        doc["topic"] = doc_hdp
        doc["time"] = data["time"]
        doc_topic_writer.write(json.dumps(doc) + "\n")
        doc_topic_writer.flush()
    doc_topic_writer.flush()
    doc_topic_writer.close()

def loadHDPModel(dataList,model_address,dictionary_address,doc_topic_distribution):
    print "loading model..."

    hdpModel = gensim.models.HdpModel.load(model_address)
    dictionary =corpora.Dictionary.load(dictionary_address)
    doc_topic_writer = file(doc_topic_distribution,'w')
    #hdpModel.print_topics(num_topics=10,num_words=10)
    for data in dataList:
        text = data["pText"]
        doc_hdp = hdpModel[dictionary.doc2bow(text)]
        doc_id = data["id"]
        doc= dict()
        doc["id"]=doc_id
        doc["topic"] = doc_hdp
        doc["time"] = data["time"]
        doc_topic_writer.write(json.dumps(doc)+"\n")
        doc_topic_writer.flush()
    doc_topic_writer.flush()
    doc_topic_writer.close()

def showHDPTopics(model_address, topic_word_file):
    topic_writer = file(topic_word_file,'w')
    hdpModel = gensim.models.HdpModel.load(model_address)
    hdpModel.optimal_ordering()
    topics=hdpModel.show_topics(num_topics=50,num_words=10,formatted=True)
    topic_dict = dict()
    for topic in topics:
        topic_id = topic[0]
        topic_string = topic[1]
        topic_words = topic_string.split("+")
        topic_content =""
        for word_score in topic_words:
            word = word_score.split("*")[1].strip()
            topic_content+=word+" "
        topic_dict[topic_id]=topic_content.strip()
    topic_writer.write(json.dumps(topic_dict))
    topic_writer.flush()
    topic_writer.close()

def showLDATopics(model_address,topic_word_file):
    topic_writer = file(topic_word_file, 'w')
    ldaModel = gensim.models.LdaModel.load(model_address)
    topics = ldaModel.show_topics(num_topics=50, num_words=8, formatted=True)
    topic_dict = dict()
    for topic in topics:
        topic_id = topic[0]
        topic_string = topic[1]
        topic_words = topic_string.split("+")
        topic_content = ""
        for word_score in topic_words:
            word = word_score.split("*")[1].strip()
            topic_content += word + " "
        topic_dict[topic_id] = topic_content.strip()
    topic_writer.write(json.dumps(topic_dict))
    topic_writer.flush()
    topic_writer.close()


document_addr ="../data/refine_document.txt"
dataList = data_process(document_addr)

#HDP
save_model_address ="../data/hdp_model.mm"
save_dictionary_address = "../data/hdp_dictionary.dict"
document_topic_distribution ="../data/hdp_document_topic.txt"
topic_word_file="../data/hdp_topic_word.txt"
#
trainHDPModel(dataList=dataList,save_model_address=save_model_address,save_dictionary_address=save_dictionary_address)
loadHDPModel(dataList=dataList,model_address=save_model_address,
             dictionary_address=save_dictionary_address, doc_topic_distribution=document_topic_distribution)

showHDPTopics(model_address=save_model_address,topic_word_file=topic_word_file)

#LDA Model
save_lda_model_address = "../data/lda_model.mm"
save_lda_dictionary_address="../data/lda_dictionary.dict"
lda_document_topic_distribution ="../data/lda_document_topic.txt"
lda_topic_word_file="../data/lda_topic_word.txt"

#trainLDAModel(dataList=dataList,save_model_address=save_lda_model_address,save_dictionary_address=save_lda_dictionary_address)
#loadLDAModel(dataList=dataList,model_address=save_lda_model_address, dictionary_address=save_lda_dictionary_address,
#             doc_topic_distribution=lda_document_topic_distribution)
#showLDATopics(model_address=save_lda_model_address,topic_word_file=lda_topic_word_file)





