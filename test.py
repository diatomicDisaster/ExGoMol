from linelist import Linelist, MergedLinelist, exomol_to_linelist, file_to_linelist
from data import y_as_fx, compare_dataframes
import matplotlib.pyplot as plt
import numpy as np
import timeit

# Dataframe printer
def print_df(df, fname="blah.txt", cols=None):
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.width', 1000)
    with open(fname, 'a') as f:
        if cols:
            print(df[cols], file=f)
        else:
            print(df, file=f)

#### Test 1 ###
## Time object creation and comparison method
# setup1 = """
# from __main__ import Linelist
# from methods import y_as_fx, compare_dataframes, diff, ratio
# """

# stmt1 = """
# testLinelist = Linelist()
# testLinelist.exomol_to_linelist(
#     states_file = "testfiles/O2XabQM.states",
#     trans_file="testfiles/O2XabQM.trans")
# """

# setup2 = """
# from __main__ import Linelist
# from methods import y_as_fx, compare_dataframes, diff, ratio
# testLinelist = Linelist()
# testLinelist.exomol_to_linelist(
#     states_file = "testfiles/H2XQM.states",
#     trans_file="testfiles/H2XQM.trans")
# compareLinelist = Linelist()
# compareLinelist.file_to_linelist("testfiles/Komasa.txt")
# """

# stmt2 = """
# einstein_ratio = ratio(testLinelist.dataframe, compareLinelist.dataframe, "einstein_coefficient", func_x="energy_f_L")
# """
# print("Time to read 78830 ExoMol transitions: ", timeit.timeit(setup=setup1, stmt=stmt1, number=10)/10)
# print("Time to compare with 4713 other transitions: ", timeit.timeit(setup=setup2, stmt=stmt2, number=10)/10)


### Test 2 ###
# Compare i and f state energies
testLinelist = exomol_to_linelist(
    states_file="testfiles/O2XabQM.states",
    trans_file="testfiles/O2XabQM.trans"
)
testLinelist.dataframe['energy_diff'] = testLinelist.diff("energy")

# Plot result as function of transition energy (should plot a straight line with unit gradient)
energy_diff = y_as_fx(testLinelist.dataframe, x="transition_wavenumber", y="energy_diff")
np.savetxt("energy_diff.txt", energy_diff, delimiter='  ')
plt.plot(energy_diff[:,0], energy_diff[:,1], ls='none', marker='.')
plt.show()

### Test 3 ###
# Compare Einstein coefficient ratios and wavenumber differences
testLinelist = exomol_to_linelist(
    states_file = "testfiles/H2XQM.states",
    trans_file="testfiles/H2XQM.trans"
) #load exomol linelist
compareLinelist = file_to_linelist("testfiles/Komasa.txt") #load Komasa linelist
testLinelist.filter_data(["energy_f", "<", 25000]) #apply filter to final energies
merged = compare_dataframes(testLinelist.dataframe, compareLinelist.dataframe) #merge dataframes
mergedLinelist = MergedLinelist(merged) #initialise merged linelist

merged['einstein_coefficient_ratio'] = mergedLinelist.ratio("einstein_coefficient") #ratio of As
testLinelist.reset_data()
merged['transition_wavenumber_diff'] = mergedLinelist.diff("transition_wavenumber") #difference of nus

# Plot results as function of final state energy
einstein_ratio = y_as_fx(merged, x='energy_f_L', y='einstein_coefficient_ratio')
np.savetxt('einstein_ratio.txt', einstein_ratio, delimiter='  ')

wavenumber_diff = y_as_fx(merged, x="energy_f_L", y="transition_wavenumber_diff")
np.savetxt("wavenumber_diff.txt", wavenumber_diff, delimiter='  ')

plt.plot(einstein_ratio[:,0], einstein_ratio[:,1], ls='none', marker='.')
plt.show()

plt.plot(wavenumber_diff[:,0], wavenumber_diff[:,1], ls='none', marker='.')
plt.show() 