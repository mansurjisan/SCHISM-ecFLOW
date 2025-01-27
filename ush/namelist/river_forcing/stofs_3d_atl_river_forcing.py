#!/usr/bin/env python3
import os
import argparse
from datetime import datetime, timedelta
import json
import numpy as np
from netCDF4 import Dataset

def get_aggregated_features(nc_feature_id, features):
    aggregated_features = []
    for source_feats in features.values():
        aggregated_features.extend(list(source_feats))
    
    in_file = []
    for feature in aggregated_features:
        idx = np.where(nc_feature_id == int(feature))[0]
        in_file.append(idx.item())
    
    in_file_2 = []
    sidx = 0
    for source_feats in features.values():
        eidx = sidx + len(source_feats)
        in_file_2.append(in_file[sidx:eidx])
        sidx = eidx
    return in_file_2

def streamflow_lookup(nc_file, indexes):
    with Dataset(nc_file) as nc:
        streamflow = nc["streamflow"][:]
        streamflow[np.where(streamflow < -1e-5)] = 0.0
        if hasattr(streamflow, 'mask'):
            streamflow[streamflow.mask] = 0.0
        
        data = []
        for indxs in indexes:
            data.append(np.sum(streamflow[indxs]))
    return data

def main():
    parser = argparse.ArgumentParser(description='Generate STOFS 3D Atlantic river forcing files')
    parser.add_argument('--start_date', required=True, help='Start date (YYYYMMDDHH)')
    parser.add_argument('--rnday', type=int, required=True, help='Simulation days')
    parser.add_argument('--nwm_dir', required=True, help='Path to NWM input files')
    parser.add_argument('--workdir', required=True, help='Working directory')
    parser.add_argument('--fix_dir', required=True, help='Path to FIX files')
    args = parser.parse_args()

    # Load configuration files
    sources = json.load(open(f"{args.fix_dir}/sources_conus.json"))
    sinks = json.load(open(f"{args.fix_dir}/sinks_conus.json"))
    relocate_map = np.loadtxt(f"{args.fix_dir}/relocate_map.txt", dtype=int)
    scale_factors = np.loadtxt(f"{args.fix_dir}/source_scale.txt", delimiter=',', skiprows=1)

    # Collect and sort NWM files
    nwm_files = []
    for root, _, files in os.walk(args.nwm_dir):
        for file in files:
            if file.endswith(".conus.nc"):
                nwm_files.append(os.path.join(root, file))
    nwm_files.sort()

    # Process discharge data
    vsource_data = []
    src_idxs = None
    for nwm_file in nwm_files:
        with Dataset(nwm_file) as nc:
            feature_id = nc['feature_id'][:]
            if src_idxs is None:
                src_idxs = get_aggregated_features(feature_id, sources)
            
            # Get streamflow data for sources
            discharge_values = streamflow_lookup(nwm_file, src_idxs)
            
            # Get time from NetCDF attribute
            model_time = datetime.strptime(
                nc.model_output_valid_time, 
                "%Y-%m-%d_%H:%M:%S"
            )
            timestamp = (model_time - datetime.strptime(args.start_date, "%Y%m%d%H")).total_seconds()
            
            # Apply scaling factors
            scaled_discharge = []
            for idx, value in enumerate(discharge_values):
                scale_factor = scale_factors[idx, 2]  # 3rd column contains scale factors
                scaled_discharge.append(value * scale_factor)
            
            vsource_data.append({
                'time': timestamp,
                'discharge': scaled_discharge
            })

    # Apply relocation mapping
    relocated_data = []
    for entry in vsource_data:
        relocated_discharge = [0.0] * len(relocate_map)
        for orig_idx, new_idx in enumerate(relocate_map):
            if new_idx >= 0:
                relocated_discharge[new_idx] += entry['discharge'][orig_idx]
        relocated_data.append({
            'time': entry['time'],
            'discharge': relocated_discharge
        })

    # Write vsource.th
    with open(f"{args.workdir}/vsource.th", "w") as f:
        for entry in relocated_data:
            line = f"{entry['time']} " + " ".join(f"{x:.4f}" for x in entry['discharge']) + "\n"
            f.write(line)

    # Copy static files
    for static_file in ["msource.th", "vsink.th"]:
        os.system(f"cp {args.fix_dir}/{static_file} {args.workdir}/")

if __name__ == "__main__":
    main()
