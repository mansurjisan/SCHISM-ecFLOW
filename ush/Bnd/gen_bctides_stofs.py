import argparse
import subprocess
import os
import shutil
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate bctides.in file')
    parser.add_argument('--year', type=int, required=True, help='Year (4 digits)')
    parser.add_argument('--month', type=int, required=True, help='Month (1-12)')
    parser.add_argument('--day', type=int, required=True, help='Day (1-31)')
    parser.add_argument('--hour', type=int, required=True, help='Hour (0-23)')
    parser.add_argument('--rnday', type=int, required=True, help='Number of days for simulation')
    parser.add_argument('--exec_path', required=True, help='Path to tide factor executable')
    parser.add_argument('--workdir', required=True, help='Working directory')
    parser.add_argument('--template_path', required=True, help='Path to bctides template file')
    return parser.parse_args()

def create_input_file(year, month, day, hour, rnday):
    """Create input_generate_bctides.in file with new parameter format"""
    input_content = [
        str(rnday),
        f"{hour},{day},{month},{year}",
        "y"
    ]
    with open('input_generate_bctides.in', 'w') as f:
        f.write('\n'.join(input_content))

def run_tide_generator(exec_path):
    # (No changes needed here - same as previous working version)
    try:
        process = subprocess.run(
            [exec_path],
            stdin=open('input_generate_bctides.in'),
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running tide generator: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    args = parse_arguments()
    
    # Create work directory if needed
    os.makedirs(args.workdir, exist_ok=True)
    os.chdir(args.workdir)
    
    # Copy template file to working directory
    shutil.copy(args.template_path, 'bctides.in_template')
    
    # Create input file with new parameters
    create_input_file(
        year=args.year,
        month=args.month,
        day=args.day,
        hour=args.hour,
        rnday=args.rnday
    )
    
    # Run tidal generator
    success = run_tide_generator(args.exec_path)
    
    # Validate output
    if success and os.path.exists('bctides.in') and os.path.getsize('bctides.in') > 1000:
        print("Successfully generated bctides.in")
        return 0
    else:
        print("Failed to generate bctides.in")
        return 1

if __name__ == "__main__":
    exit(main())
