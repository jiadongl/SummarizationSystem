import os
import sys
import operator
import nltk

import ScoreData

if __name__ == "__main__":

    InputDir = 'data/Score/'
    OutputDir = 'outputs/D2/'

    if len(sys.argv) > 1:
        InputDir = sys.argv[1]
        OutputDir = sys.argv[2]

    for f in os.listdir(InputDir):
        if not f.startswith('.'):
            print('Selecting: ', f)
            input_path = os.path.join(InputDir, f)
            score_data = ScoreData.ScoreData()
            score_data.load(input_path)

            id_part1 = score_data.topic_id[:-1]
            id_part2 = score_data.topic_id[-1:]
            file_name = ('%s-A.M.100.%s.10.txt' % (id_part1, id_part2))
            output_path = os.path.join(OutputDir, file_name)

            Sentences = []
            totalWords = 0
            for sentence in score_data.scores:
                wordsCount = len(nltk.word_tokenize(sentence[6]))
                if (totalWords + wordsCount) <= 100:
                    Sentences.append([sentence[0], sentence[1], sentence[6]])
                    totalWords += wordsCount
                else:
                    break

            for sentence in Sentences:
                sentence[0] = float(sentence[0]) - float(sentence[1])

            try:
                with open(output_path, "w+") as f:
                    for sentence in sorted(Sentences, key=operator.itemgetter(0), reverse=True):
                        f.write(sentence[2] + '\n')
            except IOError:
                print("Wrong path provided")

    print('Selecting Finished')
