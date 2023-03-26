from score_analysis.dataset import *
from score_analysis.feature import *
from pathlib import Path

dataset_path = Path('./The folk-rnn (v2) Session Book')
abc_filepaths = list(dataset_path.glob('**/*.abc'))[:2]

scores = load_scores_timeout(abc_filepaths)

score = scores[0]

rests_on_strong_ratio(score)

