## Overview
A simple Dockerized prediction pipeline for selecting the top 11 IPL fantasy players, based on pre-trained models for batsmen and bowlers.
The pipeline takes a CSV file of 22 players as input, calculates fantasy scores, and outputs the best possible squad along with captain/vice-captain selection.
This project is designed for portability and runs fully containerized using Docker


## Repository Structure
```text
fantasy/
├── people.csv                  # Player metadata for mapping IDs
├── requirements.txt            # Python dependencies
├── dream11_2_klystern_weights.ipynb  # Notebook for training and weights analysis
├── create_features.py          # Feature engineering module
├── Dockerfile                  # Docker configuration for containerized runs
├── predict.py                  # Main prediction script
├── features_batsman.txt        # List of features for batsman model
├── features_bowler.txt         # List of features for bowler model
├── model_batsman.pkl           # Pre-trained batsman model
├── model_bowler.pkl            # Pre-trained bowler model
├── names.csv                   # Player name mappings
└── __pycache__/                # Python cache

```
## Setup Instructions

**Setup Environment**

* Activate virtual environment:
  
```bash
python3 -m venv file-path
source /bin/activate
```
* Install dependencies:
```bash
pip install -r requirements.txt
```
**Dockerized Container**

* Build Docker image:
``` bash
docker build -t <file_path>.
```
* Run the container, mounting your path-to-folder:
``` bash
docker run -v <folder_path> <file_path>
```
* Install dependencies:
``` bash
pip install -r requirements.txt
```
**Run the notebook**

* Place the SquadPlayerNames_IndianT20League.xlsx file in your Downloads folder
* Set the match number in predict.py and run the script:
``` python
match_number=76
```
* The predicted team will be saved as in specified path
* 
**Requirements**

* Create virtual environment and activate it
``` text
pandas
numpy
scikit-learn
openpyxl
joblib
```
Make sure to install the appropriate versions consistent with ones used and resolve other permission errors



