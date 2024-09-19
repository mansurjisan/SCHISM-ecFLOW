#!/bin/bash
#%include <head.h>
#%include <tail.h>

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
conda activate pyschism_env2

# Set variables
START_YEAR="1994"
START_MONTH="10"
START_DAY="12"
START_HOUR="17"
RNDAY=3
PREPROCESS="/home/mjisan/workflow/pyschism_suite"

# Run the gen_sflux_era5.py script
cd $PREPROCESS/scripts/Job_card


python gen_jobcard.py --cluster hercules #Standalone SCHISM in Hercules


#python gen_jobcard.py --cluster hercules --wwm #Coupled SCHISM-WWM Module

conda deactivate

ecflow_client --port 3141 --label=info "Job car generation setup complete"
