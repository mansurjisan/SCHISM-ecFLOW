#!/bin/bash
# Load environment variables
#source /home/mjisan/workflow/schism_suite2/scripts/river_forcing/env_vars.sh

export FIXstofs3d="/work/noaa/nosofs/mjisan/STOFS/NWM"
export DATA_prep_nwm="/home/mjisan/workflow/schism_suite2/workdir"
export COMINnwm="/work/noaa/nosofs/mjisan/STOFS/NWM"
export PYstofs3d="/work/noaa/nosofs/mjisan/WCOSS_BACKUP_RMV_AFTER_DEV_SWITCH/IT-stofs.v2.1.0/ush/stofs_3d_atl/pysh"  # Directory containing gen_sourcesink.py and relocate_source_feeder_lean.py
export cycle="12"
export PDYHH_NCAST_BEGIN="2025012500"
mkdir -p ${DATA_prep_nwm}


# Clean and create working directory
cd ${DATA_prep_nwm}
rm -rf *
cp ${PYstofs3d}/gen_sourcesink.py .
cp ${PYstofs3d}/relocate_source_feeder_lean.py .

# Link fix files
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_sources_conus.json sources_conus.json
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_sinks_conus.json sinks_conus.json
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_relocate_map.txt relocate_map.txt
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_source_scale.txt source_scale.txt
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_source_sink.in.before_relocate source_sink.in.before_relocate
ln -sf ${FIXstofs3d}/stofs_3d_atl_river_vsink.th vsink.th

# Gather NWM files (adjust pattern if needed)
ln -sf ${COMINnwm}/nwm*.conus.nc .

# Execute the river forcing script
start_date="${PDYHH_NCAST_BEGIN:0:4}-${PDYHH_NCAST_BEGIN:4:2}-${PDYHH_NCAST_BEGIN:6:2}-${cycle}"
python gen_sourcesink.py ${start_date}

# Check output
ls -l vsource.th vsink.th msource.th
