#!/bin/bash
set -e

# Example usage:
# ./preprocess_catalog.sh /path/to/input_catalog.hdf5 /path/to/output_folder nside epsilon band mthr_percentile

INPUT_CATALOG="$1"
OUTPUT_FOLDER="$2"
NSIDE="$3"
EPSILON="$4"
BAND="$5"
MTHR_PERCENTILE="$6"

echo "1. Pixelizing input catalog..."
python3 scripts/make_files.py "$INPUT_CATALOG" "$OUTPUT_FOLDER" "$NSIDE" "$BAND"

echo "2. Cleaning pixel files..."
for f in "$OUTPUT_FOLDER"/pixel_*.hdf5; do
    python3 scripts/clear_NaNs.py "$f" "${f%.hdf5}_clean.hdf5"
done

echo "3. Calculating magnitude thresholds and grid..."
python3 scripts/calc_mthr_and_grid.py "$OUTPUT_FOLDER" "$BAND" "$MTHR_PERCENTILE"

echo "4. Initializing master catalog..."
python3 scripts/initialize_catalog.py "$OUTPUT_FOLDER" "$NSIDE" "$BAND" "$EPSILON"

echo "5. Building interpolant..."
python3 scripts/calc_interpolant.py "$OUTPUT_FOLDER" "$BAND" "$EPSILON"

echo "6. Finalizing output..."
python3 scripts/finish_catalog.py "$OUTPUT_FOLDER"

echo "Done. Catalog saved in '$OUTPUT_FOLDER'/."