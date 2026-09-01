import pickle
import os



def store_data(save_file, save_kwd):
    with open(f'{save_kwd}.pkl', 'wb') as f:
        pickle.dump(save_file, f)

def load_data(save_kwd):
    wd = os.getcwd()
    wd_files = os.listdir(wd)
    if f'{save_kwd}.pkl' in wd_files:
        with open(f'{save_kwd}.pkl', 'rb') as f:
            load = pickle.load(f)
            return load
    else:
        return None

