import pandas as pd

def _read_space_delimited(filename, header_dict):
    """Read a space delimited data file with the first row as headers.
        filename : str
            Name of file to read.
        header_dict : dict
            Dictionary of file headers and data types.
    returns
        df : pandas.DataFrame
            Dataframe of the file's contents
    """
    headers = [_ for _ in header_dict] #list of header strings
    use_columns, _ = _detect_file_headers(filename, headers) #list of known headers
    df = pd.read_csv(filename,
        delim_whitespace=True,
        header=0, #0-th row as headers
        skip_blank_lines=True,
        usecols=[column[1] for column in use_columns],
        dtype={column[0] : header_dict[column[0]] for column in use_columns})
    return df

def _detect_file_headers(filename, headers_to_detect):
    """Detect the headers in a file.
        filename : str
            Name of file to sample first line from.
        heads_to_detect : list-like of strings 
            List of header strings to detect.
    returns
        use_these_columns : list of lists
            List of recognised column headers (str) and their indices (int).
        garbage : list of list
            List of unrecognised column headers (str) and their indices (int).
    """
    use_these_columns = [] #collect recognised columns
    garbage = []
    with open(filename, 'r') as f:
        line = f.readline().rstrip('\n')
        for w, word in enumerate(line.split()):
            if word in headers_to_detect: #if recognised word
                use_these_columns.append([word, w]) #keep word and column index
            else:
                garbage.append([word, w])
        if len(use_these_columns) == 0: #if none known
            return None, garbage
        else:
            return use_these_columns, garbage
    

class Linelist:
    # Linelist dataframe has two of each of these columns: one for the final
    # state (suffix "_f") and another for the initial state (suffix "_i")
    state_data_types = {
        "energy": float,
        "lifetime": float,
        "degeneracy": int,
        "angmom_total": float,
        "angmom_electronic": float,
        "angmom_orbital": int,
        "angmom_spin": float,
        "angmom_proj_total": float,
        "angmom_proj_electronic": float,
        "angmom_proj_orbital": int,
        "angmom_proj_spin": float,
        "vibrational": int,
        "parity_total": str,
        "parity_rotationless": str,
        "electronic_state_no": str
    }
    # Linelist data frame has one of each of these columns, with data specific
    # to transitions between the two states
    transition_data_types = {
        "transition_wavenumber": float,
        "einstein_coefficient": float,
        "transition_linestrength": float,
        "transition_intensity": float
    }
    data_types = {**state_data_types, **transition_data_types} #union of dicts

    def __init__(self):
        self.dataframe = None

    def exomol_to_linelist(self, states_file=None, trans_file=None):
        """Convert ExoMol states and trans file to Linelist."""
        exomol_states_types = {
            "stateID": int, #exomol states files have additional 'stateID' column
            **self.data_types
        }
        exomol_trans_types  = {
            "stateID_final": int,   #exomol trans files have two 'stateID' columns
            'stateID_initial': int,
            **self.data_types
        }
        # Read '.states' and '.trans' files as space delimited
        states_df = _read_space_delimited(states_file, exomol_states_types)
        trans_df  = _read_space_delimited(trans_file, exomol_trans_types)
        # Match final state in trans file to stateID in states file
        linelist_df_ = trans_df.merge(states_df, 
            left_on="stateID_final",
            right_on="stateID",
            how="inner"
        )
        # Match initial state in trans file to stateID in state file
        linelist_df = linelist_df_.merge(states_df,
            left_on="stateID_initial",
            right_on="stateID",
            suffixes=("_f", "_i"),
            how="inner"
        )
        self.dataframe = linelist_df

# Create Linelist object and read dataframe from Exomol format
testLinelist = Linelist()
testLinelist.exomol_to_linelist(
    states_file = "testfiles/test.states",
    trans_file="testfiles/test.trans")

# Just for testing
with open("blah.txt", 'w') as f:
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(testLinelist.dataframe, file=f)
