import pickle
import operator
import Constant
import nltk


class RawData:

    def __init__(self):
        self.topic_id = ''
        self.title = ''
        self.docset = {}
        self.sentences = []
        self.parsed_sentences = []
        self.words = {}

    def save(self, data_file):
        with open(data_file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load(self, data_file):
        with open(data_file, "rb") as f:
            dump = pickle.load(f)
        self.topic_id = dump.topic_id
        self.title = dump.title
        self.docset = dump.docset
        self.sentences = dump.sentences
        self.words = dump.words

    def process_data(self, doc_index, p_index, text):
        text = text.strip().replace('\n', ' ')
        sentences = nltk.sent_tokenize(text)
        line_index = 1
        for sentence in sentences:
            sentence = sentence.strip()

            self.sentences.append([[doc_index, p_index, line_index], sentence])
            line_index += 1

            for word in Constant.word_tokenize(sentence):
                if word not in self.words:
                    self.words[word] = 0
                self.words[word] += 1

    def calculate(self):
        words_weight = {}
        for word in Constant.word_tokenize(self.title):
            if word not in words_weight:
                words_weight[word] = 0
            words_weight[word] = 10

        for sentence in self.sentences:
            f = self.calculate_frequency_score(sentence[1], self.words)
            s = self.calculate_similarity_score(sentence[1], words_weight)
            p = self.calculate_position_score(sentence[0])
            total = self.calculate_total_score(f, s, p)
            sentence.insert(1, [f, s, p])
            sentence.insert(2, total)

    def calculate_frequency_score(self, sentence, words_dict):
        score = 0
        count = 0
        for word in Constant.word_tokenize(sentence):
            if word in words_dict:
                score += words_dict[word]
                count += 1

        if count == 0:
            return 0
        else:
            return round(score, 2)

    def calculate_similarity_score(self, sentence, words_weight):
        score = 0

        for word in Constant.word_tokenize(sentence):
            if word in words_weight:
                score += words_weight[word]

        return score

    def calculate_position_score(self, index):
        score = 1
        p_index = index[1]
        line_index = index[2]

        if p_index == 1:
            score = score * 1.5
        if line_index == 1:
            score = score * 1.5

        return score

    def calculate_total_score(self, FS, PS, SS):
        return round((FS + SS) * PS, 2)

    def select_sentences(self):
        selected_sentences = []
        total = 0
        self.sentences = sorted(self.sentences, key=operator.itemgetter(2), reverse=True)
        for sentence in self.sentences:
            words_count = len(nltk.word_tokenize(sentence[3]))
            if (total + words_count) <= 100:
                selected_sentences.append(sentence)
                total += words_count
            else:
                break

        return selected_sentences
