
# Icaro Catalog Preprocessing

This repository provides a workflow to preprocess galaxy catalogs for use with the [IcaroGW](https://github.com/simone-mastrogiovanni/icarogw) cosmological inference pipeline.  
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
- [icarogw](https://github.com/icarogw-developers/icarogw)
- [healpy](https://healpy.readthedocs.io/)
- [h5py](https://www.h5py.org/)
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [tqdm](https://tqdm.github.io)

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

To be filled...

```bash
./preprocess_catalog.sh [args]
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

## Output
**Final master catalog:** HDF5 file with all galaxies, thresholds, and interpolant(s) to be used by IcaroGW.