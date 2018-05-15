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
            words = nltk.word_tokenize(sentence)
            words = nltk.pos_tag(words)

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
            f = self.calculate_frequency_score(sentence[1], self.words)
            s = self.calculate_similarity_score(sentence[1], words_weight)
            p = self.calculate_position_score(sentence[0])
            total = self.calculate_total_score(f, s, p)
            sentence.insert(1, [f, s, p])
            sentence.insert(2, total)

    def calculate_frequency_score(self, sentence, words_dict):
        score = 0
        for word in nltk.word_tokenize(sentence):
            stem_word = stemmer.stem(word)
            if stem_word in words_dict:
                score += words_dict[stem_word]
        return score

    def calculate_similarity_score(self, sentence, words_weight):
        score = 0
        for word in nltk.word_tokenize(sentence):
            stem_word = stemmer.stem(word)
            if stem_word in words_weight:
                score += words_weight[stem_word]
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

    def select_sentences(self):
        selected_sentences = []
        total = 0
        self.sentences = sorted(self.sentences, key=operator.itemgetter(2), reverse=True)
        for sentence in self.sentences:
            words_count = len(sentence[3].split())
            if words_count > 100 :
                continue
            if (total + words_count) <= 100:
                selected_sentences.append(sentence)
                total += words_count
            else:
                # selected_sentences.append(sentence)
                break

        return selected_sentences
