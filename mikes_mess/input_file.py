from mikes_mess.input_file_fucntion import file_section, filter_section, spectra_section, range_grid, technical_specs


def createInputFile(name):
    f = open(str(name)+".inp","w")
    return f

def input_file(inp_file,nram,nprocs,verbose,memory,temperature,range_def,npoints,spectra,profile,profile_params,output_file,states_file,transtions_file,upper=None,lower=None):
    technical_specs(inp_file,nram,nprocs,verbose,memory)
    range_grid(inp_file,temperature,range_def,npoints)
    spectra_section(inp_file,spectra,profile,profile_params)
    if(upper!=None and lower!=None):
        filter_section(inp_file,upper,lower)
    file_section(inp_file,output_file,states_file,transtions_file)