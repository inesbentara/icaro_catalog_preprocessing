
# Icaro Catalog Preprocessing

This repository provides a standalone, reproducible workflow to preprocess galaxy catalogs for use with the [IcaroGW](https://github.com/simone-mastrogiovanni/icarogw) cosmological inference pipeline.  
It supports splitting the catalog into sky pixels, cleaning, thresholding, and generating all necessary summary statistics for “dark siren” cosmology.

---

## Workflow Overview

1. **Pixelization:** Split the full galaxy catalog into HEALPix sky pixels.
2. **Cleaning:** Remove galaxies with invalid or missing data.
3. **Magnitude Thresholding & Gridding:** Compute completeness thresholds and setup grid for statistical analysis.
4. **Interpolant Construction:** Build the cumulative galaxy distribution used for fast cosmological likelihoods.
5. **Final Output:** Save a ready-to-use HDF5 catalog with all products for IcaroGW.

---

## Requirements

- Python 3.8+
- [healpy](https://healpy.readthedocs.io/)
- [h5py](https://www.h5py.org/)
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- tqdm

Install all requirements with:
```bash
pip install -r requirements.txt
```

---

## Input Catalog Format

Your input galaxy catalog must be an HDF5 file with at least these datasets:
- `ra` (float, degrees or radians)
- `dec` (float, degrees or radians)
- `z` (float, redshift)
- `sigmaz` (float, redshift uncertainty)
- Photometric bands: e.g., `m_K`, `m_bJ` (float, magnitudes)
- (optionally) `skymap_indices`, `GLADE_obj`, etc.

**Example structure:**
```
/ra                  Dataset {N}
/dec                 Dataset {N}
/z                   Dataset {N}
/sigmaz              Dataset {N}
/m_K                 Dataset {N}
/m_bJ                Dataset {N}
```

---

## Usage

**1. Configure your parameters.**  
Edit `make_files.py` (or your own wrapper) to set:
- Path to your input catalog
- Output folder
- HEALPix nside
- Epsilon (weighting parameter)
- Photometric band(s)

**2. Pixelize the Catalog**
```bash
python make_files.py
```

**3. Clean pixel files of NaNs**
```bash
python clear_NaNs.py path/to/pixel_xxxx.hdf5 path/to/pixel_xxxx_clean.hdf5
# (repeat for all pixels, or batch-process)
```

**4. Compute Magnitude Thresholds and Grids**
```bash
python calc_mthr_and_grid.py
```

**5. Initialize the Master Catalog**
```bash
python initialize_catalog.py
```

**6. Build the Interpolant**
```bash
python calc_interpolant.py
```

**7. Finish and aggregate**
```bash
python finish_catalog.py
```

---

## Key Parameters

- **nside:** HEALPix resolution (higher = finer pixels).
- **epsilon:** Luminosity weighting (0 = uniform, 1 = by luminosity).
- **band:** Photometric band to use for thresholds.
- **mthr_percentile:** Completeness threshold percentile (default 95%).
- **Input/output paths:** Adjust as needed for your system.

Edit the scripts or set environment variables as appropriate for your workflow.

---

## Outputs

- **Pixelated catalog files:** One per HEALPix pixel (HDF5 format).
- **Cleaned pixel files:** All galaxies with valid data.
- **Magnitude threshold/grid files:** Used for completeness.
- **Final master catalog:** HDF5 file with all galaxies, thresholds, and interpolant(s).

---

## Troubleshooting & FAQ

- **Q: My script says “file not found.”**
  - Check that all paths are correct, and input/output folders exist.
- **Q: How do I change epsilon or nside?**
  - Edit these parameters at the top of `make_files.py` or your script.
- **Q: How do I run in parallel?**
  - Use GNU parallel or a batch scheduler to run `clear_NaNs.py` or other steps for all pixels.

---

## Citations

- Please cite [IcaroGW](https://github.com/simone-mastrogiovanni/icarogw) if you use this workflow.
- Catalog reference: [GLADE+](https://glade.elte.hu)

## Contact

For questions or contributions, open an issue or contact [inesbentara](https://github.com/inesbentara).

