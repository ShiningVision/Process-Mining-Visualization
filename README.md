# Process-Mining-Visualization
Implementation of a desktop app for importing event logs, mining and visualizing process models by using different algorithms (like alpha miner, heuristic miner, inductive miner, fuzzy miner) and metrics for filtering nodes and edges on mined process models. Mined process models can be exported as images.

# Status
This project is in developement. Unfinished and likely contains bugs.

# Requirements
Python version 3.10.7 ----- Older versions likely to work as well, but not tested.
Download Python from www.python.org

Required Python libraries are in requirements.txt and can be installed with
```
pip install -r requirements.txt
```

PyGraphviz
This package is notoriously challenging to install. Especially on windows. It is required for the experimental dot editor. If you are not using the "edit dot file" option in the File menu. You don't need it.


# Usage Interface
Open a CMD in THIS folder and type 
```
python main.py
```

It will open a desktop application.
The lower right button lets you select a CSV file and mine it. Your CSV data will be saved for later.
The lower left button lets you load saved data, if you have any.

There are also the 'export png' and 'export svg' options under 'File', that lets you export the image on display as 'graph_viz.png' or 'graph_viz.svg'.

### How to run unit tests?

e.g. If you want to run unit tests of `heuristic_mining_test.py`, just type the command below:

```
python -m unittest tests.heuristic_mining_test
```

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
2. The export svg/png/dot functions in export_view.py only copy graphviz.[file extension] from the temp folder to the desired destination. It is your responsibility to generate those files in the functions required by algorithm_view_interface.py
