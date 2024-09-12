# SCHISM-ecFLOW

## Overview

SCHISM-ecFLOW is an automated workflow system for the SCHISM using ecFlow. This project aims to streamline the preprocessing steps, job setup, execution of SCHISM model runs and post-processing steps.

## Features

- Automated preprocessing steps
  - Namelist generation
  - Boundary condition generation (bctides.in)
  - Time-varying water elevation generation
  - Atmospheric forcing
  - Generation of various .gr3 files (roughness, windrot, diffmin, diffmax)
- Automated job setup
  - Run directory creation
  - Copying of fixed input files
- ecFlow-based workflow management

## Directory Structure

```
.
├── LICENSE
├── README.md
├── ecf/                  # ecFlow task scripts
├── preprocess/           # Duplicate of ecf scripts (to be consolidated)
├── pyschism_suite/
│   ├── fix/              # Symlink to fixed input files
│   ├── job_submission/   # Job submission task outputs
│   ├── preprocess/       # Preprocessing task outputs
│   ├── scripts/          # Python scripts for preprocessing tasks
│   └── workdir/          # Working directory for generated input files
├── pyschism_suite.def    # ecFlow suite definition file
└── scripts/              # Duplicate of pyschism_suite/scripts (to be consolidated)
```

## Key Components

1. Boundary Conditions: `scripts/Bnd/gen_bctides.py`
2. Elevation: `scripts/Elev/` (includes OTPS data and scripts)
3. Job Card Generation: `scripts/Job_card/gen_jobcard.py`
4. Run Directory Setup: `scripts/Job_dir/gen_rundir.py`
5. Manning Coefficient: `scripts/Manning/gen_gr3_input.py`
6. Surface Flux: `scripts/Sflux/gen_sflux_era5.py`
7. Namelist Generation: `scripts/namelist/gen_namelist.py`

## Prerequisites

- ecFlow (please see installation instructions here https://github.com/mansurjisan/ecflow-setup-test-hercules)
- Python 3.9.1
- SCHISM model 


## Installation

1. Clone this repository:
   ```
   git clone https://github.com/mansurjisan/SCHISM-ecFLOW.git
   cd SCHISM-ecFLOW
   ```

2. [Add any additional installation steps, such as setting up a Python virtual environment or installing dependencies]

## Usage

1. Configure the ecFlow suite:
   ```
   ecflow_client --port 3141 --load=/home/mjisan/pyschism_suite.def
   ```

2. Start the ecFlow suite:
   ```
   ecflow_client --port 3141 --begin=/pyschism_suite.def
   ```

3. Monitor the workflow:
   ```
   ecflow_client --port 3141 --get_state=/pyschism_suite
   ```

