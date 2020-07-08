"""6.Runnung combinations :)"""
from mikes_mess.input_file import createInputFile, input_file
from mikes_mess.interface import launchExocrossOnlyInput
from mikes_mess.variation import variation
import mikes_mess.qdef as qdef

"""
@todo: repair the interface
"""

def run_job(nram, nprocs, verbose, memory, temperature, range_def, npoints, spectra, profile, profile_params,
            output_file, states_file, transitions_file):
    combinations = variation(states_file)
    # create an input file and run it for each combination making sure the output name is correctly changed to show the changes
    for combination in combinations:
        filename = combination["name"]
        print(filename)
        output_file_temp = {"key": "output", "name": filename}
        # create temp input file
        temp_file = createInputFile(filename)
        input_file(temp_file, nram, nprocs, verbose, memory, temperature, range_def, npoints, spectra, profile,
                   profile_params, output_file_temp, states_file, transitions_file, upper=combination["upper"],
                   lower=combination["lower"])
        # inter.launchExoCrosswithOutputfileSpecified(filename+".inp",filename+".out" , "xcross_dos")
        launchExocrossOnlyInput(filename + ".inp", "xcross_dos")
        # launchExocrossOnlyInput
        print("done")
        # inter.launchExocrossOnlyInput(filename+".inp", "xcross_dos")
        # remove is broken
        # remove(output_file["name"]+"_"+combination["name"]+".inp")
        # command="xcross_dos.exe < "+filename+".inp > "+filename+".out"
        # process=subprocess.Popen(command)
        # print(command)
        # os.system(command)
    pass


run_job(qdef.nram, qdef.nprocs, qdef.verbose, qdef.memory, qdef.temperature, qdef.range_def, qdef.npoints,
        qdef.spectra_type, qdef.profile, qdef.profile_params, qdef.output_file, qdef.states_file, qdef.transtions_file)
