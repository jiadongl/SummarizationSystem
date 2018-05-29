import gzip
import re
import xml.etree.ElementTree as Tree
import RawData


def process_topic_file(topic_file):
    parse_root = Tree.parse(topic_file).getroot()
    all_raw_data = []

    for topic in parse_root:
        data = RawData.RawData()
        data.topic_id = topic.get('id')

        for content in topic:
            if content.tag == 'title':
                data.title = content.text.strip()
            elif content.tag == 'docsetA':
                data.docset[content.get('id')] = []
                for doc in content:
                    data.docset[content.get('id')].append(doc.get('id'))
        all_raw_data.append(data)
    return all_raw_data


def process_docset(data, data_files):
    for key, value in data.docset.items():
        assert len(value) == 10
        for doc in value:
            doc_file = find_doc_file(doc, data_files)
            if not doc_file:
                print('Cannot find target file for %s' % doc)
            else:
                data = process_file(value.index(doc), doc, doc_file, data)
    return data


def find_doc_file(doc_id, data_files):
    doc_id = doc_id.replace('_ENG_', '')
    src = doc_id[0:3].lower()
    year = int(doc_id[3:7])
    if year > 2000:
        date = doc_id[3:9]
    else:
        date = doc_id[3:11]
        src = src.replace('xie', 'xin')

    for k, v in data_files.items():
        if src in v and date in v:
            return k
    return None


def process_file(doc_index, doc_id, file, raw_data):
    if 'ENG-GW' in file :
        return process_gz_file(doc_index, doc_id, file, raw_data)
    elif 'AQUAINT-2' in file or 'ENG-GW' in file:
        return process_new_file(doc_index, doc_id, file, raw_data)
    else:
        return process_old_file(doc_index, doc_id, file, raw_data)


def process_gz_file(doc_index, doc_id, doc_file, data):
    try:
        with gzip.open(doc_file, 'r') as f:
            xml = f.read().decode("utf-8")
        xml = '<?xml version="1.0" encoding="utf-8"?> <root> ' + xml + ' </root> '
        xml = re.sub(r'&\S+;', ' ', xml)
        parse_root = Tree.fromstring(xml)
        for doc in parse_root:
            if doc.get('id') == doc_id:
                p_index = 1
                for p in doc.find('TEXT'):
                    data.process_data(doc_index, p_index, p.text)
                    p_index += 1
                break
    except:
        print('Fail to parse and extract file of ', doc_file)

    return data


def process_new_file(doc_index, doc_id, doc_file, data):
    parse_root = Tree.parse(doc_file).getroot()
    for doc in parse_root:
        if doc.get('id') == doc_id:
            p_index = 1
            for p in doc.find('TEXT'):
                data.process_data(doc_index, p_index, p.text)
                p_index += 1
            break
    return data


def process_old_file(doc_index, doc_id, doc_file, data):
    with open(doc_file, encoding='utf-8', errors='ignore') as f:
        xml = f.read()
    xml = '<?xml version="1.0" encoding="utf-8"?> <root> ' + xml + ' </root> '
    xml = re.sub(r'&\S+;', ' ', xml)
    parse_root = Tree.fromstring(xml)
    for doc in parse_root:
        if doc.find('DOCNO').text.strip() == doc_id:
            p_index = 1
            for p in doc.find('BODY/TEXT'):
                data.process_data(doc_index, p_index, p.text)
                p_index += 1
            break

    return data
