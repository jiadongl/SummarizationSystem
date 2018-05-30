import os
import sys

import ContentRealization
import InformationOrdering
import Preprocess
import SummaryOutput

if __name__ == "__main__":

    # dev
    TopicFile = '../data/GuidedSumm10_test_topics.xml'
    OutputDir = '../outputs/D4_devtest/'

    # Give argv
    if len(sys.argv) > 1:
        target_data = sys.argv[1]
        if target_data == 'eval':
            # eval
            TopicFile = '../data/GuidedSumm11_test_topics.xml'
            OutputDir = '../outputs/D4_evaltest/'

    # Local path
    # DataDir0 = '/Users/Jiadong/Desktop/573/573/TIPSTER_V3'
    # DataDir1 = '/Users/Jiadong/Desktop/573/573/AQUAINT'
    # DataDir2 = '/Users/Jiadong/Desktop/573/573/AQUAINT-2'
    # DataDir3 = '/Users/Jiadong/Desktop/573/573/ENG-GW'

    # Patas path
    DataDir0 = '/home2/jiadongl/dropbox/17-18/573/TIPSTER_V3'
    DataDir1 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT'
    DataDir2 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT-2'
    DataDir3 = '/home2/jiadongl/dropbox/17-18/573/ENG-GW'

    all_raw_data = Preprocess.process_topic_file(TopicFile)
    all_score_data = []

    # print(len(all_raw_data))

    DataFiles = {}
    for root, dirs, files in os.walk(DataDir0):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()
    for root, dirs, files in os.walk(DataDir1):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()
    for root, dirs, files in os.walk(DataDir2):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()
    for root, dirs, files in os.walk(DataDir3):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()

    for data in all_raw_data:
        # if data.topic_id != 'D1104A':
        # if data.topic_id != 'D1001A':
        #     continue

        data = Preprocess.process_docset(data, DataFiles)

        data.calculate()

        data.sort_sentences()

        selected_sentences = []
        summary_count = 0
        for index in range(min(20, len(data.sentences))):
            sentence = data.select_sentence(index)
            sentence = ContentRealization.realize(sentence)
            count = len(sentence[5].split())
            max_similarity = ContentRealization.max_similarity(selected_sentences, sentence)
            if summary_count + count <= 100 and max_similarity < 0.6:
                summary_count += count
                selected_sentences.append(sentence)

        summary = InformationOrdering.order(selected_sentences)

        SummaryOutput.output(OutputDir, data.topic_id, summary)

        print(data.topic_id, data.title)
        print(summary)
