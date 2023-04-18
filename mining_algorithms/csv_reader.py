import pandas as pd
'''
For reading in csv files. Returns a list of all cases.
'''
def read(filename):
    # read the CSV file
    df = pd.read_csv(filename)
    
    # check that the required columns exist
    required_columns = ['timestamp', 'case', 'event']
    if not all(col in df.columns for col in required_columns):
        print("Warning: Required columns not found in DataFrame")
        return []

    # sort by timestamp
    df = df.sort_values(by=['case', 'timestamp'])

    # create a dictionary to store the events for each case
    cases = {}

    # iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # get the case and the event
        case = row['case']
        event = row['event']
        
        # add the event to the list of events for the case
        if case in cases:
            cases[case].append(event)
        else:
            cases[case] = [event]
    
    return list(cases.values())