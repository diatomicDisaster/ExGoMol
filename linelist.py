import pandas as pd

def is_iterable(object, strings=False):
    """Check if object is iterable, return boolean result.
    arguments
        obj : object
            Any Python object.
        strings : bool
            If false, strings don't count as iterables.
    """
    try:
        iter(obj)
    except Exception:
        return False
    else:
        if type(obj) is str:
            return False
        else:
            return True

def _read_space_delimited(filename, header_dict):
    """Read a space delimited data file with the first row as headers.
    arguments
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
    """Detect the headers in the first line of a file from a given list.
    arguments
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
    
"""
@todo: Method for comparing linelists
@body: Implement class method for comparing to another linelist
"""
class Linelist:
    """The Linelist object stores information about a linelist dataset in the
    native format. It also contains methods for filtering and sorting the data,
    as well as methods for reading linelists from files and for comparing two
    linelists.
    """
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
        "electronic_state": str,
        "state_number": int
    }
    # Linelist data frame has one of each of these columns, with data specific
    # to transitions between the two states
    transition_data_types = {
        "transition_wavenumber": float,
        "einstein_coefficient": float,
        "transition_linestrength": float,
        "transition_intensity": float
    }

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def reset_data(self):
        self.dataframe = self.dataframe_persistent

    def sort_data(self, **kwargs):
        """Sort linelist using native Pandas sort_values(). Important keyword
        arguments are:
            by : string or list of strings
                The column name to sort data on.
            ascending : bool or list of bools
                If ascending is True then sort on column in ascending order,
                otherwise sort in descending order.
        """
        self.dataframe = self.dataframe.sort_values(**kwargs)

    def filter_data(self, filter_condition):
        """Filter linelist data according to some condition or series of conditions.
        arguments
            filter_condition : list or list of lists
                The filter(s) to apply in the form [left, condition, right] where 
                either one or both of left/right are linelist data series and
                condition is a Python comparator.
        """
        """
        @todo: Is this the cleanest method for implementing filters?
        @body: Applying sequential filters may be time consuming, and it is 
        already possible to apply multiple filters with Pandas, however this 
        obfuscates syntax for the user.
        """
        # If a list of filters is supplied, recursively call with each filter
        if any(isinstance(elem, list) for elem in filter_condition):
            for filter_condition_ in filter_condition:
                self.filter_data(filter_condition_)
            return
        # If filter applied without '_f' or '_i' suffix, apply filter to both states
        elif any(value in self.state_data_types for value in filter_condition[::2]):
            self.filter_data([
                [_+suffix if _ in self.state_data_types else _ for _ in filter_condition] 
                for suffix in ["_f", "_i"] #apply original filter with each suffix
            ])
        # Apply actual filter
        else:
            left_value, condition, right_value = [str(i) for i in filter_condition]
            self.dataframe = self.dataframe.query(left_value+condition+right_value)
            return

    def exomol_to_linelist(self, states_file=None, trans_file=None):
        """Convert ExoMol states and trans file to Linelist."""
        exomol_states_types = self.state_data_types
        exomol_trans_types  = {
            "state_number_final": int,   #exomol trans files have two 'stateID' columns
            'state_number_initial': int,
            **self.transition_data_types
        }
        # Read '.states' and '.trans' files as space delimited
        states_df = _read_space_delimited(states_file, exomol_states_types)
        trans_df  = _read_space_delimited(trans_file, exomol_trans_types)
        # Match final state in trans file to stateID in states file
        linelist_df_ = trans_df.merge(states_df, 
            left_on="state_number_final",
            right_on="state_number",
            how="inner"
        )
        # Match initial state in trans file to stateID in state file
        linelist_df = linelist_df_.merge(states_df,
            left_on="state_number_initial",
            right_on="state_number",
            suffixes=("_f", "_i"),
            how="inner"
        )
        self.dataframe = linelist_df
        self.dataframe_persistent = linelist_df



# Create Linelist object and read dataframe from Exomol format
testLinelist = Linelist()
testLinelist.exomol_to_linelist(
    states_file = "testfiles/O2XabQM.states",
    trans_file="testfiles/O2XabQM.trans")
testLinelist.sort_data(by="energy_f", ascending=False)
testLinelist.filter_data([
    ["angmom_total_i", "==", "angmom_total_f"]
])

# Just for testing
with open("blah.txt", 'w') as f:
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.width', 1000)
    print(testLinelist.dataframe, file=f)
