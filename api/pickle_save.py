import pickle

# Saves the class object as a pickle file. filename is the full path
def pickle_save(class_object, filename):
    filePath = filename+".pickle"
    with open(filePath,'wb') as file:
        pickle.dump(class_object,file)

# Loads the class object that was saved as a pickle file. path should include filename
def pickle_load(path):
    with open(path,'rb') as file:
        load_instance = pickle.load(file)
    return load_instance