import sys
import os
import re
import xml.etree.ElementTree as ET
import RawData


def find_doc_file(doc_id, files):
    id = doc_id.replace('_ENG_', '')
    src = id[0:3].lower()
    year = int(id[3:7])
    if year > 2000:
        date = id[3:9]
    else:
        date = id[3:11]
        src = src.replace('xie', 'xin')

    for (k, v) in files.items():
        if src in v and date in v:
            return k
    return None


def process_file(doc_index, doc_id, file, raw_data):
    if 'AQUAINT-2' in file:
        return process_new_file(doc_index, doc_id, file, raw_data)
    else:
        return process_old_file(doc_index, doc_id, file, raw_data)


def process_new_file(doc_index, doc_id, file, raw_data):
    root = ET.parse(file).getroot()
    for doc in root:
        if doc.get('id') == doc_id:
            p_index = 1
            for p in doc.find('TEXT'):
                raw_data.process_data(doc_index, p_index, p.text)
                p_index += 1
            break
    return raw_data


def process_old_file(doc_index, doc_id, file, raw_data):
    with open(file, encoding='utf-8', errors='ignore') as f:
        xml = f.read()
    xml = '<?xml version="1.0" encoding="utf-8"?> <root> ' + xml + ' </root> '
    xml = re.sub(r'&\S+;', ' ', xml)
    root = ET.fromstring(xml)
    for doc in root:
        if doc.find('DOCNO').text.strip() == doc_id:
            p_index = 1
            for p in doc.find('BODY/TEXT'):
                raw_data.process_data(doc_index, p_index, p.text)
                p_index += 1
            break

    return raw_data


if __name__ == "__main__":

    # Local path
    TopicFile = '/Users/Jiadong/Desktop/573/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml'
    DataDir1 = '/Users/Jiadong/Desktop/573/573/AQUAINT'
    DataDir2 = '/Users/Jiadong/Desktop/573/573/AQUAINT-2'

    # Patas path
    TopicFile = '/home2/jiadongl/dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml'
    DataDir1 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT'
    DataDir2 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT-2'

    # Give argv
    if len(sys.argv) > 1:
        TopicFile = sys.argv[1]
        DataDir1 = sys.argv[2]
        DataDir2 = sys.argv[3]

    OutputDir = 'data/Preprocess/'

    DataFiles = {}
    for root, dirs, files in os.walk(DataDir1):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()
    for root, dirs, files in os.walk(DataDir2):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()

    root = ET.parse(TopicFile).getroot()

    for Topic in root:
        raw_data = RawData.RawData()
        raw_data.topic_id = Topic.get('id')
        print("Preprocessing :", raw_data.topic_id)

        for Content in Topic:
            if Content.tag == 'title':
                raw_data.title = Content.text.strip()
            elif Content.tag == 'docsetA':
                doc_set_id = Content.get('id')
                doc_set = []
                for Doc in Content:
                    doc_id = Doc.get('id')
                    doc_set.append(doc_id)
                    file = find_doc_file(doc_id, DataFiles)
                    if not file:
                        print('Cannot find target file for %s' % doc_id)
                    else:
                        raw_data = process_file(len(doc_set), doc_id, file, raw_data)

                raw_data.doc_set[doc_set_id] = doc_set

        topic_file = OutputDir + raw_data.topic_id

        # print()
        # print(raw_data)
        # print(raw_data.topic_id)
        # print(raw_data.title)
        # print(raw_data.doc_set)
        # print(raw_data.sentences)
        # print(len(raw_data.sentences))
        # print(raw_data.words)
        # print(len(raw_data.words.items()))

        raw_data.save(topic_file)
    print('Preprocessing Finished')
