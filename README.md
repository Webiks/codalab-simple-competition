# CodaLab simple 2-phase custom scoring
Create a simple 2-phase competition with predictions only with custom scoring

## Ground Truth
The competition has two phases: development and final.  
The ground truth is a file named ```truth.csv```.  
The CSV has two columns: id and prediction.  
For a binary classification prediction shall be 0 or 1.  
The can be modified according to scoring program.

A ground truth for development phase should be under ```reference_dev``` directory.  
Final phase should be under ```reference_final``` directory.

## Scoring Program
The scoring program is defined how to run using ```metadata```, For example:
```metadata
command: python3 $program/scoring.py $input $output
```

The ```$input``` will have two directories:
- ref: the reference data for the phase, i.e. ground truth
- res: unzipped content of the submission.  
  The example scoring program expects a ```prediction.csv``` file to be present.

The ```$output``` expects output of ```scores.txt``` with the format of ```key: value\n```, for example:
```scores.txt
duration: 0,
roc_auc: 0.2,
accuracy: 0.5
```

Modify ```scoring.py``` to create your own metrics.  
The program reads both csvs (truth and prediction), merge them on truth (id column) and calculate metrics.  
The program is used for binary classification.  
In order to handle missing values the program sets in prediction the opposite class.  

## Competition info
Edit ```competition.yaml```.
Update the following:
- title
- description
- start_date
- end_date
- force_submission_to_leaderboard
- has_registration
- html: set html pages (data, evaluation, overview and terms)
- image (or update logo.png)
- phases - update each phase:
  - description
  - label
  - max_submissions
  - max_submissions_per_day
  - start_date
- leaderboard: add/modify files
  - keep duration as first field (rank 1)
  - set actual leaderboard score as second field (rank 2)

## Bundle
To load the competition to CodaLab a bundle.zip must be created.

First create zip file for: reference_dev, reference_final and scoring_program.  
The zip should only contain files and not the parent directory.

For example scoring_program.zip content:
```
metadata
scoring.py
```

Finally create zip for bundle which includes all the files specified in competition.yaml.  
This includes the zips created in previous step and all the files in project's root directory. For example bundle.zip content:  
```
reference_dev.zip
reference_final.zip
scoring_program.zip
competition.yaml
data.html
evaluation.html
logo.png
overview.html
terms.html
```

## Submissions
A submission is a zip file containing ```prediction.csv``` as described above.

## Development

Make sure you are using python 3 (3.7) and not python 2.

Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install required dependencies:
```
pip install pandas numpy scikit-learn
```

Prepare input directory with the following structure:
```
ref
- truth.csv
res
- prediction.csv
```

Create an output directory for results.

Run the script
```bash
python scoring_program/scoring.py INPUT_DIR OUTPUT_DIR
```

If all is well ```scores.txt``` is created and contains scores.  
Now edit ```scoring.py```, change ```truth.csv``` and ```prediction.csv``` and run again.