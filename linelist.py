import pandas as pd

def _read_space_delimited(filename, header_dict):
    """Read a space delimited data file with the first row as headers.
        filename : str
            Name of file to read.
    returns
        df : pandas.DataFrame
            Dataframe of the file's contents
    """
    headers = [_ for _ in header_dict]
    use_columns, _ = _detect_file_headers(filename, headers)
    column_inds    = [column[1] for column in use_columns]
    column_names   = [column[0] for column in use_columns]
    column_types   = {header : header_dict[header] for header in column_names}
    df = pd.read_csv(filename,
        delim_whitespace=True,
        header=0,
        skip_blank_lines=True,
        usecols=column_inds,
        dtype=column_types)
    return df

def _detect_file_headers(filename, headers_to_detect):
    """Detect the headers in a file.
        filename : str
            Name of file to sample first line from.
        heads_to_detect : list-like of strings 
            List of header strings to detect.
    returns
        use_these_columns : list of ints or None
            List of recognised column heaers and their indices.
        garbage : list of list
            List of unrecognised column headers and their indices.
    """
    use_these_columns = []
    garbage = []
    with open(filename, 'r') as f:
        line = f.readline().rstrip('\n')
        for w, word in enumerate(line.split()):
            if word in headers_to_detect:
                use_these_columns.append([word, w])
            else:
                garbage.append([word, w])
        if len(use_these_columns) == 0:
            return None, garbage
        else:
            return use_these_columns, garbage
    
def exomol_to_linelist(states_file=None, trans_file=None):
    """Convert ExoMol states and trans file to Linelist."""

    exomol_states_types = {
        "stateID": int, 
        **Linelist.data_types
    }
    exomol_trans_types  = {
        "stateID_final": int, 
        'stateID_initial': int, 
        **Linelist.data_types
    }
    states_df = _read_space_delimited(states_file, exomol_states_types)
    trans_df  = _read_space_delimited(trans_file, exomol_trans_types)
    linelist_df_ = trans_df.merge(states_df, 
        left_on="stateID_final",
        right_on="stateID",
        how="inner"
    )
    linelist_df = linelist_df_.merge(states_df,
        left_on="stateID_initial",
        right_on="stateID",
        suffixes=("_f", "_i"),
        how="inner"
    )
    return linelist_df

class Linelist:
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
    transition_data_types = {
        "transition_wavenumber": float,
        "einstein_coefficient": float,
        "transition_linestrength": float,
        "transition_intensity": float
    }
    data_types = {**state_data_types, **transition_data_types}

    def __init__(self):
        self.dataframe = None


testLinelist = Linelist()
testLinelist.dataframe = exomol_to_linelist(
    states_file = "testfiles/test.states",
    trans_file="testfiles/test.trans")

with open("blah.txt", 'w') as f:
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(testLinelist.dataframe, file=f)
