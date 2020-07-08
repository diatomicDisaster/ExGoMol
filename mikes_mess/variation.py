"""5. Variational function for states bands"""
import pandas as pd
from pathlib import Path


def variation(states_file):
    states_frame = pd.read_table(states_file["name"], header=None, delim_whitespace=True, index_col=0)
    states_frame.columns = ["energy", "NN", "J", "lande", "parity", "e/f", "state", "v", "omega", "lambda", "sigma"]
    # unique combinations

    """
    @todo: create ability to be selective about types of combinations
    @body: need to expand the combinatorial filtering ability
    """
    states_values = states_frame.state.unique()
    states_values = states_values.tolist()
    singlets = [s for s in states_values if "1" in s]
    singlet_pi = singlets.pop(2)
    triplets = [s for s in states_values if "3" in s]
    triplet_pi =triplets.pop(0)
    ground_state = states_values.pop(0)
    combinations = []

    for state in states_values:
        upper = {"key": "upper", "column": 8, "value": state}
        lower = {"key": "lower", "column": 8, "value": ground_state}
        combo = {"name": ground_state + "-" + state, "upper": upper, "lower": lower}
        combinations.append(combo)

    for state in singlets:
        upper = {"key": "upper", "column": 8, "value": state}
        lower = {"key": "lower", "column": 8, "value": singlet_pi}
        combo = {"name": singlet_pi + "-" + state, "upper": upper, "lower": lower}
        combinations.append(combo)

    for state in triplets:
        upper = {"key": "upper", "column": 8, "value": state}
        lower = {"key": "lower", "column": 8, "value": triplet_pi}
        combo = {"name": triplet_pi + "-" + state, "upper": upper, "lower": lower}
        combinations.append(combo)
    return combinations


#variation({"name": "PN_absorption_spectra_all_horiz.states"})
#print("done")
