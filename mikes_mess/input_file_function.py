"""3. Input file creation functions (printing functions)"""

def value_write_from_dict(file,dictionary):
    for k,v in dictionary.items():
        if(v!="" and v!=None):
            file.write(str(v)+" ")
    file.write(" \n")

def header_write_from_dict(file,dictionary):
    for k,v in dictionary.items():
        if(v!="" and v!=None and v>0):
            file.write(str(k)+" ")
    file.write(" \n")

def pair_write_from_dict(file,dictionary):
    for k,v in dictionary.items():
        if(v!="" and v!=None):
            file.write(str(k)+" "+str(v))
    file.write(" \n")

def technical_specs(file,nram,nprocs,verbose,memory):
    file.write("(Technical Set up) \n")
    value_write_from_dict(file,memory)
    value_write_from_dict(file,nram)
    value_write_from_dict(file,nprocs)
    value_write_from_dict(file,verbose)
    file.write("\n")

def range_grid(file,temperature,range_def,npoints):
    file.write("(Range definiton) \n")
    value_write_from_dict(file,temperature)
    value_write_from_dict(file,range_def)
    value_write_from_dict(file,npoints)
    file.write("\n")

def file_section(file,output_file,states_file,transitions_file):
    file.write("(File definitions Section) \n")
    value_write_from_dict(file,output_file)
    value_write_from_dict(file,states_file)
    value_write_from_dict(file,transitions_file)
    file.write("\n")

def spectra_section(file,spectra_type,profile,profile_params):
    file.write("(Spectra definitions Section) \n")
    header_write_from_dict(file,spectra_type)
    header_write_from_dict(file,profile)
    pair_write_from_dict(file,profile_params)
    file.write("\n")

"""
@todo: make filter section plyatomic/multicolumn compatible
@body: current filter structure relies on two separate dictionaries (lower and upper) to be of a simple format encompassing one column. 
"""

def filter_section(file,upper,lower):
    file.write("(filter section) \n")
    file.write("filter \n")
    value_write_from_dict(file,upper)
    value_write_from_dict(file,lower)
    file.write("end \n")
    file.write("\n")
