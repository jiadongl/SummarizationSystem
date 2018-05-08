import os
import sys
import RawData
import ScoreData

if __name__ == "__main__":

    InputDir = 'data/Preprocess/'
    OutputDir = 'data/Score/'

    if len(sys.argv) > 1:
        InputDir = sys.argv[1]
        OutputDir = sys.argv[2]

    for f in os.listdir(InputDir):
        if not f.startswith('.'):
            print('Scoring: ', f)
            input_path = os.path.join(InputDir, f)
            output_path = os.path.join(OutputDir, f)
            raw_data = RawData.RawData()
            raw_data.load(input_path)
            feature_data = ScoreData.ScoreData()
            feature_data.calculate(raw_data)
            feature_data.save(output_path)

    print('Scoring Finished')
