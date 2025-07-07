import numpy as np
import argparse
import os
import re
import configparser

import icarogw

def main():
    parser = argparse.ArgumentParser(
        description="Prepare pipeline scripts and settings for galaxy catalog preprocessing."
    )
    parser.add_argument("--config", type=str, help="Path to .ini config file with defaults.")

    # No default here, let config file fill in
    parser.add_argument("--catalog_before_process", type=str)
    parser.add_argument("--base_dir", type=str)
    parser.add_argument("--catalog_name", type=str)
    parser.add_argument("--band", type=str)
    parser.add_argument("--nside", type=int)
    parser.add_argument("--nside_mthr", type=int)
    parser.add_argument("--fields_to_take", nargs="+")
    parser.add_argument("--mthr_percentile", type=float)
    parser.add_argument("--Nintegration_min", type=float)
    parser.add_argument("--Nintegration_max", type=float)
    parser.add_argument("--Nintegration_points", type=int)
    parser.add_argument("--Numsigma", type=int)
    parser.add_argument("--zcut", type=float)
    parser.add_argument("--epsilon", type=float)
    parser.add_argument("--NumJobs", type=int)
    parser.add_argument("--verbose", type=bool)
    parser.add_argument("--accounting_group_user", type=str)
    parser.add_argument("--accounting_group", type=str)

    args = parser.parse_args()
    config = {}

    # Read from .ini config if provided
    if args.config:
        cp = configparser.ConfigParser()
        cp.read(args.config)
        config = dict(cp["main"])

    # Helper to fetch: CLI > config > fallback default
    def param(name, default):
        cli_val = getattr(args, name)
        if cli_val is not None:
            return cli_val
        elif name in config and config[name] not in [None, ""]:
            return config[name]
        else:
            return default

    catalog_before_process = param("catalog_before_process", "")
    base_dir = param("base_dir", "/home/ines.bentara/cosmo/Icaro_Catalog_Preprocessing")
    catalog_name = param("catalog_name", "catalog")
    band = param("band", "K")
    nside = int(param("nside", 64))
    nside_mthr = int(param("nside_mthr", 32))
    fields_to_take = param("fields_to_take", ['ra','dec','m_K','z','sigmaz'])
    if isinstance(fields_to_take, str):
        fields_to_take = [f.strip() for f in fields_to_take.split(",")]
    mthr_percentile = float(param("mthr_percentile", 50.))
    Nintegration_min = float(param("Nintegration_min", 1e-3))
    Nintegration_max = float(param("Nintegration_max", 0.5))
    Nintegration_points = int(param("Nintegration_points", 5000))
    Numsigma = int(param("Numsigma", 3))
    zcut = float(param("zcut", 0.5))
    epsilon = float(param("epsilon", 0.))
    NumJobs = int(param("NumJobs", 20))
    accounting_group_user = param("accounting_group_user", "albert.einstein")
    accounting_group = param("accounting_group", "ligo.dev.o4.cbc.hubble.icarogw")
    verbose = param("verbose", False)
    if isinstance(verbose, str):
        verbose = verbose.lower() == "true"

    # Rest as before
    catalog_base = os.path.join(base_dir, "catalogs", f"{catalog_name}.hdf5")
    outfolder = os.path.join(base_dir, catalog_name, "pixelated")
    outfile = os.path.join(base_dir, catalog_name, "output_cat.hdf5")
    home_folder = base_dir
    band_flag = f"m_{band}"
    grouping = f"{band}-band"
    apparent_magnitude_flag = band_flag
    band_label = band
    subgrouping = f"eps-{epsilon:g}"
    Nintegration = np.logspace(
        np.log10(Nintegration_min),
        np.log10(Nintegration_max),
        Nintegration_points
    )

    os.makedirs(outfolder, exist_ok=True)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)

    icarogw.utils.write_all_scripts_catalog(
        home_folder=home_folder,
        outfolder=outfolder,
        nside=nside,
        fields_to_take=fields_to_take,
        grouping=grouping,
        apparent_magnitude_flag=apparent_magnitude_flag,
        nside_mthr=nside_mthr,
        mthr_percentile=mthr_percentile,
        Nintegration=Nintegration,
        Numsigma=Numsigma,
        zcut=zcut,
        outfile=outfile,
        subgrouping=subgrouping,
        band=band_label,
        epsilon=epsilon,
        uname=accounting_group_user,
        agroup=accounting_group,
        NumJobs=NumJobs
    )

    # ---- PATCH make_pixel_files.py ----
    mpf_path = os.path.join(base_dir, "make_pixel_files.py")
    fields_list = ','.join([f"'{k}'" for k in fields_to_take])
    
    with open(mpf_path, "r") as f:
        mpf_lines = f.readlines()
    
    # Find and replace lines to include `catalog_before_process` path
    with open(mpf_path, "w") as f:
        for line in mpf_lines:
            if "with h5py.File" in line:
                f.write(f"with h5py.File('{catalog_before_process}', 'r') as cat:\n")
            elif "create_pixelated_catalogs" in line:
                f.write(f"\ticarogw.catalog.create_pixelated_catalogs(outfolder, nside, {{key: cat[key] for key in [{fields_list}]}})\n")
            else:
                f.write(line)

if __name__ == "__main__":
    main()
