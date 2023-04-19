import pandas as pd
import csv
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
    print(timeLabel, caseLabel, eventLabel)
    print(filename)
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
    
    return list(cases.values())