import pickle
import TopicData


class ScoreData:

    def __init__(self):
        self.topic_id = ''
        self.scores = []

    def save(self, data_file):
        with open(data_file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load(self, data_file):
        with open(data_file, "rb") as f:
            dump = pickle.load(f)
        self.topic_id = dump.topic_id
        self.scores = dump.scores

    def calculate(self, raw_data):
        self.topic_id = raw_data.topic_id
        words_weight = {}
        for word in TopicData.word_tokenize(raw_data.title):
            if word not in words_weight:
                words_weight[word] = 0
            words_weight[word] = 10

        for sentence in raw_data.sentences:
            FS = self.calculate_frequency_score(sentence[3], raw_data.words)
            PS = self.calculate_position_score(sentence[1], sentence[2])
            CWS = self.calculate_cue_word_score(sentence[3])
            SS = self.calculate_similarity_score(sentence[3], words_weight)
            TotalScore = self.calculate_total_score(FS, PS, CWS, SS)
            self.scores.append([TotalScore, sentence[0], FS, PS, CWS, SS, sentence[3]])

    def calculate_frequency_score(self, sentence, words_dict):
        score = 0
        count = 0
        for word in TopicData.word_tokenize(sentence):
            if word in words_dict:
                score += words_dict[word]
                count += 1

        if count == 0:
            return 0
        else:
            return score / count

    def calculate_position_score(self, p_index, line_index):
        score = 1

        if p_index == 1:
            score = score * 1.5
        if line_index == 1:
            score = score * 1.5

        return score

    def calculate_cue_word_score(self, sentence):
        score = 0

        for word in TopicData.word_tokenize(sentence):
            if word in TopicData.CueWords:
                score += 1

        return score

    def calculate_similarity_score(self, sentence, words_weight):
        score = 0

        for word in TopicData.word_tokenize(sentence):
            if word in words_weight:
                score += words_weight[word]

        return score

    def calculate_total_score(self, FS, PS, CWS, SS):

        c = 1 + (CWS * 0.1)
        return (FS + SS) * PS * c