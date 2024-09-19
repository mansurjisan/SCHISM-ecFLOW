import os
import numpy as np
from pyschism import plot_water_elevation

def find_latest_run_directory(base_path):
    """Find the most recent Test_Duck_XXX directory."""
    test_duck_dirs = [d for d in os.listdir(base_path) if d.startswith("Test_Duck_") and d[10:].isdigit()]
    if not test_duck_dirs:
        raise ValueError(f"No Test_Duck directories found in {base_path}")
    return max(test_duck_dirs, key=lambda d: int(d[10:]))

def main():
    # Base path where Test_Duck directories are located
    base_path = "/work/noaa/nosofs/mjisan/schism/schism_verification_tests"
    
    print(f"Searching for Test_Duck directories in: {base_path}")
    print(f"Contents of {base_path}:")
    print(os.listdir(base_path))
    
    # Find the latest Test_Duck directory
    latest_run_dir = find_latest_run_directory(base_path)
    run_path = os.path.join(base_path, latest_run_dir)
    
    print(f"Latest Test_Duck directory: {latest_run_dir}")
    print(f"Full path: {run_path}")
    
    # Check if the run directory exists and is accessible
    if not os.path.exists(run_path):
        print(f"Error: Run directory {run_path} does not exist.")
        return
    if not os.access(run_path, os.R_OK):
        print(f"Error: No read permission for {run_path}")
        return
    
    # List contents of run directory
    print(f"Contents of {run_path}:")
    print(os.listdir(run_path))
    
    # Construct file list, including the 'outputs' subdirectory
    outputs_dir = os.path.join(run_path, 'outputs')
    
    # Check if outputs directory exists
    if not os.path.exists(outputs_dir):
        print(f"Error: Outputs directory {outputs_dir} does not exist.")
        return
    if not os.access(outputs_dir, os.R_OK):
        print(f"Error: No read permission for {outputs_dir}")
        return
    
    print(f"Contents of {outputs_dir}:")
    print(os.listdir(outputs_dir))
    
    # Try to find any out2d files
    out2d_files = [f for f in os.listdir(outputs_dir) if f.startswith('out2d_') and f.endswith('.nc')]
    if not out2d_files:
        print(f"No out2d_*.nc files found in {outputs_dir}")
        return
    
    file_list = [os.path.join(outputs_dir, f) for f in out2d_files]
    
    print(f"Found {len(file_list)} out2d files:")
    for file in file_list:
        exists = os.path.exists(file)
        readable = os.access(file, os.R_OK) if exists else False
        print(f"  {file}")
        print(f"    Exists: {exists}")
        print(f"    Readable: {readable}")
    
    # Check if files exist and are readable
    existing_files = [f for f in file_list if os.path.exists(f) and os.access(f, os.R_OK)]
    if not existing_files:
        print(f"No readable output files found in {outputs_dir}")
        return
    
    # Set output directory within the run directory
    output_dir = os.path.join(run_path, 'elevation_plots')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing files in: {outputs_dir}")
    print(f"Output will be saved to: {output_dir}")
    
    try:
        plot_water_elevation(
            file_list=existing_files,
            output_dir=output_dir,
            contour_levels=np.linspace(-1, 1, 50),
            colorbar_ticks=np.arange(-1, 1.1, 0.2),
            title_template="Water Elevation at {time}",
            colormap='coolwarm',
            vmin=-1, vmax=1
        )
        print("Water elevation plotting completed successfully.")
    except Exception as e:
        print(f"An error occurred while plotting: {str(e)}")

if __name__ == "__main__":
    main()
