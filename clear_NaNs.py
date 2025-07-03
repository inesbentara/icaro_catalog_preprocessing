import icarogw 
import numpy as np 
import sys 
from tqdm import tqdm 
outfolder = '/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep' 
fields_to_take = ['ra', 'dec', 'm_K', 'z', 'sigmaz']
grouping = 'K-band' 
bot_pix = int(sys.argv[1])
top_pix = int(sys.argv[2])
filled_pixels = np.genfromtxt('/home/simone.mastrogiovanni/GLADEp_review/pixelated_gladep/filled_pixels.txt').astype(int) 
filled_pixels = filled_pixels[bot_pix:top_pix] 
for pix in tqdm(filled_pixels,desc='Cleaning pixel'):
	icarogw.catalog.remove_nans_pixelated_files(outfolder,pix,fields_to_take,grouping)
