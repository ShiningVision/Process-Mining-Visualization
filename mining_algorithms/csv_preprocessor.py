import pandas as pd
import csv
import os
from PyQt5.QtWidgets import QFileDialog
'''
For reading in csv files. Returns a list of all cases.
'''
def read(filename, timeLabel = 'timestamp', caseLabel = 'case', eventLabel = 'event'):
    # use csv.Sniffer to detect the delimiter
    with open(filename, 'r') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        delimiter = dialect.delimiter

    # read the CSV file
    df = pd.read_csv(filename, delimiter = delimiter)
    #print(timeLabel, caseLabel, eventLabel)
    #print(filename)
    # check that the required columns exist
    required_columns = [timeLabel, caseLabel, eventLabel]
    if not all(col in df.columns for col in required_columns):
        print("Warning: Required columns not found in DataFrame")

        return []

    # sort by timestamp
    df = df.sort_values(by=[caseLabel, timeLabel])

    # create a dictionary to store the events for each case
    cases = {}

    # iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # get the case and the event
        case = row[caseLabel]
        event = row[eventLabel]
        
        # add the event to the list of events for the case
        if case in cases:
            cases[case].append(event)
        else:
            cases[case] = [event]
    
    #save the cases, so it can be loaded in future sessions without read() again:
    array = list(cases.values())

    # Extract the name of the file from filepath
    name = os.path.splitext(os.path.basename(filename))[0]
    print(name)
    destination_path = "temp/saves/"
    destination = destination_path + name + ".txt"

    # Save array to destination.

    with open(destination, "w") as f:
        for case in array:
            for event in case:
                f.write(str(event))
                f.write(" ")
            f.write("\n")
            
    return array




