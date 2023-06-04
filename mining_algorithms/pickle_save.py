import pickle

def pickle_save(class_object, dest, name):
    filePath = dest+name+".pickle"
    with open(filePath,'wb') as file:
        pickle.dump(class_object,file)
    return

def pickle_load(path):
    with open(path,'rb') as file:
        load_instance = pickle.load(file)
    return load_instance