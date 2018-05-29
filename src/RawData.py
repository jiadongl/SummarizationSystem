import pickle
import operator
import Constant
import nltk

stemmer = nltk.stem.SnowballStemmer("english")


class RawData:

    def __init__(self):
        self.topic_id = ''
        self.title = ''
        self.docset = {}
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
        self.docset = dump.docset
        self.sentences = dump.sentences
        self.words = dump.words

    def process_data(self, doc_index, p_index, text):
        text = text.strip().replace('\n', ' ')
        sentences = nltk.sent_tokenize(text)
        line_index = 1
        for sentence in sentences:
            sentence = sentence.strip()

            words = nltk.word_tokenize(sentence)
            words = nltk.pos_tag(words)
            self.sentences.append([[doc_index, p_index, line_index], sentence, words])
            line_index += 1

            for word in words:
                if word[1] in Constant.POS_tag_weight and word[0] not in Constant.Ignore_words:
                    weight = Constant.POS_tag_weight[word[1]]
                    stem_word = stemmer.stem(word[0])
                    if stem_word not in self.words:
                        self.words[stem_word] = 0
                    self.words[stem_word] += weight

    def calculate(self):
        words_weight = {}
        for word in nltk.word_tokenize(self.title):
            stem_word = stemmer.stem(word)
            if stem_word not in words_weight:
                words_weight[stem_word] = 0
            words_weight[stem_word] = max(self.words.values())

        for sentence in self.sentences:
            sentence[2] = self.map_word_frequency_similarity(sentence[2], self.words, words_weight)
            f = self.calculate_frequency_score(sentence[2])
            s = self.calculate_similarity_score(sentence[2])
            p = self.calculate_position_score(sentence[0])
            total = self.calculate_total_score(f, s, p)
            sentence.insert(1, [f, s, p])
            sentence.insert(2, total)

    def map_word_frequency_similarity(self, tags, words_dict, words_weight):
        new_tags = []
        for tag in tags:
            frequency = 0
            similarity = 0
            stem_word = stemmer.stem(tag[0])
            if stem_word in words_dict:
                frequency = words_dict[stem_word]
            if stem_word in words_weight:
                similarity = words_weight[stem_word]
            new_tags.append([tag[0], tag[1], frequency, similarity])
        return new_tags

    def calculate_frequency_score(self, tags):
        score = 0
        for tag in tags:
            score += tag[2]
        return score

    def calculate_similarity_score(self, tags):
        score = 0
        for tag in tags:
            score += tag[3]
        return score

    def calculate_position_score(self, index):
        score = 1
        p_index = index[1]
        line_index = index[2]

        if p_index == 1:
            score = score * 1.2
        if line_index == 1:
            score = score * 1.2

        return score

    def calculate_total_score(self, f, s, p):
        return round((f + s) * p, 2)

    def sort_sentences(self):
        self.sentences = sorted(self.sentences, key=operator.itemgetter(2), reverse=True)

    def select_sentence(self, index):
        return self.sentences[index]
