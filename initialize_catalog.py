import icarogw 
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
outfile = '/home/simone.mastrogiovanni/GLADEp_review/icaro_gladep.hdf5' 
grouping = 'bJ-band' 
icarogw.catalog.initialize_icarogw_catalog(outfolder,outfile,grouping)
