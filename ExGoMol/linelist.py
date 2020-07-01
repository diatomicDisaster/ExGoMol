import pandas as pd
import numpy  as np
from ExGoMol.data import read_space_delimited

"""
@todo: Method for comparing linelists
@body: Implement class method for comparing to another linelist
"""
class LinelistObject:
    """The Linelist object stores information about a linelist dataset in the
    native format. It also contains methods for filtering and sorting the data,
    as well as methods for reading linelists from files and for comparing two
    linelists.
    """
    state_data_types = { #column headers for data linked to states
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
    transition_data_types = { #column headers for data linked to transitions
        "transition_wavenumber": float,
        "einstein_coefficient": float,
        "transition_linestrength": float,
        "transition_intensity": float
    }

    def __init__(self, df):
        self.dataframe = df
        self.dataframe_persistent = df

    def reset_data(self):
        """Resets linelist dataframe to original at initialisation time"""
        self.dataframe = self.dataframe_persistent

    def sort_data(self, **kwargs):
        """Sort linelist using native Pandas sort_values(). If kwargs is None
        then returns linelist to original order.
        arguments:
            by : string or list of strings
                The column name to sort data on.
            ascending : bool or list of bools
                If ascending is True then sort on column in ascending order,
                otherwise sort in descending order.
        """
        if not kwargs:
            self.dataframe = self.dataframe.sort_index(axis=0)
        else:
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
        @help wanted: Is this the cleanest method for implementing filters?
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
                for suffix in self.state_suffixes #apply original filter with each suffix
            ])
        # Apply actual filter
        else:
            left_value, condition, right_value = [str(i) for i in filter_condition]
            self.dataframe = self.dataframe.query(left_value+condition+right_value)
            return

    def _argument_reader(self, *args):
        """Internal method for supporting lazy arguments in linelist diff and 
        ratio methods."""
        # Decipher whether arguments are linelists or column names
        left_linelist, left_column, right_linelist, right_column = [self, None, None, None]
        if args is not None:
            for a, arg in enumerate(args):
                if arg is Linelist:
                    if right_linelist is None:
                        right_linelist = arg
                    else:
                        print("Too many values to assign.")
                elif type(arg) is str:
                    if left_column is None:
                        left_column = arg
                    elif right_column is None:
                        right_column = arg
                    else:
                        print("Too many values to assign.")
                else:
                    print("Argument type not recognised.")
        # Extract the dataframe columns correctly
        if right_linelist is None:
            # Case 1: Comparing single linelist object
            right_linelist = left_linelist
            if right_column is None:
                if type(right_linelist) is MergedLinelist: #assumes left_column is 'keyword_f' or 'keyword_i'
                    # Case 1a: Comparing left and right linelist columns in merged linelist
                    right_column = left_column + '_R'
                    left_column  = left_column + '_L'
                elif type(right_linelist) is Linelist: #assumes left_column is 'keyword'
                    if left_column in left_linelist.state_data_types:
                        # Case 1b: Comparing initial and final state in single linelist
                        right_column = left_column + '_i'
                        left_column  = left_column + '_f'
                    elif left_column in left_linelist.transition_data_types:
                        # Case 1c: Comparing singular transition value (i.e identity)
                        print("Operation invalid: Trying to compare dataframe column to itself.")
                        pass
                    else:
                        print("Column name not recognised.")
                else:
                    print("Operation invalid: Unrecognised linelist object.")
            elif type(right_column) is str:
                # Case 1d: Comparing specific columns of single linelist object
                pass
            else:
                print("'right_column' must be type None or str.")
        else:
            # Case 2: Comparing multiple linelist objects
            if right_column is None:
                # Comparing same quantity in both linelists
                if type(right_linelist) is MergedLinelist:
                    if right_linelist == left_linelist:
                        # Case 2a: Degenerate with case 1a, except right_linelist
                        # is explicity given 
                        right_column = left_column + '_R'
                        left_column  = left_column + '_L'
                    else:
                        # Case 2b: Comparing four linelists across two merges
                        print("Comparing multiple merges is not possible")
                elif type(right_linelist) is Linelist:
                    if right_linelist == left_linelist:
                        # Compare initial and final state value within a linelist
                        if left_column in left_linelist.state_data_types:
                            # Case 2c: Degenerate with case 1b
                            right_column = left_column + '_i'
                            left_column  = left_column + '_f'
                        elif left_column in left_linelist.transition_data_types:
                            # Case 2d: Degenerate with case 1c
                            print("Operation invalid: Trying to compare dataframe column to itself.")
                        else:
                            print("Column name not recognised.")
                    else:
                        if len(right_linelist.dataframe[left_column]) == len(left_linelist.dataframe[left_column]):
                            # Case 2e: Comparing a value between two linelists of equal length
                            right_column = left_column
                        else:
                            # Case 2f: Comparing a value between two linelists of different length
                            print("Merge linelists before comparing.")
                else:
                    print("'right_linelist' must be linelist object.")
            elif type(right_column) is str:
                if len(right_linelist.dataframe[right_column]) == len(left_linelist.dataframe[left_column]):
                    # Case 2g: Comparing specific linelists and columns, all user-specified
                    pass
                else:
                    # Case 2h: Comparing specific linelists columns of different length
                    print("Merge linelists before comparing.")
            else:
                print("'right_column' must be type None or str.")
        return left_linelist.dataframe[left_column], right_linelist.dataframe[right_column]
    
    def ratio(self, *args):
        """The ratio between linelist columns. Behaviour depends on object
        type and the arguments supplied.
        
        If one argument is given, then return the ratio of the two columns with
        'argument' as the prefix for their name in the dataframe. 
            - For single Linelist objects return the ratio of values for the 
              initial and final states, i.e 'argument_final'/'argument_initial'.
            - For a MergedLinelist object return the ratio of values for the
              left and right dataframes, i.e 'argument_left'/'argument_right',
              where 'argument' is not expected to contain the '_f'/'_i' suffix
              if referring to a state value.

        If two arguments are given, and both are column names, then return the
        ratio of the two columns in the dataframe specified by the arguments.

        If two arguments are given, one is a column name, and one is another
        Linelist object, then return the ratio between this column in each
        linelist, provided both linelists have the same length.

        If three arguments are given, two are column names and the third is
        another Linelist object, then return the ratio of the two columns in each
        linelist, provided both linelist columns have the same length.
            - The first column name is assumed to belong to the left linelist 
              (self), and the second to the right linelist (arg).
        """
        left, right = self._argument_reader(*args)
        return left/right

    def diff(self, *args):
        """The difference between linelist columns. Behaviour depends on object
        type and the arguments supplied. See 'Linelist.ratio()' for details."""
        left, right = self._argument_reader(*args)
        return left-right

class Linelist(LinelistObject):
    """Single linelist object."""
    state_suffixes = ['_f', '_i'] #possible suffixes for state data
    transition_suffixes = [] #possible suffixes for transition data

class MergedLinelist(LinelistObject):
    """Merged linelist object for storing two line-by-line matched linelists."""
    state_suffixes = ['_f_L', '_i_L', '_f_R', '_i_R'] #possible suffixes for state data
    transition_suffixes = ['_L', '_R'] #possible suffixes for transition data

def exomol_to_linelist(states_file=None, trans_file=None):
    """Convert ExoMol states and trans file to Linelist."""
    exomol_states_types = Linelist.state_data_types
    """
    @todo Convert to merge operator '|' at python 3.9
    """
    exomol_trans_types  = {
        **Linelist.transition_data_types,
        "state_number_final": int,   #exomol trans files have two 'stateID' columns
        "state_number_initial": int
    }
    # Read '.states' and '.trans' files as space delimited
    states_df = read_space_delimited(states_file, exomol_states_types)
    trans_df  = read_space_delimited(trans_file, exomol_trans_types)
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
    return Linelist(linelist_df)

def file_to_linelist(linelist_file):
    """Convert space delimited file with first row as headers to Linelist"""
    file_column_types = {
        **{key+"_f": Linelist.state_data_types[key] for key in Linelist.state_data_types},
        **{key+"_i": Linelist.state_data_types[key] for key in Linelist.state_data_types},
        **Linelist.transition_data_types
    }
    linelist_df = read_space_delimited(linelist_file, file_column_types)
    return Linelist(linelist_df)

