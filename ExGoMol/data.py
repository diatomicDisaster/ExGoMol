import pandas as pd
import numpy  as np

def y_as_fx(dataframe, x=None, y=None):
    """Return data series x and y from the dataframe as a (n, 2) ndarray,
    sorted by increasing x value."""
    xy = dataframe[[x, y]].to_numpy()
    return xy[xy[:,0].argsort()]

"""
@todo: Add method for merging linelists.
@body: Add a Linelist method for merging self to another Dataframe via this method
"""
def compare_dataframes(left_df, right_df, 
    merge_on=[
        "angmom_total_f", "angmom_total_i", 
        "vibrational_f", "vibrational_i"
    ]):
    """Internal method for retrieving comparisons to other linelists"""
    return left_df.merge(right_df,
        how='inner',
        on=merge_on,
        suffixes=("_L", "_R")
    )

def read_space_delimited(filename, header_dict):
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
        index_col=False,
        header=0, #0-th row as headers
        skip_blank_lines=True,
        usecols=[column[1] for column in use_columns],
        dtype={column[0] : header_dict[column[0]] for column in use_columns}
    )
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

def is_iterable(obj, strings=False):
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
