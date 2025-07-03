import icarogw 
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
outfile = '/home/simone.mastrogiovanni/GLADEp_review/icaro_gladep.hdf5' 
grouping = 'bJ-band' 
subgrouping = 'eps-1' 
icat = icarogw.catalog.icarogw_catalog(outfile,grouping,subgrouping)
icat.build_from_pixelated_files(outfolder)
icat.save_to_hdf5_file()
