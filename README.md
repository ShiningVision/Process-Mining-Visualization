# Process-Mining-Visualization
Implementation of a desktop app for importing event logs, mining and visualizing process models by using different algorithms (like alpha miner, heuristic miner, inductive miner, fuzzy miner) and metrics for filtering nodes and edges on mined process models. Mined process models can be exported as images.

# Status
This project is in developement. Unfinished and likely contains bugs.

# Requirements
Python version 3.10.7 ----- Older versions likely to work as well, but not tested.
Download Python from www.python.org

Required Python libraries are in requirements.txt


# Usage Interface
Open a CMD in THIS folder and type 
```
python main.py
```.
It will open a desktop application that has a 'File' in the left upper corner.
There are a bunch of options here. The main one is 'Heuristic mine CSV'.
Select a csv file and you will get the results of the mining algorithm displayed.

There is also the 'export png' option, that lets you export the image on display as 'graph_viz.png'.

### How to run unit tests?

e.g. If you want to run unit tests of `heuristic_mining_test.py`, just type the command below:

```
python -m unittest tests.heuristic_mining_test

in THIS folder.

# Building on this project
If you want to add your own algorithm to this project, you need to create 2 files minimum.
1. Your [algorithm].py file in mining_algorithms (optional)
2. Your [algorithm]_view.py file in custom_ui (This is your own user interface that can call your algorithm)

In main.py you need to do the following:
1. Add your algorithm name to the 'algorithms' array.
2. Add your algorithm view to the 'algorithmViews' array

In your [algorithm]_view.py file:
1. inherit from algorithm_view_interface.py like in heuristic_graph_view.py
