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


if __name__ == "__main__":
    TopicDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/Data/UpdateSumm09_test_topics.xml'
    DataDir = '/Users/Jiadong/Desktop/573/573/AQUAINT-2/'
    OutputDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/PreprocessedData/'

    if len(sys.argv) > 1:
        TopicDir = sys.argv[1]
        DataDir = sys.argv[2]
        OutputDir = sys.argv[3]

    IgnoredWords = ['the', 'of', 'a', 'to', 'that', 'and', 'in', '``', "''"]

    PS = PorterStemmer()
    root = ET.parse(TopicDir).getroot()

    for Topic in root:
        # print(Topic.tag, Topic.get('id'))
        TopicId = Topic.get('id')
        ROOT = ET.Element('Topic', id=TopicId)
        WordsDict = {}
        for Content in Topic:
            if Content.tag == 'title':
                Title = Content.text.strip()
                TITLE = ET.SubElement(ROOT, 'Title').text = Title
                # print ('\t', Title)
            elif Content.tag == 'narrative':
                Narrative = Content.text.strip()
                NARRATIVE = ET.SubElement(ROOT, 'Narrative').text = Narrative
                # print ('\t', Narrative)
            elif Content.tag == 'docsetA':
                DocSetA = Content.get('id')
                DocSetAIds = []
                DOCSETA = ET.SubElement(ROOT, 'DocSetA', id=DocSetA)
                # print ('\t', DocSetA)

                SENTENCES = ET.SubElement(ROOT, 'Sentences')

                DocIndex = 1
                for Doc in Content:
                    DocId = Doc.get('id')
                    DocSetAIds.append(DocId)
                    # print('\t\t', DocId)

                    for root, dirs, files in os.walk(DataDir):
                        for file in files:
                            if file.lower().startswith(DocId[0:14].lower()):
                                DocFile = os.path.join(root, file)
                                # print('\t\t\t', DocFile)
                                DocRoot = ET.parse(DocFile).getroot()

                                for DOC in DocRoot:
                                    if DOC.get('id') == DocId:
                                        # print('\t\t\t\t', DOC.tag, DOC.get('id'))
                                        for DocContent in DOC:
                                            if DocContent.tag == 'HEADLINE':
                                                HEADLINE = DocContent.text.strip()
                                                ET.SubElement(DOCSETA, 'doc', id=DocId).text = HEADLINE
                                                # print ('\t\t\t\t\t', HEADLINE)
                                            elif DocContent.tag == 'DATELINE':
                                                DATELINE = DocContent.text.strip()
                                                # print ('\t\t\t\t\t', DATELINE)
                                            elif DocContent.tag == 'TEXT':

                                                Sentences = []
                                                ParagraphIndex = 1

                                                for Paragraph in DocContent:
                                                    paragraph = Paragraph.text.strip().replace('\n', ' ')
                                                    # print (ParagraphIndex, '\t', paragraph)

                                                    sentences = nltk.sent_tokenize(paragraph)
                                                    LineIndex = 1
                                                    for sentence in sentences:
                                                        sentence = sentence.strip()
                                                        # print (DocIndex, '\t', ParagraphIndex, '\t', LineIndex, '\t', sentence)
                                                        Sentences.append(sentence)
                                                        ET.SubElement(SENTENCES, 'sentence', doc=str(DocIndex),
                                                                      para=str(ParagraphIndex),
                                                                      line=str(LineIndex)).text = sentence

                                                        words = nltk.word_tokenize(sentence)
                                                        # print (words)
                                                        for word in words:
                                                            if word not in string.punctuation and word not in IgnoredWords:
                                                                # print ("Ignore", word)
                                                                # else:
                                                                StemWord = PS.stem(word)
                                                                if StemWord in WordsDict.keys():
                                                                    WordsDict[StemWord] += 1
                                                                else:
                                                                    WordsDict[StemWord] = 1
                                                        LineIndex += 1
                                                    ParagraphIndex += 1
                                break
                    # sorted_WORDS = sorted(WORDS.items(), key=operator.itemgetter(1), reverse=True)
                    # print (sorted_WORDS)
                    # print ('\n\n')
                    DocIndex += 1

                    # break

        WORDS = ET.SubElement(ROOT, 'Words')
        sorted_WORDS = sorted(WordsDict.items(), key=operator.itemgetter(1), reverse=True)

        for Item in sorted_WORDS:
            ET.SubElement(WORDS, 'word', text=Item[0], count=str(Item[1]))

            # print (Item[0], Item[1])
        # print (sorted_WORDS)
        # print (Sentences)

        # TREE = ET.ElementTree(ROOT)
        TopicFile = os.path.join(OutputDir, TopicId + '.xml')
        # TREE.write(TopicFile)

        # print (prettify(ROOT))
        try:
            f = open(TopicFile, 'w')
            f.write(prettify(ROOT))
            # rough_string = ET.tostring(ROOT, 'utf-8')
            # xml = xml.dom.minidom.parseString(rough_string)
            # f.write(xml.toprettyxml())
            f.close()
        except IOError:
            print ("Wrong path provided")

        print ("Finish Preprocessing", TopicId)
        # break
    print ('Finish Preprocessing')
