"""4. input file set up definition"""
import input_file_fucntion as inpf

def createInputFile(name):
    f = open(str(name)+".inp","w")
    return f

def input_file(inp_file,nram,nprocs,verbose,memory,temperature,range_def,npoints,spectra,profile,profile_params,output_file,states_file,transtions_file,upper=None,lower=None):
    inpf.technical_specs(inp_file,nram,nprocs,verbose,memory)
    inpf.range_grid(inp_file,temperature,range_def,npoints)
    inpf.spectra_section(inp_file,spectra,profile,profile_params)
    if(upper!=None and lower!=None):
        inpf.filter_section(inp_file,upper,lower)
    inpf.file_section(inp_file,output_file,states_file,transtions_file)