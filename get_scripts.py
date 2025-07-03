import icarogw 
import numpy as np 
home_folder = '/home/simone.mastrogiovanni/GLADEp_review' 
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
fields_to_take = ['ra', 'dec', 'm_K', 'z', 'sigmaz']
grouping = 'K-band' 
apparent_magnitude_flag = 'm_K' 
nside_mthr = 32 
mthr_percentile = 50.000000 
Nintegration =  np.logspace(np.log10(0.001000),np.log10(0.500000),5000) 
Numsigma = 3 
zcut = 0.500000 
outfile = '/home/simone.mastrogiovanni/GLADEp_tests/icaro_gladep.hdf5' 
subgrouping = 'eps-1' 
band = 'K-glade+' 
epsilon = 1.000000 
NumJobs = 20 

# Writhe the condor files for NaNs and mthr computation
icarogw.utils.write_condor_files_nan_removal_mthr_computation(
home_folder=home_folder,
outfolder=outfolder,
fields_to_take=fields_to_take,
grouping=grouping,apparent_magnitude_flag=apparent_magnitude_flag,
nside_mthr=nside_mthr,mthr_percentile=mthr_percentile,Nintegration=Nintegration,Numsigma=Numsigma,zcut=zcut,NumJobs=NumJobs)
    
# Write the files to inizialize the icarogw file
icarogw.utils.write_condor_files_initialize_icarogw_catalog(home_folder=home_folder,
outfolder=outfolder,outfile=outfile,grouping=grouping)
    
# Write the files to calculate the interpolant
icarogw.utils.write_condor_files_calculate_interpolant(home_folder=home_folder,
outfolder=outfolder,grouping=grouping,subgrouping=subgrouping,
                                                   band=band,
                                                   epsilon=epsilon,
                                                  NumJobs=NumJobs
                                                  )# Write to finish off the catalog
icarogw.utils.write_condor_files_finish_catalog(home_folder=home_folder,
outfolder=outfolder,outfile=outfile, grouping=grouping,subgrouping=subgrouping)
