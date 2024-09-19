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
    
    # Find the latest Test_Duck directory
    latest_run_dir = find_latest_run_directory(base_path)
    run_path = os.path.join(base_path, latest_run_dir)
    
    # Construct file list
    file_list = [os.path.join(run_path, f'out2d_{i}.nc') for i in range(1, 9)]
    
    # Set output directory within the run directory
    output_dir = os.path.join(run_path, 'elevation_plots')
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    plot_water_elevation(
        file_list=file_list,
        output_dir=output_dir,
        contour_levels=np.linspace(-1, 1, 50),
        colorbar_ticks=np.arange(-1, 1.1, 0.2),
        title_template="Water Elevation at {time}",
        colormap='coolwarm',
        vmin=-1, vmax=1
    )

if __name__ == "__main__":
    main()
