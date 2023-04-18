# Process-Mining-Visualization
Implementation of a desktop app for importing event logs, mining and visualizing process models by using different algorithms (like alpha miner, heuristic miner, inductive miner, fuzzy miner) and metrics for filtering nodes and edges on mined process models. Mined process models can be exported as images.

# Status
This project is in developement. Unfinished and likely contains bugs.

# Requirements
Python version 3.10.7 ----- Older versions likely to work as well, but not tested.
Download Python from www.python.org

networkx ----- this dependency might be removed later as I use graphviz instead.
graphviz
pandas
If you have not installed these python-libraries, you can download networkx and graphviz simply with 
```
pip install graphviz
pip install networkx
pip install pandas
```


# Usage Interface
Open a CMD in THIS folder and type 
```
python main.py
```.
It will open a desktop application that has a 'File' in the left upper corner.
There are a bunch of options here. The main one is 'Heuristic mine CSV'.
Select a csv file and you will get the results of the mining algorithm displayed.

There is also the 'export' option, that lets you export the image on display as 'graph_viz.png'.

### How to run unit tests?

e.g. If you want to run unit tests of `heuristic_mining_test.py`, just type the command below:  
```
python -m unittest tests.heuristic_mining_test
```
in THIS folder.