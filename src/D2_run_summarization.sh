#!/bin/sh

./Preprocessing.sh /home2/jiadongl/dropbox/17-18/573/Data/Documents/training/2009/UpdateSumm09_test_topics.xml /home2/jiadongl/dropbox/17-18/573/AQUAINT-2 /home2/jiadongl/tmp/573/sandbox/PreprocessedData/
./FeatureExtraction.sh /home2/jiadongl/tmp/573/sandbox/PreprocessedData/ /home2/jiadongl/tmp/573/sandbox/FeatureExtractionData/
./SentenceScoring.sh /home2/jiadongl/tmp/573/sandbox/FeatureExtractionData/ /home2/jiadongl/tmp/573/sandbox/SentenceScoringData/
./SentenceSelection.sh /home2/jiadongl/tmp/573/sandbox/SentenceScoringData/ /home2/jiadongl/tmp/573/sandbox/SentenceSelectionData/
