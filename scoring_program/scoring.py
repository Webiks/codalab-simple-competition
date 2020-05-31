import sys
import json
import os
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score
from math import isnan

input_dir = sys.argv[1]
output_dir = sys.argv[2]

reference_dir = os.path.join(input_dir, 'ref')
prediction_dir = os.path.join(input_dir, 'res')

print('Reading prediction')
prediction = pd.read_csv(os.path.join(prediction_dir, 'prediction.csv'))
truth = pd.read_csv(os.path.join(reference_dir, 'truth.csv'))

print('Merging')
merged = pd.merge(truth, prediction, how='left', on=['id'])
# set oppsite class on missing values
for i, row in merged.iterrows():
    if isnan(row['prediction_y']):
        merged.loc[i, 'prediction_y'] = 1 - row['prediction_x']
truth = merged['prediction_x']
prediction = merged['prediction_y']

print('Calculating scores')
accuracy = accuracy_score(truth, prediction)
roc_auc = roc_auc_score(truth, prediction)
scores = {
    'roc_auc': roc_auc,
    'accuracy': accuracy
}
print('scores: ', scores)

with open(os.path.join(output_dir, 'scores.txt'), 'w') as score_file:
    score_file.write('roc_auc: %0.12f\n' % roc_auc)
    score_file.write('accuracy: %0.12f\n' % accuracy)
    score_file.write('duration: 0\n')
