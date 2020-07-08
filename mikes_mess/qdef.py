"""1. Quickly sciprted parameters for test runs"""
memory={"key":"mem","size":8,"units":"gb"}
nram={"key":"nram","size":10000000}
nprocs = {"key":"nprocs","size":6}
"""
@todo: add an ability to calculate npoints size as a function of range_def
@body: the user should be able to define the fraction, which determines the accuracy of the grid. 1 would be an example of 1 point for each cm. We need to consider what would happen when the definition comes from   wavelength rather than per cm
"""
npoints = {"key":"npoints","size":60000}
verbose = {"key":"verbose","size":4}
temperature={"key":"Temperature","q1":2000,"q2":None}
range_def={"key":"Range","q1":0,"q2":60000,"units":""}
"""
@todo: add a check that only one option is selected in some dictionaries
@body: variables that require such check are spectra and profile 
"""
spectra_type={"absorption":1,"emission":0, "lifetimes":0}

"""
@todo:add per profile type keywords as part of class expansion
@body: need to make sure correct keywords, print and other type of functionality exist per profile type
"""
profile={"Gaussian":1, "Gauss":0, "Gauss0":0, "Doppler":0, "Doppl":0, "Doppl0":0, "Box":0, "Bin":0, "Rect":0, "Sticks":0, "Stick":0, "Voigt":0, "pseudo":0, "pse-Rocco":0, "pse-Liu":0, "Voig-Quad":0}

profile_params={"hwhm":1.0}
output_file={"key":"output","name":"PN_2000K_gauss"}

"""
@todo: add the ability to select files from path
@body: currently can run 
"""
states_file= {"key":"States","name":"PN_absorption_spectra_all_horiz.states"}
transtions_file= {"key":"Transitions","name":"PN_absorption_spectra_all_horiz.trans"}
