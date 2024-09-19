#!/bin/bash
%include <head.h>

# Set the path to conda.sh
CONDA_SH="/apps/spack-managed/gcc-11.3.1/miniconda3-24.3.0-avnaftwsbozuvtsq7jrmpmcvf6c7yzlt/etc/profile.d/conda.sh"

# Check if conda.sh exists
if [ ! -f "$CONDA_SH" ]; then
    echo "Error: Could not find conda.sh at $CONDA_SH"
    exit 1
fi

# Initialize conda
source "$CONDA_SH"

# Activate the PySCHISM environment
conda activate pyschism_mjisan

# Set variables
SCRIPT_DIR="/home/mjisan/workflow/schism_suite/scripts/plot_water_elevation"

# Change to the directory containing the script
cd $SCRIPT_DIR

# Print current working directory and its contents
echo "Current working directory: $(pwd)"
echo "Contents of current directory:"
ls -l

# Run the plot_water_elevation.py script
python plot_water_elevation.py

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo "Error: plot_water_elevation.py failed to run successfully"
    conda deactivate
    exit 1
fi

# Deactivate the conda environment
conda deactivate

# Update ecFlow with task completion
ecflow_client --label=info "Water elevation plotting complete"

%include <tail.h>
