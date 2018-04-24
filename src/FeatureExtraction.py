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


def CalculateFrequencyScore(sentence):
    score = 0
    count = 0
    words = nltk.word_tokenize(sentence[3])
    for word in words:
        if word not in string.punctuation:
            count += 1
            StemWord = PS.stem(word)
            if StemWord in WordsDict.keys():
                score += WordsDict[StemWord]
    if count == 0:
        return 0
    else:
        return score / count


def CalculatePositionScore(sentence):
    score = 1
    docIndex = int(sentence[0])
    paraIndex = int(sentence[1])
    lineIndex = int(sentence[2])

    if TotalDocsWeight != 0:
        score = DocsWeight[docIndex - 1] / TotalDocsWeight + 1

    if paraIndex == 1:
        score = score * 1.5

    if lineIndex == 1:
        score = score * 1.5

    return score


def CalculateCueWordScore(sentence):
    score = 0
    words = nltk.word_tokenize(sentence[3])
    for word in words:
        if word not in string.punctuation:
            StemWord = PS.stem(word)
            if StemWord in CueWords:
                score += 1
    return score


def CalculateSimilarityScore(sentence):
    score = 0
    words = nltk.word_tokenize(sentence[3])
    for word in words:
        if word not in string.punctuation:
            StemWord = PS.stem(word)
            if StemWord in WordsWeight.keys():
                score += WordsWeight[StemWord]
    return score


if __name__ == "__main__":

    TopicDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/PreprocessedData/'
    OutputDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/FeatureExtractionData/'

    if len(sys.argv) > 1:
        TopicDir = sys.argv[1]
        OutputDir = sys.argv[2]

    for root, dirs, files in os.walk(TopicDir):
        for file in files:
            TopicFile = os.path.join(root, file)

            Topic = ET.parse(TopicFile).getroot()
            TopicId = Topic.get('id')
            Title = ''
            Narrative = ''
            DocSetAId = ''
            Docs = []
            Headlines = []
            Sentences = []
            WordsDict = {}
            WordsWeight = {}
            DocsWeight = []
            TotalDocsWeight = 0
            # maybe more cue words
            CueWords = ['therefore', 'hence', 'lastly', 'finally', 'meanwhile']

            FrequencyScore = 0
            PositionScore = 0
            CueWordScore = 0
            SimilarityScore = 0

            for Content in Topic:
                if Content.tag == 'Title':
                    Title = Content.text.strip()
                elif Content.tag == 'Narrative':
                    Narrative = Content.text.strip()
                elif Content.tag == 'DocSetA':
                    DocSetAId = Content.get('id')
                    for Doc in Content:
                        Docs.append(Doc.get('id'))
                        Headlines.append(Doc.text)
                elif Content.tag == 'Sentences':
                    for Sentence in Content:
                        Sentences.append(
                            [Sentence.get('doc'), Sentence.get('para'), Sentence.get('line'), Sentence.text])
                elif Content.tag == 'Words':
                    for Word in Content:
                        WordsDict[Word.get('text')] = int(Word.get('count'))

            PS = PorterStemmer()
            # print (TopicId)
            # print (Title)
            words = nltk.word_tokenize(Title)
            for word in words:
                if word not in string.punctuation:
                    StemWord = PS.stem(word)
                    if StemWord in WordsWeight.keys():
                        WordsWeight[StemWord] += 10
                    else:
                        WordsWeight[StemWord] = 10

            # print (Narrative)
            words = nltk.word_tokenize(Narrative)
            for word in words:
                if word not in string.punctuation:
                    StemWord = PS.stem(word)
                    if StemWord in WordsWeight.keys():
                        WordsWeight[StemWord] += 1
                    else:
                        WordsWeight[StemWord] = 1

            # print (DocSetAId)
            # print (Docs)
            # print (Headlines)
            for headline in Headlines:
                weight = 0
                words = nltk.word_tokenize(headline)
                for word in words:
                    if word not in string.punctuation:
                        StemWord = PS.stem(word)
                        if StemWord in WordsWeight.keys():
                            weight += WordsWeight[StemWord]
                DocsWeight.append(weight)
                TotalDocsWeight += weight

            # print(DocsWeight)

            # print (Sentences)
            # print (WordsDict)

            ROOT = ET.Element('Topic', id=TopicId)
            SENTENCES = ET.SubElement(ROOT, 'Sentences')

            for sentence in Sentences:
                frequencyScore = CalculateFrequencyScore(sentence)
                positionScore = CalculatePositionScore(sentence)
                cueWordScore = CalculateCueWordScore(sentence)
                similarityScore = CalculateSimilarityScore(sentence)

                ET.SubElement(SENTENCES, 'sentence', FQ=str(frequencyScore), PS=str(positionScore),
                              CW=str(cueWordScore), SM=str(similarityScore), DocIndex=sentence[0]).text = sentence[3]

                # break

            TopicFile = os.path.join(OutputDir, TopicId + '.xml')
            try:
                f = open(TopicFile, 'w')
                f.write(prettify(ROOT))
                f.close()
            except IOError:
                print ("Wrong path provided")

            print ('Finish Feature Extraction', TopicId)

    print ('Finish')
