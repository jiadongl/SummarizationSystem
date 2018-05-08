# SummarizationSystem-LING573

latest updates (05/08/2018):
Based on the latest D2 grade comments, I discovered two major issues failed my program running on patas.
1. I was try to writing file to my home directory on patas through the D2 shell script.
2. I was using the training data instead of devset.

In my latest commit , I have made a large redo for D2 to fix those problems. 
I also fixed some related filename and directory nesting issue.
Now I think it is safe to run my program on patas.



last commit:

The data set I used for the D2 is /home2/jiadongl/dropbox/17-18/573/Data/Documents/training/2009/UpdateSumm09_test_topics.xml

To run this Summarization system, you need to download the whole src dir to the patas and condor submit the D2.cmd in the src.

The preprocessed data will be stored in /home2/jiadongl/tmp/573/sandbox/PreprocessedData/ 

The feature data will be stored in /home2/jiadongl/tmp/573/sandbox/FeatureExtractionData/

The sentence score data will be stored in /home2/jiadongl/tmp/573/sandbox/SentenceScoringData/

The output of result will be stored in /home2/jiadongl/tmp/573/sandbox/SentenceSelectionData/

The config file evaluation result by ROUGE is in the result dir of this repository.




