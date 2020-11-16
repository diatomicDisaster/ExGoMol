from ExGoMol import linelist as ex 

duoLL = ex.exomol_to_linelist(
  states_file='O2XabQM-CASSCF-MRCIQ-aug-cc-pV6Z.states',
  trans_file='O2XabQM-CASSCF-MRCIQ-aug-cc-pV6Z.trans'
)

hitLL = ex.hitran_to_linelist(
  
)