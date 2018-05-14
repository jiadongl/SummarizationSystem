import sys
import os
import Preprocess, InformationOrdering, ContentRealization, SummaryOutput


if __name__ == "__main__":
    # Local path
    TopicFile = '/Users/Jiadong/Desktop/573/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml'
    DataDir1 = '/Users/Jiadong/Desktop/573/573/AQUAINT'
    DataDir2 = '/Users/Jiadong/Desktop/573/573/AQUAINT-2'

    # Patas path
    # TopicFile = '/home2/jiadongl/dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml'
    # DataDir1 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT'
    # DataDir2 = '/home2/jiadongl/dropbox/17-18/573/AQUAINT-2'

    # Give argv
    if len(sys.argv) > 1:
        TopicFile = sys.argv[1]
        DataDir1 = sys.argv[2]
        DataDir2 = sys.argv[3]

    RawOutputDir = '../data/Raw/'

    all_raw_data = Preprocess.process_topic_file(TopicFile)
    all_score_data = []

    assert len(all_raw_data) == 46

    DataFiles = {}
    for root, dirs, files in os.walk(DataDir1):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()
    for root, dirs, files in os.walk(DataDir2):
        for file in files:
            DataFiles[os.path.join(root, file)] = file.lower()

    for data in all_raw_data:
        data = Preprocess.process_docset(data, DataFiles)

        data.calculate()

        data.save(RawOutputDir + data.topic_id)

        selected_sentences = data.select_sentences()
        # for sentence in data.sentences:
        #     print(sentence)

        summary = InformationOrdering.order(selected_sentences)

        summary = ContentRealization.realize(summary)

        SummaryOutput.output(data.topic_id, summary)

        print(data.topic_id, data.title, len(data.sentences), len(data.words.items()))
        # for sentence in data.sentences:
        #     print(sentence)

        # break
