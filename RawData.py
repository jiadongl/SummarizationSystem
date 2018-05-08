import pickle
import nltk
import TopicData


class RawData:

    def __init__(self):
        self.topic_id = ''
        self.title = ''
        self.doc_set = {}
        self.sentences = []
        self.words = {}

    def save(self, data_file):
        with open(data_file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load(self, data_file):
        with open(data_file, "rb") as f:
            dump = pickle.load(f)
        self.topic_id = dump.topic_id
        self.title = dump.title
        self.doc_set = dump.doc_set
        self.sentences = dump.sentences
        self.words = dump.words

    def process_data(self, doc_index, p_index, text):
        text = text.strip().replace('\n', ' ')
        sentences = nltk.sent_tokenize(text)
        line_index = 1
        for sentence in sentences:
            sentence = sentence.strip()
            self.sentences.append([doc_index, p_index, line_index, sentence])
            line_index += 1

            for word in TopicData.word_tokenize(sentence):
                if word not in self.words:
                    self.words[word] = 0
                self.words[word] += 1
