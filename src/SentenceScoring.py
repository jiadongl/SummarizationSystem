import nltk
import operator
import os
import string
import sys
import xml.etree.ElementTree as ET
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from xml.dom import minidom


def prettify(elem):
    # Return a pretty-printed XML string for the Element.
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def CalculateSentenceScore(score):
    FrequencyScore = float(score[0])
    PositionScore = float(score[1])
    CueWordScore = int(score[2])
    SimilarityScore = float(score[3])

    c = 1 + (CueWordScore * 0.1)

    SentenceScore = (FrequencyScore + SimilarityScore) * PositionScore * c

    return SentenceScore


if __name__ == "__main__":

    TopicDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/FeatureExtractionData/'
    OutputDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/SentenceScoreData/'

    if len(sys.argv) > 1:
        TopicDir = sys.argv[1]
        OutputDir = sys.argv[2]

    for root, dirs, files in os.walk(TopicDir):
        for file in files:
            TopicFile = os.path.join(root, file)

            Topic = ET.parse(TopicFile).getroot()
            TopicId = Topic.get('id')

            Sentences = []

            for Content in Topic:
                if Content.tag == 'Sentences':
                    for Sentence in Content:
                        score = [Sentence.get('FQ'), Sentence.get('PS'), Sentence.get('CW'), Sentence.get('SM')]
                        Sentences.append([Sentence.get('DocIndex'), CalculateSentenceScore(score), Sentence.text])

            ROOT = ET.Element('Topic', id=TopicId)
            SENTENCES = ET.SubElement(ROOT, 'Sentences')

            for sentence in sorted(Sentences, key=operator.itemgetter(1), reverse=True):
                ET.SubElement(SENTENCES, 'sentence', DocIndex=sentence[0], Score=str(sentence[1])).text = sentence[2]

            TopicFile = os.path.join(OutputDir, TopicId + '.xml')
            try:
                f = open(TopicFile, 'w')
                f.write(prettify(ROOT))
                f.close()
            except IOError:
                print ("Wrong path provided")

            print ('Finish Sentence Scoring', TopicId)

    print ('Finish')
