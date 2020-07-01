"""6.Runnung combinations :)"""
import subprocess
from input_file import input_file
import interface as inter
import input_file as inp
import qdef as qdef
import variation as v

def run_job(nram,nprocs,verbose,memory, temperature,range_def,npoints,spectra,profile,profile_params,output_file,states_file,transtions_file):
    #setup environment ( only in windows I think):
    #inter.prepEnvironment()
    combinations=v.variation(states_file)
    #create an input file and run it for each combination making sure the output name is correctly changed to show the changes
    for combination in combinations:
        filename=combination["name"]
        print(filename)
        output_file_temp={"key":"output","name":filename}
        #create temp input file
        temp_file=inp.createInputFile(filename)
        inp.input_file(temp_file,nram,nprocs,verbose,memory,temperature,range_def,npoints,spectra,profile,profile_params,output_file_temp,states_file,transtions_file,upper=combination["upper"],lower=combination["lower"])
        #inter.launchExoCrosswithOutputfileSpecified(filename+".inp",filename+".out" , "xcross_dos")
        inter.launchExocrossOnlyInput(filename+".inp","xcross_dos")
        #launchExocrossOnlyInput
        print("done")
        #inter.launchExocrossOnlyInput(filename+".inp", "xcross_dos")
        #remove is broken
        #remove(output_file["name"]+"_"+combination["name"]+".inp")
        #command="xcross_dos.exe < "+filename+".inp > "+filename+".out"
        #process=subprocess.Popen(command)
        #print(command)
        #os.system(command)
    pass

run_job(qdef.nram,qdef.nprocs,qdef.verbose,qdef.memory, qdef.temperature,qdef.range_def,qdef.npoints,qdef.spectra_type,qdef.profile,qdef.profile_params,qdef.output_file,qdef.states_file,qdef.transtions_file)


