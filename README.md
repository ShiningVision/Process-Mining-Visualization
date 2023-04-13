# Process-Mining-Visualization
Implementation of a desktop app for importing event logs, mining and visualizing process models by using different algorithms (like alpha miner, heuristic miner, inductive miner, fuzzy miner) and metrics for filtering nodes and edges on mined process models. Mined process models can be exported as images.

# Status
This project is in developement. Unfinished and likely contains bugs.

# Usage Interface
Open a CMD in THIS folder and type 'python main.py'.
It will open a desktop application that has a 'File' in the left upper corner.
You can upload CSV or DOT files under the File options and it will be displayed in the App.

### How to run unit tests?

e.g. If you want to run unit tests of `heuristic_mining_test.py`, just type the command below:  
```
python -m unittest tests.heuristic_mining_test
```
in THIS folder.