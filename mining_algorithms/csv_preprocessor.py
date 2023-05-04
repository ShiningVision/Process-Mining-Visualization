import pandas as pd
import csv
import os
'''
For reading in csv files. Returns a list of all cases.
'''
def read(filename, timeLabel = 'timestamp', caseLabel = 'case', eventLabel = 'event'):
        # use csv.Sniffer to detect the delimiter
    with open(filename, 'r') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        delimiter = dialect.delimiter

    # Read the CSV file
    df = pd.read_csv(filename, delimiter = delimiter)

        # check that the required columns exist
    required_columns = [timeLabel, caseLabel, eventLabel]
    if not all(col in df.columns for col in required_columns):
        print("csv_preprocessor.py: Warning: Required columns not found in DataFrame")

        return 0

        # Sort by timestamp
    df = df.sort_values(by=[caseLabel, timeLabel])

        # create a dictionary to store the events for each case
    cases = {}

    for index, row in df.iterrows():

        case = row[caseLabel]
        event = row[eventLabel]
        
        if case in cases:
            cases[case].append(event)
        else:
            cases[case] = [event]
    
    # Save the cases, so it can be loaded in future sessions without read() again:
    array = list(cases.values())

    name = os.path.splitext(os.path.basename(filename))[0]
    print(name)
    destination_path = "saves/"
    destination = destination_path + name + ".txt"

    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))

    with open(destination, "w") as f:
        for case in array:
            for event in case:
                f.write(str(event))
                f.write(" ")
            f.write("\n")
    
    # Return the list of cases
    return array




