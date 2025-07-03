import icarogw 
import numpy as np 
from tqdm import tqdm 
import sys 
from astropy.cosmology import Planck15 
cosmo_ref = icarogw.cosmology.astropycosmology(zmax=10.)
cosmo_ref.build_cosmology(Planck15)
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
grouping = 'bJ-band' 
subgrouping = 'eps-1' 
band = 'bJ-glade+' 
epsilon = 1. 
ptype = 'gaussian' 
bot_pix = int(sys.argv[1])
top_pix = int(sys.argv[2])
filled_pixels = np.genfromtxt('/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep/filled_pixels.txt').astype(int) 
z_grid = np.genfromtxt('/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep/bJ-band_common_zgrid.txt') 
filled_pixels = filled_pixels[bot_pix:top_pix] 
for pix in tqdm(filled_pixels,desc='Calculating interpolant'):
	icarogw.catalog.calculate_interpolant_files(outfolder,z_grid,pix,grouping,subgrouping,band,cosmo_ref,epsilon,ptype=ptype)
