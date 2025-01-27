# YAML-Driven ecFlow based Workflow for SCHISM Modeling System

A modern, configuration-driven ecFlow based workflow system for SCHISM (Semi-implicit Cross-scale Hydroscience Integrated System Model) model. This implementation emphasizes a centralized YAML configuration approach, making it easy to modify and maintain complex SCHISM workflows.

## Overview

The workflow is designed to handle the following preprocessing tasks:
- SCHISM namelist generation
- required .gr3 file generation i.e. rough.gr3, elev.ic, diffmin.gr3, diffmax.gr3, watertype.gr3, windrot_geo2proj.gr3
- Surface flux (ERA5) data preparation
- Boundary condition tides generation

## Key Features

- **Single Configuration File**: All parameters managed through `config.yml`
- **Modular Task System**: Each task reads its configuration from specific YAML sections
- **Flexible Runtime Options**: Support for different SCHISM configurations (standalone, WWM+ATM coupling)
- **Automated Resource Management**: HPC resource allocation controlled via YAML
- **Standardized Error Handling**: Consistent error management across all tasks

## Configuration Structure

```yaml
# Basic suite configuration
suite:
  ecf_home: /work/noaa/nosofs/mjisan/SCHISM-ecFLOW
  ecf_include: /work/noaa/nosofs/mjisan/SCHISM-ecFLOW
  schism_run_type: schism  # Options: schism, schism+wwm+atm
  schism_cluster: hercules
  preprocess_dir: '/work/noaa/nosofs/mjisan/SCHISM-ecFLOW'

# Environment configuration
environment:
  conda:
    path: "/apps/spack-managed/gcc-11.3.1/miniconda3-24.3.0-avnaftwsbozuvtsq7jrmpmcvf6c7yzlt/etc/profile.d/conda.sh"
    env_name: "pyschism_mjisan"

# Namelist configuration
namelist:
  year: 1994            # Simulation start year
  month: 10            # Simulation start month
  day: 12             # Simulation start day
  hour: 17            # Simulation start hour
  rnday: 3            # Run duration in days
  script_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/ush/namelist"
  work_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/workdir"

# Boundary tides configuration
bctides:
  script_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/ush/Bnd"
  hgrid_path: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/fix/hgrid.ll"
  work_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/workdir"
  rnday: 20            # Duration for boundary conditions
  bc_mode: "tidal"     # Boundary condition mode
  bc_type: 3           # Boundary condition type
  constituents: "Q1,O1,P1,K1,N2,M2,S2,K2,Mm,Mf,M4,MN4,MS4,2N2,S1"
  database: "tpxo"     # Tidal database
  cutoff_depth: 40     # Cutoff depth for boundary conditions
  earth_tidal_potential: "Y"  # Include earth tidal potential

# Surface flux configuration
sflux:
  rnday: 3             # Duration for surface flux
  data_file: 'data_stream-oper.nc'
  interval: 1          # Time interval for flux data
  hgrid_path: '/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/fix/hgrid.gr3'
  script_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/ush/Sflux"
  work_dir: '/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/workdir'

# Roughness configuration
manning:
  script_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/ush/Manning"
  work_dir: "/work/noaa/nosofs/mjisan/SCHISM-ecFLOW/workdir"
```

### Suite Definition (`schism_suite.def`)

```yaml
suite schism_suite
  edit ECF_HOME "$(yq -r .suite.ecf_home ${CONFIG_FILE})"
  edit SCHISM_RUN_TYPE "$(yq -r .suite.schism_run_type ${CONFIG_FILE})"
  edit CONFIG_FILE '/path/to/config.yml'

  family preprocess
    task gen_manning
      edit ECF_SCRIPT 'ecf/gen_manning.ecf'
    task gen_sflux_era5
      edit ECF_SCRIPT 'ecf/gen_sflux_era5.ecf'
  endfamily
```

## Directory Structure

```
.
├── config/
│   └── config.yml           # Main configuration file
├── ecf/
│   ├── gen_bctides.ecf     # Boundary tides generation script
│   ├── gen_manning.ecf     # Manning coefficient generation script
│   ├── gen_namelist.ecf    # Namelist generation script
│   └── gen_sflux_era5.ecf  # Surface flux generation script
├── fix/                    # Static input files
├── scripts/               
├── ush/                    # Utility scripts
└── workdir/               # Working directory for outputs
```

## Task Implementation

### 1. Task Script Structure
Each task script (`*.ecf`) follows a standard pattern for YAML configuration:

```bash
#!/bin/bash
%include <head.h>

# Load configuration
CONDA_PATH=$(yq -r '.environment.conda.path' "${CONFIG_FILE}")
SCRIPT_DIR=$(yq -r '.taskname.script_dir' "${CONFIG_FILE}")

# Error handling function
handle_error() {
    ecflow_client --label=error "$2"
    exit $1
}

# Main task execution
source "${CONDA_PATH}" || handle_error $? "Conda initialization failed"
python script.py --param value || handle_error $? "Task failed"

%include <tail.h>
```


## Configuration

The workflow is configured through `config.yml`. Key configuration sections include:

### Basic Suite Configuration
```yaml
suite:
  ecf_home: /path/to/ecflow/home
  schism_run_type: schism
  schism_cluster: hercules
```

### Environment Setup
```yaml
environment:
  conda:
    path: "/path/to/conda.sh"
    env_name: "pyschism_env"
```

### Task-specific Configuration
Each preprocessing task has its own configuration section in `config.yml`. For example:

```yaml
bctides:
  script_dir: "/path/to/scripts"
  hgrid_path: "/path/to/hgrid.ll"
  rnday: 20
  bc_mode: "tidal"
  constituents: "Q1,O1,P1,K1,N2,M2,S2,K2"
```

## Workflow Tasks

### 1. Manning Generation (`gen_manning`)
- Generates Manning coefficients for the model domain
- Creates and processes elevation files
- Output: `elev.ic, diffmin.gr3, diffmax.gr3`

### 2. Surface Flux Generation (`gen_sflux_era5`)
- Processes ERA5 atmospheric data
- Generates surface flux files for the simulation period
- Outputs: `sflux_air_1.*.nc`, `sflux_prc_1.*.nc`

### 3. Boundary Tides Generation (`gen_bctides`)
- Processes tidal constituents
- Creates boundary conditions for the model
- Output: `bctides.in`

### 4. Namelist Generation (`gen_namelist`)
- Creates SCHISM parameter namelist
- Handles different run types (schism, schism+wwm+atm)
- Output: `param.nml`

## Usage

1. Configure your environment in `config.yml`

2. Load and start the suite:
```bash
ecflow_client --port 3141 --load=/path/to/schism_suite.def
ecflow_client --port 3141 --begin /schism_suite
```

3. Monitor the workflow:
```bash
ecflow_client --get_state=/schism_suite
```

## Adding New Tasks

1. Add Configuration Section:
```yaml
# config.yml
new_task:
  script_dir: "/path/to/scripts"
  param1: value1
  param2: value2
```

2. Create Task Script:
```bash
# ecf/new_task.ecf
#!/bin/bash
%include <head.h>
PARAM1=$(yq -r '.new_task.param1' "${CONFIG_FILE}")
# Task implementation
%include <tail.h>
```

3. Add to Suite Definition:
```
task new_task
  edit ECF_SCRIPT 'ecf/new_task.ecf'
```

## Error Handling

Each task includes comprehensive error handling:
- Checks for required input files
- Validates output file creation
- Reports errors through ecFlow's label system

## Workflow Diagram

The following diagram illustrates the SCHISM-ecFLOW workflow:


[![](https://mermaid.ink/img/pako:eNqVVUtv2zAM_iuGil4G1cijefkwYFuxw4ZhA7rTnMKQbTrRakuGJC_12v736ZVEcYMW88GmyI8UKX6UH1HBS0AJ2gjSbqOfH9cs0s_lZfSJs4puOkEU5cxpC6tK3Sfum_ou1EdXV--f9l4gn6JWQCt4AVK-CvvN80x2-euhuFRrdsjtxyEyZZvoM2lo3TujDuQqOW6enqB9yuYpqYDCVHco2zwNYUzj0g2wzMuBj6zq7sHarJSBILPAnOt4JUgL8HJgZaSBmkplzfuFtwMrgwK_8Dy67fKG6px1fmcr9OeWnmLfrE90TBtsCk4MPHTIgojSGr0c1m42Uan7GHtg2xFtMa-s4iKTtOlqS5y74camtT7Si33P2tzamkz8c6f1Q7PjTT5oTHoKDHJra65S88p2RIHIoIY_Yf6n-91AqxXACgoyykHtAFhUmV21wqGO9LNcVoJuNiCGbPeLAWRA9u-dajslB_Vwp02_Qr9H3L0gsQ2sm6lZqswYmbIyWqTmG9NiyOsh3FG8orVmtJPfxayIrOIl6YfeeWFdU2-OKTszCkOnlgjSpPYds8MFc3r8t6qvQTehooyaHu2vl5pIqbX-DnEonUGdXFSrCksl-D0kF9Pp1MtXO1qqbTJpHwYBbCv7MECe_1cAReR96F5WZeg-QLtWnuQ7xB9q_9C2de9OICx7f28GpYfWIxuxpxw2JAsLDeGePdj2HPv-4X3LsBtk7IcWuwHFZjixGaFj9WFMTz0ccAp7hmDb7vAYEEYNiIbQUv-ZHk2YNVJbaGCNEi2WUJGuVmu0Zs8aSjrFb3tWoESJDjASvNtsUVKRWupV15aaWjeU6Llp9pCWsF-cH5ZQUsXFN_cntD9EC0HJI3pAyWoer1aj5Ww0Xowmi_lygVGPkuk8no3ms-l0YZ7VbPyM0V8bcxQvp6Pr2ep6PFuNJ_PJcvL8D7aYfXM?type=png)](https://mermaid.live/edit#pako:eNqVVUtv2zAM_iuGil4G1cijefkwYFuxw4ZhA7rTnMKQbTrRakuGJC_12v736ZVEcYMW88GmyI8UKX6UH1HBS0AJ2gjSbqOfH9cs0s_lZfSJs4puOkEU5cxpC6tK3Sfum_ou1EdXV--f9l4gn6JWQCt4AVK-CvvN80x2-euhuFRrdsjtxyEyZZvoM2lo3TujDuQqOW6enqB9yuYpqYDCVHco2zwNYUzj0g2wzMuBj6zq7sHarJSBILPAnOt4JUgL8HJgZaSBmkplzfuFtwMrgwK_8Dy67fKG6px1fmcr9OeWnmLfrE90TBtsCk4MPHTIgojSGr0c1m42Uan7GHtg2xFtMa-s4iKTtOlqS5y74camtT7Si33P2tzamkz8c6f1Q7PjTT5oTHoKDHJra65S88p2RIHIoIY_Yf6n-91AqxXACgoyykHtAFhUmV21wqGO9LNcVoJuNiCGbPeLAWRA9u-dajslB_Vwp02_Qr9H3L0gsQ2sm6lZqswYmbIyWqTmG9NiyOsh3FG8orVmtJPfxayIrOIl6YfeeWFdU2-OKTszCkOnlgjSpPYds8MFc3r8t6qvQTehooyaHu2vl5pIqbX-DnEonUGdXFSrCksl-D0kF9Pp1MtXO1qqbTJpHwYBbCv7MECe_1cAReR96F5WZeg-QLtWnuQ7xB9q_9C2de9OICx7f28GpYfWIxuxpxw2JAsLDeGePdj2HPv-4X3LsBtk7IcWuwHFZjixGaFj9WFMTz0ccAp7hmDb7vAYEEYNiIbQUv-ZHk2YNVJbaGCNEi2WUJGuVmu0Zs8aSjrFb3tWoESJDjASvNtsUVKRWupV15aaWjeU6Llp9pCWsF-cH5ZQUsXFN_cntD9EC0HJI3pAyWoer1aj5Ww0Xowmi_lygVGPkuk8no3ms-l0YZ7VbPyM0V8bcxQvp6Pr2ep6PFuNJ_PJcvL8D7aYfXM)
