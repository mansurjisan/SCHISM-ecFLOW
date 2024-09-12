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

## Workflow Diagram

The following diagram illustrates the SCHISM-ecFLOW workflow:

[![](https://mermaid.ink/img/pako:eNqdlF1vmzAYhf-K5Uq7IhFgEj4uJjWQz6pTVSZVmtMLF0xiDWxkzJY0yn-fTZKlSW-2cGHhc57DaxvbO5iJnMIIriSp1-B7suRAP_c4VUSqV9DrfQUj_CRpLUVGm4bx1esBGXVe7OAp5VQSRcE3UtGSNeoScM_ASLQ8J3ILYsFzppjgzSWLzuyLbiQYl_QXMeAl5525e1WJpl5TyTIwETL7NMDBme2vJAITVtJT2XjQMYmDn0W7WnM9wSvHxS-M51KoKx3hhBVFxfiV7h10sjnpDvii18A0yDSebhKjJUZLjJZ4XXSMF-INpFS19TE77vSJg2NJzfCfWw4SJmmmhNxeMi6ORb3Vc9vQ_GKGE1Nr4nbU9LwSplRMZH6kpp0_w2n7VjFl3KMx64w5NqXTeDZPH8Gj3i_l0Z539gI_iUb1Pu2QRec-4DE3dQ5ao7al_mmgYGUZ3RVh7juZ1SgpftLoDiF0fO_9ZrlaR269-Rgb_Y0FDiL_HBvfFpvfFlvcFnv4nyWBFqyorAjL9cndmc8soVrTii5hpF9zWpC2VEu45HuNklaJdMszGCnZUgtKs9dhVJCy0b22zvWOSBjRN0B1QmrCfwjxsQujHdzAKLD7YRgEgT0c-j4a-Bbcwij0-qGN7CB0PM-3QwftLfjexe2-H4ahZzuuP_SHKPBDC1J99IV8PFw73e2z_wOn615p?type=png)](https://mermaid.live/edit#pako:eNqdlF1vmzAYhf-K5Uq7IhFgEj4uJjWQz6pTVSZVmtMLF0xiDWxkzJY0yn-fTZKlSW-2cGHhc57DaxvbO5iJnMIIriSp1-B7suRAP_c4VUSqV9DrfQUj_CRpLUVGm4bx1esBGXVe7OAp5VQSRcE3UtGSNeoScM_ASLQ8J3ILYsFzppjgzSWLzuyLbiQYl_QXMeAl5525e1WJpl5TyTIwETL7NMDBme2vJAITVtJT2XjQMYmDn0W7WnM9wSvHxS-M51KoKx3hhBVFxfiV7h10sjnpDvii18A0yDSebhKjJUZLjJZ4XXSMF-INpFS19TE77vSJg2NJzfCfWw4SJmmmhNxeMi6ORb3Vc9vQ_GKGE1Nr4nbU9LwSplRMZH6kpp0_w2n7VjFl3KMx64w5NqXTeDZPH8Gj3i_l0Z539gI_iUb1Pu2QRec-4DE3dQ5ao7al_mmgYGUZ3RVh7juZ1SgpftLoDiF0fO_9ZrlaR269-Rgb_Y0FDiL_HBvfFpvfFlvcFnv4nyWBFqyorAjL9cndmc8soVrTii5hpF9zWpC2VEu45HuNklaJdMszGCnZUgtKs9dhVJCy0b22zvWOSBjRN0B1QmrCfwjxsQujHdzAKLD7YRgEgT0c-j4a-Bbcwij0-qGN7CB0PM-3QwftLfjexe2-H4ahZzuuP_SHKPBDC1J99IV8PFw73e2z_wOn615p)


