import os
import subprocess
import argparse
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_latest_run_directory(base_path):
    """
    Find the most recently created Test_Duck_XXX directory.
    
    Args:
    base_path (str): Base path where Test_Duck directories are located
    
    Returns:
    str: Path to the most recent Test_Duck directory
    """
    test_duck_dirs = [d for d in os.listdir(base_path) if d.startswith("Test_Duck_") and d[10:].isdigit()]
    if not test_duck_dirs:
        logging.error(f"No Test_Duck directories found in {base_path}")
        return None
    
    latest_dir = max(test_duck_dirs, key=lambda d: os.path.getctime(os.path.join(base_path, d)))
    return os.path.join(base_path, latest_dir)

def submit_job(run_directory):
    """
    Submit a job using sbatch with the job card in the specified run directory.
    
    Args:
    run_directory (str): Path to the run directory
    
    Returns:
    int: The job ID if successful, None otherwise
    """
    job_card_path = os.path.join(run_directory, "job_card")
    if not os.path.exists(job_card_path):
        logging.error(f"Job card not found: {job_card_path}")
        return None

    try:
        # Run sbatch command
        result = subprocess.run(['sbatch', job_card_path], 
                                check=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                cwd=run_directory)  # Set working directory to run_directory
        
        # Extract job ID from sbatch output
        job_id = result.stdout.strip().split()[-1]
        logging.info(f"Job submitted successfully. Job ID: {job_id}")
        return job_id
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to submit job. Error: {e}")
        logging.error(f"STDERR: {e.stderr}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Submit a SCHISM job using sbatch")
    parser.add_argument("--base_path", default="/work/noaa/nosofs/mjisan/schism/schism_verification_tests",
                        help="Base path for Test_Duck directories")
    args = parser.parse_args()

    # Find the latest Test_Duck directory
    run_directory = find_latest_run_directory(args.base_path)
    if not run_directory:
        print("Failed to find a valid run directory. Check the logs for more information.")
        return

    # Submit the job
    job_id = submit_job(run_directory)

    if job_id:
        print(f"Job submitted successfully. Job ID: {job_id}")
        print(f"Run directory: {run_directory}")
    else:
        print("Failed to submit job. Check the logs for more information.")

if __name__ == "__main__":
    main()
