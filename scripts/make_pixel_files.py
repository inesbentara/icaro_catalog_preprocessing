import icarogw 
import h5py 
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
nside = 64 
with h5py.File('/home/cbc.cosmology/catalogs_for_analyses/glade+/glade+.hdf5','r') as cat:
	icarogw.catalog.create_pixelated_catalogs(outfolder,nside,{key:cat[key] for key in ['ra','dec','sigmaz','z','m_K','m_bJ']})
icarogw.catalog.clear_empty_pixelated_files(outfolder,nside) 
