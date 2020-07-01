"""5. Variational function for states bands"""
import numpy
import pandas as pd

def variation(states_file):
    states_frame= pd.read_table(states_file["name"],header=None,delim_whitespace=True,index_col=0)
    states_frame.columns= ["energy","NN","J","lande","parity","e/f","state","v","omega","lambda","sigma"]
    #unique combinations

    """
    @todo: create ability to be selective about types of combinations
    @body: need to expand the combinatorial filtering ability
    """
    states_values=states_frame.state.unique()
    states_values=states_values.tolist()
    singlets=[s for s in states_values if "1" in s]
    triplets=[s for s in states_values if "3" in s]
    ground_state=states_values.pop(0)
    combinations=[]

    for state in states_values:
        upper={"key":"upper","column":8,"value":state}
        lower={"key":"lower","column":8,"value":ground_state}
        combo={"name":ground_state+"-"+state,"upper":upper,"lower":lower}
        combinations.append(combo)
    
    return combinations