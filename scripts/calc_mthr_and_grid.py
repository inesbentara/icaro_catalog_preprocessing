import icarogw 
import numpy as np 
import sys 
from astropy.cosmology import FlatLambdaCDM 
from tqdm import tqdm 
cosmo_ref = icarogw.cosmology.astropycosmology(zmax=10.)
cosmo_ref.build_cosmology(FlatLambdaCDM(H0=67.90,Om0=0.3065))
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
grouping = 'K-band' 
apparent_magnitude_flag = 'm_K' 
nside_mthr =  32 
mthr_percentile =  50.000000 
Nintegration =  np.logspace(np.log10(0.001000),np.log10(0.500000),5000) 
Numsigma =  3 
zcut =  0.500000 
bot_pix = int(sys.argv[1])
top_pix = int(sys.argv[2])
filled_pixels = np.genfromtxt('/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep/filled_pixels.txt').astype(int) 
filled_pixels = filled_pixels[bot_pix:top_pix] 
for pix in tqdm(filled_pixels,desc='Calculating apparent magnitude'):
	icarogw.catalog.calculate_mthr_pixelated_files(outfolder,pix,apparent_magnitude_flag,grouping,nside_mthr,mthr_percentile=mthr_percentile)
for pix in tqdm(filled_pixels,desc='Calculating redshift grid'):
	icarogw.catalog.get_redshift_grid_for_files(outfolder,pix,grouping,cosmo_ref,Nintegration=Nintegration,Numsigma=Numsigma,zcut=zcut)
