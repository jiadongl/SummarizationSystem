# SummarizationSystem-LING573


latest updates (05/30/2018):
Finished the D4.
Work finished so far:
Implement content realization.
Refine content selection with new attributes and different approaches.
To run the project, please condor_submit D4.cmd in src/.



latest updates (05/14/2018):
Finished the D3.
Work finished so far:
Implement information ordering with temporal organization.
Refine content selection with new attributes and different approaches.
Restructured the D2 project.
Fix a lot of bugs for D2.
To run the project, please condor_submit D3.cmd in src/.




latest updates (05/08/2018):
Based on the latest D2 grade comments, I discovered two major issues failed my program running on patas.
1. I was try to writing file to my home directory on patas through the D2 shell script.
2. I was using the training data instead of devset.

In my latest commit 4e3c3c0c2ef8c69be41a369873861fe091b62d86 [4e3c3c0], I have made a large redo for D2 to fix those problems. 
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




