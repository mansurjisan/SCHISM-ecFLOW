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

# Activate the appropriate conda environment if needed
# conda activate your_environment_name

# Set variables
UFS_COASTAL_DIR="/work/noaa/nosofs/mjisan/ufs-weather-model/tests"  # Adjust this path


# Create build directory if it doesn't exist
cd $UFS_COASTAL_DIR

# Set compilation flags
COMPILE_FLAGS="-DAPP=%APP% -DUSE_ATMOS=%USE_ATMOS% -DNO_PARMETIS=%NO_PARMETIS% -DOLDIO=%OLDIO% -DBUILD_UTILS=%BUILD_UTILS%"

# Run the compilation command
./compile.sh %UFS_CLUSTER% "$COMPILE_FLAGS" coastalS intel YES NO

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful"
    ecflow_client --label=info "Compilation complete"
else
    echo "Compilation failed"
    ecflow_client --label=error "Compilation failed"
    exit 1
fi

# Deactivate the conda environment if one was activated
# conda deactivate

%include <tail.h>
