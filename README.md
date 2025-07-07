
# Icaro Catalog Preprocessing

This repository provides a workflow to preprocess galaxy catalogs for use with the [IcaroGW](https://github.com/simone-mastrogiovanni/icarogw) cosmological inference pipeline.  
It supports splitting the catalog into sky pixels, cleaning, thresholding, and generating all necessary summary statistics for “dark siren” cosmology.

---

## Workflow Overview

The pipeline:
1. Pixelates the raw galaxy catalog.
2. Removes invalid entries (NaNs).
3. Computes a magnitude threshold and redshift integration grid.
4. Initializes and fills the ICAROGW-compatible output catalog.
5. Produces an interpolated per-pixel galaxy distribution.
6. Merges everything into a final `.hdf5` catalog.

---

## Requirements

- Python ≥ 3.8
- `icarogw` (installed via `pip install -e path/to/icarogw`)
- `numpy`, `h5py`, `healpy`, `tqdm`
- Optionally: `HTCondor` (for job submission)

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

## Key Parameters

- **nside:** HEALPix resolution (higher = finer pixels).
- **epsilon:** Luminosity weighting (0 = uniform, 1 = by luminosity).
- **band:** Photometric band to use for thresholds.
- **mthr_percentile:** Completeness threshold percentile (default 95%).
- **Input/output paths:** Adjust as needed for your system.

Edit the scripts or set environment variables as appropriate for your workflow.

---

## Configuration

### Option 1: Use a `.ini` config file

Create a file like `config.ini`:

```ini
[main]
catalog_before_process = /path/to/glade+.hdf5
base_dir = /path/to/Icaro_Catalog_Preprocessing
catalog_name = reproduce_gladep
band = K
nside = 64
nside_mthr = 32
fields_to_take = ra,dec,m_K,z,sigmaz
mthr_percentile = 50.
Nintegration_min = 1e-3
Nintegration_max = 0.5
Nintegration_points = 5000
Numsigma = 3
zcut = 0.5
epsilon = 0.0
NumJobs = 20
accounting_group_user = your.name
accounting_group = ligo.dev.o4.cbc.hubble.icarogw
verbose = false
```

Run the setup with:

```bash
python make_files.py --config config.ini
```

### Option 2: CLI arguments (no config file)

```bash
python make_files.py \
  --catalog_before_process /path/to/glade+.hdf5 \
  --base_dir /path/to/Icaro_Catalog_Preprocessing \
  --catalog_name reproduce_gladep \
  --band K \
  --nside 64 \
  --nside_mthr 32 \
  --fields_to_take ra dec m_K z sigmaz \
  --mthr_percentile 50. \
  --Nintegration_min 1e-3 \
  --Nintegration_max 0.5 \
  --Nintegration_points 5000 \
  --Numsigma 3 \
  --zcut 0.5 \
  --epsilon 0.0 \
  --NumJobs 20 \
  --accounting_group_user your.name \
  --accounting_group ligo.dev.o4.cbc.hubble.icarogw \
  --verbose false
```

## Manual Step-by-Step Execution

Useful for debugging or validation before full DAG submission.

1. Pixelate the catalog:
    ```bash
    python make_pixel_files.py
    ```

2. Generate job scripts:
    ```bash
    python get_scripts.py
    ```

3. Clean NaNs (loop through queue_NaN.txt):
    ```bash
    while read start end; do
      python clear_NaNs.py "$start" "$end"
    done < queue_NaN.txt
    ```

4. Compute magnitude threshold and redshift grid:
    ```bash
    while read start end; do
      python calc_mthr_and_grid.py "$start" "$end"
    done < queue_NaN.txt
    ```

5. Initialize output HDF5 structure:
    ```bash
    python initialize_catalog.py
    ```

6. Compute interpolants:
    ```bash
    python calc_interpolant.py
    ```

7. Final merge:
    ```bash
    python finish_catalog.py
    ```

## HTCondor Execution

Once verified, run the pipeline with HTCondor:

```bash
condor_submit_dag produce_cat.dag
```

This handles dependency management and batch job scheduling.