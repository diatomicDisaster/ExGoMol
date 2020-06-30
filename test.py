from linelist import Linelist, print_df
import matplotlib.pyplot as plt
import numpy as np
import timeit

# Time object creation and comparison method
setup1 = """
from __main__ import Linelist
"""

stmt1 = """
testLinelist = Linelist()
testLinelist.exomol_to_linelist(
    states_file = "testfiles/O2XabQM.states",
    trans_file="testfiles/O2XabQM.trans")
"""

setup2 = """
from __main__ import Linelist
testLinelist = Linelist()
testLinelist.exomol_to_linelist(
    states_file = "testfiles/H2XQM.states",
    trans_file="testfiles/H2XQM.trans")
compareLinelist = Linelist()
compareLinelist.file_to_linelist("testfiles/Komasa.txt")
"""

stmt2 = """
xy = testLinelist.diff(compareLinelist, "einstein_coefficient", func_x="energy_f_L")
"""
print("Time to read 78830 ExoMol transitions: ", timeit.timeit(setup=setup1, stmt=stmt1, number=10)/10)
print("Time to compare with 4713 other transitions: ", timeit.timeit(setup=setup2, stmt=stmt2, number=10)/10)

# Compare Einstein coefficient ratios and wavenumber differences
testLinelist = Linelist()
testLinelist.exomol_to_linelist(
    states_file = "testfiles/H2XQM.states",
    trans_file="testfiles/H2XQM.trans")
testLinelist.filter_data(["energy_f", "<", 25000])
compareLinelist = Linelist()
compareLinelist.file_to_linelist("testfiles/Komasa.txt")

einstein_ratio = testLinelist.ratio(compareLinelist, "einstein_coefficient", func_x="energy_f_L")
np.savetxt('einstein_ratio.txt', einstein_ratio, delimiter='  ')

plt.plot(einstein_ratio[:,0], einstein_ratio[:,1], ls='none', marker='.')
plt.show()

testLinelist.reset_data()
wavenumber_diff = testLinelist.diff(compareLinelist, "transition_wavenumber", func_x="energy_f_L")
np.savetxt('wavenumber_diff.txt', wavenumber_diff, delimiter='  ')

plt.plot(wavenumber_diff[:,0], wavenumber_diff[:,1], ls='none', marker='.')
plt.show()